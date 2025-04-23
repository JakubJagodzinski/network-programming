import threading
import time

from concurrent_processes.config import THREAD_COUNT
from concurrent_processes.utils import ENUMERATE_LETTER_BEGIN, ENUMERATE_LETTER_END

critical_section = threading.Lock()


def synchronized_enumerator_function(thread_nr):
    while True:
        for char in range(ENUMERATE_LETTER_BEGIN, ENUMERATE_LETTER_END + 1):
            with critical_section:
                print(f'{chr(char)}{thread_nr % 10}')
            time.sleep(1)


def init_threads():
    for thread_nr in range(THREAD_COUNT):
        enumerator_thread = threading.Thread(
            target=synchronized_enumerator_function,
            args=(thread_nr + 1,),
            daemon=True
        )
        enumerator_thread.start()


def main():
    init_threads()
    input('Press enter to exit...')


if __name__ == '__main__':
    main()
