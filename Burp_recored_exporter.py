import re
import base64

with open('history.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
  if '<request base64="true"><!' in line:
    encoded_request = re.sub(r'<request base64="true"><!\[CDATA\[|\]\]></request>', '', line).strip()
    decoded_request = base64.b64decode(encoded_request).decode('utf-8')
    location_match = re.search(r'^(?:GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH) (.+) HTTP/[12\.]*', decoded_request, re.IGNORECASE)
    if location_match:
      location = location_match.group(1).split('?')[0].replace('\r', '')
    host_match = re.search(r'Host: (.+)', decoded_request)
    if host_match:
      host = host_match.group(1).replace('\r', '')
    if location_match and host_match:
      print("save")
      filename = host + location.replace('/', '---')
      with open(filename, 'w') as output_file:
        output_file.write(decoded_request)
