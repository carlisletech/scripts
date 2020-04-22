"""
This script generates the packet_buffer_usage graph used by 
the packet_buffer_fix script
"""

import matplotlib.pyplot as plt
import os
import time

def create_graph():
	i = 0
	xArray = []
	vArray = []
	timestr = time.strftime("%Y%m%d-%H%M%S")
	
	## Stores values from .txt file into vArray and xArray
	with open("packet_buffer_usage_temp.txt", "r") as file:
		for line in file:
			vArray.append(line)
			xArray.append(i)
			i += 1
	
	plt.plot(xArray, vArray)
	plt.title("Packet Buffer Utilization")
	plt.xlabel("Interval Iterations")
	plt.ylabel("Percentage (%)")	
	plt.savefig(timestr + "packet_buffer_usage.png")

	## Deletes temp file
	os.remove("packet_buffer_usage_temp.txt")		
