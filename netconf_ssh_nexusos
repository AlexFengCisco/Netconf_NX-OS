'''

Test for CSR1000v netconf
sth LAZY, after sent XML message to netconf server, has to sleep for more than 0.1xxx seconds, or received buffer will be reordered...
should be coded with recv_ready status and then send msg to peer!!!!!! as following example

stdout_data = []
stderr_data = []

while session.recv_ready():
stdout_data.append(session.recv(nbytes))
stdout_data = "".join(stdout_data)

while session.recv_stderr_ready():
stderr_data.append(session.recv_stderr(nbytes))
stderr_data = "".join(stderr_data)

print "exit status", exit_status
print "output"
print stdout_data
print "error"
print stderr_data

how to invoke dedicated subsystem is the key point
response content is array.array , but has to convert ascii to string ...
no netconf XML parse part

http://www.minvolai.com/blog/2009/09/how-to-ssh-in-python-using-paramiko/

Created on Jun 23, 2014

@author: AlexFeng
'''
import paramiko
import time

t=2  #wait response time

ssh=paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect('172.16.1.52',username='admin', password='admin')
cc=ssh.get_transport()
dd=cc.open_session()
dd.set_name('xmlagent')
dd.invoke_subsystem('xmlagent')
dd.in_buffer.empty()

time.sleep(t)


helloxml='''<?xml version="1.0"?>
 <nc:hello xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
   <nc:capabilities>
   <nc:capability>urn:ietf:params:xml:ns:netconf:base:1.0</nc:capability>
   </nc:capabilities>
 </nc:hello>]]>]]>'''

dd.send(helloxml)
time.sleep(t)
#response=dd.in_buffer._buffer

#rs5=''.join(map(chr,response))

shverxml='''<?xml version="1.0"?>
<nf:rpc xmlns:nf="urn:ietf:params:xml:ns:netconf:base:1.0"
   xmlns:nxos="http://www.cisco.com/nxos:1.0" message-id="110">
    <nxos:exec-command>
      <nxos:cmd>sh ver</nxos:cmd>
    </nxos:exec-command>
</nf:rpc>]]>]]>'''


dd.send(shverxml)
time.sleep(t)
response=dd.in_buffer._buffer

rs6=''.join(map(chr,response))
print rs6
time.sleep(t)
netconfclose='''<?xml version="1.0"?>
<nc:rpc message-id="101" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"
xmlns="http://www.cisco.com/nxos:1.0">
      <nc:close-session/>
</nc:rpc>]]>]]>'''

dd.send(netconfclose)

dd.in_buffer.empty()



dd.close()
cc.close()
ssh.close()
