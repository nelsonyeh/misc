import asyncio
import concurrent.futures


def blocking_io():
    for i in range(100):
        print(f'blocking_io:{i}')


def cpu_bound():
    for i in range(100):
        print(f'cpu_bound:{i}')


async def main():
    loop = asyncio.get_running_loop()

    result = await loop.run_in_executor(
        None, blocking_io)
    print('2' * 100)
    result = await loop.run_in_executor(
        None, cpu_bound)

asyncio.run(main())
