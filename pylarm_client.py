#!/usr/bin/env python3
import socket

if __name__ == '__main__':
    host = "alarm.server.tld"   # Hostname or IP address
    port = 25276                # Port number for the server
    t = input("1 == Alarm\n2 == Stop alarm\n3 == Info\n")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        if t == "1":
            s.sendall(b'alarm_token123456')
        elif t == "2":
            s.sendall(b'stop_token123456')
        elif t == "3":
            s.sendall(b'info_token123456')
        else:
            print("Incorrect entry.")
            quit(1)
        data = s.recv(1024)
    print(data.decode('ascii'))
