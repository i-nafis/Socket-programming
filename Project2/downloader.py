import sys
import socket
import threading
from urllib.parse import urlparse
import time

write_lock = threading.Lock()
def parse_content_length(headers):
    ## Extracting Content-Length from HTTP headers
    for line in headers.split('\r\n'):
        if line.startswith('Content-Length: '):
            return int(line.split(': ')[1])
    return None

def getting_hostname(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        print(f"The IP address of {hostname} is {ip}")
        return ip
    except socket.gaierror as e:
        print(f"Failed to resolve hostname: {e}")
        sys.exit(1)


def head_request(ip, host, path):
    """Send a HEAD request to the server to retrieve the file size before downloading."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)  # Setting a timeout
        try:
            s.connect((ip, 80))
            header_request = f"HEAD {path} HTTP/1.0\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            s.send(header_request.encode())

            print("Connected to the server to send HEAD request...")
            response = b""
            while True:
                data = s.recv(1024)
                if not data:
                    break
                response += data

            # Content-Length from the headers
            return parse_content_length(response.decode())
        except socket.timeout:
            print("Connection timed out while sending HEAD request.")
            sys.exit(1)
        except Exception as e:
            print(f"Error during HEAD request: {e}")
            sys.exit(1)


class DownloadWorker(threading.Thread):
    """thread class responsible for downloading a specific byte range """

    def __init__(self, ip, host, path, start_byte, end_byte, filename, thread_id):
        threading.Thread.__init__(self)
        self.ip = ip
        self.host = host
        self.path = path
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.filename = filename
        self.thread_id = thread_id
        self.message = f"Thread number {self.thread_id + 1}, IP {self.ip} Port 80: Downloading bytes {self.start_byte} to {self.end_byte}"

    def run(self):
        """Download assigned byte range and write it to the file"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)  # setting a timeout
                s.connect((self.ip, 80))

                request = (
                    f"GET {self.path} HTTP/1.0\r\n"
                    f"Host: {self.host}\r\n"
                    f"Range: bytes={self.start_byte}-{self.end_byte}\r\n"
                    "Connection: close\r\n\r\n"
                )
                s.send(request.encode())

                # First, read and discard the HTTP headers to reach the body
                response = b""
                while b"\r\n\r\n" not in response:
                    chunk = s.recv(1024)
                    if not chunk:
                        break
                    response += chunk

                headers, data = response.split(b"\r\n\r\n", 1)

                # Write the first part of the data we received
                with write_lock:
                    with open(self.filename, "r+b") as f:
                        f.seek(self.start_byte)
                        f.write(data)

                # Write the rest of the data chunks directly in place
                bytes_written = len(data)
                while True:
                    chunk = s.recv(8192)
                    if not chunk:
                        break
                    with write_lock:
                        with open(self.filename, "r+b") as f:
                            f.seek(self.start_byte + bytes_written)
                            f.write(chunk)
                            bytes_written += len(chunk)

        except socket.timeout:
            print(f"Thread number {self.thread_id + 1}: Connection timed out.")
        except Exception as e:
            print(f"Thread number {self.thread_id + 1}: Error in download: {str(e)}")


def main():
    # Parse the number of threads
    try:
        num_threads = int(sys.argv[1])
        if not 1 <= num_threads <= 16:
            print("Number of threads must be between 1 and 16")
            return
    except ValueError:
        print("Number of threads must be a valid integer between 1 and 16")
        return

    url = sys.argv[2]
    output_file = sys.argv[3]

    # Parse the given URL
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else "/"

    # hostname to an IP address
    ip = getting_hostname(host)

    # find the file size
    file_size = head_request(ip, host, path)
    if not file_size:
        print("Failed to get the file size from the server.")
        return

    print(f"FileSize: {file_size}")

    # Create a local file placeholder with the correct size.
    with open(output_file, "wb") as f:
        f.write(b'\0' * file_size)

    # Determine byte ranges for each thread
    chunk_size = file_size // num_threads
    threads = []
    start_time = time.time()

    # Create and start the worker threads
    for i in range(num_threads):
        start_byte = i * chunk_size
        end_byte = (i + 1) * chunk_size - 1 if i < num_threads - 1 else file_size - 1

        worker = DownloadWorker(ip, host, path, start_byte, end_byte, output_file, i)
        threads.append(worker)
        worker.start()
        print(worker.message)

    # Waiting for all threads to downloads
    for thread in threads:
        thread.join()

    end_time = time.time()
    print("Main thread terminating...")
    print(f"Total time to download the object: {end_time - start_time:.2f} secs")


if __name__ == "__main__":
    main()