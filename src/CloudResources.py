# CloudResources.py
# 
# _author_ = "Ashish Agarwal, P.Amulys Sri"


import os
import boto
import sys
import time
import re
import boto.manage.cmdshell
from subprocess import call
from datetime import date,timedelta
import logging
from VMInstance import VMInstance
from Image import Image

class CloudResources(object):

    # Get Connection
    def __init__(self, cred_dict):

        """
        Establishes Connection to Eucalyptus cloud. Throws an exception if there is any error in access key or secret key.

        :param cred_dict: Dictionary containing ip_address, access key and secret key of Cloud Infrastructure.
        """
        logging.basicConfig(filename='eucalyptus.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
        self._ip = cred_dict['ip_address']
        try:
            logging.info('Establishing Connection...')

            self.__conn__ = boto.connect_euca(cred_dict['ip_address'], cred_dict['access_key'], cred_dict['secret_key'])
            self._image_list = self.__conn__.get_all_images()
            self._vm_list = self.__conn__.get_only_instances()

            logging.info('Connection Established SUCCESSFULLY...')  
        except:
            logging.warning('INVALID Credentials...')
            logging.critical('Connection ABORTED...')
            raise          

    # Get Image List
    def get_image_list(self):

        """
        Returns list of images.
        """  
        im_list = []
        try:
            logging.info('Getting Image List...') 
            for image in self._image_list:
                if 'emi' in image.id:
                    im_list.append(image.name)
            logging.info('Images FOUND...')
            return im_list
        except:
            logging.error('UNABLE to find Images...')
            raise

    # Get particular name specific Image
    def get_name_specific_image(self, image_name):

        """
        Returns list of name specific images.

        :param image_name: Name of image to find.
        """
        im_list = []
        try:
            logging.info('Getting Image List...')
            for image in self._image_list:
                if re.search(image_name, image.name, re.IGNORECASE) and 'emi' in image.id:
                    #return image
                    im_list.append(image)
            logging.info('Images FOUND...')
            #print im_list[9]
            return im_list[9]
        except:
            logging.error('UNABLE to find name specific images...')
            raise

    # Get particular architecture specific Image
    def get_arch_specific_image(self, image_arch):

        """
        Returns list of architecture specific images.

        :param image_arch: Architecture of image to find.
        """
        im_list = []
        try:
            logging.info('Getting Image List...')
            for image in self._image_list:
                if re.search(image_arch, image.architecture, re.IGNORECASE) and 'emi' in image.id:
                    im_list.append(image.name)
            logging.info('Images FOUND...')
            return im_list
        except:
            logging.error('UNABLE to find architecture specific images...')
            raise

    # Get VM list
    def get_vm_list(self):

        """
        Returns list of vm's.
        """  
        vm_list = []
        try:
            logging.info('Getting VM List...') 
            for vm in self._vm_list:
                    vm_list.append(vm.id)
            logging.info('VM FOUND...')
            return vm_list
        except:
            logging.error('UNABLE to find VM...')
            raise

    # Get running VM list
    def get_running_vm_list(self):

        """
        Returns list of running vm's.
        """  
        vm_list = []
        try:
            logging.info('Getting VM List...') 
            for vm in self._vm_list:
                if vm.state == 'running':
                    vm_list.append(vm.id)
            logging.info('Running VM FOUND...')
            return vm_list
        except:
            logging.error('UNABLE to find running VM...')
            raise

    # Resource Utilization  
    def get_resource_utilization(self, file_name):

        """
        Save resource utilization data to a file.

        :param file_name: Name of the in which data is saved. 
        """
        today = date.today()
        yesterday = date.today() - timedelta(1)
        yesterday_iso = yesterday.isoformat()
        today_iso = today.isoformat()

        try:
            logging.info('Generating Report...')
            call(['eureport-generate-report', '-F', '-s', yesterday_iso, '-e', today_iso, file_name])
            logging.info('Report is saved to : %s', file_name)
        except:
            logging.error('UNABLE to calculate Resource Utilization...')
            raise
