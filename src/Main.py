# Main.py
#
# Represents Main Class
#
# _author_ = "Ashish Agarwal, P.Amulys Sri"

import os
import boto
import sys
import time
import boto.manage.cmdshell
from datetime import date,timedelta
import logging
import ConfigParser
from VMInstance import VMInstance
from Image import Image
from CloudResources import CloudResources

cred_dict = {
    "ip_address":"10.2.56.20",
    "access_key":"AKIAYL1OGJDNW3VC3OLU",
    "secret_key":"etGkEl9ipIIay0sLhDqRyZsANGCKFdMzM3FRGSUp"
}

class Main(object):

    """
    Represents Main Class.
    """

    # Get Connection
    def __init__(self, cred_dict, image_name, security_key, security_group, instance_type):

        """
        Establishes Connection to Eucalyptus cloud. Throws an exception if there is any error in access key or secret key.

        :param cred_dict: Dictionary containing ip_address, access key and secret key of Cloud Infrastructure.
        """
        logging.basicConfig(filename='eucalyptus.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
        self._ip = cred_dict['ip_address']
        try:
            logging.info('Establishing Connection...')

            self.__conn__ = boto.connect_euca(cred_dict['ip_address'], cred_dict['access_key'], cred_dict['secret_key'])

            logging.info('Connection Established SUCCESSFULLY...')  
        except:
            logging.warning('INVALID Credentials...')
            logging.critical('Connection ABORTED...')
            raise

        try:        
            resource = CloudResources(cred_dict)
            image = resource.get_name_specific_image(image_name)
            #if (image == None):
            #    print image
        except:
            logging.error('Image ERROR...')
            raise

        try:
            print image.id
            vm_instance = VMInstance(cred_dict, image.id, security_key, security_group, instance_type)
            #print vm_instance
            #print type(vm_instance.instance)
        except:
            print 'Please enter VALID Credentials...'

        print 'Instance RUNNING...'
        assert(vm_instance.instance.instance_type == 'm1.small')
        #vm_instance.connect_to_vm()


main = Main(cred_dict, 'ubuntu', 'key1', ['Group1'], 'm1.small')