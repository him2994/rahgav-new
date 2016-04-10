import time


class Sleeper:
    
    
    def __init__(self, interval=None, per_minute=None):
        if interval and per_minute:
            raise Exception("Either interval or per_minute must be set, "
                "not both.")
            
        self._last_time = None
        
        if interval:
            self.set_interval(interval)
        elif per_minute:
            self.set_per_minute(per_minute)
        else:
            self._interval = None
        
        
        
    def next_step(self):
        
        if not self._interval:
            return
        
        if self._last_time is not None and \
                self._last_time + self._interval >= time.time():
            
            time_to_sleep = self._last_time + self._interval - time.time()
            print("Sleeping for %0.2f seconds" % time_to_sleep)
            time.sleep(time_to_sleep)
            
            
        self._last_time = time.time()
        
        
    
    def set_interval(self, interval):
        self._interval = interval
        
    
    
    def set_per_minute(self, per_minute):
        if per_minute != 0:
            self._interval = 60.0/per_minute
        else:
            self._interval = 0.0    




