import asyncio
from asyncio import Future
from datetime import datetime as dt

some_global = 0

async def fetch_data():
    # some_global += 1 --> Invalid syntax, apparently globlas can't be refernced
    print('start fetching')
    await asyncio.sleep(2)
    print('done fetching')
    return {'data': 1}

async def print_numbers():
    for i in range(10):
        print(i)
        await asyncio.sleep(0.25)

async def main():
    print(dt.now())
    task = asyncio.create_task(fetch_data())
    coro = print_numbers()
    print(task)
    print(coro)
    print(isinstance(task, Future))
    print(isinstance(coro, Future))
    await coro # The task, fetch_data, also runs
    print(dt.now())


asyncio.run(main())
