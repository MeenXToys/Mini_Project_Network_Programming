# 🧠 SPG0463 Network Programming Mini Project  
## Network Scanner — Scan IP Range & Save Results to CSV  

### 📘 Project Overview
This project is developed for the **SPG0463 (Network Programming)** mini project course at the **German-Malaysian Institute (GMI)**.  
It demonstrates a basic **network scanning tool** that checks a range of IPv4 addresses to determine which hosts have an open TCP port (default: port 80).  
The tool uses Python’s `socket` module to test connectivity and stores all results in a structured CSV file.  

---

### 👨‍💻 **Group Members**
| Name | Role |
|------|------|
| Muhaimin Bin Mahadi | Developer / Tester |
| Akmal Mustofa | Research / Documentation |
| Mohamad Amir Arshad | Report / Presentation |

---

### 🎯 **Objectives**
1. To develop a Python program that scans a user-defined IP range to identify active hosts and open ports.  
2. To enhance efficiency using concurrent scanning techniques.  
3. To generate a structured CSV output for easy result analysis and reporting.  

---

### 🧩 **Features**
- User-input for Start IP, End IP, Port, and Timeout.  
- Scans multiple IPs concurrently for faster execution.  
- Determines if the target port (default 80) is **open**, **closed**, or **unreachable**.  
- Measures approximate **Round Trip Time (RTT)** for each connection attempt.  
- Automatically saves all results in a timestamped **CSV file**.  
- Includes **robust error handling** and informative console output.  

---

### ⚙️ **Technical Details**
- **Language:** Python 3.8+  
- **Libraries Used:**  
  - `socket` — for network connection handling  
  - `ipaddress` — for generating valid IP ranges  
  - `concurrent.futures` — for multi-threaded scanning  
  - `csv` — for output file generation  
  - `datetime`, `time` — for timestamps and performance measurement  

---

### 💻 **How to Run**
1. Clone or copy the project folder to your computer.  
2. Open a terminal or command prompt in the project directory.  
3. Run the following command:
   ```bash
   python network_scanner.py
