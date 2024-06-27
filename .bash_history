sudo apt update
sudo apt install unzip curl -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
aws configure
mkdir aws-iac-project
cd aws-iac-project
python -m venv venv
python3 --version
python3 --version
sudo apt update
sudo apt install python3-venv
ls
cd aws-iac-project
python3 --version
python3 -m venv venv
