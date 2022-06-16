# Simple TCP-proxy

## Usage:
 `./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]`

## Example:

```shell
    #first console window
    sudo python proxy.py 127.0.0.1 21 ftp.sun.ac.za 21 True
    #outher console window
    ftp 127.0.0.1
```

## Output:

```shell
    [*] Listening on 127.0.0.1:21
    > Received incoming connection from 127.0.0.1:57978
    0000 50:02X 50:02X 48:02X 32:02X 87:02X 101:02X 108:02X 99:02X 111:02X 109:02X 101:02X 32:02X 116:02X 111:02X 32:02X 102:02X 220 Welcome to f
    0010 116:02X 112:02X 46:02X 115:02X 117:02X 110:02X 46:02X 97:02X 99:02X 46:02X 122:02X 97:02X 13:02X 10:02X tp.sun.ac.za..
    [<==] Sending 30 bytes to localhost.
    [*] No more data. Closing connections.

```