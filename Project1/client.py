# Please run the program in Linux

import socket
import sys
import select

class ChatClient:
    def __init__(self, username, server_host='127.0.0.1', server_port=20000):
        self.server_address = (server_host, server_port)
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setblocking(False)  # Non-blocking socket
        self.running = True

    def send_message(self, message):
        self.client_socket.sendto(message.encode('utf-8'), self.server_address)

    def start(self):
        # Send the join message
        self.send_message(f"join {self.username}")
        print("You have joined the chat. Type 'leave' to exit.")

        while self.running:
            # Use select to wait for input from either socket or stdin
            read_sockets, _, _ = select.select([self.client_socket, sys.stdin], [], [], 0.05)

            for source in read_sockets:
                if source == self.client_socket:  # Message from the server
                    try:
                        data, _ = self.client_socket.recvfrom(1024)
                        print(data.decode('utf-8'))
                    except BlockingIOError:
                        pass

                elif source == sys.stdin:  # Input from the keyboard
                    user_input = sys.stdin.readline().strip()
                    self.handle_user_input(user_input)

    def handle_user_input(self, user_input):
        if user_input == "leave":
            self.send_message("leave")
            print("You have left the chat.")
            self.running = False
            self.client_socket.close()
            sys.exit()
        elif user_input == "users":
            self.send_message("users")
        elif user_input.startswith("to "):
            self.send_message(user_input)
        else:
            print("Invalid command. Use 'users', 'to <recipient> msg <message>', or 'leave'.")

if __name__ == "__main__":
    username = input("What's your name? ")
    if not username:
        print("Username cannot be empty.")
        sys.exit(1)

    client = ChatClient(username)
    client.start()
