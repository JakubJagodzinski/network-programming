import threading


def hello_world():
    print('Hello World!!')


def main():
    thread = threading.Thread(target=hello_world)
    thread.start()
    thread.join()


if __name__ == '__main__':
    main()
