import os
import shodan
import csv

SHODAN_API_KEY = "XGPN8vDnyZ0YYNL1Lp6vnHNPFpAmDd3e"
api = shodan.Shodan(SHODAN_API_KEY)

def start(ip, keyword):

	clear_dump='rm -r nmap_results.csv'
	clear_dump1='rm -r nmap_results.xml'
	clear_dump2='clear'
	clear_dump3='rm -r output.txt'

	os.system(clear_dump)
	os.system(clear_dump1)
	os.system(clear_dump2)
	os.system(clear_dump3)

	welcome_sign="""
	╦ ╦┌─┐┬  ┌─┐┌─┐┌┬┐┌─┐  ┌┬┐┌─┐
	║║║├┤ │  │  │ ││││├┤    │ │ │
	╚╩╝└─┘┴─┘└─┘└─┘┴ ┴└─┘   ┴ └─┘ """
	print(welcome_sign)

	banner = """
	  __  __                    _
	 |  \/  |  ___   _ __    __| |  __ _  _   _
	 | |\/| | / _ \ | '_ \  / _` | / _` || | | |
	 | |  | || (_) || | | || (_| || (_| || |_| | _
	 |_|  |_| \___/ |_| |_| \__,_| \__,_| \__, |( )
	                                      |___/ |/
	 __   __                    _____       _                   _  _          ____                            _  _               _     ___
	 \ \ / /___   _   _  _ __  |  ___|_ __ (_)  ___  _ __    __| || | _   _  / ___|   ___   ___  _   _  _ __ (_)| |_  _   _     / \   |_ _|
	  \ V // _ \ | | | || '__| | |_  | '__|| | / _ \| '_ \  / _` || || | | | \___ \  / _ \ / __|| | | || '__|| || __|| | | |   / _ \   | |
	   | || (_) || |_| || |    |  _| | |   | ||  __/| | | || (_| || || |_| |  ___) ||  __/| (__ | |_| || |   | || |_ | |_| |  / ___ \  | |
	   |_| \___/  \__,_||_|    |_|   |_|   |_| \___||_| |_| \__,_||_| \__, | |____/  \___| \___| \__,_||_|   |_| \__| \__, | /_/   \_\|___|
	                                                                  |___/                                           |___/

	Dont worry, I dont bite ;)
	.................................................................................................................................................
	"""
	print(banner)
	#Check if the hosts is alive or not
	#ip=str(input("Enter target IP in quotes: "))
	check_live_host='ping -c 1 '+ip
	ping_output = os.system(check_live_host)

	#Run an NMAP scan after checking host life
	print("\n\nRunning NMAP to identify services, versions and ports....\n\n")
	run_nmap = 'nmap -A -p 80 -T4 -oX nmap_results.xml '+ip+' >> output.txt'
	os.system(run_nmap)
	os.system('python3 nmap_xml_parser.py -f nmap_results.xml -csv nmap_results.csv')
	nmap_source=open('nmap_results.csv','r')
	nmap_output=csv.reader(nmap_source, delimiter=',')

	for row in nmap_output:
		#Run a dirb scan on the respective port if website is running
		if 'http' in row:
			print("\n\nHTTP detected, running dirb to enumerate directories....\n\n")
			print(row[4])
			run_dirb= 'dirb http://'+ip+':'+row[4]+' >> output.txt'
			dirb_output=os.system(run_dirb)
			#Run Nikto web scanner on the target IP to find vulns
			print("\n\nRunning NIKTO to try and identify vulnerabilities on the website....\n\n")
			run_nikto = 'nikto -url http://'+ip+' >> output.txt'
			nikto_output=os.system(run_nikto)

		#If the host has ftp service running, run a brute force attack
		if 'ftp' in row:
			print("\n\nFTP detected, running hydra to try and dictionary attack username and password....\n\n")
			run_hydra_ftp='hydra -l admin -P rockyou.txt ftp://'+ip+' >> output.txt'
			hydra_ftp_output=system.os(run_hydra_ftp)

		#If the host has ssh service running, run a brute force attack
		if 'ssh' in row:
			print("\n\nSSH detected,running hydra to bruteforce with admin....\n\n")
			run_hydra_ssh='hydra -l admin -P rocckyou.txt ssh://'+ip+' >> output.txt'

		#If the host has Ubuntu running, run a service enumeration
		if 'Ubuntu' or 'Linux' or 'Unix' in row:
			print("\n\nLinux detected, running Enum4Linux now....\n\n")
			run_enum4linux='enum4linux -a '+ip+' >> output.txt'
			os.system(run_enum4linux)

	#run spookcheck to see if sites can be spoofed
	print("Running spoof check")
	spoofcheck='python spoofcheck/spoofcheck.py '+ip+' >> output.txt'
	os.system(spoofcheck)

	print("Checking for open cloud buckets")
	cloud_enum='python3 cloud_enum/cloud_enum.py -k '+keyword+' >> output.txt'
	os.system(cloud_enum)

	#Take NMAP output and search all discovered services for vulns
	print("\n\nSearching for possible exploits....\n\n")
	run_searchsploit= 'searchsploit --nmap nmap_results.xml >> output.txt'
	print("\n\nUsable exploits are....\n\n")
	searchsploit_output=os.system(run_searchsploit)

	#Take the targeted IP and search it on shodan for available services and information gathering
	print("\n\nSearching for digital footprint....\n\n")
	shodan_output = api.host(ip)
	logshodan= str(shodan_output)+' >> output.txt'
	os.system(logshodan)
	print("\n\nNumber of matches from shoadan on target is "+str(shodan_output))

	#End of code
	print("\n\n\nMonday has finished")

def selfcheck():
	clear_dump='clear'
	clear_dump1='rm -r output.txt'
	os.system(clear_dump)
	os.system(clear_dump1)

	print('Running flightsim now')
	build_flightsim='go build flightism'
	flightsim_run='flightsim/./flightsim run >> output.txt'
	os.system(flightsim_run)

	print('Running Linux Exploit Suggester ')
	linux_exploit_suggester='perl ./Linux_Exploit_Suggester.pl >>output.txt'
	os.system(linux_exploit_suggester)

	print('Running checksec ')
	setup_checksec='chmod +x checksec.sh'
	checksec='./checksec.sh --proc-all >> output.txt'
	os.system(setup_checksec)
	os.system(checksec)

	print('Running Lynis')
	lynis='cd lynis; ./lynis audit system >> output.txt'
	move_back='cd ..'
	os.system(lynis)
	os.system(move_back)

	print('Running Otseca')
	setup_otseca='cd otseca; ./setup.sh install'
	otseca='otseca --ignore-failed >> output.txt'
	os.system(setup_otseca)
	os.system(otseca)
	os.system(move_back)
