import socket
import json

class MonopolyClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.game_state = {}

    def send_action(self, action):
        # Serialize the action into JSON and send it to the server
        action_json = json.dumps(action)
        self.client_socket.send(action_json.encode('utf-8'))

    def receive_game_state(self):
        # Receive the updated game state from the server
        game_state_json = self.client_socket.recv(1024).decode('utf-8')
        self.game_state = json.loads(game_state_json)
        print(f"Game state updated: {self.game_state}")

    def start(self):
        while True:
            # Simulating player action
            action = input("Enter your action (e.g., roll dice): ")
            self.send_action({"action": action, "player_id": 1})

            # Wait for server response
            self.receive_game_state()

if __name__ == "__main__":
    client = MonopolyClient()
    client.start()
