'''
Created on Apr 27, 2015
import requests

@author: karpagm1
'''

import simplejson
import sys
import logging
import inspect
#import time
import datetime
from authentication import authentication
from threading import Thread, current_thread
from QueueModule.q import flushableQ
from QueueModule.q import timeloggingQ
from QueueModule.q import permissionAuditEvaluatorDict
from QueueModule.q import permissionReason4ChangeEvaluatorDict

class GateWayService:

    @staticmethod    
    def callConvergeRestApi(url,httpMethod,payload):
        resultLog = logging.getLogger('resultLog') 
        if httpMethod == 'POST':
            GateWayService.logBeforeRestCall('POST', url,payload)
            response = authentication.session.post(url, data=payload)                 
        elif httpMethod == 'GET':
            GateWayService.logBeforeRestCall('GET',url,payload)
            response = authentication.session.get(url)       
        elif httpMethod == 'DELETE':
            GateWayService.logBeforeRestCall('DELETE',url,payload)
            response = authentication.session.delete(url)     
            
        if response.status_code == 200:
            if(httpMethod == 'DELETE'):
                return
            dict= simplejson.loads(response.text)
            GateWayService.logAfterRestCall(response)
            beforetimestamp = timeloggingQ.get()
            print('Time Taken: ', timeloggingQ.get()-beforetimestamp)
            timeloggingQ.queue.clear()
            if response.headers.get('X-License-Token') != None:
                licenceToken = response.headers['X-License-Token']
                authentication.session.headers.update({'X-License-Token': licenceToken})
            return dict
        elif  response.status_code == 461:
            GateWayService.logAfterRestCall(response)
            beforetimestamp = timeloggingQ.get()
            print('Time Taken: ', timeloggingQ.get() - beforetimestamp)
            timeloggingQ.queue.clear()
            resultLog.info(' Stopped the script since all licence are consumed')
            sys.exit(' Stopped the script since all licence are consumed')
        else:
            GateWayService.logAfterRestCall(response)
            beforetimestamp = timeloggingQ.get()
            print('Time Taken: ', timeloggingQ.get() - beforetimestamp)
            timeloggingQ.queue.clear()
            resultLog.info(' Stopped the script : Received error code' +str(response.status_code)) 
            sys.exit(' Stopped the script : Received error code' +str(response.status_code)) 
            
   
    @staticmethod    
    def callConverge(url, post, payload):
        resultLog = logging.getLogger('resultLog')
        calledfunction = inspect.stack()[1][3]
        headers = GateWayService.getHeadersForAudit(calledfunction, url)
        if post == 'true':
            GateWayService.logBeforeRestCall('POST', url, payload, headers)
            response = authentication.session.post(url, data=payload, headers=headers)
        else:
            headers = {}
            GateWayService.logBeforeRestCall('GET',url,payload, headers)
            response = authentication.session.get(url)       
        
        if response.status_code == 200:
            dict= simplejson.loads(response.text)
            GateWayService.logAfterRestCall(response)
            beforetimestamp = timeloggingQ.get()
            print('Time Taken: ', timeloggingQ.get() - beforetimestamp)
            timeloggingQ.queue.clear()
            if response.headers.get('X-License-Token') != None:
                licenceToken = response.headers['X-License-Token']
                authentication.session.headers.update({'X-License-Token': licenceToken})
            return dict
        elif  response.status_code == 461:
            GateWayService.logAfterRestCall(response)
            beforetimestamp = timeloggingQ.get()
            print('Time Taken: ', timeloggingQ.get() - beforetimestamp)
            timeloggingQ.queue.clear()
            resultLog.info(' Stopped the script since all licence are consumed')
            sys.exit(' Stopped the script since all licence are consumed')
        else:
            GateWayService.logAfterRestCall(response)
            beforetimestamp = timeloggingQ.get()
            print('Time Taken: ', timeloggingQ.get() - beforetimestamp)
            timeloggingQ.queue.clear()
            resultLog.info(' Stopped the script : Received error code' +str(response.status_code)) 
            sys.exit(' Stopped the script : Received error code' +str(response.status_code))

    # Add method to get the Audit header based on the permission evaluator
    @staticmethod
    def getHeadersForAudit(calledfunction, targeturl):
        if (calledfunction == 'createCase' and permissionAuditEvaluatorDict['Add Case'] == True):
            if (permissionAuditEvaluatorDict['Add Case'] == True and permissionReason4ChangeEvaluatorDict[
                'Add Case'] == True):
                # headers = {"ids": "", "klassName": "com.lifetech.converge.domain.DnaCase","reason": "Ran Py to createCase"}
                headers = {"reason": "Ran Py to createCase"}
            else:
                # headers = {"ids": "", "klassName": "com.lifetech.converge.domain.DnaCase", "reason": None}
                headers = {}
        elif (calledfunction == 'addSubjectToCase' and permissionAuditEvaluatorDict['Add Subject'] == True):
            caseId = flushableQ.get()
            if (permissionAuditEvaluatorDict['Add Subject'] == True and permissionReason4ChangeEvaluatorDict[
                'Add Subject'] == True):
                # headers = {"ids": caseId,"klassName": "com.lifetech.converge.domain.DnaCase,com.lifetech.converge.domain.Person","reason": "Ran Py to addSubjectToCase"}
                headers = {"reason": "Ran Py to addSubjectToCase"}
            else:
                # headers = {"ids": caseId,"klassName": "com.lifetech.converge.domain.DnaCase,com.lifetech.converge.domain.Person","reason": None}
                headers = {}
            flushableQ.queue.clear()
        elif (calledfunction == 'addProfileToCase' and permissionAuditEvaluatorDict['Import Profile'] == True):
            caseId = flushableQ.get()
            if (permissionAuditEvaluatorDict['Import Profile'] == True and permissionReason4ChangeEvaluatorDict[
                'Import Profile'] == True):
                # headers = {"ids": caseId, "klassName": "com.lifetech.converge.domain.DnaCase","reason": "Ran Py to addProfileToCase"}
                headers = {"reason": "Ran Py to addProfileToCase"}
            else:
                # headers = {"ids": caseId, "klassName": "com.lifetech.converge.domain.DnaCase", "reason": None}
                headers = {}
            flushableQ.queue.clear()
        elif (calledfunction == 'postAnalysisInput' and permissionAuditEvaluatorDict[
            'Save Kinship Hypotheses'] == True):
            if (permissionAuditEvaluatorDict['Save Kinship Hypotheses'] == True and
                        permissionReason4ChangeEvaluatorDict['Save Kinship Hypotheses'] == True):
                # headers = {"ids": "", "klassName": "com.lifetech.converge.domain.DnaCase","reason": "Ran Py to postAnalysisInput"}
                headers = {"reason": "Ran Py to postAnalysisInput"}
            else:
                # headers = {"ids": "", "klassName": "com.lifetech.converge.domain.DnaCase", "reason": None}
                headers = {}
        elif (calledfunction == 'saveAnalysisResults' and permissionAuditEvaluatorDict['Save Result'] == True):
            caseId = flushableQ.get()
            if (permissionAuditEvaluatorDict['Save Result'] == True and permissionReason4ChangeEvaluatorDict[
                'Save Result'] == True):
                # headers = {"ids": caseId, "klassName": "com.lifetech.converge.domain.DnaCase","reason": "Ran Py to saveAnalysisResults"}
                headers = {"reason": "Ran Py to saveAnalysisResults"}
            else:
                # headers = {"ids": caseId, "klassName": "com.lifetech.converge.domain.DnaCase", "reason": None}
                headers = {}
            flushableQ.queue.clear()
        elif (calledfunction == 'createReport' and permissionAuditEvaluatorDict['Generate Report'] == True):
            if ('/kinship/kinship/createKinshipReport/' in targeturl and permissionAuditEvaluatorDict[
                'Generate Report'] == True):
                caseId = flushableQ.get()
                if (permissionAuditEvaluatorDict['Generate Report'] == True and permissionReason4ChangeEvaluatorDict[
                    'Generate Report'] == True):
                    # headers = {"ids": caseId, "klassName": "com.lifetech.converge.domain.DnaCase","reason": "Ran Py to createReport"}
                    headers = {"reason": "Ran Py to createReport"}
                else:
                    # headers = {"ids": caseId, "klassName": "com.lifetech.converge.domain.DnaCase", "reason": None}
                    headers = {}
                flushableQ.queue.clear()
            else:
                headers = {}
        else:
            headers = {}

        return headers

# @staticmethod
    # def checkPermissionEvaluator(calledfunction, targeturl):

    @staticmethod
    def logBeforeRestCall(method, url, payload, auditenabled):
        print (method + ' post call initiated. ' +'  calling callConverge - url ' + url )
        #logging.info(method + ' post call initiated. '+' calling callConverge service -url'+ url)
        #print(authentication.session.headers )
        #logging.info( authentication.session.headers)
        BeforeRestCallSysTime = datetime.datetime.now()
        timeloggingQ.put(BeforeRestCallSysTime)
        #print(BeforeRestCallSysTime)

    @staticmethod
    def logAfterRestCall(response):
        #print(response.request.headers)
        #logging.info( response.request.headers)
        print(' status code  from server '+ str(response.status_code)) 
        #logging.info(' status code  from server '+ str(response.status_code))
        AfterRestCallSysTime = datetime.datetime.now()
        timeloggingQ.put(AfterRestCallSysTime)
        #print(AfterRestCallSysTime)
        #print('  response text from server '+ response.text)
        #logging.info(' response  text from server '+ response.text)
