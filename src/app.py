# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from handlers.secrets import get_token_secret
from handlers.secrets import set_token_secret
from handlers.streams import set_twitter_stream

from twitter.auth import get_oauth_handler
from twitter.stream import TwitterStream


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




@app.route('/setStream', methods=['POST'])
def set_stream():

	# Get request arguments
	account = request.json['twitter_account']
	token = request.json['twitter_token']

	# Retrieving token secret previously saved
	token_secret = get_token_secret(account, token)

	# Saving the stream for future use
	stream = TwitterStream(token, token_secret)
	set_twitter_stream(account, stream)

	stream.start_stream(
		queries=['Trump'],
		langs=['en'],
		coords=[-122.75, 36.8, -121.75, 37.8]
	)

	return '', 200




if __name__ == '__main__':

	app.run(
		host='127.0.0.1',
		port=5000,
		debug=True
	)
