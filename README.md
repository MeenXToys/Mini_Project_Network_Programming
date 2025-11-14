Network Scanner (SPG 0463)

A simple, multi-threaded network scanner written in Python for the SPG 0463 Network Programming mini-project.

This tool scans a user-specified range of IPv4 addresses for a specific TCP port (defaulting to port 80). It uses socket.connect_ex() to identify online hosts, performs a reverse DNS lookup to find their hostnames, measures the response time (RTT), and saves all results to a timestamped CSV file.

Features

Scan IP Ranges: Specify a start and end IPv4 address.

Configurable Port & Timeout: Choose which TCP port to scan and set a connection timeout.

Fast & Concurrent: Uses multi-threading (ThreadPoolExecutor) to scan many hosts at once.

Hostname Resolution: Performs a reverse DNS lookup (socket.gethostbyaddr) to find hostnames.

Response Time (RTT): Measures the connection time in milliseconds.

Structured CSV Export: Saves all results (open, closed, and errors) to a timestamped CSV file.

Robust Error Handling: Gracefully handles timeouts, connection refusals, and invalid input.

Graceful Stop: Press Ctrl+C at any time to stop the scan safely without crashing.

Demo

Here is the output from running the script and scanning a network range.

=== Network Scanner (SPG0463) ===

Note: You can press Ctrl+C at any time to stop the current scan

Enter Start IP (e.g. 10.0.0.0): 10.0.0.0
Enter End IP (e.g. 10.0.1.0): 10.0.1.0
Enter Port [Default 80]: 
Enter Timeout in seconds [Default 1.0]: 

Scanning 257 IP addresses on port 80...
Press Ctrl+C to stop the scan


Online IP Addresses and Hostnames:
10.0.0.27 - mikrotik.gmi.edu
10.0.0.21 - vinchin.gmi.edu
10.0.0.28 - obe.gmi.edu.my
10.0.0.24 - media.gmi.edu.my
10.0.0.13 - nms.gmi.edu.my
10.0.0.12 - ess.gmi.edu.my
10.0.0.35 - gmidashboard.gmi.edu
10.0.0.40 - vlu.gmi.edu.my
10.0.0.8 - cworks.gmi.edu.my
10.0.0.11 - class.gmi.edu

=== Scan Summary ===
Total IPs Scanned: 257
Open Hosts Found: 10
Open Hosts With Hostnames: 10
Time Elapsed: 8.79 seconds
Results saved to: scan_results_20251114_022916.csv

Do you want to scan again? (y/n): n
Thank you for using Network Scanner. Goodbye!


Sample CSV Output

The script generates a detailed CSV file (scan_results_YYYYMMDD_HHMMSS.csv) for documentation and analysis.

ip,hostname,port,status,rtt_ms,timestamp,error
10.0.0.27,mikrotik.gmi.edu,80,open,2.91,14/11/2025 2:31,
10.0.0.21,vinchin.gmi.edu,80,open,4.33,14/11/2025 2:31,
10.0.0.28,obe.gmi.edu.my,80,open,2.73,14/11/2025 2:31,
10.0.0.24,media.gmi.edu.my,80,open,1.38,14/11/2025 2:31,
10.0.0.13,nms.gmi.edu.my,80,open,2.6,14/11/2025 2:31,
10.0.0.12,ess.gmi.edu.my,80,open,2.65,14/11/2025 2:31,
10.0.0.35,gmidashboard.gmi.edu,80,open,3.6,14/11/2025 2:31,
10.0.0.40,vlu.gmi.edu.my,80,open,1.97,14/11/2025 2:31,
10.0.0.8,cworks.gmi.edu.my,80,open,2.96,14/11/2025 2:31,
10.0.0.11,class.gmi.edu,80,open,25.72,14/11/2025 2:31,
... 


How to Use

Ensure you have Python 3 installed on your system.

Clone this repository or download the network_scanner.py file.

git clone [https://github.com/your-username/network-scanner.git](https://github.com/your-username/network-scanner.git)
cd network-scanner


Run the script from your terminal:

python network_scanner.py


Follow the on-screen prompts to enter the Start IP, End IP, Port, and Timeout.

The results will be printed to the console, and a detailed CSV file will be saved in the same directory.

⚠️ Disclaimer

This tool is intended for educational purposes only. Only run this scanner on networks and hosts you have explicit permission to test. Unauthorized scanning may be illegal or violate acceptable use policies.

Authors

This project was prepared by:

Muhaimin bin Mahadi (CBS24070656)

Akmal Mustofa

Amir Arshad

This project was submitted for the SPG 0463 Network Programming course at the German-Malaysian Institute (GMI), under the supervision of Ms. Noor Atiqah Mohd Yaacob@Yahya.

License

This project is licensed under the MIT License.
