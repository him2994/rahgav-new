import re
import os
from bs4 import BeautifulSoup
from utils.simple_requests_fetcher import SimpleRequestsFetcher
from processors import CapchaRequiredException
from utils import fs
import ipdb
try:
    # Pyhton2
    import urlparse
except ImportError:
    # Python3
    import urllib.parse as urlparse
    


class SiteWOProcessor:
    
    HOST = "patentscope.wipo.int"
    SITE_URL = "http://patentscope.wipo.int"
    
    MAIN_SECTIONS = (            
        "Alias",
        "Pub. No.:",
        "Publication Date:",
        "IPC:",
        "Applicants:",
        "Inventors:",
        "Agent:",
        "Priority Data:",
        "Title",
        "Publication Language:",
        "Filing Language:",
        "International Application No.:",
        "International Filing Date:",
        "Abstract:",
    )
    
    
    def __init__(self, saver, requests_per_minute=5,
                max_proxy_use_number=15, do_download=True, proxy_list=None):
        print("Init [WO] processor...")
        
        self._saver = saver
        self._do_download = do_download
        
        self._fetcher = SimpleRequestsFetcher(requests_per_minute,
                        max_proxy_use_number, proxy_list=proxy_list,
                        use_session=True)
        
        self._fetcher.update_headers({ "Host": self.HOST })
        
        

    def _get_bs_content(self, url):
        content = self._fetcher.get_content(url)
        
        if "the automatic queries form the legitimate human" in str(content):
            try:
                print("SITE REQUIRES CAPTCHA, TRYING TO CHANGE PROXY")
                self._fetcher.change_proxy()
                return self._get_bs_content(url)
            except Exception as e:
                raise CapchaRequiredException("Site requires captcha and"
                        " failed to change proxy because: %s." % str(e))
        
        return BeautifulSoup(content)
    
    
    
    def process_number(self, number, number_type, alias, *args, **kwargs):
        number = number.strip()
        
        if number_type in ("WO"):
            self._process_number(number, number_type, alias)
        else:
            raise Exception("Unknown number type: %s" % number_type)
        
        
        
    def _normalize_date_str(self, date_str):
        try:
            date_str = re.sub(r'(\d{2})\.(\d{2})\.(\d{4})',
                                                r'\g<1>/\g<2>/\g<3>', date_str)
        except:
            pass
        
        return date_str
    
        
    def _get_info_from_table(self, table, data):
        
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            
            if len(tds) < 2 or len(tds[0].text) < 4:
                continue
            
            inner_tabel = tds[0].find("table")
            if inner_tabel:
                self._get_info_from_table(inner_tabel, data)
                continue
            
            i = 0
            while len(tds) >= i+2:
                caption = tds[i].text.strip()
                
                if caption not in self.MAIN_SECTIONS:
                    i += 1
                    continue
                
                if not tds[i+1].text.strip() and len(tds) >= i+3:
                    i += 1
                
                if caption == "IPC:":
                    tds[i+1] = tds[i+1].find("td")
                    if not tds[i+1]:
                        i += 1
                        continue
                    
                if tds[i+1].find("span", {"lang": "en"}):
                    tds[i+1] = tds[i+1].find("span", {"lang": "en"})
                
                content = tds[i+1].decode_contents(formatter=None)
                content = re.sub("\r?\n", "", content)
                content = content.replace("<br/>", "\r\n").replace("<BR/>", "\r\n")
                content = content.replace("<tr>", "\r\n")
                content = content.replace("&nbsp;", " ")
                content = re.sub("<[^>]*>", "", content).strip()
                
                
                data[caption] = self._normalize_date_str(content)
                
                i += 1
        
    
    #def _init_fetcher(self, r_fetcher):
    #    r_fetcher.get("http://patentscope.wipo.int/search/en/result.jsf")
        
        
    def _process_number(self, number, number_type, alias):
        # ipdb.set_trace()
        print("Processing number: %s (%s)" % (number, number_type))
        
        self._fetcher.clear_cookies()
        
        bs_content = self._get_bs_content(
                        "http://patentscope.wipo.int/search/en/result.jsf")
        print ("xxxxxxxxxxx------------------xxxxxxxxxxxxxxx" + str(bs_content.find("input",{"name": "javax.faces.ViewState"})["value"]))

        bs_content = self._fetcher.post(
            "http://patentscope.wipo.int/search/en/result.jsf",
            {
                "resultListForm": "resultListForm",
                "resultListForm:goToPage": "1",
                "resultListForm:refineSearchTop": number,
                "resultListForm:commandRefineSearchTop": "Search",
                "resultListForm:j_idt401": "workaround",
                "javax.faces.ViewState":
                    bs_content.find("input",
                        {"name": "javax.faces.ViewState"})["value"]
            })
