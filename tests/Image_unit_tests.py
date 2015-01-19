import os
import boto
import time
from Image import Image

cred_dict = {
    "ip_address":"10.2.56.20",
    "access_key":"AKIAYL1OGJDNW3VC3OLU",
    "secret_key":"etGkEl9ipIIay0sLhDqRyZsANGCKFdMzM3FRGSUp"
}

def run_image_tests():

    def test_create_image():
        try:
            image = Image(cred_dict, 'precise', '/home/cloud/Downloads/precise-server-cloudimg-amd64.img', 'x86_64')
            print image.__dict__
            assert(image.name == 'precise')
        except:
            print 'Image not created'

        try:
        	image.delete()
        	print 'Image DELETED...'
        except:
        	print 'Image not DELETED...'

    def test_delete_image():
    	try:
            image = Image(cred_dict, 'precise', '/home/cloud/Downloads/precise-server-cloudimg-amd64.img', 'x86_64')
            assert(image.name == 'precise')
        except:
            print 'Image not created...'

        try:
        	image.delete()
        	print 'Image DELETED...'
        except:
        	print 'Image not DELETED...'

    test_create_image()
    #test_delete_image()

run_image_tests()
