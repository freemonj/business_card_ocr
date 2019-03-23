'''
Created on Mar 22, 2019

@author: johnsf1
'''

import logging
import argparse
from logging.handlers import TimedRotatingFileHandler
import time
import os
from os import path
import sys
import traceback


# Location to log messages to.
LOG_FILE_NAME = path.join('logs', 'business-card-ocr.log')
#################################

def _log_init():
    """
    Initializes the rotating program logger.
    :params: None
    :return: logger
    :rtype: Logger Object
    """

    # Creating logs directory if it does not exist already.
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s][%(levelname)-5.5s]  %(message)s")

    logger = logging.getLogger("Rotating Log")
    '''THIS IS THE ONLY LINE YOU CHANGE BELOW FOR THE LOG LEVEL FOR OCR PROGRAM '''
    logger.setLevel(logging.DEBUG)
    
    # If you want DEBUG messages to go to stdout uncomment the next two lines
    #console_handler = logging.StreamHandler()
    #logger.addHandler(console_handler)
    
    file_handler = TimedRotatingFileHandler(LOG_FILE_NAME,
                                            when="midnight",
                                            encoding="UTF-8",
                                            backupCount=30)
    file_handler.setFormatter(logFormatter)
    logger.addHandler(file_handler)
    return logger

class ContactInfo(object):
    '''
    ContactInfo Class
    '''


    def __init__(self, doc):
        '''
        Constructor
        :params: doc
        :return: None
        :rtype: None
        '''
        self.logger = _log_init()
        self.document = doc
        self.phonenumber = self.getPhoneNumber()
        self.email = self.getEmailAddress()
        self.name = self.getName()
    
    
    def _isPhoneAFaxNum(self,line):
        """
        Checks to see if the phone number is a fax number for a given line in the input document.
        :params: String
        :return: Bool
        :rtype: Bool
        """
        
        ans = None
        if ':' in line:
            ans = line.split(':',1)[0]
            ans = ans.lower()
            if ans == "fax":
                return True
        return False
                
    def _sanitizeLine(self,line):
        """
        Sanitizes a given line from the input document by stripping all punctuation and newline/carriage returns.
        Used for the getName() and getEmail() methods.
        :params: String
        :return: String
        :rtype: String
        """
                
        line = line.replace(')','')
        line = line.replace('(', '')
        line = line.replace('-','')
        line = line.replace('+','')
        line = line.replace('\n','')
        line = line.replace('\r','')        
        return line

    def _numsanitizeLine(self,line):
        """
        Sanitizes a given line from the input document by stripping all punctuation, newline/carriage returns and whitespace.
        Used for the getPhoneNumber() method.
        :params: String
        :return: String
        :rtype: String
        """        
        line = line.replace(')','')
        line = line.replace('(', '')
        line = line.replace('-','')
        line = line.replace('+','')
        line = line.replace(' ','')
        line = line.replace('\n','')
        line = line.replace('\r','')        
        return line

     
    def _isUsernameInName(self,first,last,line):
        """
        Checks to see if the username of the email address is anywhere in the line.
        :params: String, String, String
        :return: Bool
        :rtype: Bool
        """              
        line = line.lower()
        if first is not None:
            remainder1 = first
            first = first.lower()
            first_length = len(first)
            for i in range(1,int(first_length/2)):
                if remainder1 in line:
                    return True
                remainder1 = first[i:]     
        if last is not None:
            remainder2 = last
            last = last.lower()
            last_length = len(last)
            for x in range(1,int(last_length/2)):
                if remainder2 in line:
                    return True
                remainder2 = first[x:]                            
        return False
    
    def getName(self):
        '''
        Returns the full name of the individual (eg. John Smith, Susan Malick)
        :params: None
        :return: string
        :rtype: string
        '''        
        try:
            wordlist = None
            first = None
            last = None
            wordlist = self.email.split('@',1)[0] # grab username in email
            if '.' in wordlist:
                first = wordlist.split('.',1)[0]
                last = wordlist.split('.',1)[1]
            elif '-' in wordlist:
                first = wordlist.split('-',1)[0]
                last = wordlist.split('-',1)[1]
            elif '_' in wordlist:
                first = wordlist.split('_',1)[0]
                last = wordlist.split('_',1)[1]
            else:
                first = wordlist            
            with open(self.document,mode='rt') as doc:
                for line in doc:
                                                                        
                    # Is first or last in the name found earlier?
                    if self._isUsernameInName(first, last, line):
                        self.logger.debug("type = {} and value = {}".format(type(line),line))
                        # Get rid of newlines and carriage returns for windows and Linux for output format                        
                        line = self._sanitizeLine(line)
                        return line
            return None
                    
        except Exception:
                self.logger.error(time.strftime("%b %d %Y %H:%M:%S: ", time.localtime()) +
                             'Trace =  {}'.format(traceback.format_exc()))        
        
    def getPhoneNumber(self):
        '''
        Returns the phone number formatted as a sequence of digits
        :params: None
        :return: Integer
        :rtype: Integer
        '''  
        try:
            sanitizedline = None
            with open(self.document,mode='rt') as doc:
                for line in doc:
                    sanitizedline = self._numsanitizeLine(line)
                    if ':' in sanitizedline:
                        if not self._isPhoneAFaxNum(sanitizedline):                        
                            try:
                                val = int(sanitizedline.split(':',1)[1])
                                return val                    
                            except:
                                pass
                    else:
                        try:
                            val = int(sanitizedline)
                            return val
                        except:
                            pass
                self.logger.debug("type = {} and value = {}".format(type(sanitizedline),sanitizedline))
                return None
        except Exception:
                self.logger.error(time.strftime("%b %d %Y %H:%M:%S: ", time.localtime()) +
                             'Trace =  {}'.format(traceback.format_exc()))        


        
    def getEmailAddress(self):
        '''
        Returns the email address
        :params: None
        :return: string
        :rtype: string
        '''  
        try:
            with open(self.document,mode='rt') as doc:
                for line in doc:
                    if '@' in line:                        
                        self.logger.debug("type = {} and value = {}".format(type(line),line))
                return line
        except Exception:
                self.logger.error(time.strftime("%b %d %Y %H:%M:%S: ", time.localtime()) +
                             'Trace = {}'.format(traceback.format_exc()))        

        
    def returnLog(self):
        return self.logger



