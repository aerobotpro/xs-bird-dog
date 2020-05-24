
#Todos:
# Download fresh proxies at every startup from proxyscrape!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Get latency for all requests
# Add discord notify
import json
from requests import get
import psutil
from datetime import datetime
from os import system, name, getcwd, mkdir
from random import choice, randint
from time import sleep
from config import config, glbls
#import threading
from tkinter import END

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")



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
    version = "1.0.0.0"
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

#Data handling
def global_pool_update(current_index):
    this = dict()
    this['potential_index'] = int(current_index)
    this['current_pool_len'] = len(glbls.pool)
    this['potential_difference'] = len(glbls.pool) - int(current_index)
    this['last_index'] = glbls.last_index
    this['last_pool_len'] = glbls.last_pool_len
    this['last_difference'] = int(glbls.last_pool_len - glbls.last_index)
    glbls.current_index_data = this

def index_data(tld, verbose, B_use_proxies):
    #Overall Allocations
    page_data = dict()
    index_data = 0
    #Make Initial Contant With Index. (hopefully)
    try:
        if B_use_proxies: r = anon_request(f"http://{tld}/", verbose)
        else: r = direct_request(f"http://{tld}/", verbose)
    except Exception as d:
        log_error(d)
        if verbose:
            print(d)
        try:
            if B_use_proxies: r = anon_request(f"https://{tld}/", verbose)
            else: r = direct_request(f"https://{tld}/", verbose)
        except Exception as e:
            log_error(e)
            if verbose:
                print(e)
            index_data = None
            pass

    #Vitals
    cpu = get_cpu()
    ram = get_ram()
    t_stamp = str(datetime.now())

    #Verbose - Notify Finished Index.
    if verbose:
        print(f"[{t_stamp}] - Finished Indexing index@{tld}\n[Vitals]: CPU: {cpu} | MEMORY: {ram}")

    #Success - Check Index
    if index_data is not None:
        
        #split page lines
        shred = r.text.split('\n')

        #Nested Allocations For New Links
        internal_links = []
        external_links = []
        
        for x in range(0, len(shred)):
            #Scout New Links
            if "https://" in shred[x] or "http://" in shred[x]:
                
                url = "http" + str(shred[x].split('http')[1].split('"')[0])
                
                if tld in url:
                    if any(word in url for word in glbls.drop_expressions):
                        pass
                    else:
                        internal_links.append(url)
                        if verbose:
                            try:
                                print(f"[SEED URL] - Found Internal Link @Index: {url}")
                            except Exception as D:
                                print(f"Warning: {str(D)}")
                                
                else:
                    if any(word in url for word in glbls.drop_expressions):
                        pass
                    else:
                        external_links.append(url)
                        if verbose:
                            try:
                                print(f"[SEED_URL] - Found External Link @Index: {url}")
                            except Exception as D:
                                print(f"Warning: {str(D)}")
                        
        links = dict()
        links['internal'] = internal_links
        links['external'] = external_links

        #Push BOTH lists of links to BOTTOM of global pool
        glbls.pool = internal_links + external_links
        #print(glbls.pool)

        #Push this to page_data
        page_data['url'] = "index@" + tld
        page_data['links_count'] = int(len(links['internal']) + len(links['external']))
        page_data['links'] = links
        page_data['page_len'] = len(r.text)
        page_data['text'] = r.text
        page_data['headers'] = json.dumps(dict(r.headers))
        page_data['code'] = r.status_code
        page_data['cpu'] = cpu
        page_data['ram'] = ram
        page_data['proxy'] = glbls.proxy_in_use
        page_data['time_stamp'] = t_stamp

    #if timeout etc..
        #Push this to page_data
    else:
        page_data['url'] = "index@" + tld
        page_data['links_count'] = 0
        page_data['links'] = {'internal': [], 'external': []}
        page_data['page_len'] = 0
        page_data['text'] = None
        page_data['code'] = None
        page_data['cpu'] = cpu
        page_data['ram'] = ram
        page_data['proxy'] = glbls.proxy_in_use
        page_data['time_stamp'] = t_stamp
    return page_data





