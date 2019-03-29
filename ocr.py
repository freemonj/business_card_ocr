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
import string


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


class ContactInfo():
    '''
    ContactInfo Class
    '''


    def __init__(self,doc):
        '''
        Constructor
        :params: doc
        :return: None
        :rtype: None
        '''
        self.logger = _log_init()
        self.email = None
        self.name = None
        self.number = None
        self.document = doc
        self._processFile(self.document)
            
    
    def _isPhoneAFaxNum(self,line):
        """
        Checks to see if the phone number is a fax number for a given line in the input document.
        :params: String
        :return: Bool
        :rtype: Bool
        """       
        ans = None
        ans = line.split(':',1)[0]
        ans = ans.lower()
        if ans == "fax" or ans == "cell":
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
        try:   
            char = None
            line = line.translate({ord(c): None for c in '()-_+\n\r'})
            return line
        except:
            self.logger.error(traceback.format_exc())
        

    def _numsanitizeLine(self,line):
        """
        Sanitizes a given line from the input document by stripping all punctuation, newline/carriage returns and whitespace.
        Used for the getPhoneNumber() method.
        :params: String
        :return: String
        :rtype: String
        """        
        line = line.translate({ord(c): None for c in '&()-_+\n\r" "'})
        return line


    def _processFile(self,document):
        namecache = []
        nameflag = False
        numberflag = False
        emailflag = False        
        try:
            with open(document,mode='rt') as doc:
                for line in doc:
                    if not emailflag:
                        self.email = self.getEmailAddress(line)
                        if self.email is not None:
                            emailflag = True
                    if not numberflag:
                        self.number = self.getPhoneNumber(line)                        
                        if self.number is not None:
                            numberflag = True
                    if not emailflag and not numberflag:
                        namecache.append(line)
                        emailflag = False
                        numberflag = False
            if self.email is not None:
                self.name = self.getName(self.email, namecache)
            self.logger.debug("Name: {}".format(self.name))
            self.logger.debug("Telephone: {}".format(self.number))
            self.logger.debug("Email: {}".format(self.email))                        
                
        except:
            self.logger.error(time.strftime("%b %d %Y %H:%M:%S: ", time.localtime()) +
                         'Trace =  {}'.format(traceback.format_exc()))        

    
    def getName(self,email,namecache):
        '''
        Returns the full name of the individual (eg. John Smith, Susan Malick)
        :params: None
        :return: string
        :rtype: string
        '''        
        try:
            fname = None
            username = email.split('@',1)[0]
            for ind,name in enumerate(namecache):
                orig = self._sanitizeLine(name)
                namelen = len(name)
                name = name.lower()
                for i in range(1,int(namelen/2)):
                    if username in name:
                        return orig
                    username = username[ind + 1:]
            return None                     
        except Exception:
                self.logger.error(time.strftime("%b %d %Y %H:%M:%S: ", time.localtime()) +
                             'Trace =  {}'.format(traceback.format_exc()))        
        
        
    def getPhoneNumber(self,line):
        '''
        Returns the phone number formatted as a sequence of digits
        :params: None
        :return: Integer
        :rtype: Integer
        '''  
        try:
            sanitizedline = None
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


        
    def getEmailAddress(self,line):
        '''
        Returns the email address
        :params: None
        :return: string
        :rtype: string
        '''  
        try:
            if '@' in line and '.' in line:                        
                self.logger.debug("type = {} and value = {}".format(type(line),line))
                return line
            else:
                return None
        except Exception:
                self.logger.error(time.strftime("%b %d %Y %H:%M:%S: ", time.localtime()) +
                             'Trace = {}'.format(traceback.format_exc()))        

        
    def _returnLog(self):
        '''
        Returns the instance of logger in ContactInfo
        :params: None
        :return: logger
        :rtype: Logger Object
        '''          
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
        self.log = self.cinfo._returnLog()
        self.log.debug("cinfo.name = {}".format(self.cinfo.name))
        self.log.debug("cinfo.phone = {}".format(self.cinfo.number))
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
        print("Phone: {}".format(bcpobj.number))
        print("Email: {}".format(bcpobj.email))
    except:
        if len(sys.argv) <= 1:
            print("error trace = {}".format(traceback.format_exc()))
        else:
            print("error trace = {}".format(traceback.format_exc()))
