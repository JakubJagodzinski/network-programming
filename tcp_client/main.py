import socket

BUFFER_SIZE = 1024


def receive_data(server_socket) -> bool:
    """
        Receive data from the server socket.
        @return: boolean indicating if the connection is still active
    """
    try:
        received_data = server_socket.recv(BUFFER_SIZE)

        if not received_data:
            print('[INFO] Connection closed by server.')
            return False

        bytes_received = len(received_data)
        message = received_data.decode('utf-8')
        print(f'[INFO] Data received from server [{bytes_received}B]: \'{message}\'')
    except Exception as e:
        print(f'[ERROR] Failed to receive data from server: {e}')
        return False

    return True


def send_data(server_socket) -> bool:
    """
        Send data to the server socket.
        @:return boolean indicating if the client still wants to send data to server
    """
    try:
        data = input('Enter message (or \'quit\' to exit): ')

        if data == '':
            data = '<EMPTY>'

        data = data[:BUFFER_SIZE]

        if data.lower() == 'quit':
            return False

        print('[INFO] Sending data to server...')
        server_socket.sendall(data.encode('utf-8'))
        bytes_sent = len(data)
        print(f'[INFO] Data sent to server [{bytes_sent}B]: \'{data}\'')
    except Exception as e:
        print(f'[ERROR] Failed to send data: {e}')
        return False

    return True


def establish_connection() -> None:
    host, port = get_server_address()
    server_socket = None

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, port))
        print(f'[INFO] Connected to {host}:{port}')

        while True:
            continue_sending = send_data(server_socket)
            if not continue_sending:
                break

            is_connection_active = receive_data(server_socket)
            if not is_connection_active:
                break
    except Exception as e:
        print(f'[ERROR] Connection error: {e}')
    finally:
        if server_socket:
            server_socket.close()
            print('[INFO] Connection closed')


def get_server_address() -> tuple:
    host = input('Enter server address (xxx.xxx.xxx.xxx): ')
    port = int(input('Enter port: '))

    return host, port


def main() -> None:
    establish_connection()


if __name__ == '__main__':
    main()
