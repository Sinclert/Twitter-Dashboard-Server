# -*- coding: utf-8 -*-

import json
import os

from flask import Flask
from flask import jsonify
from flask import request

from flask_cors import CORS
from flask_socketio import SocketIO

from handlers.secrets import SecretsHandler
from handlers.streams import StreamsHandler

from twitter.auth import get_oauth_handler
from twitter.stream import TwitterStream


app = Flask('Twitter-Dashboards')
app.secret_key = os.urandom(32)

socket_app = SocketIO(app)
CORS(app)


secrets = SecretsHandler()
streams = StreamsHandler()




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
	secrets.set(account, token, token_secret)

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
	token_secret = secrets.get(account, token)

	# Saving the stream for future use
	stream = TwitterStream(token, token_secret, send_tweet)
	streams.set(account, stream)

	stream.start_stream(
		queries=['Trump'],
		langs=['en'],
		coords=[-122.75, 36.8, -121.75, 37.8]
	)

	return '', 200




def send_tweet(tweet: object):

	"""
	Callback that emits a tweet object to the client

	:param tweet: SimpleTweet object
	"""

	with app.app_context():
		socket_app.emit(
			event='tweet',
			data=json.dumps(tweet),
			namespace='/stream'
		)




if __name__ == '__main__':

	socket_app.run(
		app=app,
		host='127.0.0.1',
		port=5000,
		debug=True
	)
