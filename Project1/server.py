# Please run the program in Linux

import socket
import threading


class ChatServer:
    def __init__(self, host='127.0.0.1', port=20000):
        self.server_address = (host, port)
        self.online_users = {}  # Maps usernames to their addresses
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(self.server_address)

    def start(self):
        print("Chat server is up and listening on port 20000")
        while True:
            data, addr = self.server_socket.recvfrom(1024)
            threading.Thread(target=self.handle_message, args=(data, addr)).start()

    def handle_message(self, data, addr):
        message = data.decode('utf-8').strip()

        if message.startswith("join "):
            username = message.split(" ")[1]
            self.online_users[username] = addr
            print(f"{username} joined the chat")

        elif message == "users":
            user_list = ", ".join(self.online_users.keys())
            self.server_socket.sendto(f"Online users: {user_list}".encode('utf-8'), addr)

        elif message.startswith("to "):
            self.handle_to_command(message, addr)

        elif message == "leave":
            username = self.get_username_by_addr(addr)
            if username:
                del self.online_users[username]
                print(f"{username} left the chat.")

    def handle_to_command(self, message, addr):
        parts = message.split(" msg ")
        if len(parts) != 2:
            self.server_socket.sendto("Invalid message format.".encode('utf-8'), addr)
            return

        recipients, msg_content = parts
        recipients = recipients[3:]  # Strip "to " prefix

        sender = self.get_username_by_addr(addr)
        if recipients == "all":
            self.broadcast_message(sender, msg_content, addr)
        else:
            recipient_list = recipients.split()
            for recipient in recipient_list:
                self.send_message_to_recipient(sender, recipient, msg_content, addr)

    def broadcast_message(self, sender, message, sender_addr):
        for username, addr in self.online_users.items():
            if addr != sender_addr:
                self.server_socket.sendto(f"{sender}: {message}".encode('utf-8'), addr)

    def send_message_to_recipient(self, sender, recipient, message, sender_addr):
        if recipient in self.online_users:
            recipient_addr = self.online_users[recipient]
            self.server_socket.sendto(f"{sender}: {message}".encode('utf-8'), recipient_addr)
        else:
            self.server_socket.sendto(f"Error: {recipient} is not online.".encode('utf-8'), sender_addr)

    def get_username_by_addr(self, addr):
        for username, user_addr in self.online_users.items():
            if user_addr == addr:
                return username
        return None


if __name__ == "__main__":
    server = ChatServer()
    server.start()
