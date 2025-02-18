import tkinter as tk 
import socket
from tkinter import messagebox, filedialog

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 4096

client_socket = None

def reset():
    global client_socket
    if client_socket:
        client_socket.close()
        client_socket = None
    file_label.config(text="No file received")
    print("[*] Reset complete. Socket closed and UI reset.")

def receive_file():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        file_name = filedialog.asksaveasfilename(defaultextension=".*")
        if file_name:
            with open(file_name, 'wb') as file:
                while True:
                    file_data = client_socket.recv(BUFFER_SIZE)
                    if not file_data:
                        break
                    file.write(file_data)
            file_label.config(text=f"File saved as: {file_name}")
            print("[*] File received and saved.")
            messagebox.showinfo("Success", "File received and saved successfully.")
        else:
            print("[!] No file name provided.")
    except Exception as e:
        print(f"[!] Error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        client_socket.close()
        client_socket = None

root = tk.Tk()
root.title("Receiver Side")
root.geometry("500x500+750+130")
root.iconbitmap("C:/Users/user/OneDrive/Desktop/assignment 1/images/reciever.ico")
root.config(bg="peachpuff")

home_label = tk.Label(root, text="RECEIVE FILES", font=("times new roman", 30), bg="peachpuff")
home_label.place(x=250, y=40, anchor="center")

reset_btn = tk.Button(root, text="RESET", font=("times new roman", 18), bg="peachpuff3", width=9, command=reset)
reset_btn.place(x=20, y=100, anchor="w")

receive_btn = tk.Button(root, text="RECEIVE FILE", font=("times new roman", 18), bg="peachpuff3", width=13, command=receive_file)
receive_btn.place(x=250, y=100, anchor="center")

exit_btn = tk.Button(root, text="EXIT", font=("times new roman", 18), bg="peachpuff3", width=9, command=root.destroy)
exit_btn.place(x=480, y=100, anchor="e")

file_label = tk.Label(root, text="No file received", font=("times new roman", 20), bg="peachpuff", wraplength=390)
file_label.place(x=250, y=300, anchor="center")

cc_label = tk.Label(root, text="© Divyanshu 2025", font=("times new roman", 8), bg="peachpuff")
cc_label.place(x=490, y=490, anchor="e")

root.mainloop()
