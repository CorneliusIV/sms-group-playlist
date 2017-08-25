import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import messaging_response


app = Flask(__name__)


@app.route('/')
def song_request():
    return "Hello World!"
