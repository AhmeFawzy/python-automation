import boto3
import schedule
import time


def check_instance_status():
    # Create EC2 client
    ec2 = boto3.client('ec2')

    # Retrieve all instances
    instances = ec2.describe_instances()

    # Loop through all instances
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            # Get instance ID
            instance_id = instance['InstanceId']

            # Get instance status
            instance_status = ec2.describe_instance_status(InstanceIds=[instance_id])

            print("Instance ID:", instance_id)
            print("Instance State:", instance['State']['Name'])
            print("Instance Status Check:", instance_status['InstanceStatuses'][0]['SystemStatus']['Status'])
            print("-----------------------------")


# Schedule the function to run every 1 minute
schedule.every(5).minutes.do(check_instance_status)

# Infinite loop to run the scheduled functions
while True:
    schedule.run_pending()
    time.sleep(1)
