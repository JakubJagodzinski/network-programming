import threading
import time

from concurrent_processes.config import THREAD_COUNT
from concurrent_processes.utils import parse_range, ENUMERATE_LETTER_BEGIN, ENUMERATE_LETTER_END, STOP_NRS_BEGIN_INDEX, \
    START_NRS_BEGIN_INDEX

thread_flags = [threading.Event() for _ in range(THREAD_COUNT)]


def enumerator_function(thread_nr):
    while True:
        for char in range(ENUMERATE_LETTER_BEGIN, ENUMERATE_LETTER_END + 1):
            thread_flags[thread_nr - 1].wait()
            print(f'{chr(char)}{thread_nr % 10}')
            time.sleep(1)


def init_threads():
    for thread_nr in range(THREAD_COUNT):
        enumerator_thread = threading.Thread(
            target=enumerator_function,
            args=(thread_nr + 1,),
            daemon=True
        )
        enumerator_thread.start()


def start_thread_controller(cmd_input):
    threads_to_start_nrs = parse_range(cmd_input[START_NRS_BEGIN_INDEX:])

    for thread_nr in threads_to_start_nrs:
        if thread_flags[thread_nr - 1].is_set():
            print(f'[ERROR] Thread {thread_nr} is already running')
            continue
        else:
            thread_flags[thread_nr - 1].set()
            print(f'[INFO] Thread {thread_nr} started')


def stop_thread_controller(cmd_input):
    threads_to_stop_nrs = parse_range(cmd_input[STOP_NRS_BEGIN_INDEX:])

    for thread_nr in threads_to_stop_nrs:
        if not thread_flags[thread_nr - 1].is_set():
            print(f'[ERROR] Thread {thread_nr} is already stopped')
            continue
        else:
            thread_flags[thread_nr - 1].clear()
            print(f'[INFO] Thread {thread_nr} stopped')


def thread_controller():
    command_prompt = 'Enter command (start [thread_nr] / stop [thread_nr] / start [from]-[to] / stop [from]-[to]): '

    while True:
        cmd_input = (input(command_prompt).strip().lower())

        if cmd_input.startswith('start'):
            start_thread_controller(cmd_input)
        elif cmd_input.startswith('stop'):
            stop_thread_controller(cmd_input)


def main():
    init_threads()
    thread_controller()


if __name__ == '__main__':
    main()
