#!/usr/bin/python
'''
'''
import config_parser
import os
import re
import socket
import sys
import select
import time

from os.path import expanduser
from shutil import copyfile


class Client:

  def __init__(self, server_ip_address, \
                 port, user_socket_fd): #Removed user_name and password
    '''
    Initializes the fields of the user
    ARGS:
    self       : Object created for the class "client" i.e.,[client_obj]
    user_name  : Our user name in the config file.
    password   : Our password in the config file
    ip_address : IP Address of the Server taken from command line.
    port       : Port of the server taken from the command line.
    socket_fd  : Socket descriptor that is created.
    RETURNS:
      -        :  Returns nothing.
    '''
    #self.user_name = user_name
    #self.password = password
    self.server_ip_address = server_ip_address
    self.port = int(port)
    self.user_socket_fd = user_socket_fd
    self.file_count = 0
    home = expanduser("~")

    if not os.path.isdir(home + '/G2GChatFiles/ReceivedFiles'): 
      os.makedirs(home + '/G2GChatFiles/ReceivedFiles')

    if not os.path.isdir(home + '/G2GChatFiles/Conversations'):
      os.makedirs(home + '/G2GChatFiles/Conversations')

  def ConnectToServer(self):
    '''
    Establish connection to the server with specified IP and port.
    ARGS:
    self      : Object created for the class "client" i.e.,[client_obj]
    '''
    try:
      self.user_socket_fd.connect((self.server_ip_address, self.port))
      print "\n\t\t\t\t\t\tWelcome to G2Gchat\n\n"
    except socket.error:
      print 'Server Down...! Sorry for inconvinience!!'
      sys.exit()
    # connects to the server with the specified IP Address

  def Start(self):
    while True:
      print '\t\t\t\t\t\t\t1.Login\n\t\t\t\t\t\t\t2.Register\n\t\t\t\t\t\t\t3.Exit'
      result = raw_input()
      if result == '1':
        while True:
          client_instance.LoginToServer()
          if client_instance.ReceiveFromServer() == -1:
            exit(0)
          break
        # call Receive() to handle the responses from the server.
      elif result == '2':
        client_instance.RegisterToServer()
      elif result == '3':
        sys.exit()
      else:
        print "Enter Valid option..."

  def RegisterToServer(self):
    while True:
      mail_id = raw_input("Enter your email id:")
      if self.ValidateMailId(mail_id) == 1:
        print 'Invalid mailid...!'
      else:
        break
    self.user_socket_fd.send('otp ' + mail_id)
    status = self.user_socket_fd.recv(1024)
    if status == 'sent_otp':
      print "Please enter OTP sent to your mail..!!"
      while True:
        confirm = raw_input()
        self.user_socket_fd.send('verify_otp ' + confirm)
        authentication_status = self.user_socket_fd.recv(1024)
        if authentication_status == 'verified':
          while True:
            self.username = raw_input("Enter your desired username:\t")
            print'''
                   Make sure your password has following criteria:
                   1.min length is 6 and max length is 20
                   2.at least include a digit number,
                   3.at least a upcase and a lowcase letter
                   4.at least a special characters

                '''

            password = raw_input("Enter your desired password:")
            confirm_password = raw_input("Re-enter password:")
            if password == confirm_password:
              if self.ValidatePassword(password) == 1:
                #print'''
                #   Make sure your password has following criteria:
                #   1.min length is 6 and max length is 20
                #   2.at least include a digit number,
                #   3.at least a upcase and a lowcase letter
                #   4.at least a special characters
                #'''
                continue
              self.user_name = mail_id
              self.password = password
              request = 'register_with ' + mail_id + ' ' + self.username + ' ' + password
              self.user_socket_fd.send(request)
              self.ReceiveFromServer()
            print'Passwords didnot match. Please try again..!!'
        elif authentication_status == 'invalid_otp':
          print "Invalid OTP,Please Re-enter:"
    elif status == 'not_available':
      print 'User name/Mail_id not available...!'
    elif status == '407':
          print 'Mail not sent as mail_id doesnot exist...'


  def ValidateMailId(self, mail_id):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', mail_id)
    if match == None:
      return 1
    else:
      return 0

  def ValidatePassword(self, password):
    match = re.match('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])',password)
    if match == None:
      return 1
    else:
      return 0

  def LoginToServer(self):
    '''
    Register the fields[username & password] of user in servers DataBase
    ARGS:
    self      : Object created for the class "client" i.e.,[client_obj]
    RETURNS:
        -     :  Returns nothing.
    '''
    details = config_parser.GetUserDetails()
    if len(details) is 0:
      print 'Login Details not available in config file. Configfile will be present in HOME/G2GChatFiles'
      print 'Please enter manually'
      while True:
        self.user_name = raw_input('User ID:')
        if self.user_name == '':
          print'Enter valid username..!'
          continue
        break
      while True:
        self.password = raw_input('Password:')
        if self.password == '':
          print 'Enter valid Password..!'
          continue
        break
    else:
      self.user_name = details[0]
      self.password = details[1]

    login_fields = "login_with" + ' "' + self.user_name + '" "' + \
                       self.password + '"'
    print 'Sending Details'
    self.user_socket_fd.send(login_fields)
    print "\nLogin details sent to server........."

  def ReceiveFromServer(self):
    '''
    To receive f8jrom the server.
    ARGS:
    self        : Object created for the class "client" i.e.,[client_obj]
    RETURNS:
      -         : None
    '''
    while True:
      self.server_reply = self.user_socket_fd.recv(4096)
      self.server_reply_list = self.server_reply.split()
      if len(self.server_reply) == 0:
        continue
      elif self.server_reply_list[0] == '201':
        print "\nConnection established with %s...." %(self.selected_user)
        self.SendOrReceiveFromUser()
        continue

      if self.ResponseHandler() == -1:
        return -1

  def ResponseHandler(self):
    '''
    handles the response get from the server
    [action to be performed based on server's response ]
    ARGS:
    self        : Object created for the class "client" i.e.,[client_obj]
    RETURNS:
    1   : To exit from the application
    '''

    if int(self.server_reply_list[0]) == 200:
      config_parser.SetUserDetails(self.user_name, self.password)
    # Get active user list from the server and choose specific user.
      self.GetActiveUsers()
      self.SelectUserOrRequestFromUser()
    elif int(self.server_reply_list[0]) == 203:
      print "\nExiting from the Application...."
      return -1
    elif int(self.server_reply_list[0]) == 204:
      print "\nStatus:\t%s" %self.server_reply[4:]
    elif int(self.server_reply_list[0]) == 400:
    # Selected user went offline.
      print "\n%s went offline....." %(self.selected_user)
    elif int(self.server_reply_list[0]) == 401:
    # Invalid credentials to Log in.
      print "\nInvalid username or password........."
      print "TIPS:\nCheck username or password in config file"
      print "If not registered try registering again\n\n"
      return -1
    elif int(self.server_reply_list[0]) == 402:
    # Already logged in with same username and password.
      print "\n%s Unresponsive"%(self.selected_user)
      return -1

    elif int(self.server_reply_list[0]) == 403:
    # Already logged in with same username and password.
      print "\nSomeone already Logged In....."
      return -1
    elif int(self.server_reply_list[0]) == 404:
    # Selected user declined the connection request.
      print "\n%s declined your request" %(self.selected_user)
    elif int(self.server_reply_list[0]) == 405:
    # Selected user disconnected from the session.
      print "\n%s disconnected from the session" %(self.selected_user)
    elif int(self.server_reply_list[0]) == 406:
      print "\n%s is engaged with others" %(self.selected_user)

  def GetActiveUsers(self):
    '''
    Display the list of active users based on the response list from the server
    ARGS:
    self          : Object created for the class "client" i.e.,[client_obj]
    response_list : List containing the active users.
    RETURNS:
        -         :  Returns nothing.
    '''
    self.active_users = list()
    #print "ACTIVE USERS"
    print "\n\n\t\t\t\tACTIVE USERS"
    print "\t\t\t\t------------------------------"
    for active_user in self.server_reply_list[1 : ]:
      self.active_users.append(active_user)
      print "\t\t\t\t", active_user
      # print the elements in the list.

  def SelectUserOrRequestFromUser(self):
    '''
    -> Select an user who is online or exit from application.
    otherwise,
    -> Accept or reject the request sent from other user via server.
    ARGS:
    self        : Object created for the class "client" i.e.,[client_obj]
    RETURNS:
       -        : None
                  Returns when selected user or exit or
                  Returns when accept or reject the request.
    '''
    print "\n\n\t\t\t\tCommands:\n\t\t\t\t-----------------------",
    print "----------"
    print "\t\t\t\t+ Select user(Enter user_name)"
    print "\t\t\t\t+ Get status(Enter status space user_name)"
    print "\t\t\t\t+ Exit(Enter exit)\n"

   # print "\nOptions:\n1.Select user(Enter user_name)\n2.Get status",
   # print " (Enter status space user_name)\n3. Exit(Enter exit)\n"
    sys.stdout.write('>>')
    sys.stdout.flush()
    self.decision_flag = 0
    count = 0
    while True:
      socket_list = [sys.stdin, self.user_socket_fd]
      # Get the list sockets which are readable
      # sys.stdin -> to read from standard input
      # self.user_socket_fd -> user socket descriptor to hear server response
      read_sockets, write_sockets, error_sockets = \
      select.select(socket_list, [], [])
      for socket in read_sockets:
        print'>>',
        if socket == sys.stdin:
        # Read from standard input
          valid_user_flag = 0
          self.selected_user = raw_input()
          sys.stdout.flush()
          self.selected_user_list = self.selected_user.split(' ', 1)
          if self.selected_user == '':
            break

          if self.decision_flag == 1:
            if self.selected_user.lower() in 'yes' or 'no' and len(self.selected_user) <= 3:
            # accept or reject the request.
              decision_msg = self.selected_user + ' ' + self.server_reply_list[1]
              self.selected_user = self.server_reply_list[1]
              self.user_socket_fd.send(decision_msg)
              self.decision_flag = 0
              #sys.stdout.flush()
              return
            else:
              # if user selects other than 'yes' or 'no' [case insensitive]
              print "\nselect valid option......"
              #self.selected_user = raw_input()
          elif self.selected_user_list[0] == 'exit':
          # exit from the application
            self.user_socket_fd.send('deregister')
            sys.exit()
          elif self.selected_user_list[0] == 'status':
            self.user_socket_fd.send('status ' + self.selected_user_list[1])
            return

          else:
          # user name is selected from the list.
            for active_user in self.active_users:
              if active_user == self.selected_user_list[0]:
              # check username in active list or not.
                valid_user_flag = 1
                break

          if valid_user_flag == 1 and \
            self.selected_user != self.user_name:
          # selected valid user.
            connect_to_user = 'connect_to' +  ' ' + self.selected_user
            self.user_socket_fd.send(connect_to_user)
            print "\nSent request to %s\nWaiting for response....." \
                   %self.selected_user
            sys.stdout.flush()
            return
          elif self.selected_user == self.user_name:
            print "\nYou cannot chat with yourself\nplease select others..."
            break
          else:
          # if selected invalid user.
            print "\nPlease select valid user_name..."
            break

        else:
        # Read[hear] the server reply
          self.server_reply = self.user_socket_fd.recv(4096)
          self.server_reply_list = self.server_reply.split()
          if int(self.server_reply_list[0]) == 202:
          #  got request from another user
            print "\nRequest-->from-->%s\n" %(self.server_reply_list[1])
            self.selected_user = self.server_reply_list[1]
            print "yes or no\n"
            self.decision_flag = 1
            break
            #while True:
            #  decision = raw_input("yes or no\n")
            #  if decision.lower() in 'yes' or 'no' and len(decision) <= 3:
              # accept or reject the request.
            #    decision_msg = decision + ' ' + self.selected_user
            #    self.user_socket_fd.send(decision_msg)
            #    sys.stdout.flush()
            #    return
            #  else:
              # if user selects other than 'yes' or 'no' [case insensitive]
            #    print "\nselect valid option......"
          elif int(self.server_reply_list[0]) == 200:
          # if updated active user list is sent from server
            self.GetActiveUsers()
           # print "yes or no\n"
            #print "\nselect an user or exit from application\n>>"
            sys.stdout.flush()
            break

          elif int(self.server_reply_list[0]) == 400:
            self.ResponseHandler()
            continue

          elif int(self.server_reply_list[0]) == 406:
            self.ResponseHandler()
            print "\nyou may exit from application"
            break
          else:
            continue

  def SendOrReceiveFromUser(self):
    '''
    To send or receive messages from the selected user after
    the connection between them is successfully established.
    ARGS:
    self          : Object created for the class "client" i.e.,[client_obj]
    RETURNS:
      -           : None.
                    Returns when the user enters 'exit' or 'quit' or
                    Returns when we get negative response from the server.
    '''
    self.messages = []
    #print "\nOptions:\n1.send message\n2.quit from session[enter quit]\n",
    #print "3.Exit from App[enter exit]\n4.Transfer file[file]"
    print "\n\n\t\t\t\tCommands:\n\t\t\t\t-----------------------",
    print "--------------"
    print "\t\t\t\t+ Send message[...]"
    print "\t\t\t\t+ Quit from session[enter quit]"
    print "\t\t\t\t+ Exit from App[enter exit]"
    print "\t\t\t\t+ Transfer file[file file_name] --Include full path i.e from home directory"

    print "-->%s :\t" %self.username,
    sys.stdout.flush()
    self.file_count = 0
    while True:
      socket_list = [sys.stdin, self.user_socket_fd]
      # Get the list sockets which are readable.
      # sys.stdin -> to read from standard input
      # self.user_socket_fd -> user socket descriptor to hear server response
      read_sockets, write_sockets, error_sockets = \
                          select.select(socket_list, [], [])
      for socket in read_sockets:
      # incoming message from remote server
        if socket == self.user_socket_fd:
          self.server_reply = self.user_socket_fd.recv(4096)
          self.server_reply_list = self.server_reply.split()
          negative_ack = ['203', '400', '402', '401', '403', '404', '405']
          if self.server_reply_list[0] in negative_ack:
          # Negative ACK from the server instead MSG from selected user.
            self.DumpMessagesToFile()
            self.ResponseHandler()
            return
          elif self.server_reply_list[0] == '402':
          # No response from the selected user.
            print "\nno response from %s" %(self.selected_user)
            print "\nyou may quit the session"
            print "-->%s :\t" %(self.user_name),
            sys.stdout.flush()
          elif self.server_reply_list[0] == '200':
            self.GetActiveUsers()
            break
          elif self.server_reply_list[0] == 'file':
            #print 'L',self.server_reply
            if self.server_reply[-8:] == 'file end':
              receiving_file_des.write(self.server_reply[5:-8])
              print '\nFile received successfully'
              receiving_file_des.close()
              print 'Closed the file'
              self.file_count = 0
            elif self.file_count == 0:
              self.file_count += 1
              receiving_file_des = open(home + '/G2GChatFiles/ReceivedFiles/'+self.server_reply_list[1], "w")
              print 'Opened file succesfully..!!'
            else:
              receiving_file_des.write(self.server_reply[5:]) #TODO: Changing from [5:] to nothing
              #receiving_file_des.write('Written this too')
          else:
          # message from the other user.
            message = '<--' + self.selected_user + ' :\t' + self.server_reply
            print "\n%s" %message
            self.messages.append(message)
            print "-->%s :\t" %(self.user_name),
            sys.stdout.flush()
        else:
    # Enter message to be sent to the selected user.
          msg_to_user = raw_input()
          if msg_to_user == '':
            continue

          if msg_to_user == 'exit':
          # Exit from the application.
            self.user_socket_fd.send('deregister')
            self.DumpMessagesToFile()
            sys.exit()
          elif msg_to_user == 'quit':
          # Disconnect from the session with selected user.
            self.user_socket_fd.send('quit')
            self.DumpMessagesToFile()
            return
          elif msg_to_user[:4] == 'file':
            home = expanduser("~")  
            file_path = home + '/' + msg_to_user[5:]
            file_to_send = file_path.split('/')[-1]
            try:
              sending_file_des = open(file_path, "r")
            except IOError:
              print "\nFile not exists\n"
            else:
              print'Upload Speed : 232 KB/sec'
              self.user_socket_fd.send('file ' + file_to_send)
              time.sleep(0.1)
              temporary_buffer = sending_file_des.read(500)
              while temporary_buffer:
                time.sleep(0.0021)
                self.user_socket_fd.send('file ' + temporary_buffer)
                temporary_buffer = sending_file_des.read(500)
                print '\nSending Rest'

              print "\nfile sent succesfully\n"
              sending_file_des.close()
              self.user_socket_fd.send('file end')
          else:
          # Send message to the selected user.
            msg = 'send_msg' + ' ' + msg_to_user
            self.user_socket_fd.send(msg)
            message = '-->' + self.user_name + ' :\t' + msg_to_user
            self.messages.append(message)
            print "-->%s :\t" %(self.user_name),
            sys.stdout.flush()

  def DumpMessagesToFile(self):
    home = expanduser("~")
    file_name = home + '/G2GChatFiles/Conversations/' + self.selected_user + '_to_' + \
                  self.user_name + time.strftime('_%d-%m-%Y_%H:%M:%S')+ '.txt'
    file_des = open(file_name, "w")
    for message in self.messages:
      file_des.write(message + '\n')
    file_des.close()


if __name__ == '__main__':

  user_socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # create a socket descriptor

  if config_parser.IpValidation(config_parser.server_ip_address) != 4:
    print "Invalid IP Address......\n\n"
    exit()
  if not config_parser.PortValidation(config_parser.port):
    print "Invalid Port number......\n\n"
    exit()

  client_instance = Client(config_parser.server_ip_address, \
                    config_parser.port,\
                    user_socket_fd)#Removed user_name and password

  # client_obj  -> object for the class client
  client_instance.ConnectToServer()
  # call ConnectToServer() to establish connection with the server.

  client_instance.Start()


