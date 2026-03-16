import socket
import time

SERVER_IP = "127.0.0.1"
PORT = 12345

# Ask user for client ID
CLIENT_ID = input("Enter Client ID: ")

# Create UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Add timeout handling
client.settimeout(5)

print("\nClock Sync Client Started...\n")

while True:

    try:
        # Record send time
        T1 = time.time()

        message = f"TIME_REQUEST:{CLIENT_ID}"
        client.sendto(message.encode(), (SERVER_IP, PORT))

        # Receive response
        data, addr = client.recvfrom(1024)

        # Record receive time
        T4 = time.time()

        # Extract timestamps
        T2, T3 = map(float, data.decode().split(","))

        # Calculate delay
        delay = (T4 - T1) - (T3 - T2)

        # Calculate offset
        offset = ((T2 - T1) + (T3 - T4)) / 2

        # Calculate server time estimate
        server_time = (T2 + T3) / 2
        local_time = time.time()

        corrected_time = time.time() + offset

        print("------ Synchronization Result ------")
        print("Client ID:", CLIENT_ID)
        print("Local Time:", time.ctime(local_time))
        print("Server Time:", time.ctime(server_time))
        print("Network Delay:", delay)
        print("Clock Offset:", offset)
        print("Corrected Time:", time.ctime(corrected_time))
        print("-----------------------------------\n")

        time.sleep(5)

    except socket.timeout:
        print("Server did not respond. Retrying...\n")

    except Exception as e:
        print("Client Error:", e)
        break

    except KeyboardInterrupt:
        print("\nClient stopped.")
        break