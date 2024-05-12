import requests
import urllib.parse
import re
import string

class reflection_point:
  def __init__(self,response_text,reflected_position):
    self.response_text = response_text
    self.reflected_position = reflected_position
    self.analyze_reflection()
  def analyze_reflection(self):
    self.extract_reflected_payload()
    self.set_nested_tag()
    self.set_is_in_tag()
    self.set_is_in_quote()
    self.check_letter_availability()
  def extract_reflected_payload(self):
    reflected_portion = self.response_text[self.reflected_position:]
    payload_end = reflected_portion.find(payload[-6:])+6
    self.reflected_payload = reflected_portion[:payload_end]
  def set_nested_tag(self):
    tag_start = self.response_text[:self.reflected_position].rfind("<")
    tag_end = self.reflected_position + len(self.reflected_payload) + self.response_text[self.reflected_position+len(self.reflected_payload):].find(">")
    self.nested_tag = self.response_text[tag_start:tag_end+1]
  def set_is_in_tag(self):
    if self.nested_tag[1:].find("<")==-1:
      self.is_in_tag = True
    else:
      self.is_in_tag = False
  def set_is_in_quote(self):
    self.is_in_quote = False
    self.quote_type = None
    if self.is_in_tag:
      matches = list(re.finditer(r'(?:"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')', self.nested_tag))
      for match in matches:
        if match.start() <= self.nested_tag.find(self.reflected_payload) <= match.end() - 1:
          self.is_in_quote = True
          self.quote_type = self.nested_tag[match.start()]
  def is_in_safe_tag(self):
    pass
  def check_letter_availability(self):
    self.available_letters = []
    self.escaped_letters = []
    for letter in letters_to_check:
      if self.reflected_payload.find(payload[payload.find(letter)-2:payload.find(letter)+3])!=-1:
        self.available_letters.append(letter)
      else:
        self.escaped_letters.append(letter)

def check_XSS_probability(rp):
  XSS_status = "To Be Assessed."
  if rp.is_in_tag:
    if rp.is_in_quote:
      can_escapte_quote = (rp.quote_type in rp.available_letters)
      if can_escape_quote:
        XSS_status = "XSS likely."
      else:
        XSS_status = "No XSS likely."
    else:
      XSS_status = "XSS likely."
  else:
    if "<" in rp.escaped_letters:
      XSS_status = "No XSS likely."
    else:
      XSS_status = "XSS likely."
  print(XSS_status)

def craft_payload_string(letters_to_check):
  payload = "xxxx"
  num = 0
  for letter in letters_to_check:
    payload = payload+str(num%10)+string.ascii_lowercase[num%26]
    num += 1
    payload = payload+str(num%10)+string.ascii_lowercase[num%26]+letter
    num += 1
  payload = payload+str(num%10)+string.ascii_lowercase[num%26]
  num += 1
  payload = payload+str(num%10)+string.ascii_lowercase[num%26]
  num += 1
  payload += "xxxx"
  print("Crafted payload:",payload)
  return payload

letters_to_check = ["<","\"","'","&","\\"] # global
payload = craft_payload_string(letters_to_check) # global

target = "https://0ad6000d037689a281e3200c008a0076.web-security-academy.net/?search="

# Initial Scan
response = requests.get(target+urllib.parse.quote(payload))
response_text = response.text
for match in re.finditer(payload[:6], response_text):
  position = match.start()
  rp = reflection_point(response_text, position)
  print("Reflected payload found:",rp.nested_tag)
  print("In Tag:",str(rp.is_in_tag))
  print("In quote:{} ({})".format(rp.is_in_quote,rp.quote_type))
  print("Available Letters : ", ' '.join(rp.available_letters),"  (Escaped Letters : ",' '.join(rp.escaped_letters),")")
  check_XSS_probability(rp)
  print()
  print()
