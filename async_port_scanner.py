#!/usr/bin/env python3
"""
interactive_scanner.py

Interactive, threaded multi-port TCP scanner with banner grabbing.
Prompts the user for inputs (host or start/end, ports, timeout, threads, etc.)

Educational use only.
"""

import csv
import ipaddress
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Optional, Dict

# ----------------- Utilities -----------------

def parse_ports(port_str: str) -> List[int]:
    """Parse port strings like '22,80,8000-8010' into a sorted list of ints."""
    parts = [p.strip() for p in port_str.split(",") if p.strip()]
    ports = set()
    for p in parts:
        if "-" in p:
            a, b = p.split("-", 1)
            a = int(a); b = int(b)
            if a > b:
                a, b = b, a
            for x in range(max(1, a), min(65535, b) + 1):
                ports.add(x)
        else:
            x = int(p)
            if 1 <= x <= 65535:
                ports.add(x)
    return sorted(ports)

def generate_ips(start: Optional[str], end: Optional[str], host: Optional[str]) -> List[str]:
    """Return a list of IPs for single host or inclusive start..end range."""
    if host:
        return [host]
    if not start or not end:
        raise ValueError("Either host or both start and end must be provided.")
    s = ipaddress.IPv4Address(start)
    e = ipaddress.IPv4Address(end)
    if s > e:
        raise ValueError("Start IP must be <= End IP.")
    return [str(ipaddress.IPv4Address(i)) for i in range(int(s), int(e) + 1)]

