import tkinter as tk
import socket
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO
from pynput.keyboard import Controller, Key

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)
keyboard = Controller()

# Tkinter GUI
class ServerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nvision Latex Keyboard")

        # Labels for UI
        self.status_label = tk.Label(root, text="Status: Not Connected", fg="red", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.server_info_label = tk.Label(root, text="Server Address: N/A", font=("Arial", 12))
        self.server_info_label.pack(pady=5)

        self.port_info_label = tk.Label(root, text="Port: 5000", font=("Arial", 12))
        self.port_info_label.pack(pady=5)

        # Start the Flask server in a separate thread
        self.start_server()

    def start_server(self):
        def run_server():
            # Get local IP address
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            self.server_info_label.config(text=f"Server Address: {ip_address}")

            try:
                # Update status when server starts
                self.status_label.config(text="Status: Connected", fg="green")
                socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
            except Exception as e:
                self.status_label.config(text=f"Error: {e}", fg="red")

        # Run the server in a separate thread to avoid blocking the Tkinter UI
        server_thread = Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()


# Flask route and SocketIO handler
@app.route("/")
def index():
    return render_template("keyboard_eng_new.html")

@socketio.on("keypress")
def handle_keypress(data):
    key = data["key"]
    try:
        if key == "space":
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        elif key == "enter":
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        elif key == "backspace":
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
        elif key.startswith("Key."):
            # Handle special keys
            special_key = getattr(Key, key.split(".")[1], None)
            if special_key:
                keyboard.press(special_key)
                keyboard.release(special_key)
        elif len(key) > 1:
            for char in key:
                keyboard.press(char)
                keyboard.release(char)
        else:
            # Handle regular keys
            keyboard.press(key)
            keyboard.release(key)
    except Exception as e:
        print(f"Error handling key {key}: {e}")

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    ui = ServerUI(root)
    root.mainloop()

