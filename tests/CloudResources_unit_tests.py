import os
import boto
import time
from VMInstance import VMInstance
from Image import Image
from CloudResources import CloudResources


cred_dict = {
    "ip_address":"10.2.56.20",
    "access_key":"AKIAYL1OGJDNW3VC3OLU",
    "secret_key":"etGkEl9ipIIay0sLhDqRyZsANGCKFdMzM3FRGSUp"
}

def run_cloud_resources_tests():

    def test_get_image_list():
        try:
            resource = CloudResources(cred_dict)
            assert(resource._ip == cred_dict['ip_address'])
        except:
            print 'Please enter VALID Credentials...'

        try:
            image_list = resource.get_image_list()
            print image_list
        except:
            print 'UNABLE to find images...'


    def test_get_name_specific_image():
        try:
            resource = CloudResources(cred_dict)
            assert(resource._ip == cred_dict['ip_address'])
        except:
            print 'Please enter VALID Credentials...'

        try:
            image_id = resource.get_name_specific_image('ubuntu')
            print image_id
        except:
            print 'UNABLE to find images...'


    def test_get_arch_specific_image():
        try:
            resource = CloudResources(cred_dict)
            assert(resource._ip == cred_dict['ip_address'])
        except:
            print 'Please enter VALID Credentials...'

        try:
            image_list = resource.get_arch_specific_image('x86_64')
            print image_list
        except:
            print 'UNABLE to find images...'

    def test_get_vm_list():
        try:
            resource = CloudResources(cred_dict)
            assert(resource._ip == cred_dict['ip_address'])
        except:
            print 'Please enter VALID Credentials...'

        try:
            vm_list = resource.get_vm_list()
            print vm_list
        except:
            print 'UNABLE to find VM...'

    def test_get_running_vm_list():
        try:
            resource = CloudResources(cred_dict)
            assert(resource._ip == cred_dict['ip_address'])
        except:
            print 'Please enter VALID Credentials...'

        try:
            vm_list = resource.get_running_vm_list()
            print vm_list
        except:
            print 'UNABLE to find VM...'

    def test_resource_utilization():
        try:
            resource = CloudResources(cred_dict)
            assert(resource._ip == cred_dict['ip_address'])
        except:
            print 'Please enter VALID Credentials...'

        try:
            resource.get_resource_utilization('Report.html')
            print 'Save to file Report.html...'
        except:
            print 'UNABLE to calculate Resource Utilization...'

    #test_get_image_list()
    test_get_name_specific_image()
    #test_get_arch_specific_image()
    #test_get_vm_list()
    #test_get_running_vm_list()
    #test_resource_utilization()

run_cloud_resources_tests()
