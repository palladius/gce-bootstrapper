# host : webserver1/2/3.sh

BGCOLOR="$(curl http://metadata/0.1/meta-data/attributes/bgcolor)"
VER='1.1'

apt-get install -y apache2

cat > /var/www/index.html <<EOF
<html>
 <body bgcolor='$BGCOLOR' >
  <h1>First: $HOSTNAME</h1> 
  <p>Testing Load Balancer simply with BGCOLOR=$BGCOLOR.</p>

  <p>Click on <a href='/index.html'  >index.html</a>.  </p>
  <p>Click on <a href='/index2.html' >index2.html</a>. </p>

 </body>
</html>
EOF

cat /var/www/index.html | sed -e s/First/Second/g > /var/www/index2.html

hostname > /var/www/hostname

chmod 755 /var/www/index.html /var/www/index2.html /var/www/hostname

# stops apache on www5 to test Load Balancer
if /bin/hostname | egrep -q "www5|www1" ; then
    touch /root/apache-stopping.touch
    service apache2 stop && touch /root/apache-stopped-ok.touch
fi

touch /root/installed-gclb-addon-v$VER.touch