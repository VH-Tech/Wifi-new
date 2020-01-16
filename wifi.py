import socket
from multiprocessing import Pool, Manager
from multiprocessing.dummy import Pool as ThreadPool
from itertools import repeat
import os

aval_ips=[]
pool = ThreadPool()

print("finding router..")
for x in range(2,-1,-1):
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # setting up the default timeout in seconds for new socket object
    socket.setdefaulttimeout(1)
    # returns 0 if connection succeeds else raises error
    try:
        socket_obj.connect(('192.168.' + str(x) + '.1', 8888))

    except ConnectionRefusedError:
        router = x
        break

    except TimeoutError:
        pass


def scan(c,d):
    global aval_ips
    # creates a new socket using the given address family.
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # setting up the default timeout in seconds for new socket object
    socket.setdefaulttimeout(1)
    # returns 0 if connection succeeds else raises error
    try:
        socket_obj.connect(('192.168.'+str(c)+'.' + str(d), 8888))

    except ConnectionRefusedError:
        L.append('192.168.'+str(c)+'.' + str(d))

    except:
        pass

    else:
        L.append('192.168.' + str(c) + '.' + str(d))

    socket_obj.close()


def getMAC(ip):

    host = ip

    # ping is optional (sends a WHO_HAS request)
    os.popen('ping -c 1 %s' % host)

    # grep with a space at the end of IP address to make sure you get a single line
    fields = os.popen('grep "%s " /proc/net/arp' % host).read().split()
    if len(fields) == 6 and fields[3] != "00:00:00:00:00:00":
        return fields[3]


def main():
    global L
    ip = range(0, 256)
    print("Starting Processing..")
    with Manager() as manager:
        L = manager.list()

        with Pool() as pool:
            pool.starmap(scan, zip(repeat(router),ip))

        print("Following people are on your Wi-Fi")
        y = list(L)

        for k in y:
            print('ip: {}, MAC: {}'.format(k,getMAC(k)))

if __name__=="__main__":

    main()
