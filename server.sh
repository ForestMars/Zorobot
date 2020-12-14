# server.sh - bare bones install script for running zorobot on bare metal (ie. w/o docker/k8s)

sudo apt update
sudo apt install python3-dev python3-pip nginx
cp docker/bot/files/zorobot /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/zorobot /etc/nginx/sites-enabled
python3 app.py &
sudo systemctl restart nginx
