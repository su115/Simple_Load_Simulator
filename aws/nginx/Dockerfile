FROM ubuntu
WORKDIR "/workdir/"
RUN apt update && apt install build-essential mercurial libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev wget -y
RUN wget http://nginx.org/download/nginx-1.20.2.tar.gz
RUN tar xf nginx-1.20.2.tar.gz
RUN mkdir /nginx && hg clone http://hg.nginx.org/njs
#RUN ls -al
WORKDIR "/workdir/njs/"
RUN ./configure && make

WORKDIR "/workdir/nginx-1.20.2/"
RUN ./configure --prefix=/nginx --with-http_ssl_module --with-http_auth_request_module --with-pcre --with-http_v2_module --add-module=/workdir/njs/nginx 

RUN  make && make install
RUN  mv /nginx/sbin/nginx /bin/
COPY nginx.conf  /nginx/conf/nginx.conf
COPY headers.js  /nginx/conf/headers.js
COPY ssl/nginx.crt  /nginx/conf/ssl/nginx-selfsigned.crt
COPY ssl/nginx.key  /nginx/conf/ssl/nginx-selfsigned.key
#COPY nginx.service  /lib/systemd/system/nginx.service
EXPOSE 80
EXPOSE 443
EXPOSE 444
RUN nginx -t #&&  systemctl enable nginx.service &&  systemctl start nginx.service
CMD ["nginx", "-g", "daemon off;"]
