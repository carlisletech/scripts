# Packet Buffer Abuse Mitigation Script #

## Credit to Palo Alto Networks for providing these scripts. I just made some minor modifications to add timestamps to the graphs and fit my needs better. ## 

### Requirements: ###
<ul>
<li>Windows OS  
<li>Python 3  
<li>requests - pip3 install requests  
<li>matplotlib - pip3 install matplotlib
</ul>

Tip: Run with a read-only admin account if you just want to monitor packet buffers and not actually clear abusive sessions.  

### Disclaimer ###
This script is provided on an "as is" bases. Palo Alto Networks does not provide support or guarantee the operation of this script. Customers are free to use the script and make modifications to suit their needs and network environments.  

## Purpose ##
This document describes the issue of a single, or multiple sessions, using up the firewall's packet buffers which can cause the firewall to operate in a sluggish manner and cause applications to time out.The commands to show and clear an abusive session was introduced in PAN-OS 7.1.0 and back ported to 6.1.10 and 7.0.6. As of PAN-OS 7.1.0, there isn't an automated way to clear sessions that are using a large percentage of the packet buffers and it's still a manual process.  

## Solution ##
To automate the discarding of abusive sessions, a Python script can be used to proactively monitor a firewall's packet buffer utilization for a specific threshold (high water mark). When the threshold is reached, the script will identify the top sessions using more than 2% of the packet buffers and discard the sessions if they match the input parameters provided.  

Upon termination, the script will generate a log and graph file. The log file named, "packet_buffer_usage.txt" depicts the start and end time the script was active, as well as the packet buffer utilization at each polling interval. The graph file named, "packet_buffer_usage.png" shows the packet buffer utilization graphed over the script's running duration.


## Script Parameters ## 
### Note: these are commented out in my script and variables are hardcoded.  ###
Update the variables and run this:
~~~
python3 packet_buffer_fix.py
~~~

packet_buffer_fix.py : Main script - contains the key generation and the main function definition.  
&nbsp;&nbsp;-p : IP-Address of the firewall to monitor  
&nbsp;&nbsp;-t : Mitigation threshold percentage range <10%-95%>  
&nbsp;&nbsp;-i : Interval to analyze the packet buffer utilization <3-600 seconds>  
&nbsp;&nbsp;-a : The type of AppID session(s) to discard  
&nbsp;&nbsp;-z : The zone(s) to remove the abusive sessions from  
&nbsp;&nbsp;-l : Enables/Disables logging features  

This script monitors the packet buffer utilization for a firewall with IP address 10.1.1.1, with a username admin and password of password.  
<ul>
<li>The script will poll and analyze the packet buffer utilization threshold every 3 seconds  
<li>Any sessions identified over the monitored threshold of 80% will be considered for mitigation  
<li>The script will discard abusive sessions for ANY application when the threshold is exceeded (unless using a read-only account)  
</ul>

## Script Termination ##  
Once the correct input parameters are entered and the script is successfully running, the user can press any key to terminate the script. When the script is terminated, the log and graph files are created in the same local directory that contains the python script.   
