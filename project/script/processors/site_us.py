import re
import os
import tempfile
import time
#import urllib.parse as urlparse

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import ui as webDriverUi
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utils.deathbycaptcha import SocketClient as CatchaClient 
from utils.simple_requests_fetcher import SimpleRequestsFetcher

from utils.proxy_list import ProxyList
from utils import fs


class SiteUsException(Exception):
    pass

class SiteUsNoNumberException(SiteUsException):
    pass

class SiteUsLinkNotFound(SiteUsException):
    pass


class SiteUSProcessor:
    
    HOST = "portal.uspto.gov"
    SITE_URL = "http://portal.uspto.gov"
    
    
    def __init__(self, saver, captcha_login, captcha_pwd,
            do_download=True, proxy_list=None):
        print("Init [USA, USPUB, USPAT] processor...")
        
        self._saver = saver
        self._do_download = do_download
        
        self._proxy_list = ProxyList(proxy_list=proxy_list)
        self._driver = None
        
        self._fetcher = SimpleRequestsFetcher(0, 0, proxy_list=[])
        
        self._captcha_login = captcha_login 
        self._captcha_pwd = captcha_pwd
        
    
    def _init_fetcher(self):
        try:
            self._driver.close()
        except:
            pass
        
        proxy = self._proxy_list.get_next_proxy()
        
        service_args = ["--ssl-protocol=any"]
        if proxy:
            service_args += ['--proxy=%s' % proxy,
                             '--proxy-type=[http|ssl|ftp]']
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = \
                                    self._fetcher.HEADERS["User-Agent"]
        #'''                    
        self._driver = webdriver.PhantomJS(
            service_args=service_args,
            desired_capabilities=dcap)
        '''
        self._driver = webdriver.Firefox()
        '''
        driver = self._driver
        driver.set_window_size(1440, 900)
        
        driver.get("http://portal.uspto.gov/pair/PublicPair")
        
        print("Decoding captcha...")
        while True:
            captcha = webDriverUi.WebDriverWait(driver, 20).until(
                (EC.presence_of_element_located(
                                        [By.ID, "recaptcha_challenge_image"])))
            #if not captcha:
            #    return
            
            src = captcha.get_attribute("src")
            temp_jpg = tempfile.mktemp(".jpg")
            self._fetcher.download_file(src, temp_jpg)
            
            client = CatchaClient(self._captcha_login, self._captcha_pwd)
            decoded = client.decode(temp_jpg)
            
            if "text" in decoded:
                print("Got captcha text: %s" % decoded["text"])
                
                f = driver.find_element_by_id("recaptcha_response_field")
                f.send_keys(decoded["text"])
                
                driver.find_element_by_id("SubmitPAIR").click()
                
                if "Enter the RECAPTCHA text" not in driver.page_source:
                    print("Captcha decoded successfully: %s" % 
                                                            decoded["text"])
                    return
                
            print("Failed to decode captcha. Decoding again...")

        

    def process_number(self, number, number_type, alias, *args, **kwargs):
        
        if number_type in ("USA", "USPUB", "USPAT"):
            try:
                self._process_number(number, number_type, alias)
            except SiteUsNoNumberException:
                raise
            except:
                #raise
                print("Reiniting fetcher and trying once more...")
                self._saver.cancel_changes()
                self._init_fetcher()
                self._process_number(number, number_type, alias)
            
        else:
            raise Exception("Unknown number type: %s" % number_type)


    
    def _switch_page(self, href, raise_e=False):
        if not self._driver:
            self._init_fetcher()
            raise_e = True
        
        if "cannot be retrieved as entered" in self._driver.page_source:
            if href == "javascript:submitTab('pair_search')":
                return # already there
            else:
                raise Exception("Link for page not found on search page: %s" %
                    href)
        
        if href == "javascript:submitTab('pair_search')":
            try:
                if self._driver.find_element_by_id("SubmitPAIR"):
                    return # already there
            except:
                pass
        
        try:
            link = self._driver.find_element_by_xpath('//a[@href="%s"]' % href)
        except NoSuchElementException:
            raise SiteUsLinkNotFound("No such a tab")
            
        
        if not link:
            if raise_e:
                raise Exception("Failed to switch to page: %s" % href)
            
            self._init_fetcher()
            self._switch_page(href, raise_e=True)
        
        link.click()
        try:
            link.click() # javascript glitch
        except:
            pass
        
        try:
            element = self._driver.get_element_by_xpath(
                        "//table[@class='epoTableBorder']//font[@color='red']")
        except:
            return
        
        if element.text.strip(): 
            print("Server said: %s" % element.text.strip())
            print("Reiniting browser...")
            self._init_fetcher()
            return self._switch_page(href, raise_e)
    


    def _wait(self, xpaths):
        
        def wait(driver):
            for xpath in xpaths:
                try:
                    if self._driver.find_element_by_xpath(xpath):
                        return self._driver.find_element_by_xpath(xpath)
                except:
                    pass
                
            return False
        
        return wait



    def _process_number(self, number, number_type, alias):
        
        def _normalize_date_str(date_str):
            date_str = re.sub(r'(\d{2})\-(\d{2})\-(\d{4})',
                                                r'\g<2>/\g<1>/\g<3>', date_str)
            return date_str
        
        
        def get_main_data():
            table = driver.find_element_by_id("bibview")
    
            data = {
                    "Alias": alias
                }
            for tr in table.find_elements_by_tag_name("tr"):
                tds = tr.find_elements_by_tag_name("td")
                even = False
                key = None
                for td in tds:
                    if not even:
                        key = td.text.strip() 
                    else:
                        if key and td.text.strip() not in ["", "-"]:
                            data[key] = _normalize_date_str(
                                td.text.strip().replace(" all Inventors", ""))
                    even = not even
                    
                table = driver.find_element_by_id("bibviewTitle")
                td = table.find_elements_by_tag_name("td")
                data["Title"] = td[1].text.strip()
            
            try:        
                print("ptaptetab")
                self._switch_page("javascript:submitTab('ptaptetab')")
                table = webDriverUi.WebDriverWait(driver, 20).until(
                    (EC.presence_of_element_located(
                        [By.XPATH, "//table[@id='ptaptesummarytable' and "
                            "@cellpadding='3']"])))
                
                key = None
                for td in table.find_elements_by_tag_name("td"):
                    if not key:
                        key = td.text.strip()
                    else:
                        data[key] = _normalize_date_str(td.text.strip())
                        key = None
                
            except SiteUsLinkNotFound:
                print("No tab Patent term Adjustments")
                
                
            try:
                print("Correspondencetab")
                self._switch_page("javascript:submitTab('Correspondencetab')")
                table = webDriverUi.WebDriverWait(driver, 20).until(
                    (EC.presence_of_element_located(
                        [By.XPATH, "//table[@id='correspondence']"])))
                
                key = None
                for td in table.find_elements_by_tag_name("td")[1:]:
                    if not key:
                        key = td.text.strip()
                    else:
                        data[key] = _normalize_date_str(td.text.strip())
                        key = None
                        
                data["Agent"] = "Name: " + data["Name:"] + "\n\n" + \
                    "Address:\n" + data["Address:"]
                
            except SiteUsLinkNotFound:
                print("No tab Address & Attorney/Agent")
            
            try:     
                print("continuitytab")   
                self._switch_page("javascript:submitTab('continuitytab')")
                table = webDriverUi.WebDriverWait(driver, 10).until(
                    (EC.presence_of_element_located(
                        [By.XPATH, "//table[@id='continuityparent']"])))
                
                try:
                    con_data = []
                    keys = []
                    for td in table.find_elements_by_tag_name("th"):
                        keys.append(td.text.strip())
                    
                    for tr in table.find_elements_by_id("parentdata0"):
                        key = None
                        value = ""
                        
                        one = {
                                "Alias": alias,
                            }
                        con_data.append(one)
                        i = 0
                        for td in tr.find_elements_by_tag_name("td"):
                            one[keys[i]] = _normalize_date_str(td.text.strip())
                            i += 1
                            
                    self._saver.save_parent_continuity(con_data)
                except:
                    print("No parent data.")
                    
                try:
                    str_ = ""
                    for tr in driver.find_elements_by_id("childdata0"):
                        str_ += "\n" + _normalize_date_str(tr.text.strip())
                        
                    data["Child Continuity Data"] = str_.strip()
                except:
                    print("No child data.")
                    
                            
            except SiteUsLinkNotFound:
                print("No tab Continuity Data")
            
                
            try:
                print("foreignPrioritiestab")        
                self._switch_page(
                                "javascript:submitTab('foreignPrioritiestab')")
                
                td = webDriverUi.WebDriverWait(driver, 20).until(
                    (EC.presence_of_element_located(
                        [By.XPATH, "//td[@id='forpriority']"])))
                table = td.find_element_by_tag_name("table")
                key = "Country |Priority |Priority Date ;"
                value = ""
                for tr in table.find_elements_by_xpath(
                    "//tr[@class='wpsTableNrmRow' or @class='wpsTableShdRow']"):
                    
                    next_val = ""
                    for td in tr.find_elements_by_tag_name("td"):
                        next_val += " |" + td.text.strip()
                        
                    next_val = next_val[2:]
                    
                    value += "\n" + next_val
                    
                data[key] = _normalize_date_str(value.strip())
                    

            except SiteUsLinkNotFound:
                print("No tab Foreign Priority")
                



            self._saver.save_main_data(data)
            return data
        
        
        def get_event_data():
            table = driver.find_element_by_id("bibcontents")
            
            data = []
            for tr in table.find_elements_by_xpath(
                    "//tr[@class='wpsTableNrmRow' or @class='wpsTableShdRow']"):
                tds = tr.find_elements_by_tag_name("td")
                data.append({
                    "Alias": alias,
                    "Input": input_field,
                    "Date": _normalize_date_str(tds[0].text.strip()),
                    "Action": tds[1].text.strip(),
                })
        
            self._saver.save_evt_history_data(data)
            return data
        
        
        
        def get_documents_data():
        
            table = driver.find_element_by_id("ifwinnertable")
            
            data = []
            for tr in table.find_elements_by_xpath("//tr"
                    "[@class='wpsTableNrmRow' or @class='wpsTableShdRow']"):
                tds = tr.find_elements_by_tag_name("td")
                
                data.append({
                    "Alias": alias,
                    "Input": input_field,
                    "Date": _normalize_date_str(tds[0].text.strip()),
                    "Document type": tds[2].text.strip(),
                    "Category": tds[3].text.strip(),
                    "Number of pages": tds[4].text.strip(),
                })
            
            
            
            dosnum = re.search("document\.downloadForm\.dosnum\.value='(\d+)';",
                driver.page_source)
            
            dosnum = dosnum.group(1)
        
            sels = "0" * len(data)
            
            try:
                i = 0
                for d in data:
                    
                    sel = sels[:i] + "1" + sels[i+1:] 
                    url = "http://portal.uspto.gov/pair/download/ShowPdfBook?" \
                        "dosnum=%s&sels=%s" % (dosnum, sel)
                        
                    d["Link"] = url
                    i += 1
            except Exception as e:
                print(e)
                raise
            
            self._saver.save_documents_data(data)
            
            print("")
            if not self._do_download:
                print("Download is turned off.")
                return
            
            print("Downloading files.")
            
            
            
            self._fetcher.clear_cookies()
            s = self._fetcher.get_session()
            
            for cook in driver.get_cookies():
                s.cookies[cook["name"]] = cook["value"] 
            
            
            files_dir = os.path.dirname(os.path.realpath(__file__))
            files_dir = os.path.join(files_dir, "../Output/%s" % alias)
            
            try:
                os.stat(files_dir)
            except:
                os.mkdir(files_dir)     
            
            for i in range(len(sels)):
                sel = sels[:i] + "1" + sels[i+1:] 
            
                url = "http://portal.uspto.gov/pair/download/ShowPdfBook?" \
                    "dosnum=%s&sels=%s" % (dosnum, sel)
                
                filename = "%d - %s.pdf" % \
                            (i, fs.clean_filename(data[i]["Document type"]))
                
                print("Downloading file: %s" % filename)
                
                self._fetcher.download_file(url,
                                            os.path.join(files_dir, filename))
        
            return data
        
        
        print("Processing number: %s (%s)" % (number, number_type))
        
        input_field = "%s (%s)" % (number, number_type) # setting up input field
        
        print("")
        print("Entering number...")
        
        self._switch_page("javascript:submitTab('pair_search')")
        driver = self._driver
        
        # waiting for JavaScript to finish
        webDriverUi.WebDriverWait(driver, 20) \
                .until(EC.presence_of_element_located([By.ID, "SubmitPAIR"]))
        
        if number_type == "USA":
            driver.find_element_by_xpath(
                                "//input[@title='application number']").click()
        elif number_type == "USPUB":
            driver.find_element_by_xpath(
                                "//input[@title='publication number']").click()
        elif number_type == "USPAT":
            driver.find_element_by_xpath(
                                "//input[@title='patent number']").click()
        else:
            raise Exception("Unknown number type: %s" % number_type)
        
        driver.find_element_by_id("number_id").send_keys(number)
        driver.find_element_by_id("SubmitPAIR").click()
        
        
        print("WAITING...")
        element = webDriverUi.WebDriverWait(driver, 20).until(self._wait(
            ["//img[@alt='Application Data']", "//div[@id='ERRORDIV']",
                "//div[@id='ERRORDIVPALMPROBLEM']",
                "//table[@class='epoTableBorder']//font[@color='red']"]))
        
        if element.get_attribute('id') == 'ERRORDIVPALMPROBLEM':
            print("Overloaded, trying again in 5 seconds...")
            time.sleep(5)
            return self._process_number(number, number_type, alias)
        
        if element.text:
            if "Service not available at this time" in element.text:
                print("Service not available, trying again in 5 seconds...")
                time.sleep(5)
                return self._process_number(number, number_type, alias)
            
            raise SiteUsNoNumberException("Error: %s" % element.text.strip())
        
        
        self._switch_page("javascript:submitTab('detailstab')")
        try:
            element = webDriverUi.WebDriverWait(driver, 20).until(self._wait(
                ["//img[@src='/pair/img/tabs/image1on.gif']"]))
        except:
            print("Wrong tab opened?...")
            self._process_number(number, number_type, alias)
        
        # main data
        print("")
        print("Getting main data...")
        get_main_data()
        
        # history data
        print("")
        print("Getting history data...")
        
        try:
            self._switch_page("javascript:submitTab('fileHistorytab')")
            webDriverUi.WebDriverWait(driver, 20).until(
                (EC.presence_of_element_located([By.ID, "bibcontents"])))
            
            get_event_data()
        except SiteUsException:
            print("No history data")
        
            
        print("")
        print("Getting document data...")
        
        try:
            self._switch_page("javascript:submitTab('ifwtab')")
            webDriverUi.WebDriverWait(driver, 20).until(
                (EC.presence_of_element_located([By.ID, "ifwinnertable"])))
            get_documents_data()
            
        except SiteUsException:
            print("No document data")
            
            
    def close(self):
        try:
            self._driver.close()
        except:
            pass
        

'''
us = SiteUs(None, requests_per_minute=0)
us.process_number(number="8274168", number_type="USPAT", alias="alias")
print("\n\ndone")
'''

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        