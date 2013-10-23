# host : webserver1/2/3.sh

BGCOLOR=$(curl http://metadata/0.1/meta-data/attributes/bgcolor)
VER='1.0'

apt-get install -y apache2

cat > /var/www/index.html <<EOF
<html>
 <body bgcolor='$BGCOLOR' >
  <h1>Welcome to $HOSTNAME</h1> 
  <p>Testing Load Balancer with BGCOLOR=$BGCOLOR 'alla vecchia'.</p>
 </body>
</html>
EOF
hostname > /var/www/hostname

chmod 755 /var/www/index.html

# stops apache on www5 to test Load Balancer
if /bin/hostname | grep -q www5 ; then
    touch /root/apache-stopping.touch
    service apache2 stop &&
        touch /root/apache-stopped-ok.touch
fi

touch /root/installed-gclb-addon-v$VER.touch