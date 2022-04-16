# (install)[https://www.digitalocean.com/community/tutorials/how-to-set-up-dante-proxy-on-ubuntu-20-04]
```sh
sudo apt update
sudo apt install dante-server

sudo nano /etc/danted.conf
```
### /etc/danted.conf
```
logoutput: syslog
user.privileged: root
user.unprivileged: nobody

# The listening network interface or address.
internal: 0.0.0.0 port=1080

# The proxying network interface or address.
external: eth0

# socks-rules determine what is proxied through the external interface.
socksmethod: username

# client-rules determine who can connect to the internal interface.
clientmethod: none

client pass {
    from: 0.0.0.0/0 to: 0.0.0.0/0
#   from: your_ip_address/0 to: 0.0.0.0/0

}

socks pass {
    from: 0.0.0.0/0 to: 0.0.0.0/0
}
```
## __Bash__
```sh
sudo useradd -r -s /bin/false your_dante_user
sudo passwd your_dante_user

sudo systemctl restart danted.service
```
## __Test connection__
```sh
curl -v -x socks5://your_dante_user:your_dante_password@your_server_ip:1080 http://www.google.com/
```

