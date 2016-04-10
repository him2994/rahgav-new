import random


_global_proxy_list = []


def _load_lines_from_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if line]
        
    return  lines


def set_proxy_list(proxy_list):
    global _global_proxy_list
    # have to save all references
    _global_proxy_list.clear()
    _global_proxy_list.extend(proxy_list)
    
    
    
def add_ptoxies(proxy_list):
    global _global_proxy_list
    _global_proxy_list.extend(proxy_list)



def load_from_file(filepath):
    global _global_proxy_list
    # have to save all references
    _global_proxy_list.clear()
    _global_proxy_list.extend(_load_lines_from_file(filepath))




class NoMoreProxiesException(Exception):
    pass




class ProxyList:
    
    def __init__(self, proxy_list=None):
        self._cur_proxy_no = None
        
        if proxy_list is not None:
            self._proxy_list = proxy_list
            
        else:
            self._proxy_list = _global_proxy_list.copy()
            
            
    def load_from_file(self, filepath):
        self._proxy_list = _load_lines_from_file(filepath)
        
      
            
    def get_next_proxy(self):
        if len(self._proxy_list) == 0:
            return None
        
        
        if self._cur_proxy_no is None:
            self._cur_proxy_no = random.randrange(len(self._proxy_list))
            
        else:
            self._cur_proxy_no += 1
            
            if len(self._proxy_list) <= self._cur_proxy_no:
                self._cur_proxy_no = 0
                 
        
        return self._proxy_list[self._cur_proxy_no]
            
            
            
    def change_proxy(self):
        if (self.get_proxy_count() <= 1):
            raise NoMoreProxiesException("Less then 2 proxies available")
        
        return self.get_next_proxy()
            
            
            
    def get_proxy_count(self):
        return len(self._proxy_list)
    
    
    
    def get_current_proxy(self):
        if self._cur_proxy_no is not None:
            return self._proxy_list[self._cur_proxy_no]
        
        return None

    
    
    def remove_current_proxy(self):
        del self._proxy_list[self._cur_proxy_no]
        
        if len(self._proxy_list) == 0:
            self._cur_proxy_no = None
            raise NoMoreProxiesException("No available proxies")
        
        
        if len(self._proxy_list) <= self._cur_proxy_no:
            self._cur_proxy_no = 0
        
        return self._proxy_list[self._cur_proxy_no]
        
            
            
            
            
            
            
            
            