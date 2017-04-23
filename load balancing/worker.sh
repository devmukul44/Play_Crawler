ssh -i check_dev.pem ubuntu@ec2-54-213-19-241.us-west-2.compute.amazonaws.com <<ENDOFCOMMANDS
sudo apt-get update
sudo apt-get install python -y
sudo apt-get install python-mysql.connector
sudo apt-get install python-pip -y
sudo pip install configparser
sudo pip install beautifulsoup4
git clone https://github.com/devmukul44/Play_Crawler.git
cd Play_Crawler/cloud/
echo "starting scraper...."
python scraper1.py
<< ENDOFCOMMANDS
