# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

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

	# Obtaining authentication token
	token, token_secret = oauth_handler.get_access_token(oauth_verifier)
	return jsonify({
		'twitter_account': '',
		'twitter_token': token
	})




@app.route('/tweets')
def get_tweets():
	return jsonify([])


@app.route('/tweets/location')
def get_tweets_location():
	return jsonify([])


@app.route('/tweets/platform')
def get_tweets_platform():
	return jsonify([])


@app.route('/tweets/sentiment')
def get_tweets_sentiment():
	return jsonify([])




if __name__ == '__main__':



	app.run(
		host='127.0.0.1',
		port=5000,
		debug=True
	)
