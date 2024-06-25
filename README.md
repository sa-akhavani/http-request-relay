# HTTP and HTTPS Request Relay
Send and receive HTTP and HTTPS requests to target server using sockets.
Supports all content types and request methods.

Usage examples:
Provide the code your target `hostname` and `port` and `request data` in byte string format such as:
### Example HTTP POST Request
```python
relay = Relay(host='example.com', port=80, use_ssl=False)
request = b'POST / HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/json\r\nContent-Length: 16\r\n\r\n{"key": "value"}'
response = relay.forward_request(request)
print(response.decode())
```

### Example HTTPS GET Request
```python
relay = Relay(host='example.com', port=443, use_ssl=True)
request = b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n'
response = relay.forward_request(request)
print(response.decode())
```

