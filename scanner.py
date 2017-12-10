import optparse
from socket import *
from threading import *
screenLock=Semaphore(value=1)
def connScan(tgtHost,tgtPort):
    try:
        connSkt=socket(AF_INET,SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))
        connSkt.send('Hi!')
        result=connSkt.recv(100)
        screenLock.acquire()
        print('[+]%d/tcp open' %tgtPort)
        print('[+]'+str(result))
    except:
        screenLock.acquire()
        print('[+]%d/tcp closed' % tgtPort)
    finally:
        screenLock.release()
        connSkt.close()
def portScann(tgtHost,tgtPort):
    try:
        tgtIP=gethostbyname(tgtHost)
    except:
        print('[-] Cannot resolve %s' %tgtHost)
        return
    try:
        tgtName=gethostbyaddr(tgtIP)
        print('\n[+] Scan results for :'+tgtName[0])
    except:
        print('\n[+] Scan results for :'+tgtIP)
    setdefaulttimeout(1)
    for Port in tgtPort:
        t=Thread(target=connScan,args=(tgtHost,int(Port)))
        t.start()
def main():
    parser=optparse.OptionParser('Usage %prog'+'-H <targetHost> -p <taregt port>')
    parser.add_option('-H',dest='tgtHost',type='string',help='specify target host')
    parser.add_option('-p',dest='tgtPort',type='string',help='specify target port[s] separated by comma')
    (options,args)=parser.parse_args()
    tgtHost=options.tgtHost
    tgtPort=str(options.tgtPort).split(',')
    if (tgtHost==None)| (tgtPort[0]==None):
        print(parser.usage)
        exit(0)
    portScann(tgtHost,tgtPort)

if __name__=="__main__":
    main()