#        print(self._fetcher.get_session().cookies["JSESSIONID"])
      #  bs_content = self._fetcher.post(
       #     "https://patentscope.wipo.int/search/en/search.jsf",
      #      data)


        if bs_content.status_code != 200:
            raise Exception("Server error: %s (%s)" % (bs_content.status_code))
        
        bs_content = BeautifulSoup(bs_content.content)
        with open("post.txt", "w") as x:
            x.write(repr(bs_content.prettify))
        if bs_content.find("meta", {"http-equiv": "refresh"}):
            print("Server asks to refresh the page...")
            return self._process_number(number, number_type, alias)
        
        '''
        with open("x.html", "w") as fl:
            fl.write(str(bs_content))
        
        link = bs_content.find("a",
            { "id" : "resultTable:0:resultListTableColumnLink" })
    
        if not link:
            raise Exception("Invalid number: %s (%s)" % (number, number_type))
        
        link = urlparse.urljoin(self.SITE_URL, "/search/en/" + link["href"])
        
        # main data
        print("")
        print("Getting main data...")
        
        data = {
                "Alias": alias,
            }
        
        url = link
            
        bs_content = self._get_bs_content(url)
        '''
        
        table = bs_content.find("table",
            { "cellspacing": "3", "id": "detailPCTtableHeader"})
        data = {
                "Alias": alias,
            }
        
        try:
            self._get_info_from_table(table, data)
        except:
            raise Exception("Invalid number: %s (%s)" % (number, number_type))
        
        try:
            table = bs_content.find_all("table",
                { "cellspacing": "3", "cellpadding": "2", "width": "650"})[1]
            self._get_info_from_table(table, data)
        except:
            pass
        
        self._saver.save_main_data(data)
        
        
        
        # setting up input field
        input_field = "%s (%s)" % (number, number_type)
        
        url_number = data["Pub. No.:"].replace("/", "")
        print("")
        print("Getting National Phase data...")
        # getting National Phase data
        print("")
        print("Getting National Phase data...")
        
        url = "http://patentscope.wipo.int/search/en/detail.jsf?" \
                "docId=%s&recNum=1&tab=NationalPhase&maxRec=&" \
                "office=&prevFilter=&sortOption=&queryString=" % url_number
        bs_content = self._get_bs_content(url)
        
        table = bs_content.find("table",
            { "id": "detailMainForm:natPhaseTableDataEntries" })
        
        if not table:
            print("No National Phase data.")
            
        else:
        
            data = []
            for tr in table.find_all("tr")[1:]:
                
                tds = tr.find_all("td")
                
                if len(tds) != 4:
                    continue
                            
                data.append({
                    "Alias": alias,
                    "Input": input_field,
                    "Office": tds[0].text.strip(), 
                    "Entry Date": self._normalize_date_str(tds[1].text.strip()),
                    "National Number": tds[2].text.strip(),
                    "National Status":
                        self._normalize_date_str(tds[3].text.strip()),
                })
                
            self._saver.save_national_phase(data)
        
        
        # getting documents data
        print("")
        print("Getting document data...")
        url = "http://patentscope.wipo.int/search/en/detail.jsf?" \
            "docId=%s&recNum=1&tab=PCTDocuments&maxRec=&office=" \
            "&prevFilter=&sortOption=&queryString=" % url_number
        bs_content = self._get_bs_content(url)
        
        div = bs_content.find("div",
                            { "id": "detailMainForm:PCTDocuments:content" })
        
        if not div:
            print("No document data...")
            return
        
        data = []
        for table in div.find_all("table"):
            for tr in table.find_all("tr"):
                tds = tr.find_all("td")
                
                if len(tds) != 4:
                    continue
                
                if tds[0].text.strip() == "Date":
                    continue
                
                try:
                    page_count = re.search("\d+", tds[3].text).group(0)
                except:
                    page_count = ""
                
                data.append({
                    "Alias": alias,
                    "Date": self._normalize_date_str(tds[0].text.strip()),
                    "Document type": tds[1].text.strip(),
                    "Number of pages": page_count,
                    "Link": urlparse.urljoin(self.SITE_URL, tds[3].find("a")["href"]),
                })
        
        self._saver.save_documents_data(data)
        
        print("")
        if not self._do_download:
            print("Download turned off.")
            return
        
        if len(data) == 0:
            print("No documents to download.")
            return
        
        files_dir = os.path.dirname(os.path.realpath(__file__))
        files_dir = os.path.join(files_dir, "../Output/%s" % alias)
        
        try:
            os.stat(files_dir)
        except:
            os.mkdir(files_dir) 
        
        file_no = 0
        for document in data:
            file_no += 1
            
            #_, file_extension = os.path.splitext(document["link"])
            filename = fs.clean_filename(document["Document type"])
            filename = "%d - %s.pdf" % (file_no, filename)

            print("Downloading file number %d: %s..." % (file_no, filename))
            
            url = document["Link"]
            
            self._fetcher.download_file(url, os.path.join(
                files_dir.strip(), filename.strip()))
            
            
        
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        