#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
from socket import * 
import time
import TurCrypt

class Messenger:
	def __init__(self):
		pass

	def send(host, port, data):
		# host is destination computer IP address
		# data format is string
		addr = (host, port)
		UDPSock = socket(AF_INET, SOCK_DGRAM)
		UDPSock.sendto(data, addr)
		UDPSock.close()
		os._exit(0)

	def receive(port):
		host = ""
		buf = 1024
		addr = (host, port)
		UDPSock = socket(AF_INET, SOCK_DGRAM)
		UDPSock.bind(addr)
		(data, addr) = UDPSock.recvfrom(buf)
		UDPSock.close()
		return data

	def source(pwd, ips_ports):
		x = TurCrypt.TurCrypter()
		y = Messenger()
		while True:
			msg = raw_input("> ")
			enc_msg = x.encrypt(msg, pwd)
			for [ip, port] in ip_ports:
				y.send(ip, port, enc_msg)
	def target(pwd, port):
		x = TurCrypt.TurCrypter()
		y = Messenger()
		while True:
			(enc_msg, findata) = eval(y.receive(port))
			msg = x.decrypt(findata, pwd, enc_msg, "empty")