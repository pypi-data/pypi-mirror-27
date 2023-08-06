import asyncio as aio

from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor(4)
allObs = []
loop = aio.get_event_loop()

def main_loop(ui):
    # the workers should be closed first
    obs = [o.observe() for o in allObs]
    loop.run_until_complete(aio.gather(*ui, *obs))
    pool.shutdown(wait=True)
    loop.close()


