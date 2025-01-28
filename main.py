import socket
import ssl
import sys
import os

# from hostnames import target_urls

_BUFFER_SIZE = 4096 # 4 KB
_TIMEOUT = 20 # 20 seconds (Change if you receive empty response)

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

def read_requests_from_file(filename):
    """
    Read raw HTTP requests from a file where each line is a Python byte object.
    Requests in the file have to be in Byte-Object format. b'''<request>'''
    """
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' does not exist.")
        return []

    with open(filename, 'r') as file:
        requests = file.readlines()

    # Parse each line into a Python bytes object
    return [eval(req.strip()) for req in requests if req.strip()]



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]


    relay = Relay(host="localhost", port=12345, use_ssl=False)

    # Read the requests from the file
    requests = read_requests_from_file(filename)

    if not requests:
        print("No requests to send. Exiting.")
        sys.exit(0)

    # Send each request sequentially
    for i, request in enumerate(requests, 1):
        print(f"Sending request {i}:")
        print(request)

        response = relay.forward_request(request)

        if response:
            print("Response:")
            print(response.decode())
        else:
            print("No response received.")
        print("##########################")

