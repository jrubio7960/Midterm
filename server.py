"""
Part 1: Server
"""

import socket
import sys


def run_server(host='127.0.0.1', port=9999):
    

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind((host, port))

        sock.listen(1)
        print(f"[*] Listening on {host}:{port} — press Ctrl+C to quit\n")

        while True:
            conn, addr = sock.accept()
            print(f"[+] Accepted connection from {addr[0]}:{addr[1]}")

            handle_session(conn, addr)

    except KeyboardInterrupt:
        print("\n[*] Shutting down — goodbye!")
    except OSError as err:
        print(f"[!] Could not start server: {err}")
        sys.exit(1)
    finally:
        sock.close()
        print("[*] Server has stopped.")


def handle_session(conn, addr):
    
    try:
        while True:
            data = conn.recv(1024)

            if not data:
                print(f"[-] {addr} closed the connection.")
                break

            text = data.decode('utf-8').strip()
            print(f"[>>] {addr[0]} says: {text}")

            if text.lower() == 'quit':
                conn.send("Farewell! Connection closing.".encode('utf-8'))
                print(f"[-] {addr} requested exit.")
                break

            reply = f"[Server] Got it: {text}"
            conn.send(reply.encode('utf-8'))
            print(f"[<<] Replied: {reply}")

    except ConnectionResetError:
        print(f"[!] {addr} dropped the connection unexpectedly.")
    except OSError as err:
        print(f"[!] Socket error during session with {addr}: {err}")
    finally:
        conn.close()
        print(f"[*] Session with {addr} ended.\n")


if __name__ == '__main__':
    run_server()
