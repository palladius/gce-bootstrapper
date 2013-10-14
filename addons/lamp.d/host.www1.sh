


apt-get install -y apache2

echo '<!doctype html><html><body><h1>Hello World!</h1> Im an apache server</body></html>' | sudo tee /var/www/index.html
chmod 755 /var/www/index*html

touch /root/apache-installed.touch

