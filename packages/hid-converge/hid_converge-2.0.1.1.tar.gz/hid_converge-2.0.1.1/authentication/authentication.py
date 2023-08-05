'''
Created on Apr 27, 2015
import requests

@author: karpagm1
'''

import requests
import logging
import json
import datetime
from QueueModule.q import totalTime
from QueueModule.q import permissionAuditEvaluatorDict
from QueueModule.q import permissionReason4ChangeEvaluatorDict
session = requests.session()
class Authentication(object):
    
    def performLogOut(self,baseUrl,username):
        cookie ={}
        cookie['name'] = username
        cookie['username'] = username
        cookie['authToken'] = self.authToken
        cookieJson = json.dumps(cookie)
        response = session.post(baseUrl+'/platform/common/user/logout/',data=cookieJson)
        if response.status_code == 200:
            #print('Successfully logged out of the system')
            logging.info('Successfully logged out of the system') 
        else:
            #print(response.request.headers)
            logging.info( response.request.headers) 
            #print('Error logging out the system. response code' +  str(response.status_code))
            logging.info('Error logging out the system.  response code' + str(response.status_code))
            #print('Error logging out the system.  response text' + response.text)
            logging.info('Error logging out the system. response text' + response.text)
        finalTime = datetime.datetime.now()
        print('\n')
        print('-----------Total Time Taken To Execute The Flow: ', finalTime - totalTime.get(),'-----------')
        print('\n')
        
    def performLogin(self, baseUrl, userName, password):
        iniTime = datetime.datetime.now()
        totalTime.put(iniTime)
        response = requests.post(baseUrl+'/platform/common/user/login?username='+userName+'&password='+password,headers={"X-Auth-Username":userName})
        if response.status_code == 200:
            #print('Successfully logged into the system')
            logging.info('Successfully logged into the system') 
            self.session = requests.session()
            self.authToken = response.json()['authToken']
            headers = {'X-Auth-Token': response.json()['authToken'], 'Content-Type':'application/json;charset=UTF-8','X-Auth-Username':userName}
            session.headers = headers;
            self.doSystemInnitialization(baseUrl,headers,userName)
            return True
        else:
            #print('Error logging in the system. response code' +  str(response.status_code))
            logging.info('Error logging in the system.  response code'+ str(response.status_code))
            #print('Error in out the system.  response text' + response.text)
            logging.info('Error in  the system. response text' + response.text)
            return False

    def doSystemInnitialization(self,baseURL,headers,userName):
        self.evaluatePermissions(baseURL,headers,userName)

    # Permission Related API
    def evaluatePermissions(self,baseUrl,headers,userName):
        # CaseService.logService('getAnalysisInput')
        permissionEvaluatorUrl = baseUrl + '/platform/common/role/getAllPermissions?language=en_US'
        response = self.session.get(permissionEvaluatorUrl,headers=headers)
        if response.status_code == 200:
            for index in range(len(response.json())):
                permissionAuditEvaluatorDict.update({response.json()[index]['name'] : response.json()[index]['audit']})
                permissionReason4ChangeEvaluatorDict.update({response.json()[index]['name'] : response.json()[index]['reason']})
        else:
            self.performLogOut(baseUrl,userName)

            
        
    

