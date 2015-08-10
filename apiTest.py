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
		# prepare body json for login key request
		logging.info("No session key in memcache, fetching a new one")

		uname = { 'user_name' : username }
		upass = { 'password' : password }
		auth_creds = []
		auth_creds.append(uname)
		auth_creds.append(upass)

		name_val = []
		lang = { "language" : "en_uk" }
		notify =  { "notifyonsave" : True }
		name_val.append(lang)
		name_val.append(notify)

		user_auth = {}
		user_auth["name_value_list"] = name_val
		user_auth["application_name"] = "DaveTest"
		user_auth["user_auth"] = auth_creds

		print "JSON " + json.dumps(user_auth)
		post_args = {'method': 'login', 'input_type' : 'JSON', 'response_type' : 'JSON', 'rest_data' : json.dumps(user_auth) }

		response_data = requests.post(url, data=post_args)
		reponse_code = response_data.status_code
		if reponse_code != 200:
                	logging.error("session key request failed")
			response_data.raise_for_status()
			raise http_error

		string = response_data.text
		print "Response " + string

#		logging.info("adding new session key to memcache " + str(session_key) + " with ttl " + str(ttl) )
#               mc.set("sessionkey", session_key, int(ttl))
                return session_key



#Get Global config attributes

try:
	config = json.loads(open('./config.json').read())
	so_url = config["signon_url"]
	username = config["username"]
	password = config["password"]
	md5bin = hashlib.md5(password)
	md5pass = md5bin.hexdigest()
	mc = config["memcache_client"]
	logfile = config["logfile"]
	logging.basicConfig(filename=logfile,level=logging.DEBUG)
except:
	print "Config load failed. Script expects a JSON config file called config.json in local Directory"
	raise
	

session_key = login_api(username,md5pass,mc,so_url)
