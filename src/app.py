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
from taggers.sentiment import SentimentTagger
from twitter.auth import get_oauth_handler
from twitter.stream import TwitterStream


app = Flask('Twitter-Dashboards')
app.secret_key = os.urandom(32)

socket_app = SocketIO(app)
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
	secrets.set(account, token, token_secret)

	return jsonify({
		'twitter_account': account,
		'twitter_token': token
	})




@app.route('/startStream', methods=['POST'])
def start_stream():

	# Get request arguments
	account = request.json['twitter_account']
	token = request.json['twitter_token']

	# Retrieving token secret previously saved
	token_secret = secrets.get(account, token)

	# Creates and starts the stream
	stream = TwitterStream(token, token_secret, send_tweet)
	streams.start_stream(account, stream)

	return '', 200




@app.route('/stopStream', methods=['POST'])
def stop_stream():

	# Get request arguments
	account = request.json['twitter_account']

	# Stops the stream
	streams.stop_stream(account)

	return '', 200




def send_tweet(tweet: dict):

	"""
	Callback that sends a tweet object to the client

	:param tweet: SimpleTweet object
	"""

	# Assigning a sentiment label
	tweet['label'] = tagger.predict(tweet['text'])

	with app.app_context():

		socket_app.send(
			data=json.dumps(tweet),
		    json=True,
			namespace='/stream'
		)




if __name__ == '__main__':

	secrets = SecretsHandler()
	streams = StreamsHandler()
	tagger = SentimentTagger()

	socket_app.run(
		app=app,
		host='127.0.0.1',
		port=5000,
		debug=True
	)
