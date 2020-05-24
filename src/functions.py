import json
from requests import get
import psutil
from datetime import datetime
from os import system, name, getcwd, mkdir
from random import choice, randint
from time import sleep

#INCLUDES
from config import config, glbls

def trueTLD(url):
    replaces = ["https", "http", ":","'", "\"", "www."]
    for x in range(len(replaces)):
        out = url.replace(replaces[x], "")
    try:out = out.split("//")[1]
    except: pass
    out = out.split("/")[0].split("?")[0]
    return out

def TLDtoUid(tld):
    reps = [".", "-", ""]
    for x in range(len(reps)):
        uid = tld.replace(reps[x], "")
    return uid

def load_proxies(http_proxy_file, ssl_proxy_file, verbose):
    with open(http_proxy_file,"r") as d:
        glbls.http_proxies = d.read().split('\n')
        if verbose:
            #print(str(glbls.http_proxies))
            print(f"\n\n\n[LOGGING]: [HTTP Proxies Loaded!] - [File: {http_proxy_file} / Amount: {len(glbls.http_proxies)}]")
    with open(ssl_proxy_file,"r") as d:
        glbls.ssl_proxies = d.read().split('\n')
        if verbose:
            #print(str(glbls.ssl_proxies))
            print(f"\n\n\n[LOGGING]: [SSL Proxies Loaded!] - [File: {ssl_proxy_file} / Amount: {len(glbls.ssl_proxies)}]\n\n")

class version:
    version = "1.0.0.1"
    start_time = str(datetime.now())
    

def get_good_proxy(url, verbose):
    if "https" in url:
        src = glbls.ssl_proxies
    else:
        src = glbls.http_proxies
        
    for x in range(0, len(src)):
        t = src[x]
        p={}
        if "https" in url:
            prefix = "http://" # <problem1> Might not work with universal "http"
        else:
            prefix = "http://"
        p['http'] = prefix + t
        p['https'] = prefix + t
        if verbose:
            print(f"\n\n\n[LOGGING]: [Testing Proxy: {p}...]")
            
        # Quality Checks
        if x == (len(src) / 2):
            if verbose:
                clear()
                print("\n\n[Warning]: Failed To Find ANY Good Proxies after testing 50% of list!!!")
        
        if x == len(src):
            if verbose:
                clear()
                print("\n\n[FATAL ERROR]: [Reached End Of List But Failed To Find Good Proxy!!!]")
                
            good_proxy = None
            break
        
        try:
            
            r = get("https://google.com/", headers=get_headers(), proxies=p, timeout=glbls.proxy_timeout_seconds)
            good_proxy = t
            glbls.proxy_in_use = t
            break
        
        except Exception as e:
            print(f"[Proxy: {str(p)}] [Bad Proxy] [{str(e)}]")
            if "https" in url:
                del glbls.ssl_proxies[x]
            else:
                del glbls.http_proxies[x]
            pass
            
    return good_proxy        
                
                
        
    
    
#proxytypes: http = 0;socks5 >= 1
def anon_request(url, verbose):
    proxies = {}
    proxy = get_good_proxy(url, verbose)
    proxies['http'] = proxy
    proxies['https'] = proxy
    r = get(
        url, 
        headers = get_headers(),
        proxies = proxies
        )
    
    ## APPEND USED LINKS TO DROP LIST
    glbls.drop_expressions.append(url)
    return r

def direct_request(url, verbose):
    r = get(
        url, 
        headers = get_headers()
        )
    
    ## APPEND USED LINKS TO DROP LIST
    glbls.drop_expressions.append(url)
    return r    



def get_headers():
    useragents = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/57.0.2987.110 '
        'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.79 '
        'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
        'Gecko/20100101 '
        'Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.91 '
        'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/62.0.3202.89 '
        'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/63.0.3239.108 '
        'Safari/537.36'),  # chrome
    ]
    user_agent = choice(useragents)
    headers = {'User-Agent' : user_agent}
    return headers

def log(info):
    with open("{getcwd()}/log/log.txt", "w+") as log:
        log.write(f"\n[{str(datetime.now)}] - {info}")

def log_error(info):
    with open(f"{getcwd()}/log/error.txt", "w+") as log:
        log.write(f"\n[{str(datetime.now)}] - {info}")
    
def clear():
    if name == 'nt': _ = system('cls')
    else: _ = system('clear')

def get_cpu():
    return f"{psutil.cpu_percent(interval=None)}%"

def get_ram():
    return f"{psutil.virtual_memory().percent}%"    

def unique_id():
    idu = str(randint(1000, 9999))
    ida = str()
    try:
        with open("crypto.dat", "r") as this:
            historical_crypto = this.read().splitlines()
    except:
        with open("crypto.dat", "w+") as fp:
            fp.close()
        with open("crypto.dat", "r") as this:
            historical_crypto = this.read().splitlines()
            
    for c in range(0, len(historical_crypto)):
        if idu in historical_crypto[c]:
            ida = unique_id()
            break
        else: ida = idu
    with open("crypto.dat", "a") as d:
        d.write("\r\n" + idu)
    return ida   
    
