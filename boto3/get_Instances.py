import boto3
from pprint import pprint
from collections import defaultdict
from boto3.session import Session
import csv

with open('aws_instance.csv', 'w') as csvfile:
  fieldnames = ['Name', 'Type', 'State', 'Private_IP', 'Public_IP', 'Launch_Time']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()

def retrieve_running_instances():
	s3 = boto3.resource('s3')
	buckets = s3.buckets.all()
	for bucket in buckets:
		print bucket.name

def retrieve_running_instances1():
	ec2 = boto3.resource('ec2')
	# Get information for all running instances
	running_instances = ec2.instances.filter(Filters=[{
	    'Name': 'instance-state-name',
	    'Values': ['running']}])

	ec2info = defaultdict()

	for instance in running_instances:
		for tag in instance.tags:
			if 'Name' in tag['Key']:
				name = tag['Value']

		ec2info[instance.id] = {
	    	'Name': name,
	    	'Type': instance.instance_type,
	    	'State': instance.state['Name'],
	    	'Private IP': instance.private_ip_address,
	    	'Public IP': instance.public_ip_address,
	    	'Launch Time': instance.launch_time
	    }

	attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time']
	for instance_id, instance in ec2info.items():
		# print ec2info[instance_id]
		# print instance['Name']
		# print instance['Type']
		with open('aws_instance.csv', 'a') as csvfile:
			fieldnames = ['Name', 'Type', 'State', 'Private_IP', 'Public_IP', 'Launch_Time']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writerow({'Name' : instance['Name'], 'Type' : instance['Type'] , 'State' : instance['State'] , 'Private_IP' : instance['Private IP'] , 'Public_IP' : instance['Public IP'] , 'Launch_Time' : instance['Launch Time']})

def main():
	retrieve_running_instances()
	retrieve_running_instances1()

if __name__ == '__main__':
	main()
