
#Todos:
# Fix Proxy usage
# Download fresh proxies at every startup from proxyscrape
# Get latency for all requests
# Add discord notify for hits/completions.


import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

#INCLUDES
from config import config, glbls    
from functions import *



def index_data(tld, verbose, B_use_proxies):
    #Overall Allocations
    page_data = dict()
    index_data = 0
    #Make Initial Contant With Index. (hopefully)
    try:
        if B_use_proxies: r = anon_request(tld, verbose)
        else: r = direct_request(tld, verbose)
    except Exception as d:
        log_error(d)
        if verbose:
            print(d)
        try:
            if B_use_proxies: r = anon_request(f"http://{glbls.tld}/", verbose)
            else: r = direct_request(f"http://{glbls.tld}/", verbose)
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
                    if any(word in url.lower() for word in glbls.drop_expressions):
                        if verbose:
                            print(f"Dropped: {url}")
                        pass
                    else:
                        internal_links.append(url)
                        if verbose:
                            try:
                                print(f"[SEED URL] - Found Internal Link @Index: {url}")
                            except Exception as D:
                                print(f"Warning: {str(D)}")
                                
                else:
                    if any(word in url.lower() for word in glbls.drop_expressions):
                        if verbose:
                            print(f"Dropped: {url}")              
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
                #Push new lists of links to BOTTOM of each global pool
        glbls.pool = {
            "internal_links": list(internal_links),
            "external_links": list(external_links)
            }
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
def new_data(new_url, verbose, B_use_proxies):
    index_data = 0
    page_data = dict()
    
    #Make Initial Contant With Index. (hopefully)
    try:
        if B_use_proxies: r = anon_request(new_url, verbose)
        else: r = direct_request(new_url, verbose)
    except Exception as d:
        log_error(d)
        try:
            if B_use_proxies:r = anon_request(f"http://{new_url}", verbose)
            else: r = direct_request(f"http://{new_url}", verbose)
        except Exception as dd:
            log_error(dd)
            index_data = None
            pass

    #Vitals
    cpu = get_cpu()
    ram = get_ram()
    t_stamp = str(datetime.now())

    #Success - Check Index
    if index_data is not None:

        #GET TRUE TLD
        tld = trueTLD(new_url)
        
        #split page lines
        shred = r.text.split('\n')

        #Nested Allocations For New Links
        internal_links = []
        external_links = []
        
        for x in range(0, len(shred)):
            #Scout New Links
            if "https://" in shred[x] or "http://" in shred[x]:
                url = "http" + str(shred[x].split('http')[1].split('"')[0])
                
                if any(word in new_url.lower() for word in glbls.sought_expressions):
                    with open(f"{glbls.data_dir}/{glbls.sesh_id}_hits.dat", "a+") as ddd:
                        if verbose:
                            print(f"Found: {url}")                        
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
                        
                if tld in url:
                    if any(word in url.lower() for word in glbls.drop_expressions):
                        if verbose:
                            print(f"Dropped: {url}")
                        pass
                    else:
                        internal_links.append(url)
                        if verbose:
                            try:
                                print(f"[{new_url}] - Found Internal Link: {url}")
                            except Exception as D:
                                print(f"Warning: {str(D)}")

                else:
                    if any(word in url.lower() for word in glbls.drop_expressions):
                        if verbose:
                            print(f"Dropped: {url}")                        
                        pass
                    else:
                        external_links.append(url)
                        if verbose:
                            try:
                                print(f"[{new_url}] - Found Internal Link: {url}")
                            except Exception as E:
                                print(f"Warning: {str(E)}")

       
                                            
    
        links = dict()
        links['internal'] = internal_links
        links['external'] = external_links
        

        #Push new lists of links to BOTTOM of each global pool
        glbls.pool = {
            "internal_links": glbls.pool['internal_links'] + list(internal_links),
            "external_links": glbls.pool['external_links'] + list(external_links)
            }

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
    for x in range(0, len(glbls.pool[glbls.usageType])):
        try:
            glbls.tmp.append(
                new_data(
                    glbls.pool[glbls.usageType][x],
                    B_verbose,
                    B_use_proxies
                    )
                )    
        except Exception as ddd:
            log_error(ddd)
            if B_verbose:
                print(f"Warning: {str(ddd)}")
        # DEFACTOR THE USED NW URL    
        glbls.pool[glbls.usageType].remove(glbls.pool[glbls.usageType][x])


#Main
class void:
    class crawler:
        def __init__(self, url, usagetype, generations, B_verbose=True, B_use_proxies=False, http_proxy_file_name=None, ssl_proxy_file_name=None):

            ##USAGE SCHEMA:
            if usagetype == 0:
                glbls.usageType = "internal_links"
            else:
                glbls.usageType = "external_links"

            if B_use_proxies:
                #Load Proxies
                load_proxies(http_proxy_file_name, ssl_proxy_file_name, B_verbose)
                if B_verbose:
                    print("Proxies Loaded!")
                
            #Check for user entering a url not a tld
            isUrl = False        
            urlSigs = ["http", "://", "/"]
            for x in range(len(urlSigs)):
                if urlSigs[x] in url:
                    isUrl = True

            #Clean up params for now   //TODO     
            url = url.split("?")[0]        
                    
            # GET TRUE TLD                
            glbls.tld = trueTLD(url)
            
            if B_verbose:
                print("Top Level Domain Validated!")
            

            # MAKE SESH ID
            glbls.sesh_id =  glbls.tld + "-" + unique_id()
            
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
                    sleep(.1)#1 seconds
                    tstat -= 1
                

            #Master Stack
            master_data = []

            # First is always index page then so on and so on...
            master_data.append(index_data(url, B_verbose, B_use_proxies))

            #Pass master_data to temporary global scope.
            glbls.tmp = master_data

            #Main Worker Loop
            for x in range(0, generations):

                #LOOP THROUGH GENERATIONS. 
                flex(glbls.tld, usagetype, B_verbose, B_use_proxies)

                #SAVES OUR PROGRESS - Dumps To JSON. 
                try:
                    file = f"{glbls.data_dir}/" + url.replace(".", "_").replace("/", "-") + f"gen_{x}.json"
                    with open(file, 'w+') as f: json.dump(list(glbls.tmp), f)
                except Exception as Dd:
                    print(str(Dd))
                    if B_verbose:
                        xx = input("Hit enter to continue...")
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



####


void.crawler(
    "https://www.instagram.com/joerogan/?hl=en", 1, 10, True, False, "proxies/http_proxies.txt", "proxies/ssl_proxies.txt"
    )
###


