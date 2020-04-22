#!/usr/bin/env python3

"""
See readme

Update the IP addrress, user, and password as necessary.
You can also replace define the API key in the "key = " definition

"""

import getopt
import logging
import msvcrt
import re
import requests
import sys
import time
import graph_data


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def key_grab(IP,user,password):
    """Take in input IP, uname and password and retrieve API key from firewall"""
    logging.debug("In API key gen routine")
    try:
        resp = requests.get('https://{0}/api?type=keygen&user={1}&password={2}'.format(IP, user, password), verify=False, timeout = 240)
    except IOError:
        print ("Unable to get the device's API key as the connection was refused/timed out. Please check connectivity.")
        logging.debug("Error occurred when trying to retrieve API key")
        raise SystemExit(1)
    data1 = resp.text
    keystart = data1.find("<key>")
    keystart = data1.find(">", keystart) + 1
    keyend = data1.find("</key>", keystart)
    api_key = data1[keystart:keyend]
    return api_key

def main(argv):
	IP = '10.1.1.1'
	threshold = '80'
	interval = '3'
	applications = 'Any'
	default = False
	zone = 'Any'
	default2 = False
	log = 'Yes'
	list1 = []
	list2 = []
	vArray = []
	tArray = []
	errormsg = """
#Note: I have all this commented out and am using hardcoded variables
usage: packet_buffer_fix.py -p <IP-Address> -t <mitigation percentage> -i <polling interval> -a [arguments] -z [zones] -l <Yes/No>
	
	-p 		IP-Address of firewall
	-t 		Mitigation Percentage Range: <10-95>
	-i 		Polling Interval Range in seconds: <3-600> 
	-a 		Type "Any" to remove all AppID sessions 
			Type sepecific AppID session(s) to remove separated by a comma  	Ex) -a argument1,argument2,argument3
	-z		Type "Any" to remove all sessions reguardless of zone
			Type specific zone(s) separated by a comma to remove specific sessions		Ex) -z Trust-L3,Untrust
	-l		Create a graph and log file or not
	
	***Note: App-IDs and Zones are case sensitive.*** 
	"""
	"""	
	## Checks command line arguments for correct input
	if len(sys.argv) != 13:
		print (errormsg)
		sys.exit(1)
	try:
		opts, args = getopt.getopt(argv,"p:t:i:a:z:l:",["pfile=","tfile=","ifile=","afile=","zfile=","lfile"])
	except getopt.GetoptError:
		print (errormsg)
		sys.exit(1)
	for opt, arg in opts:
		if opt in ("-p", "--pfile"):
			IP = arg
		elif opt in ("-t", "--tfile"):
			threshold = arg
		elif opt in ("-i", "--ifile"):
			interval = arg
		elif opt in ("-a", "--afile"):
			applications = arg
		elif opt in ("-z", "--zfile"):
			zone = arg
		elif opt in ("-l", "--lfile"):
			log = arg
	"""				
	## Ensures input values are within proper value range
	threshold = int(threshold)
	if threshold < 10 or threshold > 95:
		print ("ERROR - Mitigation Percentage Range: <10-95>")
		sys.exit(1)
	interval = int(interval)
	if interval < 3 or interval > 600: 
		print ("ERROR - Polling Interval Range: <3-600>")
		sys.exit(1)
	
	if applications == "any" or applications == "Any":
		default = True
	else:
		## Stores user arguments in a list
		argidx = applications.find(",")
		## User entered a single argument
		if argidx == -1:
			list1.append(applications)
		## User entered multiple arguments separated by a comma
		else:
			argstart = 0
			while(argidx != -1):
				list1.append(applications[argstart:argidx])
				argstart = argidx + 1
				argidx = applications.find(",", argstart)
			list1.append(applications[argstart:len(applications)])

	if zone == "any" or zone == "Any":
		default2 = True
	else:
		## Stores user arguments in a list
		zoneidx = zone.find(",")
		## User entered a single zone
		if zoneidx == -1:
			list2.append(zone)
		## User entered multiple zones separated by a comma
		else:
			zonestart = 0
			while(zoneidx != -1):
				list2.append(zone[zonestart:zoneidx])
				zonestart = zoneidx + 1
				zoneidx = zone.find(",", zonestart)
			list2.append(zone[zonestart:len(zone)])
	
	print("IP: ", IP)
	print("Threshold: ", threshold)
	print("Interval: ", interval)
	print("Applications: ", applications)
	print("Zone: ", zone)
	print("Logging: ", log)
	print("***Press any key to stop script***")
	
	## Generates key for use with the firewall
	key = key_grab('10.1.1.1','admin','password')
	
	if(log == "YES" or log == "Yes" or log == "yes"):
		## Adds start time to output log file
		file = open("packet_buffer_usage.txt", "w")
		file.write("Start Time: " + time.strftime("%d/%m/%Y ") + time.strftime("%I:%M:%S") + "\n")
		file.close()

	## Look for packet buffer usage and terminates a session if it is using more than the given percentage amount
	while 1:
		print("...")
		## Ends program if user input is detected
		if msvcrt.kbhit():
			break
		resp = requests.get('https://{0}/api/?type=op&cmd=op&cmd=<show><running><resource-monitor><second><last>1<%2Flast><%2Fsecond><%2Fresource-monitor><%2Frunning><%2Fshow>&key={1}'.format(IP, key), verify=False)
		data = resp.text
		pvalue = data.find("buffer")
		startidx = data.find("value", pvalue)
		startidx = data.find(">", startidx) + 1 ## Goes to the end of <value>
		endidx = data.find("</value", startidx)
		#import pdb; pdb.set_trace()
		pvaluepercent = int(data[startidx:endidx])
		#import pdb; pdb.set_trace()
		vArray.append(pvaluepercent)
		tArray.append(time.strftime("%I:%M:%S"))
		if pvaluepercent > threshold:
			ingresslog = requests.get('https://{0}/api/?type=op&cmd=<show><running><resource-monitor><ingress-backlogs><%2Fingress-backlogs><%2Fresource-monitor><%2Frunning><%2Fshow>&key={1}'.format(IP, key), verify=False)
			data2 = ingresslog.text
			c2sstart = data2.find("<c2s>")
			appstart = data2.find("application")
			sessidstart = data2.find("SESS-ID")
			while(sessidstart != -1):
				c2sstart = data2.find(">", c2sstart) + 1 ## Goes to end of <c2s>
				zstart = data2.find("source-zone", c2sstart)
				zstart = data2.find(">", zstart) + 1 ## Goes to end of <source-zone>
				appstart = data2.find(">", appstart) + 1 ## Goes to the end of <application>
				sessidstart = data2.find(">", sessidstart) + 1 ## Goes to the end of <SESS-ID>
				c2send = data2.find("</c2s>", c2sstart)
				zend = data2.find("</source-zone>", zstart)
				append = data2.find("</application>", appstart)
				sessidend = data2.find("</SESS-ID>", sessidstart)
				zid = data2[zstart:zend]
				appid = data2[appstart:append]
				sessid = int(data2[sessidstart:sessidend])
				print (sessid)
				## "Any" AppID and "Any" zone
				if(default and default2):
					discard = requests.get('https://{0}/api/?type=op&cmd=<request><session-discard><reason>"Packet Buffer Overflow Testing"<%2Freason><timeout>60<%2Ftimeout><id>{2}<%2Fid><%2Fsession-discard><%2Frequest>&key={1}'.format(IP,key,sessid), verify = False)
					distxt = discard.text
					print(distxt)
				## Specific AppID and "Any" zone	
				elif(not(default) and default2):
					i = 0
					while(i < len(list1)):
						if appid == list1[i]:
							discard = requests.get('https://{0}/api/?type=op&cmd=<request><session-discard><reason>"Packet Buffer Overflow Testing"<%2Freason><timeout>60<%2Ftimeout><id>{2}<%2Fid><%2Fsession-discard><%2Frequest>&key={1}'.format(IP,key,sessid), verify = False)
							distxt = discard.text
							print(distxt)
						i = i+1
				## "Any" AppID and specific zone		
				elif(default and not(default2)):
					j = 0
					while(j < len(list2)):
						if zid == list2[j]:
							discard = requests.get('https://{0}/api/?type=op&cmd=<request><session-discard><reason>"Packet Buffer Overflow Testing"<%2Freason><timeout>60<%2Ftimeout><id>{2}<%2Fid><%2Fsession-discard><%2Frequest>&key={1}'.format(IP,key,sessid), verify = False)
							distxt = discard.text
							print(distxt)
						j = j+1
				## Specific AppID and specific zones		
				elif(not(default) and not(default2)):
					k = 0
					l = 0
					while(k < len(list1)):
						while(l < len(list2)):
							if((appid == list1[k]) and (zid == list2[l])):
								discard = requests.get('https://{0}/api/?type=op&cmd=<request><session-discard><reason>"Packet Buffer Overflow Testing"<%2Freason><timeout>60<%2Ftimeout><id>{2}<%2Fid><%2Fsession-discard><%2Frequest>&key={1}'.format(IP,key,sessid), verify = False)
								distxt = discard.text
								print(distxt)
							l = l+1
						k = k+1
						
				index = sessidend + 10 ## Goes to the end of current </SESS-ID> to continue looking for further <SESS-ID>
				index2 = append + 14 ## Goes to the end of current </application>
				index3 = c2send + 6 ## Goes to the end of current </c2s>
				sessidstart = data2.find("SESS-ID", index)
				appstart = data2.find("application", index2)
				c2sstart = data2.find("<c2s>", index3)		
		time.sleep(interval)
	
	## End while loop
	if(log == "YES" or log == "Yes" or log == "yes"):
		i = 0
		with open("packet_buffer_usage.txt", "a") as file, open("packet_buffer_usage_temp.txt", "w") as tempfile:
			while(i < len(vArray)):
				file.write(str(vArray[i]) + "	" + str(tArray[i]) + "\n")
				tempfile.write(str(vArray[i]) + "\n")
				i += 1	
			file.write("End Time: " + time.strftime("%d/%m/%Y ") + time.strftime("%I:%M:%S") + "\n")

		print("Generating Log and Graph Files...")
		graph_data.create_graph()
	
if __name__ == "__main__":
	main(sys.argv[1:])		
