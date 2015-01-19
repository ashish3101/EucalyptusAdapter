# Image.py
#
# Represents Image Class.
# Contains operations related to Images.
#
# _author_ = "Ashish Agarwal, P.Amulys Sri"

import os
import boto
import sys
import time
import boto.manage.cmdshell
from datetime import date, timedelta
import logging
import ConfigParser
from subprocess import call
import subprocess

class Image(object):

    """
    Represents Image.
    """

    # Get Connection
    def __init__(self, cred_dict, image_name, image_path, image_arch):

        """
        Establishes Connection to Eucalyptus cloud. Throws an exception if there is any error in access key or secret key.

        :param cred_dict: Dictionary containing ip_address, access key and secret key of Cloud Infrastructure.
        :param image_name: The name of the AMI. Valid only for EBS-based images.
        :param image_path: Full path to your AMI manifest in Amazon S3 storage. Only used for S3-based AMI's.
        :param image_arch: The architecture of the AMI. Valid choices are:
            * i386
            * x86_64
        """    
        self._is_image_exists = False
        logging.basicConfig(filename='eucalyptus.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
        try:
            logging.info('Establishing Connection...')
            self.__conn__ = boto.connect_euca(cred_dict['ip_address'], cred_dict['access_key'], cred_dict['secret_key'])
            logging.info('Connection Established SUCCESSFULLY...')

            self._create_(image_name, image_path, image_arch)
        except:
            logging.warning('INVALID Credentials...')
            logging.critical('Connection ABORTED...')
            raise          

    # Create a new VM Instance
    def _create_(self, image_name, image_path, image_arch):

        """
        Register an EMI.

        :param image_name: The name of the EMI. Valid only for EBS-based images.
        :param image_path: Full path to your EMI manifest.
        :param image_arch: The architecture of the AMI. Valid choices are:
            * i386
            * x86_64
        """
        logging.info('Creating Image...')
        try:
            logging.info('Waiting for Image to CREATE...')

            bundle_path = self._bundle_(image_name, image_path, image_arch)
            upload_path = self._upload_(bundle_path)
            register_id = self._register_(image_name, upload_path)

            self.id = register_id
            self.name = image_name
            self.architecture = image_arch

            logging.info('Image is in PENDING state...')
            self._is_image_exists = True
        except:
            logging.error('Image not CREATED...')
            raise

    # Bundling Image
    def _bundle_(self, image_name, image_path, image_arch):
        
        """
        Returns the bundled image manifest path.

        :param image_name: The name of the AMI. Valid only for EBS-based images.
        :param image_path: Full path to your AMI manifest in Amazon S3 storage. Only used for S3-based AMI's.
        :param image_arch: The architecture of the AMI. Valid choices are:
            * i386
            * x86_64
        """    
        logging.info('Bundling Image...')
        print 'Bundling Image...'
        try:
            bundle_xml = subprocess.Popen(['euca-bundle-image', '-i', image_path, '--arch', image_arch], stdout=subprocess.PIPE)
            bundle_xml_out = bundle_xml.stdout.read()
            logging.info('Wrote bundled manifest: %s', bundle_xml_out.split()[2])
            print 'Wrote bundled manifest: ', bundle_xml_out.split()[2]
            return bundle_xml_out.split()[2]
        except:
            logging.error('Image bundling FAILED...')
            raise

    # Uploading Image
    def _upload_(self, bundle_path):

        """
        Returns the uploaded image manifest path.

        :param bundle_path: The bundled image manifest path.
        """
        logging.info('Uploading Image...')
        print 'Uploading Image...'
        try:    
            upload_xml = subprocess.Popen(['euca-upload-bundle', '-b', 'MyBucket', '-m', bundle_path], stdout=subprocess.PIPE)
            upload_xml_out = upload_xml.stdout.read()
            logging.info('Wrote uploaded manifest: %s', upload_xml_out.split()[1])
            print 'Wrote uploaded manifest: ', upload_xml_out.split()[1]
            return upload_xml_out.split()[1]
        except:
            logging.error('Image uploading FAILED...')
            raise

    # Registering Image
    def _register_(self, image_name, upload_path):

        """
        Returns registered image ID.

        :param upload_path: The uploaded image manifest path.
        """
        logging.info('Registering Image...')
        print 'Registering Image...'
        try:
            register_xml = subprocess.Popen(['euca-register', '-n', image_name, upload_path], stdout=subprocess.PIPE)
            register_xml_out = register_xml.stdout.read()
            logging.info('Registered Image ID: %s', register_xml_out[6:-1])
            print 'Registered Image ID: ', register_xml_out[6:-1]
            return register_xml_out[6:-1]
        except:
            logging.error('Image registering FAILED...')
            raise

    #Delete a Image
    def delete(self):
        
        """
        Unregister an EMI.
        """
        try:
            assert(self._is_image_exists)
        except:
            logging.info('Instance NOT FOUND')
            raise

        try:
            logging.info('Deleting Image...')
            self.__conn__.deregister_image(self.id)
            self._is_image_exists = False
        except:
            logging.error('Image not DELETED')
            raise      