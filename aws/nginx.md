```sh
cd $HOME
mkdir /nginx

# NJS module
sudo apt  install mercurial -y
hg clone http://hg.nginx.org/njs
cd njs/
./configure
make
cd ..

# NGINX
wget http://nginx.org/download/nginx-1.20.2.tar.gz
tar xf nginx-1.20.2.tar.gz
cd nginx-1.20.2/
sudo apt install build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev -y
./configure --prefix=/nginx --with-http_ssl_module --with-http_auth_request_module --with-pcre --with-http_v2_module --add-module=$HOME/njs/nginx
make 
make install
```
### /lib/systemd/system/nginx.service
```sh
[Unit]
Description=The NGINX server
After=syslog.target network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/nginx/logs/nginx.pid
ExecStartPre=/bin/nginx -t
ExecStart=/bin/nginx
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
