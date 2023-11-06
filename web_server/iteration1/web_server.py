import socket
import os
import json
import time
import threading


active_connections = 0
max_connections = 200  # example limit

# Define host and port for the server
HOST, PORT = '127.0.0.1', 8080

# Base directory where client websites are stored
BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'client_websites')

# Path to the server log file
LOG_FILE = 'serverLog.txt'

# Function to log messages
def log_message(message):
    print(message)
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(message + '\n')

def get_content_type(file_path):
    # You could expand this function to return different content types based on the file extension
    return "Content-Type: text/html; charset=UTF-8\r\n"


# Function to handle client connection
def handle_client_connection(client_connection, client_address):
    global active_connections
    print("num active connections: " + str(active_connections) + "\n")
    if active_connections >= max_connections:
        print("exceeded server load of max #connections :(")
        client_connection.close()
        return  # Close connection if limit is reached
    active_connections += 1

    log_message(f"Accepted connection from {client_address}")
    try:
        # Receive the request
        request_data = client_connection.recv(1024)
        request = request_data.decode()

        # Parse the HTTP request to determine the file requested
        headers, body = request.split('\r\n\r\n', 1)
        request_lines = headers.splitlines()
        if not request_lines:
            raise ValueError("Empty request received")

        log_message("recieved request: " + request_lines[0])
        request_line = request_lines[0]
        components = request_line.split()

        if len(components) < 3:
            raise ValueError("Invalid HTTP request line")

        method, path, _ = components

        # Dispatch request to appropriate handler
        if method == 'GET':
            handle_get(path, client_connection)
        elif method == 'POST':
            handle_post(path, body, client_connection)
        elif method == 'PUT':
            handle_put(path, body, client_connection)
        elif method == 'DELETE':
            handle_delete(path, client_connection)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

    except Exception as e:
        log_message(f"Error: {e}")
        # Send a 500 Internal Server Error response
        client_connection.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")

    finally:
        # Clean up the connection
        print("will wait 1sec, then continue (to simulate a heavy connection")
        time.sleep(1)  
        active_connections -= 1  # Decrement the counter when the connection is closed
        client_connection.close()

messages = {}

def handle_get(path, client_connection):
    if path.startswith("/messages"):
        try:
            # Assuming path format is "/messages" or "/messages/{id}"
            # Return all messages or a specific one based on the path
            if path == "/messages":
                response_body = json.dumps(messages).encode('utf-8')
            else:
                message_id = path.split('/')[-1]
                response_body = json.dumps(messages.get(message_id, "Message not found")).encode('utf-8')

            response_headers = get_content_type(path) + "Content-Length: {}\r\n\r\n".format(len(response_body))
            client_connection.sendall(b"HTTP/1.1 200 OK\r\n" + response_headers.encode('utf-8') + response_body)

        except Exception as e:
            log_message(f"Error in handle_get: {e}")
            client_connection.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
    else:
        serve_file(path, client_connection)


def handle_post(path, body, client_connection):
    if path.startswith("/messages"):
        log_message(f"POST request body: {body}")

       # Extract the message from the body and generate a message ID
        message_id = len(messages) + 1  # Simple incremental ID for demonstration
        messages[message_id] = body  # Store the message body in the messages dictionary

        # Construct a success response
        response_line = "HTTP/1.1 201 Created\r\n"
        response_headers = "Content-Type: text/html; charset=UTF-8\r\n"
        response = response_line.encode() + response_headers.encode() + b"\r\n" + f"Message stored with ID: {message_id}".encode()
        client_connection.sendall(response)
    else:
        pass

