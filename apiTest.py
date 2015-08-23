# API test for SugarCRM API version 4.1
# DW 2015-08-10

import memcache
import json
import requests
import logging
import hashlib

def login_api(username,password,mclient,url):
        mc = memcache.Client([mclient])
        session_key = mc.get("sessionkey")

        if session_key:
            logging.info("Found session key in memcache")
            return session_key
        else:
            encpass = md5pass(password)
            logging.info("No session key in memcache, fetching a new one")
            rest_data = {'user_auth' : {'user_name' : username, 'password' : encpass}}
            logging.info("JSON data" + json.dumps(rest_data))
            post_args = {'method': 'login', 'input_type' : 'json', 
            'response_type' : 'json', 'rest_data' : json.dumps(rest_data) }
            
            response_data = requests.post(url, verify=False, data=post_args)
            reponse_code = response_data.status_code
            if reponse_code != 200:
                logging.error("session key request failed")
                response_data.raise_for_status()
                raise http_error
            string = response_data.text
            print "Response " + string
            
        return session_key



def md5pass(password):
    encoded = hashlib.md5(password.encode('utf-8'))
    mypass = encoded.hexdigest()
    return mypass


#Get Global config attributes

try:
	config = json.loads(open('./config.json').read())
	so_url = config["signon_url"]
	username = config["username"]
	password = config["password"]
	mc = config["memcache_client"]
	logfile = config["logfile"]
	logging.basicConfig(filename=logfile,level=logging.DEBUG)
except:
	print "Config load failed. Script expects a JSON config file called config.json in local Directory"
	raise
	

session_key = login_api(username,password,mc,so_url)
