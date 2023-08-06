import ConfigParser
import os
from os.path import expanduser
from shutil import copyfile

home = expanduser("~")

if os.path.isdir(home + "/G2GChatFiles") == False:
  os.mkdir(home + '/G2GChatFiles')
  file_path = os.path.join(home, 'G2GChatFiles', 'config_file.conf')
  with open(file_path, 'w') as f:
        f.write('[Section1]\nserver_ip_address = 172.16.6.33\nport = 55555\n\n[LoginDetails]\nid = \npassword = \n')

path = os.path.join(home ,'G2GChatFiles')
config_parser = ConfigParser.RawConfigParser()
file_path = os.path.join(path, 'config_file.conf')

config_parser.read(file_path)

if config_parser.has_section('Section1'):
  server_ip_address = config_parser.get('Section1', 'server_ip_address')
  port  = config_parser.get('Section1', 'port')
else:
  print'Cannot find config file...'
  exit(0)

def IpValidation(server_ip_address):   #function for ip_validation
  ip_octets = server_ip_address.split('.')

  count = 0
  for i in range(len(ip_octets)):      # upto 4 octets
    if(int(ip_octets[i]) >=0 and int(ip_octets[i]) < 256): #range 0 - 255
      count += 1                       # after processing 1 octet
      continue      		
    else:
      return 0
  return count

def PortValidation(port):
  if int(port) >= 0 and int(port) < 65535:
    return 1
  else:
    return 0

def GetUserDetails():
    temp_list = []
    temp_list.append(config_parser.get('LoginDetails','id'))
    temp_list.append(config_parser.get('LoginDetails','password'))
    if len(temp_list[0]) is 0 and len(temp_list[1]) is 0:
      return []
    return temp_list

def SetUserDetails(id, password):
  config_parser.set('LoginDetails','id',id)
  config_parser.set('LoginDetails','password',password)
