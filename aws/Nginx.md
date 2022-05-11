wget http://nginx.org/download/nginx-1.20.2.tar.gz

tar xf nginx-1.20.2.tar.gz

sudo apt install build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev -y
sudo mkdir /nginx
sudo apt  install mercurial -y
hg clone http://hg.nginx.org/njs

# inside njs
cd njs/
./configure
make

# inside nginx
cd ../nginx-1.20.2/
./configure --prefix=/nginx --with-http_ssl_module --with-http_auth_request_module --with-pcre --with-http_v2_module --add-module=$HOME/njs/nginx

make
sudo make install

sudo mv /nginx/sbin/nginx /bin/

sudo nginx -t
/nginx/conf/nginx.conf
/nginx/conf/headers.js
/nginx/conf/ssl/nginx-selfsigned.crt
/nginx/conf/ssl/nginx-selfsigned.key
/lib/systemd/system/nginx.service

sudo systemctl enable nginx.service
sudo systemctl start nginx.service
