# 🛰️ Network Scanner (SPG 0463)

[![Python](https://img.shields.io/badge/Python-3.x-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Status](https://img.shields.io/badge/Project-Completed-success)]()
[![GMI](https://img.shields.io/badge/GMI-Network%20Programming-orange)]()

A fast, multi-threaded **IPv4 Network Scanner** developed for the  
**SPG 0463 – Network Programming** course at the **German-Malaysian Institute (GMI)**.

This tool scans a user-defined IP range, checks TCP port connectivity, resolves hostnames, measures RTT, and exports the results into a timestamped CSV file.

---

## 🚀 Features

✔ **Scan IP Ranges** – Enter start & end IPv4 addresses  
✔ **Configurable Port & Timeout**  
✔ **Fast Multi-threaded Execution** using ThreadPoolExecutor  
✔ **Reverse DNS Lookup** (`socket.gethostbyaddr`)  
✔ **RTT Measurement** in milliseconds  
✔ **CSV Export** with timestamps  
✔ **Rich Console Output**  
✔ **Graceful Ctrl+C Stop**  
✔ **Robust Error Handling**  

---

## 📦 Demo Output

=== Network Scanner (SPG0463) ===

Enter Start IP (e.g. 10.0.0.0): 10.0.0.0


Enter End IP (e.g. 10.0.1.0): 10.0.1.0


Scanning 257 IP addresses on port 80...


Online IP Addresses and Hostnames:

10.0.0.27 - mikrotik.gmi.edu

10.0.0.21 - vinchin.gmi.edu

10.0.0.28 - obe.gmi.edu.my

...


=== Scan Summary ===

Total IPs Scanned: 257

Open Hosts Found: 10

Time Elapsed: 8.79 seconds

Results saved to: scan_results_20251114_022916.csv


---

## 📊 Sample CSV Output

ip,hostname,port,status,rtt_ms,timestamp,error

10.0.0.27,mikrotik.gmi.edu,80,open,2.91,14/11/2025 02:31,

10.0.0.21,vinchin.gmi.edu,80,open,4.33,14/11/2025 02:31,

10.0.0.28,obe.gmi.edu.my,80,open,2.73,14/11/2025 02:31,


---

## 🛠️ How to Use

### 1️⃣ Install Python 3  
Make sure your system has **Python 3.8+**.

---

### 2️⃣ Clone the Repository  

```bash
git clone https://github.com/your-username/network-scanner.git
cd network-scanner
````

---

### 3️⃣ Run the Program
python network_scanner.py


### 4️⃣ Follow On-Screen Prompts
Enter:

Start IP


End IP


Port (optional)


Timeout (optional)


Results will be displayed and exported as a CSV file.


---

### ⚠️ Legal Disclaimer
This tool is intended for educational and authorized use only.

Do NOT scan networks or hosts without explicit permission.

Unauthorized scanning may violate:


Local laws


Institutional policies


Ethical cybersecurity guidelines


Use responsibly.


---

### 👨‍💻 Authors

| Name                 | ID            |
|----------------------|---------------|
| **Muhaimin Bin Mahadi** | CBS24070656   |
| **Akmal Mustofa**       | CBS24070556   |
| **Amir Arshad**         | CBS24070519   |

**Course:** SPG 0463 – Network Programming  
**Supervisor:** Ms. Noor Atiqah Mohd Yaacob @ Yahya  
**Institution:** German-Malaysian Institute (GMI)


---

### 📄 License
This project is licensed under the MIT License.
You are free to use, modify, and distribute this tool with proper attribution.

---

### ⭐ Support This Project
If you find this project useful, consider giving the repo a:

