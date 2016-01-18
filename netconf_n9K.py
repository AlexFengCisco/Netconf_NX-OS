'''
Created on Jan 15, 2016

@author: AlexFeng
'''
import paramiko
import time
import xml.etree.cElementTree as ET

helloxml='''<?xml version="1.0"?>
<nc:hello xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <nc:capabilities>
  <nc:capability>urn:ietf:params:xml:ns:netconf:base:1.0</nc:capability>
  </nc:capabilities>
</nc:hello>]]>]]>'''



shverxml='''<?xml version="1.0"?>    
<nc:rpc message-id="1" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"      xmlns="http://www.cisco.com/nxos:1.0:sysmgrcli">      
 <nc:get>        
  <nc:filter type="subtree">          
    <show>              
      <version>              
      </version>          
    </show>        
  </nc:filter>      
 </nc:get> 
</nc:rpc>]]>]]>'''


CLI_xml='''<?xml version="1.0"?>
<nf:rpc xmlns:nf="urn:ietf:params:xml:ns:netconf:base:1.0"
   xmlns:nxos="http://www.cisco.com/nxos:1.0" message-id="110">
   <nxos:exec-command>
      <nxos:cmd>%s</nxos:cmd>
    </nxos:exec-command>
</nf:rpc>]]>]]>'''

netconfclose='''<?xml version="1.0"?> 
<nc:rpc message-id="101" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" 
xmlns="http://www.cisco.com/nxos:1.0"> 
      <nc:close-session/> 
</nc:rpc>]]>]]>'''

t=1  #wait response time  , lazy to code recv_ready ;-P

ssh=paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect('10.66.164.155',username='admin', password='123Cisco123')
Transport=ssh.get_transport()
session=Transport.open_session()
session.set_name('xmlagent')
session.invoke_subsystem('xmlagent')
# for IOS-XE , ssh subsystem name not xmlagent ,should be netconf
session.in_buffer.empty()
time.sleep(t)


session.send(helloxml)
time.sleep(t)

response=session.in_buffer._buffer
results=''.join(map(chr,response))
print results


session.in_buffer.empty()
session.send(shverxml)
time.sleep(t)
response=session.in_buffer._buffer
results=''.join(map(chr,response))
print '#-----------------response sh ver XML here------------------------------------------------------'
print results
print '#######Result XML with tail length : '+str(len(results))

#cut the netconf tail for parsing XML
rsxmlstr=results[:-6]
print rsxmlstr
print "####After cut the tail length :"+str(len(rsxmlstr))

print '#------------------Netconf XML version parsing here:---------------------------------------------'
tree=ET.fromstring(rsxmlstr)
for child in tree.iter():
    if child.tag=='{http://www.cisco.com/nxos:1.0:sysmgrcli}chassis_id' :
        print "Chasis id :"+child.text
    if child.tag=='{http://www.cisco.com/nxos:1.0:sysmgrcli}kick_file_name' :
        print 'System kick start image name :'+child.text


CLI='sh vlan'
session.in_buffer.empty()
session.send(CLI_xml%(CLI))
time.sleep(t)
response=session.in_buffer._buffer
results=''.join(map(chr,response))
print '#--------------response show vlan XML here--------------------------------------------------------'
print results
print '#######Result XML with tail length : '+str(len(results))

#cut the netconf tail for parsing XML
rsxmlstr=results[:-6]
print rsxmlstr
print "####After cut the tail length :"+str(len(rsxmlstr))
vlan_tree=ET.fromstring(rsxmlstr)
print '##--------------VLAN data parsing here:-----------------------------------------------------------'
for child in vlan_tree.iter():
    #print child.tag,child.attrib,child.text
    if child.tag=='{http://www.cisco.com/nxos:1.0:vlan_mgr_cli}vlanshowbr-vlanname':
        print 'VLAN name is :'+child.text



#close netconf Session close session XML and Close TCP transport and close SSH      
session.in_buffer.empty()
session.send(netconfclose)
session.close()
Transport.close()
ssh.close()
'''
THE END

'''
