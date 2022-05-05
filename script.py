#FINAL

#Combina LOG + SPLIT_LOG
#Lee la columna "ip" file.xlsx y aplica la el metodo servidor.comando()
#toda la lsta de ips y almacena las ips con su respectiva salida en fileRES.xlsx

get_ipython().run_line_magic('reset', '-f')

import pandas as pd
import numpy as np
import time
import paramiko

class conexion:
    def __init__(self,user,pwd,rpwd = None):
        self.usuario = user
        self.password = pwd
        if rpwd == None:
            rpwd = pwd
        self.rootpassword = rpwd
    def comando(self,ip,com,root = None):
        def esperabuffer(canal):
            while not canal.recv_ready():
                time.sleep(0.1)
            time.sleep(0.5)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:    
            client.connect(ip, username = self.usuario, password = self.password)
            chan = client.invoke_shell()
            if root=='root':
                esperabuffer(chan)
                chan.send('su - root\n')
                esperabuffer(chan)
                chan.send(self.rootpassword+'\n')
            esperabuffer(chan)
            chan.recv(9999)
            chan.send('\n')
            esperabuffer(chan)
            chan.send(com+'\n')
            esperabuffer(chan)
            output = chan.recv(99999) #OJO AQUI, LOS LOGS SUPERAN LOS 10000 BYTES
            output = output.decode('utf-8')
            output = output.split('\n')        
            output = "\n".join(output[2:len(output)-1])
            client.close()
        except:
            output = 'Sin conexion'   
        return(output)

datos = pd.read_excel('file.xlsx')
ips = datos['ip']
df = pd.DataFrame(columns=['ip','output'])    
  
comandogard = 'comando'
servidor = conexion('user','password','rootpassword')

for ip in ips:
    y=servidor.comando(ip,comandogard,'root')
    data = np.array([[ip,y]])
    row = pd.DataFrame(data,columns=['ip','output'])
    df = pd.concat([df,row], axis = 0)
    print(ip+" listo.")

df['res1'], df['res2'], df['res3'], df['res4'], df['res5'], df['res6']= df['output'].str.split('XXXXXXXXXXXXXXXXXX').str

df.to_excel('fileRES.xlsx')
