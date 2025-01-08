import asyncio
import requests

url = 'https://www.baidu.com'


async def execute(index):
    print(f'Starting task {index}')
    response = requests.get(url)
    print(f'Task {index} done')
    return response


print('Event loop start')

tasks = [asyncio.ensure_future(execute(index)) for index in range(10)]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    print(f'Task: {task}')
    print(f'Task result: {task.result()}')

print('End of the program')
