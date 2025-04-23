from concurrent_processes.config import THREAD_COUNT

ENUMERATE_LETTER_BEGIN = ord('A')
ENUMERATE_LETTER_END = ord('Z')

START_NRS_BEGIN_INDEX = len('start ')
STOP_NRS_BEGIN_INDEX = len('stop ')

CANCEL_NRS_BEGIN_INDEX = len("cancel ")


def parse_range(text):
    try:
        if '-' in text:
            range_begin, range_end = map(int, text.split('-'))

            if range_begin > range_end:
                print('[ERROR] Invalid range (begin > end)')
                return []

            if range_begin < 1 or range_end > THREAD_COUNT:
                print(f'[ERROR] Invalid range (out of bounds, [1;{THREAD_COUNT}] required)')
                return []

            return list(range(range_begin, range_end + 1))
        else:
            task_nr = int(text)

            if task_nr < 1 or task_nr > THREAD_COUNT:
                print(f'[ERROR] Invalid task nr (out of bounds, [1;{THREAD_COUNT}] required)')
                return []

            return [task_nr]
    except Exception:
        return []
