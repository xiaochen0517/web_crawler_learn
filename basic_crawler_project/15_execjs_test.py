import execjs
import json

item = {
    'name': '凯文-杜兰特',
    'image': 'durant.png',
    'birthday': '1988-09-29',
    'height': '208cm',
    'weight': '108.9KG'
}

file = 'data/execjs_crypto.js'
node = execjs.get()
ctx = node.compile(open(file).read())

js = f"getToken({json.dumps(item, ensure_ascii=False)})"
print(f'js: {js}')
result = ctx.eval(js)
print(f'result: {result}')