class BusinessCardParser(ContactInfo):
    '''
    Business Card Parser Class that inherits from ContactInfo
    '''      
        
    def __init__(self):
        '''
        Constructor
        :params: None
        :return: None
        :rtype: None
        '''        
        self.cinfo = None
        self.log = None
        
        
    def getContactInfo(self,document):
        '''
        Returns ContactInfo object
        :params: string
        :return: string
        :rtype: ContactInfo Object
        '''  
        
        self.cinfo = ContactInfo(document)
        self.log = self.cinfo.returnLog()
        self.log.debug("cinfo.name = {}".format(self.cinfo.name))
        self.log.debug("cinfo.phone = {}".format(self.cinfo.phonenumber))
        self.log.debug("cinfo.email = {}".format(self.cinfo.email))        
        return self.cinfo











if __name__ == '__main__':
    assert (sys.version_info >= (3,0,0)), "python version 3.x is required!"
    if len(sys.argv) <= 1:
        print("Usage:")
        print("python ocr.py -f <input document filename>")
        sys.exit()
    try:
        cliparser = argparse.ArgumentParser(description="Business Card OCR")
        cliparser.add_argument('-f', '--file',
                            action='store',
                            help='The absolute path of input document or relative path from the program execution.')
        
        args = cliparser.parse_args()
        inputfile = args.file
        bcp = BusinessCardParser()
        bcpobj = bcp.getContactInfo(inputfile)
        bcpobj.logger.info("TEST")
        print("Name: {}".format(bcpobj.name))
        print("Phone: {}".format(bcpobj.phonenumber))
        print("Email: {}".format(bcpobj.email))
    except:
        if len(sys.argv) <= 1:
            print("error trace = {}".format(traceback.format_exc()))
    