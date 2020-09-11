#!/usr/bin/env python3

import requests, csv, json, ssl, time

ssl._create_default_https_context = ssl._create_unverified_context

#threat_key = ""
#api_key = ""
#idr_url = "https://eu.api.insight.rapid7.com/idr/v1/customthreats/key/" + threat_key + "/indicators/replace?format=json"

#headers = {
#    'X-Api-Key': api_key,
#    'Content-Type': 'application/json',
#}

#### Above for insightidr upload

def lataustesti_all(url, url2, url3, url4):
    #url = "https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.txt"
    #url2 = "https://bazaar.abuse.ch/export/txt/md5/recent/"
    #url3 = "https://bazaar.abuse.ch/export/txt/sha256/recent/"
    #url4 = "https://urlhaus.abuse.ch/downloads/csv_recent/"
    #Urls above for future reference

    test_list = [] #For downloading
    json_list = {
	'ips':[''],
	'MD5hashes':[''],
	'SHA256hashes':[''],
	'urls':['']
	} #For storing the data

    try:
	i = requests.get(url) #for ips
        h = requests.get(url2) #for md5
	s = requests.get(url3) #for sha26
	u = requests.get(url4) #for urls

    except i.status_code and h.status_code and s.status_code and u.status_code as e:
	if e.code == 404:     #Test if the page is valid
	  print("This is not the page you are looking for\n")
	else:
	  print("Something")

    except i.status_code and h.status_code and s.status_code and u.status_code as e:
	  print("Something went wrong\n")

    else:
	print("Fetch successful\n\n\n")
	time.sleep(2)
	print("Starting the processing\n\n\n")
	time.sleep(1)
        ibody = i.text    #Store
	hbody = h.text	  #The
	sbody = s.text    #Data
	ubody = u.text    #Here

    ##############################
    ##########          ##########
    ##########   IPs    ##########
    ##########          ##########
    ##############################

    ilines = ibody.splitlines()
    ireader = csv.reader(ilines, delimiter=",")

    for row in ireader:
	test_list.append(row)

    del test_list[0:9]  #Remove the header for urlhaus
    test_list.pop()  #Remove the footer for urlhaus

    for value in test_list:
        json_list['ips'].append(value[0])
    test_list = [] #empty the list for next IoC


    ##############################
    ##########          ##########
    ##########   MD5    ##########
    ##########          ##########
    ##############################

    hlines = hbody.splitlines()
    hreader = csv.reader(hlines, delimiter=",")

    for row in hreader:
        test_list.append(row)

    del test_list[0:9]
    test_list.pop()

    for value in test_list:
        json_list['MD5hashes'].append(value[0])

    test_list = [] #empty the list

    ##############################
    ##########          ##########
    ##########  SHA256  ##########
    ##########          ##########
    ##############################

    slines = sbody.splitlines()
    sreader = csv.reader(slines, delimiter=",")

    for row in sreader:
	test_list.append(row)

    del test_list[0:9]
    test_list.pop()

    for value in test_list:
	json_list['SHA256hashes'].append(value[0])

    test_list = [] #empty the list

    ##############################
    ##########          ##########
    ##########   URLs   ##########
    ##########          ##########
    ##############################


    ulines = ubody.splitlines()
    ureader = csv.reader(ulines, delimiter=",")

    for row in ureader:
        test_list.append(row)

    del test_list[0:9]
    test_list.pop()

    for value in test_list:
	json_list['urls'].append(value[2])

    ##############################
    ##########          ##########
    ########## PRINTS   ##########
    ##########  FOR     ##########
    ########## TESTING  ##########
    ##########          ##########
    ##############################


    #print(test_list)
    #print(json_list)
    print(json.dumps(json_list['ips'], indent=4))

    #r = requests.post(idr_url, headers=headers, data=json.dumps(json_list))


lataustesti_all("https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.txt", "https://bazaar.abuse.ch/export/txt/md5/recent/", "https://bazaar.abuse.ch/export/txt/sha256/recent/", "https://urlhaus.abuse.ch/downloads/csv_recent/")
