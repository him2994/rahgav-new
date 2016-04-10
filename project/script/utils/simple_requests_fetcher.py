import requests
import time
from utils.sleeper import Sleeper
from utils.proxy_list import ProxyList


class SimpleRequestsFetcher:
    
    # requests headers
    HEADERS = { 
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Ubuntu Chromium/39.0.2171.65 "
                "Chrome/39.0.2171.65 Safari/537.36",
    }
    
    
    def __init__(self, requests_per_minute, max_proxy_use_number=15,
            use_session=True, proxy_list=None,
            init_fetcher_func=None, reinit_mins=10):
        
        self._use_session = use_session
        if use_session:
            if init_fetcher_func is None:
                self._session = requests.Session()
            else:
                self._session = None
        else:
            if init_fetcher_func is not None:
                raise Exception("Parameter init_fetcher_func can only be used"
                    " with sessions")
                
            self._session = None
            
            
        self._proxy_list = ProxyList(proxy_list=proxy_list)
        self._set_same_proxies(self._proxy_list.get_next_proxy())
        self._max_proxy_use_number = max_proxy_use_number
        
        
        self._inited_proxies = {
                # proxy_str: init_time
            }
        self._reinit_mins = reinit_mins
        self._being_inited = False
        
        self._headers = {}
        self.update_headers(self.HEADERS.copy())
        
        self._requests_per_minute = requests_per_minute
        
        self._sleeper = Sleeper()
        self._update_sleeper_interval()
        
        self._init_fetcher_func = init_fetcher_func


        
    def _update_sleeper_interval(self):
        proxy_count = self._proxy_list.get_proxy_count()
        
        
        if proxy_count <= 1 or self._max_proxy_use_number > 1:
            requests_per_minute = self._requests_per_minute
        else:
            requests_per_minute = proxy_count * self._requests_per_minute
        
        print("Set requests per minute: %0.2f (cur. proxy count: %d)." %
            (requests_per_minute, proxy_count))
        
        self._sleeper.set_per_minute(per_minute=requests_per_minute)
        
        
        
    def update_headers(self, headers):
        self._headers.update(headers)
        
        
        
    def _set_same_proxies(self, proxy):
        print("Simple request fetcher proxy set: %s." % proxy)
        
        
        self._proxies = {
          "http": proxy,
          "https": proxy,
        }
        
        self._cur_proxy_use_number = 0
        self._cur_proxy = proxy
        
        
    def change_proxy(self):
        self._set_same_proxies(self._proxy_list.change_proxy())
        
    
    def get_cur_proxy(self):
        return self._cur_proxy
    
    
    def _get(self, url, autochange_proxy, *args, **kwargs):
        
        try:
            if self._use_session:
                return self._session.get(url, *args, **kwargs)
            else:
                return requests.get(url, *args, **kwargs)
        except requests.exceptions.ProxyError as e:
            if autochange_proxy:
                print("Current proxy(\"%s\") will be removed from the list: %s."
                    % (self._proxy_list.get_current_proxy(), str(e)))
                
                self._set_same_proxies(self._proxy_list.remove_current_proxy())
                
                
                kwargs['proxies'] = self._proxies
                return self._get(url, autochange_proxy, *args, **kwargs)
            else:
                raise # don't handle this exception here
            
            
            
    def _post(self, url, data, autochange_proxy, *args, **kwargs):
        
        
        try:
            if self._use_session:
                #print("With data: %s" % str(data))
                return self._session.post(url, data=data, *args, **kwargs)
            else:
                return requests.post(url, data=data, *args, **kwargs)
            
        except requests.exceptions.ProxyError as e:
            if autochange_proxy:
                print("Current proxy(%s) will be removed from the list: %s." %
                                (self._proxy_list.get_current_proxy(), str(e)))
                
                self._set_same_proxies(self._proxy_list.remove_current_proxy())
                
                
                kwargs['proxies'] = self._proxies
                return self._post(url, data, autochange_proxy, *args, **kwargs)
            else:
                raise # don't handle this exception here
            
            
    def _request(self, url, *args, **kwargs):
        self.do_interval()
        
        if (self._proxy_list.get_proxy_count() >= 2):
            if self._max_proxy_use_number <= self._cur_proxy_use_number:
                self._set_same_proxies(self._proxy_list.get_next_proxy())
        
        self._check_fetcher_init()
        
        self._cur_proxy_use_number += 1
             
        
        print("Request: %s" % url)
        
        
        autochange_proxy = False
        if "proxies" not in kwargs:
            kwargs["proxies"] = self._proxies
            autochange_proxy = True
        
        if not self._use_session and "headers" not in kwargs:
            kwargs["headers"] = self._headers
        
        kwargs["autochange_proxy"] = autochange_proxy
        
        return kwargs


    def get(self, url, *args, **kwargs):
        kwargs = self._request(url, *args, **kwargs)
        
        if self._use_session and self._init_fetcher_func is not None:
            self._inited_proxies[self._cur_proxy]["time"] = time.time()
        
        return self._get(url, verify=False, timeout=30, *args, **kwargs)
        
        
    def post(self, url, data, *args, **kwargs):
        kwargs = self._request(url, *args, **kwargs)
        
        if self._use_session and self._init_fetcher_func is not None:
            self._inited_proxies[self._cur_proxy]["time"] = time.time()
        
        return self._post(url, data, verify=False,  timeout=30, *args, **kwargs)

            
    def get_content(self, url, *args, **kwargs):
        return self.get(url, *args, **kwargs).content
    
    
    def post_content(self, url, data, *args, **kwargs):
        return self.post(url, data, *args, **kwargs).content
    
    
    def _check_fetcher_init(self):

        if self._being_inited or self._init_fetcher_func is None:
            return
        
        proxy = self._cur_proxy
        
        if proxy in self._inited_proxies and \
        self._inited_proxies[proxy]["time"] is not None and \
        self._inited_proxies[proxy]["time"]+ 60*self._reinit_mins > time.time():
            return
        
        self._being_inited = True
        
        print("Time to initialize proxy: %s" % str(proxy))
        
        try:
            self._session = requests.Session()
            self._inited_proxies[self._cur_proxy] = {
                    "time": None,
                    "session": self._session,
                }
            
            self._init_fetcher_func(self)
            
        except Exception as e:
            print("Changing proxy because: %s" % str(e))
            self.change_proxy()
            
        finally:
            self._being_inited = False
            
        
        self._being_inited = False
        
    
    
    def download_file(self, url, local_filename):
        self._check_fetcher_init()
        
        self.do_interval()
        r = self.get(url)
        
        if "Content-Type" in r.headers and \
                r.headers["Content-Type"] == "text/html":
            
            print("SITE RETURNED HTML RESPONSE, TRYING TO CHANGE PROXY")
            self.change_proxy()
            return self.download_file(url, local_filename)
        
        if self._use_session and self._init_fetcher_func is not None:
            self._inited_proxies[self._cur_proxy]["time"] = time.time()
        
        with open(local_filename, 'wb') as f:
            f.write(r.content)

    
    
    def do_interval(self):
        self._sleeper.next_step()
    
    
    def get_session(self):
        return self._session
    
    
    def clear_cookies(self):
        if self._use_session:
            self._session.cookies.clear()
    
    
    
    
    
    