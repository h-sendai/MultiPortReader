#!/usr/bin/python

import os
import sys
import time # for sleep
import socket

# from Python Howto: socket programming

class MySocket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    def __init__(self, sock=None):
         if sock is None:
             self.sock = socket.socket(
                 socket.AF_INET, socket.SOCK_STREAM)
         else:
             self.sock = sock

    def connect(self, host, port):
         self.sock.connect((host, port))

    def send(self, msg):
         totalsent = 0
         msglen = len(msg)
         while totalsent < msglen:
             sent = self.sock.send(msg[totalsent:])
             if sent == 0:
                 raise RuntimeError("socket connection broken")
             totalsent = totalsent + sent

    def recv_all(self, msglen):
         msg = ''
         while len(msg) < msglen:
             chunk = self.sock.recv(msglen-len(msg))
             if chunk == '':
                 raise RuntimeError("socket connection broken")
             msg = msg + chunk
         return msg

def main():
    s = MySocket()
    s.connect('127.0.0.1', 2222)

if __name__ == '__main__':
    main()
