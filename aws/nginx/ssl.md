### Create key
```sh
sudo openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout nginx-selfsigned.key -out nginx-selfsigned.crt

Country Name (2 letter code) [AU]:UA
State or Province Name (full name) [Some-State]:Ukraine
Locality Name (eg, city) []:Lviv
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Simple Load Simulator
Organizational Unit Name (eg, section) []:DevOps section
Common Name (e.g. server FQDN or YOUR name) []:simple_load_simulator.org
Email Address []:ihor.prots.lviv@gmail.com





```
