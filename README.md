**Comprehensive SSH Incident Response & System Hardening**

**Objective:**

To simulate a secure network environment, analyze historical SSH authentication logs for malicious activity, generate network traffic artifacts, and execute post-incident system hardening and data sanitization protocols.

**Phase 1: Artifact Generation & Log Analysis**

The initial phase involved parsing raw system logs to identify unauthorized access attempts and generating a realistic packet capture (PCAP) for forensic analysis.

**Log Extraction:** Extracted raw authentication logs from the Linux jump server targeting the SSH service (port 22).

**Traffic Synthesis:** Developed and executed a custom Python script using the Scapy library. This script parsed the raw log text, extracted source and destination IP addresses, and encapsulated the syslog data into UDP packets to generate a forensic PCAP file.

**Network Protocol Analysis:** Imported the generated PCAP into Wireshark for deep packet inspection.

        Identified a failed password authentication event for an invalid user account (attacker) originating from an external IP at 21:11:16.

        Identified a subsequent successful login event for the valid system user ([default_user]) from the identical external IP at 21:18:10.

        **Forensic Conclusion:** The approximate seven-minute delta between the failed and successful attempts strongly indicates manual, human-driven access rather than an automated brute-force attack.

**Phase 2: System Isolation & Service Hardening**

Following the incident analysis, immediate remediation steps were taken to isolate the compromised virtual machine and secure listening services.

**Network Segmentation:** Modified the hypervisor network adapter settings, transitioning the environment from Bridged to NAT. This successfully hid the virtual machine behind the host's IP routing, blocking further unauthorized inbound external connections.

**Service Termination:** Terminated the active SSH daemon to close port 22 and drop any lingering persistent connections:

    sudo systemctl stop ssh

**Persistent Disablement:** Removed the SSH service from the system boot sequence to prevent the service from automatically restarting during future reboots:

    sudo systemctl disable ssh

**Phase 3: Identity & Access Management (IAM)**

To further secure the system, default credentials and standard usernames were systematically eradicated and replaced with custom, secure administrative accounts.

**Superuser Activation:** Temporarily established a password for the locked root account to allow for deep system modifications without active user background process interference.

    sudo passwd root

**Account Migration:** Logged directly into the root environment to overwrite the default system identity. Executed the following commands to rename the user, group, and home directory to a hardened standard (e.g., sec_admin):

    usermod -l sec_admin [default_user]
    
    groupmod -n sec_admin [default_user]
    
    usermod -d /home/sec_admin -m sec_admin

**Credential Hardening:** Assigned new, cryptographically secure passwords to the newly established sec_admin account.

**Privilege Verification:** Logged back in as the new user and successfully verified file ownership continuity (ls -la ~) and administrative capabilities (sudo whoami).

**Phase 4: Operational Security (OPSEC) & Sanitization**

Before publishing this incident report and the associated artifacts, a strict data sanitization process was executed to ensure zero leakage of private host identifiers.

**Data Scrubbing:** Utilized text manipulation to replace real private IP addresses and personal Windows hostnames within the raw logs and Python script with standard documentation placeholders (Attacker: 203.0.113.10, Server: 10.0.0.50).

**Artifact Regeneration:** Re-executed the Python PCAP generation script using the newly sanitized log files, producing a 100% clean, publicly shareable network capture.

**Visual Redaction:** Applied strict black-box redactions to raw screenshots, completely obscuring legacy IP addresses and personal profile paths to maintain professional OPSEC standards.
