#this is a non-critical file. just for your viewing pleasure. 
#I was gonna implement UDP with the current TCP in my web-server. 
#but realised unnecessary.

import socket

###BLAH OTHER SERVER CODE

# Define a new function to handle UDP traffic
def handle_udp_traffic(udp_socket):
    while True:
        data, addr = udp_socket.recvfrom(1024)  # Buffer size is 1024 bytes
        log_message(f"Received UDP packet from {addr}: {data.hex()}")

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_port = 8080  # This should be the port you expect to receive NTP traffic on
udp_socket.bind((HOST, udp_port))

# Start a new thread to listen for UDP traffic
udp_thread = threading.Thread(target=handle_udp_traffic, args=(udp_socket,))
udp_thread.daemon = True  # This ensures that the thread will close when the main program exits
udp_thread.start()

# BLAH OTHER REQUESTS....
