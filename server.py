import socket
import time
from collections import defaultdict
from cryptography.fernet import Fernet

# ─────────────────────────────────────────────
# SHARED SECRET KEY (must match client.py)
# In a real system, exchange this securely once at startup.
# ─────────────────────────────────────────────
SHARED_KEY = b'DMGpGgCZTHSYOGEqBP8j0JW0OzMSwtqnH0TZAbLnLWM='  # 32-byte base64 Fernet key
cipher = Fernet(SHARED_KEY)

HOST = "0.0.0.0"
PORT = 12345

# Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
server_socket.settimeout(10)

# ─────────────────────────────────────────────
# MOD 1: Per-client stats tracking
# ─────────────────────────────────────────────
client_stats = defaultdict(lambda: {
    "request_count": 0,
    "delays": [],
    "offsets": [],
    "corrected_times": [],
    "client_id": "Unknown"
})

def print_server_summary(addr, stats):
    """Print summary report after every 10 requests from a client."""
    count = stats["request_count"]
    delays = stats["delays"]
    offsets = stats["offsets"]
    corrected_times = stats["corrected_times"]

    print("\n" + "=" * 55)
    print(f"  SERVER SUMMARY — Client: {stats['client_id']} ({addr[0]}:{addr[1]})")
    print(f"  Total Requests Handled: {count}")
    print("-" * 55)
    print(f"  Avg Network Delay : {sum(delays)/len(delays):.6f} sec")
    print(f"  Min Network Delay : {min(delays):.6f} sec")
    print(f"  Max Network Delay : {max(delays):.6f} sec")
    print(f"  Avg Clock Offset  : {sum(offsets)/len(offsets):.6f} sec")
    print(f"  Last Corrected Time: {time.ctime(corrected_times[-1])}")
    print("  Last 10 Corrected Times:")
    for i, ct in enumerate(corrected_times[-10:], 1):
        print(f"    [{i:2d}] {time.ctime(ct)}")
    print("=" * 55 + "\n")

print("Clock Sync Server Started (Secure + Reliable UDP)...\n")

try:
    while True:
        try:
            # ─────────────────────────────────────────
            # MOD 3: Receive encrypted + sequenced packet
            # ─────────────────────────────────────────
            raw_data, addr = server_socket.recvfrom(4096)

            # MOD 2: Decrypt the incoming packet
            try:
                decrypted = cipher.decrypt(raw_data).decode()
            except Exception:
                print(f"[SECURITY] Failed to decrypt packet from {addr} — dropping.")
                continue

            # Expected format: "SYNC|<seq>|<client_id>|<T1>|<delay>|<offset>|<corrected_time>"
            parts = decrypted.split("|")
            if parts[0] != "SYNC" or len(parts) < 7:
                print(f"[WARN] Malformed packet from {addr}: {decrypted}")
                continue

            seq         = parts[1]
            client_id   = parts[2]
            T1          = float(parts[3])
            c_delay     = float(parts[4])
            c_offset    = float(parts[5])
            c_corrected = float(parts[6])

            # Server timestamps
            T2 = time.time()
            time.sleep(0.001)   # simulate small processing
            T3 = time.time()

            # ─────────────────────────────────────────
            # MOD 1: Record stats for this client
            # ─────────────────────────────────────────
            stats = client_stats[addr]
            stats["client_id"] = client_id
            stats["request_count"] += 1
            stats["delays"].append(c_delay)
            stats["offsets"].append(c_offset)
            stats["corrected_times"].append(c_corrected)

            count = stats["request_count"]
            print(f"[{time.strftime('%H:%M:%S')}] Request #{count} from {client_id} ({addr[0]}) | "
                  f"seq={seq} | delay={c_delay:.6f}s | offset={c_offset:.6f}s")

            # Print summary every 10 requests
            if count % 10 == 0:
                print_server_summary(addr, stats)

            # ─────────────────────────────────────────
            # MOD 3: Send ACK + timestamps back (with seq echoed)
            # MOD 2: Encrypt the response
            # ─────────────────────────────────────────
            response_plain = f"ACK|{seq}|{T2}|{T3}"
            encrypted_response = cipher.encrypt(response_plain.encode())
            server_socket.sendto(encrypted_response, addr)

        except socket.timeout:
            continue

except KeyboardInterrupt:
    print("\nServer stopped.")

finally:
    server_socket.close()
