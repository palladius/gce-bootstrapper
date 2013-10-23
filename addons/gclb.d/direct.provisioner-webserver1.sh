# host : webserver1/2/3.sh

BGCOLOR=$(curl http://metadata/0.1/meta-data/attributes/bgcolor)

apt-get install -y apache2

cat > /var/www/index.html <<EOF
<html>
 <body bgcolor='$BGCOLOR' >

  <h1>Welcome to $HOSTNAME</h1> 

  Testing Load Balancer with BGCOLOR=$BGCOLOR 'alla vecchia'.

EOF
chmod 755 /var/www/index.html

if /bin/hostname | grep -q www5 ; then
    touch /root/apache-stopping.touch
    service apache2 stop &&
        touch /root/apache-stopped-ok.touch
fi
