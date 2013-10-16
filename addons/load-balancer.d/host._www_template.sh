#!/bin/bash

VER=1.2

apt-get install -y apache2

#COLOR=$(getmetadata color)
BGCOLOR=$(curl http://metadata/0.1/meta-data/attributes/bgcolor)

echo "<html><body bgcolor='$BGCOLOR' ><h1>Welcome to $HOSTNAME</h1> Try also <a href='index2'.html >index2</a> or  <a href='index3'.html >index3</a> to test Session Affinity." > /var/www/index4.html
echo "<html><h1>Index2 for $HOSTNAME</h1><body bgcolor='$BGCOLOR'> Go back to <a href='/index'.html >index</a>." > /var/www/index2.html
echo "<!doctype html><html><body bgcolor=\"$BGCOLOR\" ><h1>Hello World 3!</h1></body></html>" | sudo tee /var/www/index3.html

cat > /var/www/index.html <<EOF
<!doctype html>
<html>
  <title>Welcome to $HOSTNAME (color $COLOR)</title>
<body bgcolor="$BGCOLOR">

<h1>Welcome to $HOSTNAME</h1> 

Try also the following:

- <a href='index2'.html >index2</a><br/> 
- <a href='index3'.html >index3</a><br/> 
- <a href='index4'.html >index4</a><br/> 
- ... to test Session Affinity.

<hr/><br/><br/>

Installer Version: $VER <br/>
Hostname: $HOSTNAME <br/>
Color: $COLOR (works if the bash is imported correctly, hence "getmetadata")<br/>
BgColor: $BGCOLOR (should just work)<br/>


</body>
</html>
EOF

chmod 755 /var/www/index*html

touch /root/apache-installed-v$VER.touch

