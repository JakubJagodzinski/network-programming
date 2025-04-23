import socket

DEFAULT_PORT = 7
BUFFER_SIZE = 1024


def start_server(port=DEFAULT_PORT) -> None:
    server_socket = None

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(1)
        print(f'[INFO] Server is listening on port {port}...')

        client_id = 0
        while True:
            try:
                client_socket, address_info = server_socket.accept()
                client_address, client_port = address_info

                print(f'[INFO] Client #{client_id} connected: {client_address}:{client_port}')

                while True:
                    received_data = client_socket.recv(BUFFER_SIZE)

                    if not received_data:
                        print(f'[INFO] Client #{client_id} disconnected.')
                        break

                    bytes_received = len(received_data)
                    message = received_data.decode('utf-8')
                    print(f'[INFO] Data received from client #{client_id} [{bytes_received}B]: \'{message}\'')

                    print(f'[INFO] Sending data back to client #{client_id}...')
                    client_socket.sendall(received_data)
                    print(f'[INFO] Data sent back to client #{client_id} [{bytes_received}B]: \'{message}\'')

                client_socket.close()
            except ConnectionResetError:
                print(f'[ERROR] Connection reset by client #{client_id}')
            except Exception as e:
                print(f'[ERROR] General error with client #{client_id}: {e}')
            finally:
                client_id += 1
    except KeyboardInterrupt:
        print('[INFO] Server stopping.')
    except Exception as e:
        print(f'[ERROR] Server error: {e}')
    finally:
        server_socket.close()
        print('[INFO] Server stopped.')


def get_port() -> int:
    try:
        port_input = input(f"Enter port number (default {DEFAULT_PORT}): ").strip()
        return int(port_input) if port_input else DEFAULT_PORT
    except ValueError:
        print("[ERROR] Invalid port number. Using default.")
        return DEFAULT_PORT


def main() -> None:
    start_server(get_port())


if __name__ == '__main__':
    main()
