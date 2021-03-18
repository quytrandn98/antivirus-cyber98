import socket
import os
import signal
import time
import threading
import sys
import subprocess
from queue import Queue
from datetime import datetime

# Start Threader3000 with clear terminal
subprocess.call('clear', shell=True)

# Main Function
def main_p():
   socket.setdefaulttimeout(0.30)
   print_lock = threading.Lock()
   discovered_ports = []
   t1 = datetime.now()
   myip = socket.gethostbyname(socket.gethostname())

   def portscan(port):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      try:
         conx = s.connect((myip, port))
         with print_lock:
            print("Port {} is open".format(port))
            discovered_ports.append(str(port))
         conx.close()
      except (ConnectionRefusedError, AttributeError, OSError):
          pass

   def threader():
      while True:
         worker = q.get()
         portscan(worker)
         q.task_done()
      
   q = Queue()
     
    #startTime = time.time()
     
   for x in range(200):
      t = threading.Thread(target = threader)
      t.daemon = True
      t.start()

   for worker in range(1, 65536):
      q.put(worker)

   q.join()

   t2 = datetime.now()
   total = t2 - t1
   print("Port scan completed in "+str(total))
   print("-" * 60)
   print("Threader3000 recommends the following Nmap scan:")
   print("*" * 60)
   print("nmap -p{ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=myip))
   print("*" * 60)
   outfile = "nmap -p{ports} -sV -sC -Pn -T4 -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=myip)
   t3 = datetime.now()
   total1 = t3 - t1

#Nmap Integration (in progress)

   def automate():
      choice = '0'
      while choice =='0':
         print("Would you like to run Nmap or quit to terminal?")
         print("-" * 60)
         print("1 = Run suggested Nmap scan")
         print("2 = Run another Threader3000 scan")
         print("3 = Exit to terminal")
         print("-" * 60)
         choice = input("Option Selection: ")
         if choice == "1":
            try:
               print(outfile)
               os.mkdir(target)
               os.chdir(target)
               os.system(outfile)
               #The xsltproc is experimental and will convert XML to a HTML readable format; requires xsltproc on your machine to work
               #convert = "xsltproc "+target+".xml -o "+target+".html"
               #os.system(convert)
               t3 = datetime.now()
               total1 = t3 - t1
               print("-" * 60)
               print("Combined scan completed in "+str(total1))
               print("Press enter to quit...")
               input()
            except FileExistsError as e:
               print(e)
               exit()
         elif choice =="2":
            main()
         elif choice =="3":
            sys.exit()
         else:
            print("Please make a valid selection")
            automate()
   automate()

if __name__ == '__main__':
   try:
      main_p()
   except KeyboardInterrupt:
      print("\nGoodbye!")
      quit()