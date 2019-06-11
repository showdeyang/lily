# -*- coding: utf-8 -*-
from flask import (Flask, render_template, request)
import chatbot

app = Flask("lily")

@app.route("/")
def hello():
    return render_template('chat2.html')#, name=name

@app.route('/', methods = ["POST"])
def post():
    query = request.data.decode()
    
    answer = chatbot.reply(query)
    return answer

app.run(host='0.0.0.0')