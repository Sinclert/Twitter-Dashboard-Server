# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from handlers.tokens import set_token_secret

from twitter.auth import get_oauth_handler


app = Flask('Twitter-Dashboards')
CORS(app)




@app.route('/login', methods=['POST'])
def get_auth_url():

	# Obtaining authentication URL
	oauth_handler = get_oauth_handler()
	oauth_url = oauth_handler.get_authorization_url()

	return jsonify({
		'auth_url': oauth_url
	})




@app.route('/token', methods=['POST'])
def get_auth_token():

	# Get request arguments
	oauth_token = request.json['oauth_token']
	oauth_verifier = request.json['oauth_verifier']

	oauth_handler = get_oauth_handler()
	oauth_handler.request_token = {
		'oauth_token': oauth_token,
	    'oauth_token_secret': oauth_verifier
	}

	# Obtaining authentication account and token
	token, token_secret = oauth_handler.get_access_token(oauth_verifier)
	account = oauth_handler.get_username()

	# Saving the token secret for future usage
	set_token_secret(account, token, token_secret)

	return jsonify({
		'twitter_account': account,
		'twitter_token': token
	})




if __name__ == '__main__':

	app.run(
		host='127.0.0.1',
		port=5000,
		debug=True
	)
