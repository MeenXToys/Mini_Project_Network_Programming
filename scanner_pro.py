#!/usr/bin/env python3
"""
SPG0463 Network Programming – Mini Project
Title: Network Scanner – Scan IP Range & Save Results to CSV
Group Size: 3
Author: Muhaimin, Akmal Mustofa, Amir Arshad
Date: 25 OCT 2025

Description:
This script scans a user-specified range of IPv4 addresses for an open TCP port
(default port 80). It determines which hosts are online using socket.connect_ex(),
records response time, and saves the results into a structured CSV file.
"""

import socket
import csv
import ipaddress
import time
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global flag to control scanning
scanning_active = True

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
    # Check if scanning should stop
    if not scanning_active:
        return None

    result = {
        'ip': ip,
        'port': port,
        'status': 'closed',
        'hostname': '',
        'rtt_ms': None,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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

            # Hostname Lookup (Reverse DNS)
            try:
                # gethostbyaddr returns (hostname, aliases, ipaddrlist). We take the first element (hostname)
                hostname = socket.gethostbyaddr(ip)[0]
                result['hostname'] = hostname
            except (socket.herror, socket.gaierror):
                # Heror/Gaierror means the IP is active but no registered name was found
                result['hostname'] = ''
        else:
            result['status'] = 'closed'

        sock.close()

    # Catch common network/socket exceptions
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        result['status'] = 'error'
        result['error'] = str(e)

    return result

# -------------------------------
# Function: scan_ip_range
# -------------------------------
def scan_ip_range(start_ip, end_ip, port=80, timeout=1.0, max_workers=100):
    """Scan all IPs in the range concurrently using ThreadPoolExecutor."""
    global scanning_active
    
    ips = generate_ip_range(start_ip, end_ip)
    results = []

    print(f"Scanning {len(ips)} IP addresses on port {port}...")
    print("Press Ctrl+C to stop the scan\n")

    workers = min(max_workers, len(ips))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_ip = {executor.submit(scan_ip, ip, port, timeout): ip for ip in ips}
        for future in as_completed(future_to_ip):
            if not scanning_active:
                executor.shutdown(wait=False)
                print("\nScan stopped by user!")
                break
                
            try:
                result = future.result()
                if result:  # Only append if we got a result (not None)
                    results.append(result)
            except (socket.timeout, ConnectionRefusedError, OSError) as e:
                if scanning_active:  # Only add errors if we're still scanning
                    results.append({
                        'ip': future_to_ip[future],
                        'port': port,
                        'status': 'error',
                        'hostname': '',
                        'rtt_ms': None,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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
# Function: display_online_hosts_with_hostnames
# -------------------------------
def display_online_hosts_with_hostnames(results):
    """Display only online hosts that have a valid hostname."""
    # Filter: only online hosts with non-empty hostnames
    online_hosts_with_names = [
        r for r in results 
        if r['status'] == 'open' and r['hostname'] and r['hostname'].strip()
    ]
    
    if online_hosts_with_names:
        print("\nOnline IP Addresses and Hostnames:")
        for host in online_hosts_with_names:
            ip = host['ip']
            hostname = host['hostname'].strip()
            print(f"{ip} - {hostname}")
    else:
        print("\nNo online hosts with hostnames found.")

# -------------------------------
# Function: signal_handler
# -------------------------------
def signal_handler(sig, frame):
    """Handle Ctrl+C interruption."""
    global scanning_active
    print("\n\nReceived interrupt signal...")
    scanning_active = False

# -------------------------------
# Main Function
# -------------------------------
def main():
    """Main entry point — handles user input, runs the network scan, and displays summary output."""
    global scanning_active
    
    print("=== Network Scanner (SPG0463) ===\n")
    print("Note: You can press Ctrl+C at any time to stop the current scan\n")

    while True:
        try:
            # Reset the scanning flag
            scanning_active = True
            
            # Set up signal handler for Ctrl+C
            import signal
            signal.signal(signal.SIGINT, signal_handler)

            start_ip = input("\nEnter Start IP (e.g. 192.168.1.1): ").strip()
            if not start_ip:
                print("No IP entered. Exiting.")
                break
                
            end_ip = input("Enter End IP (e.g. 192.168.1.10): ").strip()
            if not end_ip:
                print("No IP entered. Exiting.")
                break
                
            port = input("Enter Port [Default 80]: ").strip()
            timeout = input("Enter Timeout in seconds [Default 1.0]: ").strip()

            port = int(port) if port else 80
            timeout = float(timeout) if timeout else 1.0

            # Safety check for port range
            if not (1 <= port <= 65535):
                raise ValueError("Port number must be between 1 and 65535.")

            start_time = time.time()
            results = scan_ip_range(start_ip, end_ip, port=port, timeout=timeout)
            elapsed = time.time() - start_time

            # Display only online hosts with hostnames
            display_online_hosts_with_hostnames(results)
            
            # Only save to CSV if we have results and scanning wasn't interrupted
            if results and scanning_active:
                csv_file = save_results_to_csv(results)
                open_count = sum(1 for r in results if r['status'] == 'open')
                open_with_hostname_count = sum(1 for r in results if r['status'] == 'open' and r['hostname'] and r['hostname'].strip())

                print("\n=== Scan Summary ===")
                print(f"Total IPs Scanned: {len(results)}")
                print(f"Open Hosts Found: {open_count}")
                print(f"Open Hosts With Hostnames: {open_with_hostname_count}")
                print(f"Time Elapsed: {elapsed:.2f} seconds")
                print(f"Results saved to: {csv_file}")
            elif not scanning_active:
                print(f"\nPartial scan completed: {len(results)} IPs scanned in {elapsed:.2f} seconds")

            # Ask if user wants to scan again
            while True:
                again = input("\nDo you want to scan again? (y/n): ").strip().lower()
                if again in ['y', 'yes', 'n', 'no']:
                    break
                print("Please enter 'y' for yes or 'n' for no.")
            
            if again in ['n', 'no']:
                print("Thank you for using Network Scanner. Goodbye!")
                break

        except ValueError as ve:
            print(f"Input error: {ve}")
        except KeyboardInterrupt:
            print("\n\nScan cancelled by user.")
            break
        except (OSError, socket.error) as e:
            print(f"Unexpected error: {e}")

# -------------------------------
# Script Entry Point
# -------------------------------
if __name__ == '__main__':
    main()
