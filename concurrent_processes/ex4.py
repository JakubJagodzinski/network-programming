import asyncio

from concurrent_processes.config import THREAD_COUNT
from concurrent_processes.utils import parse_range, ENUMERATE_LETTER_BEGIN, ENUMERATE_LETTER_END, CANCEL_NRS_BEGIN_INDEX

tasks = {}


async def async_enumerator_function(task_nr):
    try:
        while True:
            for char in range(ENUMERATE_LETTER_BEGIN, ENUMERATE_LETTER_END + 1):
                print(f'{chr(char)}{task_nr % 10}')
                await asyncio.sleep(1)
    except asyncio.CancelledError:
        print(f'[INFO] Task {task_nr} cancelled.')


async def init_tasks():
    for thread_nr in range(THREAD_COUNT):
        task = asyncio.create_task(async_enumerator_function(thread_nr + 1))
        tasks[thread_nr] = task


async def async_input(prompt: str) -> str:
    return await asyncio.get_event_loop().run_in_executor(None, input, prompt)


async def task_controller():
    while True:
        is_any_task_left = False
        for task in tasks.values():
            if not task.done():
                is_any_task_left = True
                break

        if not is_any_task_left:
            print('[INFO] All tasks are done')
            break

        cmd_input = await async_input('Enter command (cancel [task_nr] / cancel [from]-[to]): ')

        if cmd_input.startswith('cancel'):
            task_nrs = parse_range(cmd_input[CANCEL_NRS_BEGIN_INDEX:])
            for task_nr in task_nrs:
                if not tasks[task_nr - 1].done():
                    tasks[task_nr - 1].cancel()
                else:
                    print(f'[ERROR] Task {task_nr} is already cancelled')


async def main_async():
    await init_tasks()
    await task_controller()


def main():
    asyncio.run(main_async())


if __name__ == '__main__':
    main()
