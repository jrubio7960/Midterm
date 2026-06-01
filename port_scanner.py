"""
Midterm Part 2: Port Scanner 
"""

import socket
import sys
import time
from datetime import datetime


ALLOWED_TARGETS  = ('127.0.0.1', 'localhost', 'scanme.nmap.org')
PORT_TIMEOUT     = 0.5   
DELAY_BETWEEN    = 0.05  
HIGHEST_PORT     = 65535

def check_port(host: str, port: int, timeout: float = PORT_TIMEOUT) -> bool:
    """
    Try opening a TCP connection to host:port.

    Returns True when the connection succeeds (port is open),
    False when it is refused or times out.
    The 'with' block guarantees the socket is closed afterwards.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        code = s.connect_ex((host, port))
        return code == 0

def lookup_host(host: str) -> str:
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[!] Hostname '{host}' could not be resolved.")
        print("    Double-check the address or your internet connection.")
        sys.exit(1)

def check_port_range(first: int, last: int):
    for label, value in (("Start", first), ("End", last)):
        if not (1 <= value <= HIGHEST_PORT):
            print(f"[!] {label} port {value} is outside the valid range (1–{HIGHEST_PORT}).")
            sys.exit(1)
    if first > last:
        print(f"[!] Start port ({first}) cannot be greater than end port ({last}).")
        sys.exit(1)


def run_scan(host: str, first_port: int, last_port: int):
    

    if host.lower() not in ALLOWED_TARGETS:
        print(f"[!] Scanning '{host}' is not allowed.")
        print(f"    Permitted targets: {', '.join(ALLOWED_TARGETS)}")
        sys.exit(1)

    check_port_range(first_port, last_port)

    resolved_ip  = lookup_host(host)
    num_ports    = last_port - first_port + 1
    found_open   = []

    print("=" * 56)
    print("  TCP Port Scanner")
    print(f"  Host    : {host}  ({resolved_ip})")
    print(f"  Ports   : {first_port} to {last_port}  ({num_ports} total)")
    print(f"  Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 56)

    t_start = time.time()

    for port in range(first_port, last_port + 1):
        if (port - first_port) % 50 == 0:
            print(f"  Progress: testing port {port} ...", end='\r')

        if check_port(resolved_ip, port):
            try:
                svc_name = socket.getservbyport(port, 'tcp')
            except OSError:
                svc_name = 'unrecognized'

            print(f"  [OPEN]   {port:<6}  {svc_name}")
            found_open.append((port, svc_name))

        time.sleep(DELAY_BETWEEN)

    elapsed = time.time() - t_start

    print()
    print("=" * 56)
    print(f"  Finished in {elapsed:.2f}s  |  {len(found_open)} open / {num_ports} scanned")

    if found_open:
        print("\n  Open ports:")
        for p, name in found_open:
            print(f"    {p:<7} {name}")
    else:
        print("  No open ports found in this range.")

    print("=" * 56)



def gather_inputs():
    """
    Pull host and port range from sys.argv if provided (3 extra args),
    otherwise ask the user interactively.
    Returns (host, first_port, last_port).
    """
    if len(sys.argv) == 4:
        target = sys.argv[1]
        try:
            p_start = int(sys.argv[2])
            p_end   = int(sys.argv[3])
        except ValueError:
            print("[!] Both port values must be whole numbers.")
            sys.exit(1)
        return target, p_start, p_end

    print("\n=== Port Scanner Setup ===")
    print(f"Allowed targets: {', '.join(ALLOWED_TARGETS)}\n")

    target  = input("Target host [127.0.0.1]: ").strip() or '127.0.0.1'

    try:
        p_start = int(input("First port  [1]:    ").strip() or 1)
        p_end   = int(input("Last port   [1024]: ").strip() or 1024)
    except ValueError:
        print("[!] Port values must be whole numbers.")
        sys.exit(1)

    return target, p_start, p_end


if __name__ == '__main__':
    target_host, start, end = gather_inputs()
    run_scan(target_host, start, end)
