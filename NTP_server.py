import socket

# This will act as a mock NTP server for educational purposes.

def send_monlist_response(client_socket, address):
    # Simulate a large response to 'monlist' command.
    # In reality, 'monlist' would send back a list of the last 600 IPs.
    data = "MONLIST RESPONSE" * 100  # Make the data payload large.
    print(f"sending monlist data back to client")
    client_socket.sendto(data.encode(), address)

def run_ntp_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", port))

    print(f"NTP server listening on port {port}...")

    try:
        while True:
            message, address = server_socket.recvfrom(1024)
            print(f"Received message from {address}")

            # We'll assume that any message received is a 'monlist' request.
            send_monlist_response(server_socket, address)

    except KeyboardInterrupt:
        print("Shutting down the server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    NTP_SERVER_PORT = 123  # Default NTP port is 123. Use a high port if you need non-root access.
    run_ntp_server(NTP_SERVER_PORT)
