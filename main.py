import boto3
from threading import Thread
import threading

class iam_user(object):

  def __init__(self, name,ca):
     self.name = name
     self.console_access = ca
     
  def check_for_mfa(self):
   client = boto3.client('iam')
   list_mfa_devices=client.list_mfa_devices(UserName=self.name)
   if list_mfa_devices['MFADevices'] == [] and self.console_access==True:   
     no_mfa_users.append(self.name)
   
   
if __name__ == '__main__':
  client = boto3.client('iam')
  list_users= client.list_users() 
  no_mfa_users=[]
  threads=[]

  for user in list_users['Users']:
    try:
      if user['PasswordLastUsed']:
        console_access= True 
    except KeyError:
       console_access=False
    user= iam_user(user['UserName'],console_access)
    thread=(threading.Thread(target=user.check_for_mfa))
    threads.append(thread)
    
  for i in range (0,len(threads)):
    threads[i].start()
  for i in range (0,len(threads)):
    threads[i].join()

  print ("Usernames \n")
  for user in no_mfa_users:
    print(user) 
  print ("\n Number of users without MFA device:",len(no_mfa_users))



