"""
Part 1: Client
"""

import socket
import sys


def run_client(host='127.0.0.1', port=9999):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
        print(f"[+] Successfully connected to {host}:{port}")
        print("[*] Start typing to chat with the server. Enter 'quit' to leave.\n")

        while True:
            user_input = input(">> ").strip()

            if not user_input:
                continue

            sock.send(user_input.encode('utf-8'))

            incoming = sock.recv(1024)

            if not incoming:
                print("[!] The server ended the connection.")
                break

            print(f"Server: {incoming.decode('utf-8')}\n")

            if user_input.lower() == 'quit':
                print("[*] Closing connection.")
                break

    except ConnectionRefusedError:
        print(f"[!] Unable to connect — make sure the server is running on {host}:{port}.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[*] Interrupted — closing.")
    except OSError as err:
        print(f"[!] Network error: {err}")
        sys.exit(1)
    finally:
        sock.close()
        print("[*] Socket closed.")


if __name__ == '__main__':
    run_client()
