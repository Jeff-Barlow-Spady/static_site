import os
import argparse
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import sys

# Define the FastAPI app
app = FastAPI()

# Mount the static files directory
static_dir = os.path.join(os.path.dirname(__file__), "public")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

class HotReloadHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_any_event(self, event):
        print("Change detected. Restarting server...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

def find_available_port(port):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                return port
        except OSError:
            port += 1

def main():
    parser = argparse.ArgumentParser(description="Start an ASGI server with hot-reloading.")
    parser.add_argument("--port", type=int, default=8888, help="Port number")
    parser.add_argument("--directory", type=str, default="public", help="Directory to serve")
    args = parser.parse_args()

    port = find_available_port(args.port)
    directory = args.directory

    # Set up the watchdog observer
    event_handler = HotReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)
    observer.start()

    try:
        # Start the uvicorn server with the correct import string
        uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True, reload_dirs=[directory])
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
