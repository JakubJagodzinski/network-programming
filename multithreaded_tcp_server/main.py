import socket
import threading

DEFAULT_PORT = 7
BUFFER_SIZE = 1024

ACTIVE_CONNECTIONS_LIMIT = 3

active_connections = {}
active_clients_lock = threading.Lock()
client_id_counter = 0


def handle_client(client_socket, address_info, client_id) -> None:
    client_address, client_port = address_info
    print(f'[INFO] Client #{client_id} connected: {client_address}:{client_port}')

    with active_clients_lock:
        active_connections[client_id] = f'{client_address}:{client_port}'
        print_clients()

    try:
        while True:
            received_data = client_socket.recv(BUFFER_SIZE)

            if not received_data:
                break

            message = received_data.decode('utf-8')
            print(f'[INFO] Data received from client #{client_id} [{len(received_data)}B]: \'{message}\'')

            client_socket.sendall(received_data)
            print(f'[INFO] Data sent back to client #{client_id} [{len(received_data)}B]: \'{message}\'')
    except ConnectionResetError:
        print(f'[ERROR] Connection reset by client #{client_id}')
    except Exception as e:
        print(f'[ERROR] Error with client #{client_id}: {e}')
    finally:
        client_socket.close()
        print(f'[INFO] Client #{client_id} disconnected.')
        with active_clients_lock:
            if client_id in active_connections:
                del active_connections[client_id]
                print_clients()


def print_clients() -> None:
    print()
    print('[CONNECTED CLIENTS]')
    for client_id, client_address in active_connections.items():
        print(f'#{client_id} {client_address}')
    print()


def start_server(port=DEFAULT_PORT) -> None:
    global client_id_counter

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    print(f'[INFO] Server is listening on port {port}...')

    try:
        while True:
            client_socket, address_info = server_socket.accept()
            client_address, client_port = address_info

            with active_clients_lock:
                if len(active_connections) >= ACTIVE_CONNECTIONS_LIMIT:
                    print(f'[INFO] Server busy. Rejecting connection from {client_address}:{client_port}')
                    client_socket.sendall(b'SERVER BUSY')
                    client_socket.close()
                    continue

            client_id_counter += 1
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address_info, client_id_counter),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print('[INFO] Server stopping...')
    except Exception as e:
        print(f'[ERROR] Server error: {e}')
    finally:
        server_socket.close()
        print('[INFO] Server stopped.')


def get_port() -> int:
    try:
        port_input = input(f'Enter port number (default {DEFAULT_PORT}): ').strip()
        return int(port_input) if port_input else DEFAULT_PORT
    except ValueError:
        print('[ERROR] Invalid port number. Using default.')
        return DEFAULT_PORT


def main() -> None:
    start_server(get_port())


if __name__ == '__main__':
    main()
