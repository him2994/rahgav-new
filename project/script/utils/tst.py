from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import ui as webDriverUi
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re
from datetime import datetime
import requests


def _normalize_date_str(date_str):
    date_str = re.sub(r'(\d{2})\-(\d{2})\-(\d{4})', r'\g<1>/\g<2>/\g<3>', date_str)
    
    return date_str


def x(driver):
    
    table = driver.find_element_by_id("ifwinnertable")
    
    data = []
    for tr in table.find_elements_by_xpath("//tr[@class='wpsTableNrmRow' or "
            "@class='wpsTableShdRow']"):
        tds = tr.find_elements_by_tag_name("td")
        
        data.append({
            "Date": _normalize_date_str(tds[0].text.strip()),
            "Document type": tds[2].text.strip(),
            "Category": tds[3].text.strip(),
            "Number of pages": tds[4].text.strip(),
        })
    
    dosnum = re.search("document\.downloadForm\.dosnum\.value='(\d+)';",
        driver.page_source)
    dosnum = dosnum.group(1)

    sels = "0" * len(data)
    
    for i in range(len(sels)):
        sel = sels[:i] + "1" + sels[i+1:] 
    
        url = "http://portal.uspto.gov/pair/download/ShowPdfBook?" \
            "dosnum=%s&sels=%s" % (dosnum, sel)
    
    
    s = requests.Session()
    for cook in driver.get_cookies():
        s.cookies[cook["name"]] = cook["value"] 
    
    r = s.get(url)
    print(r.headers)
        

def event_data(driver):
    table = driver.find_element_by_id("bibcontents")
    
    data = []
    for tr in table.find_elements_by_xpath("//tr[@class='wpsTableNrmRow']"):
        tds = tr.find_elements_by_tag_name("td")
        data.append({
            "date": _normalize_date_str(tds[0].text.strip()),
            "action": tds[1].text.strip(),
        })
        
    print(data)


def main_data(driver):

    table = driver.find_element_by_id("bibview")
    
    data = {}
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
            
            
    print(data)
        
    