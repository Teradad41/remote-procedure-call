import socket
import os
import signal
import math
import json
from collections import Counter


class Method(object):
    def floor(self, x):
        return math.floor(x)

    def nroot(self, n, x):
        if n <= 0:
            raise ValueError("n must be a positive integer")
        if x < 0 and n % 2 == 0:
            raise ValueError("Cannot calculate even-root of a negative number")

        r = x
        delta = 1.0
        while delta > 1e-6:
            r_next = ((n - 1) * r + x / r ** (n - 1)) / n
            delta = abs(r_next - r)
            r = r_next

        return int(r)

    def reverse(self, s):
        return ''.join(reversed(s))

    def validAnagram(self, str1, str2):
        dict1 = Counter(str1)
        dict2 = Counter(str2)

        return dict1 == dict2

    def sort(self, str_arr):
        return sorted(str_arr)


def get_server_pid(port):
    try:
        pid = int(os.popen(f"lsof -ti :{port}").read())
        return pid
    except ValueError:
        return None


def initialize_server_socket():
    # ループバックアドレス
    server_ip = '127.0.0.1'
    server_port = 12345
    server_pid = get_server_pid(server_port)

    if server_pid is not None:
        os.kill(server_pid, signal.SIGTERM)
        print("Killed one process...")
    else:
        pass

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((server_ip, server_port))
    sock.listen(1)
    print(f'Starting up on {server_ip}:{server_port} ...')

    return sock


def handle_req_res(sock):
    method = Method()

    method_map = {
        'floor': method.floor,
        'nroot': method.nroot,
        'reverse': method.reverse,
        'validAnagram': method.validAnagram,
        'sort': method.sort,
    }

    while True:
        print('\nServer started. Waiting connection from client...')
        client_socket, client_address = sock.accept()

        try:
            while True:
                data = client_socket.recv(1024).decode()

                if not data:
                    print("no data from client...")
                    break
                try:
                    print(f'Received data from client: {data}')
                    request_data = json.loads(data)

                    method_name = request_data.get('method')
                    params = request_data.get('params', [])

                    if method_name in method_map:
                        result = method_map[method_name](*params)

                        response_data = {
                            "result": result,
                            'result_type': str(type(result)),
                            'id': request_data.get("id")
                        }

                        print(f'Response to client: {response_data}')

                        response_json = json.dumps(response_data)
                        client_socket.sendall(response_json.encode())
                    else:
                        response_data = f"unsupported method {method_name}"
                        client_socket.sendall(response_data.encode())
                except json.JSONDecodeError:
                    print("Invalid JSON data")
                    break
        finally:
            print('Closing current connection...')
            client_socket.close()


def main():
    sock = initialize_server_socket()
    handle_req_res(sock)


if __name__ == "__main__":
    main()
