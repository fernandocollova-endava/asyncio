import asyncio
import time
 
t = time.time()
 
async def c1():
    print("finished c1 {}".format(time.time() - t))
 
async def c2():
    await asyncio.sleep(3)
    print("finished c2 {}".format(time.time() - t))
 
called = False
 
async def c3():
    global called
    # raises an exception the first time it's called
    if not called:
        called = True
        raise RuntimeError("c3 called the first time")
    print("finished c3 {}".format(time.time() - t))
 
async def run():
    tasks = {asyncio.ensure_future(c()): c for c in (c1, c2, c3)}
    pending = set(tasks.keys())
 
    num_times_called = 0
    while pending:
        num_times_called += 1
        print("{} times called with {} pending tasks: {}".format(num_times_called, len(pending), pending))
 
        finished, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_EXCEPTION)
        for task in finished:
            if task.exception():
                print("{} got an exception {}, retrying".format(task, task.exception()))
                coro = tasks[task]
                new_task = asyncio.ensure_future(coro())
                tasks[new_task] = coro
                pending.add(new_task)
 
        print("finished {}".format(finished))
 
    print("finished all {}".format(time.time() - t))

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())
