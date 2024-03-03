aerich:
aerich init -t app.aerich.base.config  

RUN in EC2
sudo yum install git -y
git clone https://github.com/Sergey582/investment_tracking_bot.git
sudo yum install docker -y
sudo service docker start
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
cd investment_tracking_bot/
sudo docker-compose up --build