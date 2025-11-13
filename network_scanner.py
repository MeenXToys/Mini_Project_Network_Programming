#!/usr/bin/env python3
"""
SPG0463 Network Programming – Mini Project
Title: Network Scanner – Scan IP Range & Save Results to CSV
Group Size: 3
Author: Muhaimin, Akmal Mustofa, Amir Arshad
Date: 5 OCT 2025

Description:
This script scans a user-specified range of IPv4 addresses for an open TCP port
(default port 80). It determines which hosts are online using socket.connect_ex(),
records response time, and saves the results into a structured CSV file.
"""

import socket
import csv
import ipaddress
import time
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed



# -------------------------------
# Function: validate_ip
# -------------------------------
def validate_ip(ip_str):
    """Validate IPv4 address format."""
    try:
        return ipaddress.IPv4Address(ip_str)
    except ipaddress.AddressValueError:
        raise ValueError(f"Invalid IP address: {ip_str}") from None


# -------------------------------
# Function: generate_ip_range
# -------------------------------
def generate_ip_range(start_ip_str, end_ip_str):
    """Generate a list of IP addresses from start to end (inclusive)."""
    start_ip = validate_ip(start_ip_str)
    end_ip = validate_ip(end_ip_str)
    if int(end_ip) < int(start_ip):
        raise ValueError("End IP must not be smaller than Start IP.")
    return [str(ipaddress.IPv4Address(i)) for i in range(int(start_ip), int(end_ip) + 1)]


# -------------------------------
# Function: scan_ip
# -------------------------------
def scan_ip(ip, port=80, timeout=1.0):
    """
    Attempt to connect to a single IP address on the given TCP port.
    Returns a dictionary with scan details (status, RTT, etc.).
    """
    result = {
        'ip': ip,
        'port': port,
        'status': 'closed',
        'hostname': '',
        'rtt_ms': None,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'error': ''
    }

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        start = time.perf_counter()
        code = sock.connect_ex((ip, port))
        end = time.perf_counter()

        rtt = (end - start) * 1000.0  # convert to milliseconds
        result['rtt_ms'] = round(rtt, 2)

        if code == 0:
            result['status'] = 'open'
            try:
                result['hostname'] = socket.gethostbyaddr(ip)[0]
            except (socket.herror, socket.gaierror):
                result['hostname'] = ''
        else:
            result['status'] = 'closed'

        sock.close()

    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        result['status'] = 'error'
        result['error'] = str(e)

    return result


# -------------------------------
# Function: scan_ip_range
# -------------------------------
def scan_ip_range(start_ip, end_ip, port=80, timeout=1.0, max_workers=100):
    """Scan all IPs in the range concurrently using ThreadPoolExecutor."""
    ips = generate_ip_range(start_ip, end_ip)
    results = []

    print(f"Scanning {len(ips)} IP addresses on port {port}...")

    workers = min(max_workers, len(ips))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_ip = {executor.submit(scan_ip, ip, port, timeout): ip for ip in ips}
        for future in as_completed(future_to_ip):
            try:
                result = future.result()
                results.append(result)
            except (socket.timeout, ConnectionRefusedError, OSError) as e:
                results.append({
                    'ip': future_to_ip[future],
                    'port': port,
                    'status': 'error',
                    'hostname': '',
                    'rtt_ms': None,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'error': str(e)
                })

    return results


# -------------------------------
# Function: save_results_to_csv
# -------------------------------
def save_results_to_csv(results):
    """Save scan results to a CSV file with a timestamped filename."""
    filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    fieldnames = ['ip', 'hostname', 'port', 'status', 'rtt_ms', 'timestamp', 'error']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    return filename


# -------------------------------
# Main Function
# -------------------------------
def main():
    """Main entry point — handles user input, runs the network scan, and displays summary output."""
    print("=== Network Scanner (SPG0463) ===\n")

    try:
        start_ip = input("Enter Start IP (e.g. 10.0.0.0): ").strip()
        end_ip = input("Enter End IP (e.g. 10.0.1.0): ").strip()
        port = input("Enter Port [Default 80]: ").strip()
        timeout = input("Enter Timeout in seconds [Default 1.0]: ").strip()

        port = int(port) if port else 80
        timeout = float(timeout) if timeout else 1.0

        start_time = time.time()
        results = scan_ip_range(start_ip, end_ip, port=port, timeout=timeout)
        elapsed = time.time() - start_time

        csv_file = save_results_to_csv(results)
        open_count = sum(1 for r in results if r['status'] == 'open')

        print("\n=== Scan Summary ===")
        print(f"Total IPs Scanned: {len(results)}")
        print(f"Open Hosts Found: {open_count}")
        print(f"Time Elapsed: {elapsed:.2f} seconds")
        print(f"Results saved to: {csv_file}")

    except ValueError as ve:
        print(f"Input error: {ve}")
    except KeyboardInterrupt:
        print("\nScan cancelled by user.")
    except (OSError, socket.error) as e:
        print(f"Unexpected error: {e}")


# -------------------------------
# Script Entry Point
# -------------------------------
if __name__ == '__main__':
    main()
