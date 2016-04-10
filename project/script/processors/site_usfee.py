import time
from processors.base import SiteBase
from utils.simple_requests_fetcher import SimpleRequestsFetcher
#from urllib.parse import quote


class SiteUSFEEProcessor(SiteBase):
    
    HOST = "ramps.uspto.gov"
    SITE_URL = "https://ramps.uspto.gov"
    
    
    
    def __init__(self, saver, requests_per_minute=5,
                max_proxy_use_number=15, do_download=True, proxy_list=None):
        print("Init [USFEE] processor...")
        
        self._saver = saver
        self._do_download = do_download
        
        self._fetcher = SimpleRequestsFetcher(requests_per_minute,
                        max_proxy_use_number, proxy_list=proxy_list,
                        use_session=False)
        
        self._fetcher.update_headers({ "Host": self.HOST })
        
        
        
    def process_number(self, app_num, number_type, alias, put_num,
            *args, **kwargs):
        
        app_num = app_num.strip()
        put_num = put_num.strip()
        
        if number_type in ("USFEE"):
            self._process_number(app_num, number_type, alias, put_num)
            
        else:
            raise Exception("Unknown number type: %s" % number_type)
        
    
    
    def _process_number(self, app_num, number_type, alias, put_num):
        
        # getting main data
        bs_content = self._get_bs_content(
            "https://ramps.uspto.gov/eram/patentMaintFees.do")
        time.sleep(3) # doesn't work without this
        
        signature = bs_content.find("input", {"name": "signature"})["value"]
        load_time = bs_content.find("input", {"name": "loadTime"})["value"]
        session_id = bs_content.find("input", {"name": "sessionId"})["value"]
        
        
        def get_base_payload():
            return {
                "patentNum": str(put_num),
                "applicationNum": str(app_num),
                "signature": signature,
                "loadTime": load_time,
                "sessionId": session_id,
                "maintFeeYear": "04",
            }
        
        url = "https://ramps.uspto.gov/eram/getMaintFeesInfo.do;" \
            "jsessionid=%s" % session_id
        
        print("")
        print("Getting main data...")
        
        payload = get_base_payload()  
        payload["maintFeeAction"] = "Get Bibliographic Data"

        bs_content = self._post_bs_content(url, payload)
        
        table = bs_content.find("table", {"class": "border1"})
        
        key = None
        data = {
            "Alias": alias,
        }
        for td in table.find_all("td"):
            try:
                if "label2" in td["class"]:
                    key = td.text.strip()
                elif "info4" in td["class"]:
                    data[key] = td.text.strip()
            except KeyError:
                pass
        
        #self._saver.save_bibliographic_data(data)
        
        
        print("")
        print("Getting Payment Windows...")
        bs_content = self._get_bs_content(
            "https://ramps.uspto.gov/eram/patentMaintFees.do")
        time.sleep(3) # doesn't work without this
        
        signature = bs_content.find("input", {"name": "signature"})["value"]
        load_time = bs_content.find("input", {"name": "loadTime"})["value"]
        session_id = bs_content.find("input", {"name": "sessionId"})["value"]
        
        payload = get_base_payload()
        payload["maintFeeAction"] = "View Payment Windows"
        
        bs_content = self._post_bs_content(url, payload)
        
        table = bs_content.find("table",
            { "class": "border1", "width": "75%"})
        
        trs = table.find_all("tr")
        captions = []
        for c in trs[0].find_all("td")[1:]:
            captions.append(c.text.strip())
        
        for tr in trs[1:]:
            tds = tr.find_all("td")
            key = tds[0].text.strip()
            
            for i in range(1, len(tds)):
                data.update({
                    "%s %s" % (key, captions[i-1]): tds[i].text.strip(),
                })
        
        self._saver.save_bibliographic_data(data)
        
                
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        