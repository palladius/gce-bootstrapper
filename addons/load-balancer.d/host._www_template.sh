

apt-get install -y apache2

echo "<h1>Welcome to $HOSTNAME</h1> Try also <a href='index2'.html >index2</a> or  <a href='index3'.html >index3</a> to test Session Affinity." > /var/www/index.htmlnext_trip
echo "<h1>Index2 for $HOSTNAME</h1> Go back to <a href='/index'.html >index</a>." > /var/www/index2.htmlnext_trip
echo '<!doctype html><html><body><h1>Hello World 3!</h1></body></html>' | sudo tee /var/www/index3.html

chmod 755 /var/www/index*html

touch /root/apache-installed.touch

