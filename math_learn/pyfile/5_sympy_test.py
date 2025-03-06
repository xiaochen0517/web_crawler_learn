from sympy import *

# print(Mul(Symbol('y'), Add(3, Symbol('x'))))

# x = Symbol('x')
# print((3*x**2).integrate(x))

# 计算导数
# exp = (3*x**2+x)*sin(x)
# print(diff(exp, x))

# 定义符号变量
x = symbols('x')

# 定义函数
# f = 3*x**4 + 2*x**2 - 5  # 例1的函数
# f = sin(2*x**2)         # 例2的函数
f = x**2 * exp(x)       # 例3的函数

# 计算导数
f_prime = diff(f, x)
print("导数结果：", f_prime)