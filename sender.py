import tkinter as tk
import threading
import socket
from tkinter import filedialog, messagebox

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 4096

server_socket = None

def reset():
    global server_socket, file_path
    try:
        if server_socket:
            server_socket.close()
            server_socket = None
        file_path = None
        file_label.config(text="No file selected")
        print("[*] Reset complete. Server stopped, file deselected, and UI reset.")
    except Exception as e:
        print(f"[!] Error during reset: {e}")

def select_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.config(text=file_path)
        threading.Thread(target=start_server, args=(file_path,)).start()

def start_server(file_path):
    global server_socket
    if server_socket is None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print(f"[*] Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        try:
            if server_socket.fileno() == -1:  
                print("[!] Server socket is closed. Re-initializing...")
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind((SERVER_HOST, SERVER_PORT))
                server_socket.listen(1)

            client_socket, client_address = server_socket.accept()
            print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
            threading.Thread(target=handle_client, args=(client_socket, file_path)).start()
        except OSError as e:
            print(f"[!] Socket error: {e}")
            messagebox.showerror("Socket Error", f"An error occurred with the socket: {e}")
            break  # Exit the loop if the socket is invalid
        except Exception as e:
            print(f"[!] Unexpected error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            break

def handle_client(client_socket, file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            client_socket.sendall(file_data)
            print("[*] File sent successfully.")
            messagebox.showinfo("Success", "File sent successfully.")
    except FileNotFoundError:
        print("[!] File not found.")
        client_socket.sendall(b'File not found')
    finally:
        client_socket.close()

root = tk.Tk()
root.title("Sender Side")
root.geometry("500x500+200+130")
root.iconbitmap("images/sender.ico")
root.config(bg="thistle1")

home_label = tk.Label(root, text="SEND FILES", font=("times new roman", 30), bg="thistle1")
home_label.place(x=250, y=40, anchor="center")

reset_btn = tk.Button(root, text="RESET", font=("times new roman", 18), bg="plum1", width=10, command=reset)
reset_btn.place(x=20, y=100, anchor="w")

send_btn = tk.Button(root, text="SELECT FILE", font=("times new roman", 18), bg="plum1", width=12, command=select_file)
send_btn.place(x=250, y=100, anchor="center")

exit_btn = tk.Button(root, text="EXIT", font=("times new roman", 18), bg="plum1", width=10, command=root.destroy)
exit_btn.place(x=480, y=100, anchor="e")

file_label = tk.Label(root, text="No file selected", font=("times new roman", 20), bg="thistle1", wraplength=390)
file_label.place(x=250, y=300, anchor="center")

cc_label = tk.Label(root, text="© Divyanshu 2025", font=("times new roman", 8), bg="thistle1")
cc_label.place(x=490, y=490, anchor="e")

root.mainloop()
