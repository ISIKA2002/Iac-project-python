### Project: Infrastructure as Code (IaC) for AWS Deployments with Python

This guide will walk you through the steps to create a project that uses Infrastructure as Code (IaC) to automate AWS deployments with Python. We'll use AWS CloudFormation for IaC and set up a CI/CD pipeline with GitHub Actions for automated deployment.

### Prerequisites

1. AWS Account
2. AWS CLI installed and configured
3. Python installed
4. Git installed
5. GitHub account

### Step-by-Step Process

#### 1. Setting Up Your Local Development Environment

**1.1 Install AWS CLI**
   - Follow the official [AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
     or
   - ### Installing AWS CLI on Ubuntu

The AWS Command Line Interface (CLI) is a unified tool to manage your AWS services. Here are the detailed steps to install AWS CLI on an Ubuntu system:

#### Step 1: Update the Package List

It's a good practice to update the package list to ensure you have the latest information about available packages.

```sh
sudo apt update
```

#### Step 2: Install Required Packages

You'll need `unzip` and `curl` to download and extract the AWS CLI package.

```sh
sudo apt install unzip curl -y
```

#### Step 3: Download the AWS CLI Installation Package

Use `curl` to download the AWS CLI installation package from the AWS website.

```sh
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

#### Step 4: Unzip the Package

Extract the downloaded ZIP file.

```sh
unzip awscliv2.zip
```

#### Step 5: Run the Installation Script

Run the installation script to install AWS CLI.

```sh
sudo ./aws/install
```

#### Step 6: Verify the Installation

Check the installed version of AWS CLI to verify that the installation was successful.

```sh
aws --version
```

You should see an output similar to this, confirming the installation:

```
aws-cli/2.7.24 Python/3.8.8 Linux/4.15.0-142-generic exe/x86_64.ubuntu.20
```

#### Step 7: Clean Up

(Optional) Remove the downloaded ZIP file and the extracted directory to clean up.

```sh
rm -rf awscliv2.zip aws
```

### Summary

You have now installed the AWS CLI on your Ubuntu system. The AWS CLI is ready to use for managing your AWS services. Remember to configure the CLI with your AWS credentials by running `aws configure`:

```sh
aws configure
```

You'll be prompted to enter your AWS Access Key ID, Secret Access Key, default region, and output format.

**1.2 Configure AWS CLI**
   - Run `aws configure` and enter your AWS credentials.
     ```sh
     aws configure
     ```

**1.3 Set Up Project Directory**
   - Create a project directory and navigate into it.
     ```sh
     mkdir aws-iac-project
     cd aws-iac-project
     ```

**1.4 Set Up a Virtual Environment**
   - Create and activate a Python virtual environment.
     ```sh
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

#### 2. Writing Infrastructure as Code with AWS CloudFormation

**2.1 Create a CloudFormation Template**
   - Create a directory for your CloudFormation templates and add a basic template.
     ```sh
     mkdir cloudformation
     touch cloudformation/main.yaml
     ```

   - Add the following content to `cloudformation/main.yaml` to create a VPC, Subnets, and an EC2 instance:
     ```yaml
     AWSTemplateFormatVersion: '2010-09-09'
     Description: AWS Infrastructure as Code Project

     Resources:
       MyVPC:
         Type: AWS::EC2::VPC
         Properties:
           CidrBlock: 10.0.0.0/16
           EnableDnsSupport: true
           EnableDnsHostnames: true

       PublicSubnet:
         Type: AWS::EC2::Subnet
         Properties:
           VpcId: !Ref MyVPC
           CidrBlock: 10.0.1.0/24
           MapPublicIpOnLaunch: true

       MyEC2Instance:
         Type: AWS::EC2::Instance
         Properties:
           InstanceType: t2.micro
           ImageId: ami-0c55b159cbfafe1f0  # Amazon Linux 2 AMI
           SubnetId: !Ref PublicSubnet
           KeyName: my-key-pair
     ```

**2.2 Create a Python Script for Deployment**
   - Create a script to deploy the CloudFormation stack using the AWS SDK for Python (Boto3).
     ```sh
     touch deploy.py
     ```

   - Add the following content to `deploy.py`:
     ```python
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
     ```

**2.3 Install Boto3**
   - Install Boto3 in your virtual environment.
     ```sh
     pip install boto3
     ```

#### 3. Version Control with GitHub

**3.1 Initialize Git Repository**
   - Initialize a git repository in your project directory.
     ```sh
     git init
     ```

**3.2 Create `.gitignore`**
   - Create a `.gitignore` file to exclude unnecessary files.
     ```sh
     touch .gitignore
     echo "venv/" >> .gitignore
     echo "*.pyc" >> .gitignore
     echo "__pycache__/" >> .gitignore
     ```

**3.3 Commit Code**
   - Commit your code to the repository.
     ```sh
     git add .
     git commit -m "Initial commit"
     ```

**3.4 Push to GitHub**
   - Create a new repository on GitHub and push your code.
     ```sh
     git remote add origin https://github.com/your-username/aws-iac-project.git
     git branch -M main
     git push -u origin main
     ```

#### 4. Setting Up CI/CD Pipeline with GitHub Actions

**4.1 Create GitHub Actions Workflow**
   - Create a directory for GitHub Actions workflows.
     ```sh
     mkdir -p .github/workflows
     touch .github/workflows/deploy.yml
     ```

**4.2 Define the Workflow**
   - Add the following content to `deploy.yml` to define the deployment pipeline:
     ```yaml
     name: Deploy Infrastructure

     on:
       push:
         branches:
           - main

     jobs:
       deploy:
         runs-on: ubuntu-latest

         steps:
           - name: Checkout code
             uses: actions/checkout@v2

           - name: Set up Python
             uses: actions/setup-python@v2
             with:
               python-version: '3.x'

           - name: Install dependencies
             run: |
               python -m venv venv
               source venv/bin/activate
               pip install boto3

           - name: Configure AWS credentials
             uses: aws-actions/configure-aws-credentials@v1
             with:
               aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
               aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
               aws-region: us-east-1

           - name: Deploy CloudFormation stack
             run: |
               source venv/bin/activate
               python deploy.py
     ```

**4.3 Configure GitHub Secrets**
   - Go to your GitHub repository settings and configure the following secrets:
     - `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
     - `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.

**4.4 Push Changes to GitHub**
   - Commit and push the workflow file to trigger the pipeline.
     ```sh
     git add .github/workflows/deploy.yml
     git commit -m "Add GitHub Actions workflow for deployment"
     git push
     ```

### Summary

By following these steps, you have set up an automated deployment pipeline for AWS infrastructure using Python and Infrastructure as Code (IaC) principles. You can now manage and deploy AWS resources in a consistent and automated manner, ensuring that your infrastructure is versioned, repeatable, and reliable.

**Architecture Diagram**





                              +-----------------------+
                              |      Developer        |
                              |      Workstation      |
                              +-----------+-----------+
                                          |
                                          | Python Code (IaC scripts)
                                          |
                              +-----------v-----------+
                              |        IDE/Editor     |
                              +-----------+-----------+
                                          |
                                          |
                              +-----------v-----------+
                              |     Version Control   |
                              |      (GitHub/GitLab)  |
                              +-----------+-----------+
                                          |
                                          | git push
                                          |
                              +-----------v-----------+
                              |  CI/CD Pipeline       |
                              | (e.g., Jenkins, GitHub|
                              |  Actions, GitLab CI)  |
                              +-----------+-----------+
                                          |
                                          | Deploy IaC Scripts
                                          |
                              +-----------v-----------+
                              |     AWS CloudFormation|
                              |        (or Terraform) |
                              +-----------+-----------+
                                          |
                                          |
                                          |
    +-------------------------------------v-----------------------------------+
    |                               AWS Account                              |
    |                                                                         |
    | +-------------------+      +-----------------+      +-----------------+ |
    | |   Networking      |      |   Compute       |      |   Storage       | |
    | |   (VPC, Subnets,  |      |   (EC2, Lambda) |      |   (S3, EBS)     | |
    | |   Route Tables)   |      +-----------------+      +-----------------+ |
    | +-------------------+                                                | |
    |                                                                         |
    | +---------------------+   +-----------------+     +------------------+  |
    | |  Database Services  |   |  Security       |     |  Monitoring      |  |
    | |  (RDS, DynamoDB)    |   |  (IAM, Security |     |  (CloudWatch,    |  |
    | |                     |   |   Groups,       |     |   CloudTrail)    |  |
    | +---------------------+   |   Policies)     |     +------------------+  |
    |                           +-----------------+                            |
    +-------------------------------------------------------------------------+

