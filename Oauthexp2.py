from io import SEEK_END
from urllib import response
import requests, json
import webbrowser
import time
from bs4 import BeautifulSoup
from lxml import html
import mechanize
import os
import http.cookiejar

from requests.api import get

authorize_url = "https://tcfhirsandbox.intersystems.com.au/oauth2/authorize"
token_url = "https://tcfhirsandbox.intersystems.com.au/oauth2/token"
state = 'asdasdasdasdasdasasd'
scope = 'patient%2F*.read%20launch%2Fpatient'#patient/*.read launch/patient'
callback_uri = "x-argonaut-app://HealthProviderLogin/"
test_api_url = "https://tcfhirsandbox.intersystems.com.au/fhir/dstu2/Patient?identifier=RN000000200"
client_id = '6A605kYem9GmG38Vo6TTzh8IFnjWHZWtRn46K1hoxQY'
client_secret = 'POrisHrcdMvUKmaR6Cea0b8jtx-z4ewVWrnaIXASO-H3tB3g5MgPV7Vqty7OP8aEbSGENWRMkeVuJJKZDdG7Pw'
username = 'superuser'
password = 'SYS'

OAuth_url = authorize_url + '?response_type=code&state=' + state + '&client_id=' + client_id + '&scope='+scope+'&redirect_uri=' + callback_uri
#webbrowser.open(OAuth_url)
#authorization_code = input(":")

#"""
#mcookiejar = mechanize.CookieJar()
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_redirect(True)

#cj = mechanize.LWPCookieJar()
#opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))
#mechanize.install_opener(opener)
#front_page = 
br.open(OAuth_url)
#fp = front_page.read()
#rsoup = BeautifulSoup (fp)
#print (front_page)
#print(rsoup)
br.select_form(nr=0)
br.form['Username'] = 'superuser'
br.form['Password'] = 'SYS'
#r = 
br.submit()
#print(r.read())
#resp = r.read()
#soup = BeautifulSoup(resp, 'html')
#print(soup)

br.select_form(nr=0)
ac = br.form.click(name = 'Accept')
print(f"Allow Access Response = {ac}")

auth_code = str(ac)
get_url = auth_code[13:-1]
authorization_code = auth_code[90:176]
referer_url = auth_code[13:176] + "&stage=login:1"
print(f"authorization code = {authorization_code}")#"""
print(f"get url = {get_url}")
print (f"referer url = {referer_url}")

lheader = {"referer" : referer_url,
            "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            }

last_resp = requests.get(get_url, headers = lheader)


"""

data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri}
access_token_response = requests.post(token_url, data=data, verify=True, allow_redirects=True, auth=(client_id, client_secret))

print(f"status code = {access_token_response.status_code}")
tokens = json.loads(access_token_response.text)
access_token = tokens['access_token']

print(f"Response = {access_token_response.text}")

"""

"""
#authorization_code = request.args.get('code')
#authorization_code = input("Code:")

#use this once you have authorization code

"""
"""
# GET DATA FROM THE WEBSITE USING THE TOKEN

api_call_headers = {'Authorization': 'Bearer ' + access_token}
api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=True)

print(api_call_response.status_code)
print (api_call_response.text)"""

"""
# USING MECHANIZE TO NAVIGATE THROUGH PAGES


"""

"""
# BEAUTIFUL SOUP
soup = BeautifulSoup(OAuth_AccessRequest.content, 'html.parser')
form = soup.form
fields = form.find
login_data = {form.input.attrs['Username'] : form.input['Password']}
print (login_data)
login_data = {'Username': 'superuser', 'Password': 'SYS'}
headers = {'Referer': OAuth_AccessRequest.url}
login_url = OAuth_AccessRequest.url
r = session.post(login_url, data=login_data, headers=headers)

"""

"""
# Constructing URL (won't work without session)

req_response = log_url.split("&")
get_response = requests.get(code_url)

print (get_response)
#########################

authorization_code = input(":")
print(authorization_code)

"""
"""
# SESSION TO MAINTAIN THE SESSION AND SAVE COOKIES

#s = requests.session()    # use session to handle cookies
#OAuth_AccessRequest = session.get(OAuth_url)
authorization_code = input(":")

"""
"""
# USING NERODIA TO AUTOMATE BROWSER

from nerodia.browser import Browser

browser = Browser(browser = 'chrome')
browser.window().maximize()

browser.goto(OAuth_url)
browser.text_field(data_set = '').set('superuser')
browser.text_field(data_set = '').set('SYS')
log_resposne = browser.button(name='Login').click()

print(log_resposne)

browser.button(name = 'Accept').click()

browser.quit()
"""
"""
# lxml and html (Not Working)
s = requests.session()
login_url = s.get(OAuth_url)

payload = {
    'Username' : username,
    'Password' : password
}

print(login_url)
#perform login

login_result = s.post(login_url, data=payload)

print(login_result)
"""