# Essentially for every page besides initial index *
def new_data(new_url, tld, verbose, B_use_proxies):
    index_data = 0
    #Overall Allocations
    page_data = dict()

    #Make Initial Contant With Index. (hopefully)
    try:
        if B_use_proxies: r = anon_request(new_url, verbose)
        else: r = direct_request(new_url, verbose)
        
    except Exception as d:
        log_error(d)
        index_data = None
        pass

    #Vitals
    cpu = get_cpu()
    ram = get_ram()
    t_stamp = str(datetime.now())

    #Success - Check Index
    if index_data is not None:
        
        #split page lines
        shred = r.text.split('\n')

        #Nested Allocations For New Links
        internal_links = []
        external_links = []
        
        for x in range(0, len(shred)):
            #Scout New Links
            if "https://" in shred[x] or "http://" in shred[x]:
                url = "http" + str(shred[x].split('http')[1].split('"')[0])
                if tld in url:
                    if any(word in url for word in glbls.drop_expressions):
                        pass
                    else:
                        internal_links.append(url)
                        if verbose:
                            try:
                                print(f"[{new_url}] - Found Internal Link: {url}")
                            except Exception as D:
                                print(f"Warning: {str(D)}")

                else:
                    if any(word in url for word in glbls.drop_expressions):
                        pass
                    else:
                        external_links.append(url)
                        if verbose:
                            try:
                                print(f"[{new_url}] - Found Internal Link: {url}")
                            except Exception as E:
                                print(f"Warning: {str(E)}")

                if any(word in new_url for word in glbls.sought_expressions):
                    with open(f"{glbls.data_dir}/{glbls.sesh_id}_hits.dat", "a+") as ddd:
                        ddd.write(
                            f"""
            ---------------------
            Found {new_url} @ {url}

            CPU: {get_cpu()}

            RAM: {get_ram()}

            TIME: {str(datetime.now())}
            ---------------------

            
            """
                            )                
                                            
    
        links = dict()
        links['internal'] = internal_links
        links['external'] = external_links
        

        #Push BOTH lists of links to BOTTOM of global pool
        glbls.pool = list(list(glbls.pool) + list(internal_links) + list(external_links))

        #Push this to page_data
        page_data['url'] = new_url
        page_data['links_count'] = int(len(links['internal']) + len(links['external']))
        page_data['links'] = links
        page_data['page_len'] = len(r.text)
        page_data['text'] = r.text
        page_data['headers'] = json.dumps(dict(r.headers))
        page_data['code'] = r.status_code
        page_data['cpu'] = cpu
        page_data['ram'] = ram
        page_data['proxy'] = glbls.proxy_in_use
        page_data['time_stamp'] = t_stamp

    #if timeout etc..
        #Push this to page_data
    else:
        page_data['url'] = new_url
        page_data['links_count'] = 0
        page_data['links'] = {'internal': [], 'external': []}
        page_data['page_len'] = 0
        page_data['text'] = None
        page_data['code'] = "*4xx/5xx [Failed] "
        page_data['cpu'] = cpu
        page_data['ram'] = ram
        page_data['proxy'] = glbls.proxy_in_use
        page_data['time_stamp'] = t_stamp        
        

    return page_data
       

def flex(tld, usagetype, B_verbose, B_use_proxies):
    for x in range(0, len(glbls.pool)):
        glbls.tmp.append(
            new_data(
                glbls.pool[x],
                tld,
                B_verbose,
                B_use_proxies
                )
            )

def unique_id():
    ## Chances are (1 in 8999 *)^2 of non-unique id, still not good enough to be "cryptographic" - needs work
    idu = str(randint(1000, 9999))
    ida = str() #Best Chance Value
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
    

