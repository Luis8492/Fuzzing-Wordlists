import requests
import re
#from bs4 import BeautifulSoup

target = "https://0a26001c038dd2a680526209001a0054.web-security-academy.net"

def get_connection():
  url = target +"/post?postId=1"
  response = requests.get(url)
  cookies = response.cookies
  csrf_token = grep_csrf_token(response.text)
  return cookies,csrf_token

def grep_csrf_token(response_text):
  matches = list(re.finditer(r'<input required type="hidden" name="csrf" value=".*?">', response_text))
  return response_text[matches[0].start()+49:matches[0].end()-2]

def post_comment(cookies,csrf_token):
  url = target + "/post/comment"
  data = {
    "csrf" : csrf_token,
    "postId" : "1",
    "comment" : "asdf1",
    "name" : "asdf2",
    "email" : "asdf3@a.a",
    "website" : "http://asdf4.a"
  }
  response = requests.post(url,data=data,cookies=cookies,verify=False)

cookies,csrf_token = get_connection()
post_comment(cookies,csrf_token)
