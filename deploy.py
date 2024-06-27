import boto3
import time

def deploy_stack(stack_name, template_file):
    with open(template_file, 'r') as file:
        template_body = file.read()

    client = boto3.client('cloudformation')
    response = client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_IAM']
    )

    waiter = client.get_waiter('stack_create_complete')
    waiter.wait(StackName=stack_name)

    print(f"Stack {stack_name} created successfully.")

if __name__ == '__main__':
    deploy_stack('my-iac-stack', 'cloudformation/main.yaml')
