from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)

# --- Game Logic ---
class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.properties = []

    def move(self, steps):
        self.position = (self.position + steps) % 40  # Assuming 40 spaces on the board

    def pay(self, amount):
        self.money -= amount

    def receive_money(self, amount):
        self.money += amount

    def is_bankrupt(self):
        return self.money < 0

players = []  # List to store players

board = [
    {"name": "GO", "type": "go"},
    {"name": "Mediterranean Avenue", "type": "property", "price": 60, "owner": None},
    {"name": "Baltic Avenue", "type": "property", "price": 60, "owner": None},
    # Add the rest of the spaces...
]

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')  # Serve the main game page

# --- SocketIO Events ---
@socketio.on('connect')
def handle_connect():
    print("Player connected")

@socketio.on('join_game')
def handle_join_game(data):
    player_name = data['name']
    player = Player(player_name)
    players.append(player)
    emit('game_update', {'message': f"{player_name} has joined the game!"}, broadcast=True)

@socketio.on('roll_dice')
def handle_roll_dice(data):
    player_name = data['name']
    player = next((p for p in players if p.name == player_name), None)
    if player:
        dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
        player.move(dice1 + dice2)
        emit('game_update', {'message': f"{player_name} rolled {dice1 + dice2} and landed on {board[player.position]['name']}."}, broadcast=True)

@socketio.on('buy_property')
def handle_buy_property(data):
    player_name = data['name']
    property_name = data['property_name']
    player = next((p for p in players if p.name == player_name), None)
    if player:
        property = next((p for p in board if p['name'] == property_name), None)
        if property and property.get('owner') is None:
            player.pay(property['price'])
            property['owner'] = player
            emit('game_update', {'message': f"{player_name} bought {property_name}!"}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print("Player disconnected")

if __name__ == '__main__':
    socketio.run(app, debug=True)
