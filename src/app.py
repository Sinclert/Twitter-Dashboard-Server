# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify

app = Flask('Twitter-Dash')




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
