
# **Download Accelerator over HTTP**
This project is a **multi-threaded HTTP downloader** that speeds up downloads by splitting the file into **parallel chunks** and retrieving them **concurrently** using **HTTP range requests**.

## 📌 Features
- Uses **HTTP HEAD requests** to determine file size.
- Splits the file into **equal parts** and downloads each part **simultaneously**.
- Supports **1 to 16 parallel threads** for efficient downloading.

## 🔹 **How It Works**
1. The downloader first sends an **HTTP HEAD request** to determine the file size.
2. It splits the file into **equal parts** based on the number of threads.
3. Each thread sends a **GET request with the `Range` header** to fetch a specific part.
4. The parts are written to a file **simultaneously** to reconstruct the complete file.

## 🔹 **How to Run**
Run the downloader with:
```bash
python3 downloader.py <NumberOfThreads> <ObjectURI> <LocalFilename>