def handle_put(path, body, client_connection):
    if path.startswith("/messages"):
        log_message(f"PUT request for {path} with body: {body}")
        # Send a response (simulated as always successful)
        parts = path.split('/')
        if len(parts) == 3 and parts[1] == 'messages':
            message_id = parts[2]
            try:
                message_id = int(message_id)  # Convert the id to an integer
                if message_id in messages:
                    # Update the message
                    messages[message_id] = body
                    response_line = "HTTP/1.1 200 OK\r\n"
                    response_headers = "Content-Type: text/plain; charset=UTF-8\r\n"
                    response = (response_line.encode() + response_headers.encode() +
                                b"\r\n" + f"Message ID {message_id} updated".encode())
                else:
                    # Message ID does not exist
                    response_line = "HTTP/1.1 404 Not Found\r\n"
                    response_headers = "Content-Type: text/plain; charset=UTF-8\r\n"
                    response = (response_line.encode() + response_headers.encode() +
                                b"\r\n" + f"Message ID {message_id} not found".encode())
            except ValueError:
                # The message ID is not an integer
                response_line = "HTTP/1.1 400 Bad Request\r\n"
                response_headers = "Content-Type: text/plain; charset=UTF-8\r\n"
                response = (response_line.encode() + response_headers.encode() +
                            b"\r\n" + "Invalid message ID".encode())
        else:
            # Incorrect path format
            response_line = "HTTP/1.1 400 Bad Request\r\n"
            response_headers = "Content-Type: text/plain; charset=UTF-8\r\n"
            response = (response_line.encode() + response_headers.encode() +
                        b"\r\n" + "Incorrect path format for message update".encode())
        
        client_connection.sendall(response)
    else:
        pass

def handle_delete(path, client_connection):
    if path.startswith("/messages"):
        print("path is: " + path)
        try:
            log_message(f"DELETE request for {path}")
            message_id = int(path.split('/')[2])  # Assuming path format is /messages/{id}
            if message_id in messages:
                # Delete the message if the ID exists
                del messages[message_id]
                response_line = "HTTP/1.1 200 OK\r\n"
                response_body = f"Message with ID: {message_id} has been deleted.\r\n"
            else:
                # If the message ID doesn't exist, return a 404 Not Found
                response_line = "HTTP/1.1 404 Not Found\r\n"
                response_body = "Message ID not found.\r\n"
        except ValueError:
            # Handle the case where the ID is not an integer
            response_line = "HTTP/1.1 400 Bad Request\r\n"
            response_body = "Invalid message ID.\r\n"
        except IndexError:
            # Handle the case where the ID is not provided in the path
            response_line = "HTTP/1.1 400 Bad Request\r\n"
            response_body = "Message ID not specified.\r\n"
        
        # Send the response back to the client
        response_headers = "Content-Type: text/plain; charset=UTF-8\r\n"
        response = response_line.encode() + response_headers.encode() + b"\r\n" + response_body.encode()
        client_connection.sendall(response)
    else:
        pass


# Function to serve a file
def serve_file(path, client_connection):
    # Normalize the path to prevent directory traversal attacks
    requested_path = os.path.normpath(path).lstrip('/')

    # Assuming the first component in the path is the website identifier
    website_id = requested_path.split('/')[0]

    # Construct the file path relative to the client_websites directory
    file_path = os.path.join(BASE_DIR, website_id, *requested_path.split('/')[1:])

    # Default to index.html if the path ends with a slash
    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, 'index.html')

    try:
        # Check if the file_path exists and is not a directory before serving
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            with open(file_path, 'rb') as f:
                response_body = f.read()
                response_line = "HTTP/1.1 200 OK\r\n"
                response_headers = "Content-Type: text/html; charset=UTF-8\r\n"
        else:
            # File not found, use a hardcoded 404 response
            response_body = b"<h1>404 Not Found</h1>"
            response_line = "HTTP/1.1 404 Not Found\r\n"
            response_headers = "Content-Type: text/html; charset=UTF-8\r\n"

        response = response_line.encode() + response_headers.encode() + b"\r\n" + response_body
        client_connection.sendall(response)

    except IOError as e:
        log_message(f"File IO Error: {e}")
        client_connection.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")


# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Reuse the socket address (helpful for server restart)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)
log_message(f"Server listening on {HOST}:{PORT}")

while True:
    # Wait for a connection
    client_connection, client_address = server_socket.accept()
    # Create and start a new Thread to handle the client connection
    client_thread = threading.Thread(target=handle_client_connection, args=(client_connection, client_address))
    client_thread.daemon = True  # This ensures that the thread will close when the main program exits
    client_thread.start()

