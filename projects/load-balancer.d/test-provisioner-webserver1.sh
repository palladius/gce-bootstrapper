# host.webserver1/2/3.sh

apt-get install -y apache2
echo Welcome to MYNAME > /var/www/index.html
chmod 755 /var/www/index.html