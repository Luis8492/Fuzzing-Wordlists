import requests
import urllib.parse
import re
import string

target = "http://.../?search="
check_letters = ["<","\"","'","&"]
payload = "xxxx"
num = 0
for letter in check_letters:
  payload = payload+str(num)+string.ascii_lowercase[num]+letter
  num += 1
  payload = payload+str(num)+string.ascii_lowercase[num]
  num += 1
payload += "xxxx"
print("Crafted payload:",payload)

response = requests.get(target+urllib.parse.quote(payload))
response_text = response.text

reflect_positions = []
for match in re.finditer(payload[:6], response_text):
  reflect_positions.append(match.start())
for position in reflect_positions:
  print("Reflected payload found:")
  print(response_text[position-20:position+100])
  reflected_payload = response_text[position:position+100]
  payload_end = reflected_payload.find(payload[-6:])
  reflected_payload = reflected_payload[:payload_end+8]
  
  available_letters = []
  escaped_letters = []
  for letter in check_letters:
    if reflected_payload.find(payload[payload.find(letter)-2:payload.find(letter)+3])!=-1:
      available_letters.append(letter)
    else:
      escaped_letters.append(letter)
  print("Available Letters: ", ' '.join(available_letters))
  print("Escaped Letters  : ",' '.join(escaped_letters))
  print()
