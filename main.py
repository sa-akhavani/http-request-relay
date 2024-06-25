import socket
import ssl

_BUFFER_SIZE = 4096 # 4 KB
_TIMEOUT = 4 # 4 seconds

class Relay:
    def __init__(self, host, port, use_ssl=False):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl

    def forward_request(self, raw_request) -> bytes:
        """
            Forward the raw request to the target server and return the response
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                client_socket.settimeout(_TIMEOUT)

                if self.use_ssl:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    with context.wrap_socket(client_socket, server_hostname=self.host) as ssl_socket:
                        ssl_socket.sendall(raw_request)
                        response = self._receive_response(ssl_socket)
                else:
                    client_socket.sendall(raw_request)
                    response = self._receive_response(client_socket)

                return response

        except Exception as e:
            print(f'Error: {e}')
            return None

    def _receive_response(self, client_socket) -> bytes:
        """
            Receive the response from the target server and return it
        """
        response = b''
        while True:
            try:
                data = client_socket.recv(_BUFFER_SIZE)
                if not data:
                    break
                response += data
            except socket.timeout:
                break
            except Exception as e:
                print(f'Error while receiving data: {e}')
                break

        return response


# Example usage
if __name__ == '__main__':
    relay = Relay('example.com', 443, use_ssl=True)
    # get_request = b'GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n'
    post_request = b'POST / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\nContent-Type: application/json\r\nContent-Length: 16\r\n\r\n{"key": "value"}'
    response = relay.forward_request(post_request)
    print(response.decode())
