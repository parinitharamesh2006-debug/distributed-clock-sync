import socket
import time

# Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Add timeout handling
server_socket.settimeout(10)

# Bind server to port
server_address = ('0.0.0.0', 12345)
server_socket.bind(server_address)

print("Time Server running on port 12345...")

while True:

    try:
        # Wait for client request
        data, client_address = server_socket.recvfrom(1024)

        message = data.decode()

        if message.startswith("TIME_REQUEST"):

            print(f"Client {client_address} requested time")

            # Record receive timestamp
            T2 = time.time()

            # Record send timestamp
            T3 = time.time()

            response = f"{T2},{T3}"

            server_socket.sendto(response.encode(), client_address)

            print(f"Response sent to {client_address}\n")

        else:
            print(f"Invalid request from {client_address}")

    except socket.timeout:
        print("No client requests received. Server still running...\n")

    except Exception as e:
        print("Server error:", e)