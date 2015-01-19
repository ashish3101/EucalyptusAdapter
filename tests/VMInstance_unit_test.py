import os
import boto
import time
from VMInstance import VMInstance

cred_dict = {
    "ip_address":"10.2.56.20",
    "access_key":"AKIAYL1OGJDNW3VC3OLU",
    "secret_key":"etGkEl9ipIIay0sLhDqRyZsANGCKFdMzM3FRGSUp"
}

def run_instance_tests():

    def test_create_instance():
        try:
            vm_instance = VMInstance(cred_dict, 'ubuntu', 'key1', ['Group1'], 'm1.small')
            #print vm_instance
        except:
            print 'Please enter VALID Credentials...'

        vm_state = vm_instance.check_state()   
        if vm_state != 'running':
        	print 'Instance creation FAILED'
        	vm_instance.destroy()
        else:
            print 'Instance RUNNING...'
            assert(vm_instance.instance.instance_type == 'm1.small')
            vm_instance.destroy()
            print 'Instance TERMINATED...'
            vm_instance.stop()

    def test_stop_instance():
        try:
            vm_instance = VMInstance(cred_dict, 'emi-C65144D4', 'key1', ['Group1'], 'm1.small')
        except:
            print 'Please enter VALID Credentials...'

        try:
            vm_instance.stop()
            print 'Instance STOPPED...'
            assert(vm_instance.instance.instance_type == 'm1.small')
        except:
        	print 'Instance NOT FOUND...'

    def test_start_instance():
        try:
            vm_instance = VMInstance(cred_dict, 'emi-C65144D4', 'key1', ['Group1'], 'm1.small')
        except:
            print 'Please enter VALID Credentials...'

        try:
            vm_instance.start()
            print 'Instance STARTED...'
            assert(vm_instance.instance.instance_type == 'm1.small')
        except:
        	print 'Instance NOT FOUND...'

    def test_restart_instance():
        try:
            vm_instance = VMInstance(cred_dict, 'emi-C65144D4', 'key1', ['Group1'], 'm1.small')
        except:
            print 'Please enter VALID Credentials...'

        try:
            vm_instance.restart()
            print 'Instance RESTARTED...'
            assert(vm_instance.instance.instance_type == 'm1.small')
        except:
        	print 'Instance NOT FOUND...'

    def test_destroy_instance():
        try:
            vm_instance = VMInstance(cred_dict, 'emi-C65144D4', 'key1', ['Group1'], 'm1.small')
        except:
            print 'Please enter VALID Credentials...'

        try:
            vm_instance.destroy()
            print 'Instance TERMINATED...'
        except:
        	print 'Instance NOT FOUND...'

    test_create_instance()
    #test_stop_instance()
    #test_start_instance()
    #test_restart_instance()
    #test_destroy_instance()

run_instance_tests()