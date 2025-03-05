from abc import ABC, abstractmethod
import math


class Expression(ABC):
    @abstractmethod
    def evaluate(self, **bindings):
        pass

    @abstractmethod
    def expand(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Power(Expression):
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent

    def evaluate(self, **bindings):
        return self.base.evaluate(**bindings) ** self.exponent.evaluate(**bindings)

    def expand(self):
        return Power(self.base.expand(), self.exponent.expand())

    def __str__(self):
        return f'{self.base}^{self.exponent}'


class Number(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self, **bindings):
        return self.value

    def expand(self):
        return self

    def __str__(self):
        return str(self.value)


class Variable(Expression):
    def __init__(self, symbol):
        self.symbol = symbol

    def evaluate(self, **bindings):
        try:
            return bindings[self.symbol]
        except KeyError:
            raise ValueError(f"Variable '{self.symbol}' not found in bindings.")

    def expand(self):
        return self

    def __str__(self):
        return self.symbol


class Product(Expression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def evaluate(self, **bindings):
        return self.exp1.evaluate(**bindings) * self.exp2.evaluate(**bindings)

    def expand(self):
        expanded1 = self.exp1.expand()
        expanded2 = self.exp2.expand()
        if isinstance(expanded1, Sum):
            return Sum(*[Product(exp, expanded2).expand() for exp in expanded1.args])
        elif isinstance(expanded2, Sum):
            return Sum(*[Product(expanded1, exp).expand() for exp in expanded2.args])
        else:
            return Product(expanded1, expanded2)

    def __str__(self):
        return f'{self.exp1}*{self.exp2}'


class Sum(Expression):
    def __init__(self, *args):
        self.args = args

    def evaluate(self, **bindings):
        result = 0
        for arg in self.args:
            result += arg.evaluate(**bindings)
        return result

    def expand(self):
        return Sum(*[arg.expand() for arg in self.args])

    def __str__(self):
        return '+'.join([str(arg) for arg in self.args])


_function_bindings = {
    'sin': lambda x: math.sin(x),
    'cos': lambda x: math.cos(x),
    'tan': lambda x: math.tan(x),
    'exp': lambda x: math.exp(x),
    'log': lambda x: math.log(x),
    'sqrt': lambda x: math.sqrt(x),
    'abs': lambda x: abs(x),
    'min': lambda *args: min(args),
    'max': lambda *args: max(args),
    'round': lambda x: round(x),
    'floor': lambda x: math.floor(x),
    'ceil': lambda x: math.ceil(x),
    'pow': lambda x, y: pow(x, y)
}


class Function(Expression):
    def __init__(self, name):
        self.name = name

    def evaluate(self, **bindings):
        return _function_bindings[self.name]

    def expand(self):
        return self

    def __str__(self):
        return self.name


class Apply(Expression):
    def __init__(self, function, *args):
        self.function = function
        self.args = args

    def evaluate(self, **bindings):
        return self.function.evaluate(**bindings)(*[arg.evaluate(**bindings) for arg in self.args])

    def expand(self):
        return Apply(self.function, *[arg.expand() for arg in self.args])

    def __str__(self):
        return f'{self.function}({", ".join([str(arg) for arg in self.args])})'


f_expression = Product(
    Sum(
        Product(
            Number(3),
            Power(Variable('x'), Number(2))
        ),
        Variable('x')
    ),
    Apply(Function('sin'), Variable('x'))
)


def distinct_variables(exp):
    if isinstance(exp, Variable):
        return set(exp.symbol)
    elif isinstance(exp, Number):
        return set()
    elif isinstance(exp, Sum):
        return set().union(*[distinct_variables(exp) for exp in exp.args])
    elif isinstance(exp, Product):
        return distinct_variables(exp.exp1).union(distinct_variables(exp.exp2))
    elif isinstance(exp, Power):
        return distinct_variables(exp.base).union(distinct_variables(exp.exponent))
    elif isinstance(exp, Apply):
        return distinct_variables(exp.function).union(*[distinct_variables(exp) for exp in exp.args])
    elif isinstance(exp, Function):
        return set()
    else:
        raise TypeError("Not a valid expression.")


def test_distinct_variables():
    variables_name = distinct_variables(f_expression)
    print(f'distinct_variables: {variables_name}')
    assert variables_name == {'x'}


def test_evaluate():
    exp = Product(Product(Variable('x'), Number(2)), Variable('y'))
    evaluate_data = exp.evaluate(x=3, y=4)
    print(f'evaluate: {evaluate_data}')
    assert evaluate_data == 24


def test_default_evaluate():
    evaluate_data = f_expression.evaluate(x=1)
    print(f'default_evaluate: {evaluate_data}')
    assert evaluate_data == 3.365883939231586


def test_expand():
    expand_data = f_expression.expand()
    print(f'expand: {expand_data}')


if __name__ == '__main__':
    test_distinct_variables()
    test_evaluate()
    test_default_evaluate()
    test_expand()
