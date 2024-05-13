#
#for burp_history in burp_histories_with_params:
#  send_requests
#  record
#  if reflected:
#    check Reflected_XSS
#
#for burp_history:
#  crawl_and_find_reflection

import re

filename = "0a26001c038dd2a680526209001a0054.web-security-academy.net---post---comment"
f = open(filename,"r")
burp_entry = f.read()
f.close()
#print(burp_entry)

method = burp_entry[:burp_entry.find(" ")+1]
host = burp_entry[burp_entry.find("Host: ")+6:burp_entry.find("\n",burp_entry.find("Host: "))]
referer = burp_entry[burp_entry.find("Referer: ")+9:burp_entry.find("\n",burp_entry.find("Referer: "))]
location_and_param = burp_entry[burp_entry.find(" ")+1:burp_entry.find(" ",burp_entry.find(" ")+1)]
if location_and_param.find("?")!=-1:
  location = location_and_param[:location_and_param.find("?")]
  params = location_and_param[len(location)+1:].split("&")
else:
  location = location_and_param
  params = []
if burp_entry.find("\n\n")!=-1:
  data=burp_entry[burp_entry.find("\n\n")+2:].split("&")
else:
  data=None

if method=="GET":
  print(method,referer[:referer.find("://")+3]+host+location+"?"+"&".join(params))
else:
  print(method,referer[:referer.find("://")+3]+host+location)
  print("&".join(data))
