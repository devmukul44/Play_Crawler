import boto3
import os
import time


def create_instances(num_of_instances):

	ec2 = boto3.resource('ec2')
	num_of_instances =1
	print("Do you have Existing Key Pair (y/n) ? ")
	val = raw_input()

	if val =='n':
		key_name = raw_input('Enter key name: ')
		outfile = open(key_name,'w')
		key_pair = ec2.create_key_pair(KeyName = key_name)
		KeyPairOut = str(key_pair.key_material)
		outfile.write(KeyPairOut)
		print outfile
	else:
		key_name = raw_input('Specify the name of already existing key: ')

	#Create Instance
	instances = ec2.create_instances(
		ImageId='ami-b7a114d7',
		MinCount=1,
		MaxCount=num_of_instances,
		KeyName= key_name,
		InstanceType="t2.micro"
	)
	for instance in instances:
		print(instance.id, instance.instance_type)

		name_tag = raw_input('Enter name of the instance: ')
		ec2.create_tags(
			Resources=[instance.id],
            Tags=[{
                "Key":"Name",
                "Value":name_tag
            }]
        )

	instance.wait_until_running()
	instance.load()
	print(instance.public_dns_name)


	public_dns = '"check_dev.pem" ubuntu@' + instance.public_dns_name #ec2-54-202-232-111.us-west-2.compute.amazonaws.com
	to_ssh_temp = "1i ssh -i " + public_dns + " <<ENDOFCOMMANDS"
	to_ssh = '"' + to_ssh_temp + '"'
	print to_ssh
	cmd = ("sed -i %s worker.sh" %to_ssh)
	cmd2 = "sudo ./worker.sh"
	os.system(cmd)
	print ("waiting for instance to initiate...")
	time.sleep(200)
	os.system(cmd2)


def main():
	num_of_instances = 1
	create_instances(num_of_instances)


if __name__ == '__main__':
    main()
