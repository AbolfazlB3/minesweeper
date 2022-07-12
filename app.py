import json
from flask import Flask, redirect, url_for, render_template, request, flash, jsonify, Response
import flask
import numpy as np
from functools import wraps

from game import Game


# w, h = 8, 6
# game = Game(w, h)


# state = game.get_state()

# state = json.loads(state)

# grid = np.reshape(np.array(state['grid'], dtype=np.int8), (h, w))

# print(grid)


# while True:
#     x, y = [int(_) for _ in input().split(" ")]

#     game.reveal(x, y)

#     state = game.get_state()

#     state = json.loads(state)
    
#     grid = np.reshape(np.array(state['grid'], dtype=np.int8), (h, w))

#     print(grid)


app = Flask(__name__)

game = None

def handle_cors():
    response = Response('')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response

@app.route('/start', methods=['OPTIONS'])
def start_options(): return handle_cors()

@app.route('/reveal', methods=['OPTIONS'])
def reveal_options(): return handle_cors()


@app.route('/start', methods=['POST'])
def start():
    global game
    print("start")
    
    try:
        content_type = request.headers.get('Content-Type')
        print(content_type)
        print(request.data)
        if (content_type == 'application/json'):
            json = request.json
            game = Game(json['w'], json['h'])
            print(json)
            response = jsonify(game.get_state())
            print(response)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            return 'Only json content type is allowed'
    except:
        return flask.Response('', status=500)

@app.route('/reveal', methods=['POST'])
def reveal():
    global game

    print("reveal")
    try:
        content_type = request.headers.get('Content-Type')
        print(content_type)
        print(request.data)
        
        if(game == None):
            return Response('First Initialize the game with /start', status=400)

        if (content_type == 'application/json'):
            json = request.json
            game.reveal(json['x'], json['y'])
            print(json)
            response = jsonify(game.get_state())
            print(response)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            return Response('Only json content type is allowed', status=400)
    except Exception as e:
        return Response('', status=400)

app.run()
