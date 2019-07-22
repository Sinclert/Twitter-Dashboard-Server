# Twitter dashboard server

This project contains the back end functionality of a web application that displays _near real-time_ data over a socket.
It can be used in combination with the [Twitter dashboard client][dashboard-client] project, to serve near real-time
Twitter data to a web interface. Check the [video demo][video-demo] for context.


## How does it work?

### Authentication
Given that this project was originally created to work with a [Twitter Streaming API][twitter-stream-api] data source,
log-in must be done trough the official Twitter page. This log-in process will generate two values: `oauth_token` 
and `oauth_verifier`. This last one is used to obtain a _token_secret_, which is stored here in the back-end.

### Handlers
Within the project there are certain entities called _handlers_. These entities manage several resources, by now:
- **Token secrets** (accessible by user account - user token).
- **Running streams**.

### Taggers
There are also entities called _taggers_, which are supposed to add tags / labels to the originally provided data.
By now, there is only one tagger, a **hierarchical ML model**, which is in charge of inferring the **sentiment** of each
piece of text, assigning a label to the resulting data structure.

If you want to learn more about how that ML model was trained, check my [SentimentAI][sentiment-ai-project] project.

### Data communication
The data communication between a supposed back-end and this front-end client was designed to be done in an **asynchronous manner**,
meaning each time a _data point_ (tweet) is retrieved by a data stream, it must be send over the open socket (allowing real-time visualization).

The technologies involved in making it possible are:
- The [Flask][flask-webpage] WSGI.
- The [Flask SocketIO adaptation][flask-socketio-webpage] package.
- The [Google geocoding API][geocoding-api] (transforms a region description, into a pair of geo-located points).

### Data structure
Each data point interchanged between back-end and any front-end have the following structure:
```json
{
    "coords":  [123, -75],
    "label":   "neutral",
    "source":  "android",
    "text":    "This is just an example",
}
```


## What is in the repository?
The Python modules has been organized in the following structure:

```yaml
/src:
    # Files
    app.py: Flask application entry point
    
    # Folders
    /handlers: contains server managed entities.
        secrets.py: manages token secrets.
        streams.py: manages Twitter data streams.
        ...
    /taggers: containes data taggers.
        /sentiment: sentiment inferrer.
        ...
    /twitter: contains the Twitter connecting functionality.
        ...
    /utils: contains utilities modules.
        ...
...
requirements.txt: project dependencies
```

## Usage

### Developers side
When deploying this back-end server, execute the following commands:

```sh
pip install -r requirements.txt

# If on a Linux machine, install gevent for extra socket performance
# sudo apt-get install gevent

python3 src/app.py
```


[dashboard-client]: https://github.com/Sinclert/Twitter-Dashboard-Client
[flask-webpage]: https://palletsprojects.com/p/flask/
[flask-socketio-webpage]: https://flask-socketio.readthedocs.io/en/latest/
[geocoding-api]: https://developers.google.com/maps/documentation/geocoding/intro
[sentiment-ai-project]: https://github.com/Sinclert/SentimentAI
[twitter-stream-api]: https://developer.twitter.com/en/docs/tweets/filter-realtime
[video-demo]: https://github.com/Sinclert/Twitter-Dashboard-Client/blob/master/demo/video-demo.mov
