import urllib.request

url='https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts'
path='C:\Windows\System32\drivers\etc\hosts'
host=urllib.request.urlopen(url)
with open(path,'w') as f:
    content = host.read().decode()
    if content:
        f.write(content)
        print("Complete!")
    else:
        print("Get host failed!")
    f.close()