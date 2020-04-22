Credit to Palo Alto Networks for providing these scripts. I just made some minor modifications to add
timestamps to the graphs and fit my needs better

Requirements:
Windows OS
Python 3
requests - pip3 install requests
matplotlib - pip3 install matplotlib

Tip: Run with a read-only admin account if you just want to monitor packet buffers and not actually clear
abusive sessions.

Packet Buffer Abuse Mitigation Script

Disclaimer
This script is provided on an "as is" bases. Palo Alto Networks does not provide support or guarantee the
operation of this script. Customers are free to use the script and make modifications to suit their needs and
network environments.

Purpose
This document describes the issue of a single, or multiple sessions, using up the firewall's packet buffers which
can cause the firewall to operate in a sluggish manner and cause applications to time out.The commands to
show and clear an abusive session was introduced in PAN-OS 7.1.0 and back ported to 6.1.10 and 7.0.6.
As of PAN-OS 7.1.0, there isn't an automated way to clear sessions that are using a large percentage of the
packet buffers and it's still a manual process.

Solution
To automate the discarding of abusive sessions, a Python script can be used to proactively monitor a firewall's
packet buffer utilization for a specific threshold (high water mark). When the threshold is reached, the script will
identify the top sessions using more than 2% of the packet buffers and discard the sessions if they match the
input parameters provided.

Upon termination, the script will generate a log and graph file. The log file named, "packet_buffer_usage.txt"
depicts the start and end time the script was active, as well as the packet buffer utilization at each polling
interval. The graph file named, "packet_buffer_usage.png" shows the packet buffer utilization graphed over the
script's running duration.

Script Parameters
packet_buffer_fix.py : Main script - contains the key generation and the main function definition.
-p : IP-Address of the firewall to monitor
-t : Mitigation threshold percentage range <10%-95%>
-i : Interval to analyze the packet buffer utilization <3-600 seconds>
-a : The type of AppID session(s) to discard
-z : The zone(s) to remove the abusive sessions from
-l : Enables/Disables logging features

An example of the script is shown in the illustration below. The script monitors the packet buffer utilization for a
firewall with IP address 192.168.2.254
• The script will poll and analyze the packet buffer utilization threshold every 3 seconds
• Any sessions identified over the monitored threshold of 50% will be considered for mitigation
• The script will discard abusive sessions for ANY application when the threshold is exceeded


Packet Buffer Abuse Mitigation Script

• The script will discard abusive sessions for ANY zone when the threshold is exceeded

Script Termination
Once the correct input parameters are entered and the script is successfully running, the user can press any
key to terminate the script. When the script is terminated, the log and graph files are created in the same local
directory that contains the python script. 