def try_reverse_dns(ip: str) -> str:
    """Best-effort reverse DNS lookup (blocking)."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""

# ----------------- Scanner -----------------

def scan_target(ip: str, port: int, timeout: float = 1.0, banner: bool = False,
                read_bytes: int = 512) -> Dict:
    """
    Attempt to connect to ip:port using TCP.
    Returns dict with keys: ip, port, status, rtt, banner, error
    """
    result = {"ip": ip, "port": port, "status": "closed", "rtt": None, "banner": "", "error": ""}
    sock = None
    start = time.perf_counter()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        err = sock.connect_ex((ip, port))
        elapsed = time.perf_counter() - start
        result["rtt"] = round(elapsed, 4)

        if err == 0:
            result["status"] = "open"
            # banner grab (best-effort)
            if banner:
                try:
                    sock.settimeout(min(timeout, 1.0))
                    data = sock.recv(read_bytes)
                    if data:
                        try:
                            result["banner"] = data.decode(errors="replace").strip()
                        except Exception:
                            result["banner"] = repr(data[:200])
                except socket.timeout:
                    pass
                except Exception as e:
                    result["error"] = f"banner_err:{e}"
        else:
            result["status"] = "closed"
            result["error"] = str(err)
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    finally:
        if sock:
            try:
                sock.close()
            except Exception:
                pass
    return result

def scan_many(ips: List[str], ports: List[int], timeout: float = 1.0, banner: bool = False,
              threads: int = 200, read_bytes: int = 512, reverse_dns: bool = False):
    """Scan all ips x ports using a thread pool. Return list of result dicts."""
    results = []
    total_tasks = len(ips) * len(ports)
    printed = 0
    start_time = datetime.now()
    print(f"[{start_time.isoformat()}] Starting scan: {len(ips)} hosts x {len(ports)} ports = {total_tasks} checks")
    with ThreadPoolExecutor(max_workers=threads) as exe:
        future_to_target = {}
        for ip in ips:
            for port in ports:
                future = exe.submit(scan_target, ip, port, timeout, banner, read_bytes)
                future_to_target[future] = (ip, port)
        for future in as_completed(future_to_target):
            ip, port = future_to_target[future]
            try:
                res = future.result()
            except Exception as e:
                res = {"ip": ip, "port": port, "status": "error", "rtt": None, "banner": "", "error": str(e)}
            if reverse_dns and res.get("status") == "open":
                try:
                    res["hostname"] = try_reverse_dns(ip)
                except Exception:
                    res["hostname"] = ""
            else:
                res["hostname"] = ""
            results.append(res)
            printed += 1
            # lightweight progress prints
            if printed % max(1, total_tasks // 20) == 0 or res.get("status") == "open":
                print(f"[{datetime.now().isoformat()}] Progress: {printed}/{total_tasks}  Last: {ip}:{port} {res['status']}")
    duration = datetime.now() - start_time
    print(f"[{datetime.now().isoformat()}] Scan complete in {duration}. Open ports: {sum(1 for r in results if r['status']=='open')}")
    return results

# ----------------- I/O -----------------

def save_csv(results: List[Dict], filename: str):
    fieldnames = ["ip", "hostname", "port", "status", "rtt", "banner", "error"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({
                "ip": r.get("ip"),
                "hostname": r.get("hostname", ""),
                "port": r.get("port"),
                "status": r.get("status"),
                "rtt": r.get("rtt"),
                "banner": (r.get("banner") or "")[:1000],
                "error": r.get("error", ""),
            })

# ----------------- Interactive prompts -----------------

def prompt(prompt_text: str, default: Optional[str] = None) -> str:
    if default is not None:
        full = f"{prompt_text} [{default}]: "
    else:
        full = f"{prompt_text}: "
    val = input(full).strip()
    return val if val else (default or "")

def ask_yes_no(prompt_text: str, default: bool = False) -> bool:
    d = "Y/n" if default else "y/N"
    val = input(f"{prompt_text} ({d}): ").strip().lower()
    if val == "":
        return default
    return val in ("y", "yes")

def interactive_main():
    print("Interactive Port Scanner (educational use only)\n")

    mode = prompt("Scan mode - single host or range? Enter 'host' or 'range'", "host").lower()
    if mode not in ("host", "range"):
        print("Invalid mode, defaulting to 'host'.")
        mode = "host"

    host = ""
    start = ""
    end = ""
    if mode == "host":
        host = prompt("Enter target host (IP or hostname)", "127.0.0.1")
    else:
        start = prompt("Enter start IPv4 (inclusive)", "192.168.1.1")
        end = prompt("Enter end IPv4 (inclusive)", "192.168.1.254")

    ports_input = prompt("Enter ports (e.g. 22,80,8000-8010)", "22,80,443")
    try:
        ports = parse_ports(ports_input)
        if not ports:
            raise ValueError("No ports parsed")
    except Exception as e:
        print("Invalid ports input:", e)
        return

    timeout = float(prompt("Socket timeout seconds", "1.0") or 1.0)
    threads = int(prompt("Worker threads (concurrency)", "200") or 200)
    banner = ask_yes_no("Attempt banner grabbing?", False)
    rdns = ask_yes_no("Attempt reverse DNS for open hosts?", False)
    read_bytes = int(prompt("Max banner bytes to read", "512") or 512)
    csv_file = prompt("CSV output filename (leave empty to skip)", "")

    # expand IP list
    try:
        ips = generate_ips(start if start else None, end if end else None, host if host else None)
    except Exception as e:
        print("IP error:", e)
        return

    print(f"\nStarting scan: {len(ips)} hosts, {len(ports)} ports, threads={threads}, timeout={timeout}s")
    results = scan_many(
        ips=ips,
        ports=ports,
        timeout=timeout,
        banner=banner,
        threads=threads,
        read_bytes=read_bytes,
        reverse_dns=rdns,
    )

    if csv_file:
        try:
            save_csv(results, csv_file)
            print(f"Saved CSV to {csv_file}")
        except Exception as e:
            print("Error writing CSV:", e)

    open_ports = [r for r in results if r["status"] == "open"]
    if open_ports:
        print("\nOpen ports found (first 50):")
        for r in open_ports[:50]:
            print(f"  {r['ip']}:{r['port']}  hostname={r.get('hostname') or '-'}  banner={(r.get('banner') or '')[:120]}")
    else:
        print("\nNo open ports found.")

if __name__ == "__main__":
    interactive_main()
