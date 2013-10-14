# host.webserver1/2/3.sh

apt-get install -y apache2
echo "<h1>Welcome to $HOSTNAME</h1> Testing Load Balancer" > /var/www/index.html
chmod 755 /var/www/index.html