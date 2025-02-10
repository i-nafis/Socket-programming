# **Socket Programming Projects**
This repository contains two **socket programming** projects developed as part of my **Data Communication Course**. These projects demonstrate fundamental **network programming concepts** using **UDP and TCP protocols**.

## 📌 **Projects Overview**
1. **[Chat Application over UDP](Project1-ChatApp/README.md)**  
   - A simple **client-server** chat system where clients communicate via a centralized **UDP server**.
2. **[Download Accelerator over HTTP](Project2-DownloadAccelerator/README.md)**  
   - A **multi-threaded HTTP downloader** that accelerates file downloads by splitting the request into multiple **parallel threads**.

---

## **1️⃣ Chat Application over UDP**
### **🔹 Description**
This project implements a **UDP-based chat system** where multiple clients communicate through a central **chat server**. Messages are sent to the server, which then **forwards them** to the intended recipients.

### **🔹 Features**
- Clients can **join** the chat by sending a `"join <username>"` request.
- Clients can **list online users** with the `users` command.
- Messages can be sent:
  - **To a specific user** (`to <username> msg <message>`).
  - **To multiple users** (`to <username1> <username2> msg <message>`).
  - **To all users** (`to all msg <message>`).
- Clients can **leave** the chat with the `leave` command.

### **🔹 How to Run**
1. Start the **server**:
     ```bash
     python3 server.py
2. Start the **client**:
     ```bash
     python3 client.py
3. Enter a username and start chatting!

 ---
 ## 2️⃣ Download Accelerator over HTTP

### 🔹 Description
This project is a **multi-threaded HTTP downloader** that speeds up downloads by splitting the file into **parallel chunks** and retrieving them **concurrently** using **HTTP range requests**.

### 🔹 Features
- Uses **HTTP HEAD requests** to determine file size.
- Splits the file into **equal parts** and downloads each part **simultaneously**.
- Supports **1 to 16 parallel threads** for efficient downloading.

### **🔹 How to Run**
Run the downloader with:
```bash
python3 downloader.py <NumberOfThreads> <ObjectURI> <LocalFilename>
```
Example:
```bash
python3 downloader.py 4 http://www.textfiles.com/art/cowz.txt out.txt
```

---

## 📚 Course Information
These projects were developed as part of my **Data Communication Course**, where I explored **socket programming, network protocols, and multi-threaded applications**.




   
