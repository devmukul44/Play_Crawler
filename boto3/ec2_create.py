import boto3
import sys
import os

def create_instances():

	ec2 = boto3.resource('ec2')
	# key_name = raw_input('Enter key name: ')
	# outfile = open(key_name,'wb')
	# key_pair = ec2.create_key_pair(KeyName = key_name)
	# KeyPairOut = str(key_pair.key_material)
	# outfile.write(KeyPairOut)
	# print outfile
	#Create Instance
	instances = ec2.create_instances(
		ImageId='ami-1e299d7e',
		MinCount=1,
		MaxCount=1,
		KeyName= 'check_dev',
		InstanceType="t2.micro"
	)
	print(instances.id, instances.instance_type)
	# ids = ['i-0459d981ad244f921']
	# ec2.instances.filter(InstanceIds=ids).stop()
	# ec2.instances.filter(InstanceIds=ids).terminate()


def main():
	create_instances()


if __name__ == '__main__':
    main()
