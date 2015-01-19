# VMInstance.py
#
# Represents Virtual Machine.
# Contains operations related to Virtual Machine.
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


class VMInstance(object):

    """
    Represents Virtual Machine.
    """

    # Get Connection
    def __init__(self, cred_dict, image_id, security_key_name, security_group_name, instance_type):

        """
        Establishes Connection to Eucalyptus cloud. Throws an exception if there is any error in access key or secret key.

        :param cred_dict: Dictionary containing ip_address, access key and secret key of Cloud Infrastructure.
        :param image_id: The ID of the EMI used to launch this instance.
        :param security_key_name: The name of the SSH key associated with the instance.
        :param security_group_name: List of security Groups associated with the instance.
        :param instance_type: The type of instance (e.g. m1.small).
        """

        self._ram_size = -1
        self._disk_size = -1
        self._is_instance_exists = False
        logging.basicConfig(filename='eucalyptus.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
        
        try:
            logging.info('Establishing Connection...')

            self.__conn__ = boto.connect_euca(cred_dict['ip_address'], cred_dict['access_key'], cred_dict['secret_key'])

            logging.info('Connection Established SUCCESSFULLY...')  
            self._create_(image_id, security_key_name, security_group_name, instance_type)

        except:
            logging.error('INVALID Credentials...')
            logging.critical('Connection ABORTED...')
            raise          

    # Create a new VM Instance
    def _create_(self, image_id, security_key_name, security_group_name, instance_type):

        """
        Create a VM instance.

        :param image_id: The ID of the EMI used to launch this instance.
        :param security_key_name: The name of the SSH key associated with the instance.
        :param security_group_name: List of security Groups associated with the instance.
        :param instance_type: The type of instance (e.g. m1.small).
        """  
        count = 0
        try:    
            reservation = self.__conn__.run_instances(image_id=image_id, key_name=security_key_name, security_groups=security_group_name, instance_type=instance_type)
            instance = reservation.instances[0]
            logging.info('Waiting for instance to CREATE...')
            self.instance = instance
            self._is_instance_exists = True         
            logging.info('Instance is in PENDING state...')
            vm_state = self.check_state()   
            if vm_state != 'running':
                print 'Instance creation FAILED'
                logging.info('Instance cretion FAILED...')
                self.destroy()
            else:
                print 'Instance created SUCCESSFULLY'
                logging.info('Instance created SUCCESSFULLY...')
                self.connect_to_vm()
        except:
            logging.error('Instance not CREATED...')
            raise

    # Start a VM Instance
    def start(self):

        """
        Starts the Virual Machine.
        """
        self.validate_vm()

        if self.instance.state == 'running':
            logging.info('%s Instance is already RUNNING', self.instance.id)
        else:
            try:
                logging.info('Waiting for Instance to Start...')
                self.__conn__.start_instances(self.instance.id)
                logging.info('Instance is in PENDING state...')
            except:
                logging.error('Instance not STARTED...')
                raise

    # Stop a VM Instance
    def stop(self):

        """
        Stops the Virtual Machine.
        """
        self.validate_vm()

        if self.instance.state == 'stopped':
            logging.info('%s Instance is already STOPPED', self.instance.id)
        else:
            try:
                logging.info('Waiting for instance to stop...')
                self.__conn__.stop_instances(self.instance.id)   
                logging.info('Instance is in STOPPING state...')
            except:
                logging.error('Instance not STOPPED...')
                raise

    # Restart a VM Instance 
    def restart(self):
        
        """
        Restart the Virtual Machine.
        """
        self.validate_vm()

        if self.instance.state == 'running':
            try:
                logging.info('Waiting for instance to restart...')
                self.__conn__.reboot_instances(self.instance.id)
                logging.info('Instance is in PENDING state...')
            except:
                logging.error('Instance not REBOOTED...') 
                raise  

    # Destroy a VM Instance
    def destroy(self):

        """
        Terminates the Virtual Machine.
        """
        self.validate_vm()

        try:
            logging.info('Waiting for instance to terminate...')
            self.__conn__.terminate_instances(self.instance.id)
            self._is_instance_exists = False
            logging.info('Instance in TERMINATING state...')
        except:
            logging.error('Instance not TERMINATED...')
            raise

    # Gey RAM Size of VM
    def get_ram_size(self):

        """
        Returns the ram size in megabytes for Virtual Machine.
        """
        self.validate_vm()

        if self._ram_size > 0:
            return self._ram_size
        else:
            try:
                instance_info = self.__conn__.get_all_zones('verbose')
                instance = self.__conn__.get_only_instances(self.instance.id)
                instance_type = instance[0].instance_type
                dict = { }  
                for count in instance_info:
                    list = []
                    list.insert(0, count.name)
                    list.insert(1, count.state)
                    spt_str = str(list[0][3:])
                    dict[spt_str] = list[1] 
                flavor = dict[instance_type]
                ram_size = flavor.split()[4]
                self._ram_size = ram_size
                return self._ram_size
                logging.info('Ram Size : %s', self._ram_size)
            except:
                logging.error('Ram Size not RETRIEVED')
                raise

    # Get Disk Size of VM
    def get_disk_size(self):
    
        """
        Returns the disk space in gigabytes for Virtual Machine. 
        """
        self.validate_vm()

        if self._disk_size > 0:
            return self._disk_size
        else:
            try:
                instance_info = self.__conn__.get_all_zones('verbose')
                instance = self.__conn__.get_only_instances(self.instance.id)
                instance_type = instance[0].instance_type
                print type
                dict = { }
                for count in instance_info:
                    list = []
                    list.insert(0, count.name)
                    list.insert(1, count.state)
                    spt_str = str(list[0][3:])
                    dict[spt_str] = list[1]
                flavor = dict[instance_type]
                disk_size = flavor.split()[5]
                self._disk_size = disk_size
                return self._disk_size
                logging.info('Disk Size : %s', self._disk_size)
            except:
                logging.error('Disk Size not RETRIEVED')
                raise   

    # Get VM State
    def get_state(self):

        """
        Returns the current state of Virtual Machine (e.g. running, pending).
        """
        self.validate_vm()

        try:
            self.instance.update()
            logging.info('Instance Status: %s', self.instance.state)
            return self.instance.state
        except:
            logging.error('Instance status not RETREIVED...')
            raise         

    # Get VM IP
    def get_ip(self):

        """
        Returns the IP Address of Virtual Machine.
        """
        self.validate_vm()

        try:
            logging.info('Instance Status: %s', self.instance)
            return self.instance.ip_address
        except:
            logging.error('Instance IP Address not RETREIVED...')
            raise 

    # Check VM State
    def check_state(self):

        """
        
        """
        self.validate_vm()

        count = 0
        while count <= 6:  
            time.sleep(pow(2,count))
            vm_state = self.get_state()
            print vm_state
            count += 1
        return vm_state

    # SSH Connection into VM 
    def connect_to_vm(self):

        """
        Create SSH connection into Virtual Machine and performs operation.
        """
        self.validate_vm()

        key_path = os.path.join(os.path.expanduser('~/Downloads'), 'key1.private')
        print "Key found :", key_path
        logging.info(key_path)
        #instance = __conn__.get_only_instances(self.instance.id)
        cmd = boto.manage.cmdshell.sshclient_from_instance(self.instance, key_path, user_name='ubuntu')
        print cmd
        logging.info(cmd)
        status, stdin, stderr = cmd.run('mkdir VMManager')
        print "Copying VMManager API..."
        cmd.put_file('/home/cloud/VMManager/Logging.py', '/home/ubuntu/VMManager/Logging.py')
        cmd.put_file('/home/cloud/VMManager/LabActionScript.py', '/home/ubuntu/VMManager/LabActionScript.py')
        cmd.put_file('/home/cloud/VMManager/VMManager.py', '/home/ubuntu/VMManager/VMManager.py')
        cmd.put_file('/home/cloud/VMManager/VMManagerServer.py', '/home/ubuntu/VMManager/VMManagerServer.py')
        cmd.put_file('/home/cloud/VMManager/LabActionRunner.py', '/home/ubuntu/VMManager/LabActionRunner.py')
        print "VMManager API copied..."
        #return cmd


    def validate_vm(self):

        """
        Checks whether Instance ID is valid or not.
        """
        try:
            assert(self._is_instance_exists)
        except:
            logging.warning('Instance NOT FOUND')
            raise



