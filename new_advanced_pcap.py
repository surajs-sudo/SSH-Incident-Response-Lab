import re
import time
from datetime import datetime
from scapy.all import IP, UDP, Raw, wrpcap

log_file = "new_extracted_ssh_logs.txt"
pcap_file = "new_realistic_ssh_logs.pcap"
kali_ip = "10.0.0.50" # We know this is the server

# This is a Regular Expression (Regex) pattern that perfectly matches IPv4 addresses
ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

packets = []

try:
    with open(log_file, "r") as file:
        for line in file:
            # 1. SEARCH FOR IPs
            found_ips = ip_pattern.findall(line)
            
            # Set defaults in case the log line doesn't contain an IP
            src_ip = "203.0.113.10" 
            dst_ip = kali_ip
            
            # If the script finds IPs in the text, assign them to the packet headers
            if found_ips:
                src_ip = found_ips[0] # The first IP found is usually the attacker/client
                if len(found_ips) > 1:
                    dst_ip = found_ips[1] # If a second IP is found (like in the timeout log), it's the destination
            
            # 2. CREATE THE PACKET
            packet = IP(src=src_ip, dst=dst_ip) / UDP(sport=514, dport=514) / Raw(load=line.strip())
            
            # 3. FIX THE TIMESTAMP (Optional but makes it perfect)
            # This attempts to read the "Mar 04 21:11:16" text and convert it to a Wireshark time value
            try:
                time_str = line[:15] # Grabs the first 15 characters (the date/time)
                # Adds the current year to make it a complete date, then converts to Unix Epoch time
                full_time_str = f"{datetime.now().year} {time_str}"
                epoch_time = time.mktime(time.strptime(full_time_str, "%Y %b %d %H:%M:%S"))
                packet.time = epoch_time
            except ValueError:
                pass # If it fails to read the time properly, it just skips and uses the current time
                
            packets.append(packet)
            
    wrpcap(pcap_file, packets)
    print(f"Successfully created a realistic PCAP with {len(packets)} packets.")

except FileNotFoundError:
    print(f"Error: Could not find {log_file}.")
