# **Chat Application over UDP**
This is a **client-server chat application** built using **UDP sockets**. The server manages messages between clients, while clients can send and receive messages via the server.

## 📌 Features
- Clients can **join** the chat by sending a `"join <username>"` request.
- Clients can **list online users** with the `users` command.
- Clients can send messages:
  - **To a specific user** (`to <username> msg <message>`).
  - **To multiple users** (`to <username1> <username2> msg <message>`).
  - **To all users** (`to all msg <message>`).
- Clients can **leave** the chat with the `leave` command.

## 🔹 **How It Works**
1. **The server** listens on **port 20000** for incoming messages.
2. Clients **register** by sending a `"join <username>"` message.
3. The server **tracks online users** and **forwards messages** accordingly.

## 🔹 **How to Run**
First, start the **server**:
```bash
python3 server.py
```
Then, start the **client**:
```bash
python3 client.py
```
Your ready to text you're friends!
