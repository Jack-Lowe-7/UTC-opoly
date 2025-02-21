import socket
import threading
import json

class MonopolyServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.clients = []
        self.game_state = {}  # Store game state like player info, board, etc.
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def handle_client(self, client_socket, player_id):
        while True:
            try:
                # Receive player action (JSON)
                action = client_socket.recv(1024).decode('utf-8')
                if not action:
                    break
                action = json.loads(action)  # Deserialize JSON data

                # Process action (e.g., move, buy property)
                self.process_action(action, player_id)

                # Send updated game state to all clients
                self.broadcast_game_state()

            except ConnectionResetError:
                break

        # Clean up client on disconnect
        client_socket.close()

    def process_action(self, action, player_id):
        # Update game state based on action (for simplicity, assuming we handle it)
        print(f"Player {player_id} performs action: {action}")

    def broadcast_game_state(self):
        # Serialize and send updated game state to all clients (as JSON)
        for client in self.clients:
            client.send(json.dumps(self.game_state).encode('utf-8'))

    def start(self):
        print("Server started...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection: {client_address}")
            
            # Add client to the list
            self.clients.append(client_socket)
            player_id = len(self.clients) - 1

            # Start a new thread for handling this client
            threading.Thread(target=self.handle_client, args=(client_socket, player_id)).start()


if __name__ == "__main__":
    server = MonopolyServer()
    server.start()
