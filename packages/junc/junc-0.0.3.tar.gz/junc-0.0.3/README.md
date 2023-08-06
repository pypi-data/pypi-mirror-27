# Junc (Short for Junction)
## SSH to servers easily
```bash
# Connect to a raspberry pi
$ junc connect my_rpi
# Connect to an AWS EC2
$ junc connect my_ec2

# Connect to anything with an ip
```

## Usage
```bash
# Add a server
$ junc add [server_name] [username]@[ip]
# OR
$ junc add
Name: [server_name]
Username: [username]
IP: [ip]

# See all your servers
$ junc list
# TODO: Add a server table here

$ junc connect [server_name]
Connecting...
# OR
$ junc connect
Name: [server_name]
Connecting...
```