#Main
class void:
    class crawler:
        def __init__(self, tld, usagetype, generations, B_verbose=True, B_use_proxies=False, http_proxy_file_name=None, ssl_proxy_file_name=None):

            ##USAGE SCHEMA:
            #if usagetype == 0:
            #    internal_only = True
            #else:
            #    internal_only = False

            if B_use_proxies:
                #Load Proxies
                load_proxies(http_proxy_file_name, ssl_proxy_file_name, B_verbose)
                if B_verbose:
                    print("Proxies Loaded!")
                
            #Check for user entering a url not a tld
            glbls.tld = tld.replace("http", "").replace("//", "").split("/")[0].replace("/", "")
            if B_verbose:
                print("Top Level Domain Validated!")        
            

            #
            glbls.sesh_id = tld.replace(".", "-") + "_" + unique_id()
            if B_verbose:
                print(f"Session ID: {glbls.sesh_id}")        


            glbls.data_dir = str(getcwd() + f"\\data\\saves\\{glbls.sesh_id}")
            if B_verbose:
                print("Saving To: " + glbls.data_dir)         

            #MAKE THE NEW DATA DIR
            try:
                mkdir(glbls.data_dir)
            except Exception as F:
                xxy = input("Failed to create directory: " + str(F))
                exit()

            if B_verbose:
                tstat = 5
                for _ in range(0, tstat):
                    print(f"Runtime Environment Created - Beginning Session in {tstat} Seconds...\r")
                    sleep(1)
                    tstat -= 1
                

            #Master Stack
            master_data = []

            # First is always index page then so on and so on...
            master_data.append(index_data(tld, B_verbose, B_use_proxies))

            #Pass master_data to temporary global scope.
            glbls.tmp = master_data

            #Main Worker Loop
            for x in range(0, generations):

                #LOOP THROUGH GENERATIONS. 
                flex(tld, usagetype, B_verbose, B_use_proxies)

                #SAVES OUR PROGRESS - Dumps To JSON. 
                try:
                    file = f"{glbls.data_dir}/" + tld.replace(".", "_").replace("/", "-") + f"gen_{x}.json"
                    with open(file, 'w+') as f: json.dump(list(glbls.tmp), f)
                except Exception as Dd:
                    print(str(Dd))
                    if B_verbose: xx = input("Hit enter to continue...")
                    pass
                
                stat = 5    
                for _ in range(0, 5):
                    print(f"Completed Generation {x}/{generations} | json file saved as {file}!\n\nSleeping for {stat} seconds\r")
                    stat -= 1
                    sleep(1)
                    
                

            #End Of Session, Reguardless Of Performance. 
            #Pass Main Data Back To Local Scope, Session Is Done.     
            master_data = glbls.tmp
            
            #Explicit Decl. For later use mabye. idk. 
            self.master = master_data

            

            #Dump master
            #file = f'final-{str(randint(1111, 9999))}{tld}.json'
            #with open(file, 'w+') as f:
            #    json.dump(self.master, f)
            
            #Lets See How We Did! > Only uncomment below if you've done less than two scrapes else you'll crash any shell! ****
                
            #self.table = draw_table(self.master)
            #print(str(self.table))


            #messagebox.askquestion(title="Complete!", message="Would you like to start another session?")
            
    




### THE JUNKYARD


#def draw_table(data):
#    table = PrettyTable()
    
#    table.field_names = [
#        "URL", "Status Code", "Page Len", "Internal Links", "External Links","CPU", "RAM", "Proxy", "Time"
#        ]
#    for x in range(0, len(data)):
#        links = data[x]['links']
#        try:
#            internal_len = len(links['internal'])
#            external_len = len(links['external'])
#        except:
#            internal_len = 0
#            external_len = 0
#        table.add_row([
#            data[x]['url'],
#            data[x]['code'],
#            data[x]['page_len'],
#            internal_len,
#            external_len,
#            data[x]['cpu'],
#            data[x]['ram'],
#            data[x]['proxy'],
#            data[x]['time_stamp']
#            ])

        
#    return table


#def grab_url(tld, int_ext, verbose):#0 for internal/ anything else for external
#    current_url = None
#    for x in range(0, len(glbls.pool)):
#        if "https://" in glbls.pool[x] or "http://" in glbls.pool[x]:
#            url = "http" + str(glbls.pool[x].split('http')[1].split('"')[0])
#            if int_ext == 0:
#                if tld in url:
#                    current_url = url
#                    glbls.current_url = url
#                    glbls.pool = glbls.pool.pop(x)
#                    global_pool_update(x)
#                    if verbose:
#                        print(glbls.current_index_data)
#                    break
#            else:
#                if tld in url:
#                    pass
#                else:
#                    current_url = url
#                    glbls.current_url = url
#                    glbls.pool = glbls.pool.pop(x)
#                    global_pool_update(x)
#                    if verbose:
#                        print(glbls.current_index_data)                        
#                    break
#                
#        
#        
#    return current_url     






