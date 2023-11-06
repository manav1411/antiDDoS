import socket

target_host = '0.0.0.0'
target_port = 8080
connections = []

# Try to open max_connections to get overload server limit
for _ in range(11):  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((target_host, target_port))
        connections.append(client_socket)
        print("Connection established.")
    except Exception as e:
        print(f"Failed to establish connection: {e}")

# Keep the connections open
try:
    while True:
        pass
except KeyboardInterrupt:
    for conn in connections:
        conn.close()

