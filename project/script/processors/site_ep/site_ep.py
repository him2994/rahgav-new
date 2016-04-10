import re
import os
from bs4 import BeautifulSoup
from utils.simple_requests_fetcher import SimpleRequestsFetcher
from processors.site_ep.get_patent_family import get_patent_family
from utils import fs


try:
    # Pyhton2
    import urlparse
except ImportError:
    # Python3
    import urllib.parse as urlparse
    
    
    
class SiteEPProcessor:
    
    HOST = "register.epo.org"
    SITE_URL = "https://register.epo.org"
    
    
    
    def __init__(self, saver, driver, requests_per_minute=5,
            max_proxy_use_number=15, do_download=True, proxy_list=None,
            *args, **kwargs):
        print("Init [EPA] processor...")
        
        self._saver = saver
        self._do_download = do_download
        
        self._fetcher = SimpleRequestsFetcher(requests_per_minute,
                        max_proxy_use_number, proxy_list=proxy_list,
                        use_session=False)

        self._fetcher.update_headers({ "Host": self.HOST })
        self._driver = driver
        
        
    def _get_bs_content(self, url):
        content = self._fetcher.get_content(url)
        content = str(content).replace("</tr><td", "</tr><tr><td")
        return BeautifulSoup(content)
    
    
    def process_number(self, number, number_type, alias, *args, **kwargs):
        if number_type == "EPA":
            self._process_number(number, number_type, alias)
            
        else:
            raise Exception("Unknown number type: %s" % number_type)
    
    
    
    def _get_tag_content(self, tag):
        content = tag.decode_contents(formatter=None)
        content = re.sub("\r?\n", "", content)
        content = content.replace("<br/>", "\n")
        content = content.replace("&nbsp;", " ")
        content = re.sub("<[^>]*>", " ", content).strip()
        
        content = content.replace("\\r\\n", "").replace("\\t", "")
        content = re.sub(" +", " ", content)
        
        return content.strip()
    
    
    def _normalize_date_str(self, date_str):
        try:
            date_str = re.sub(r'(\d{2})\.(\d{2})\.(\d{4})',
                                                r'\g<1>/\g<2>/\g<3>', date_str)
        except:
            pass
        
        return date_str
    
    
    def _process_number(self, number, number_type, alias):
        print("Processing number: %s (%s)" % (number, number_type))
    
        
        files_dir = os.path.dirname(os.path.realpath(__file__))
        files_dir = os.path.join(files_dir, "../../Output/%s" % alias)
        
        if self._do_download:
            try:
                os.stat(files_dir)
            except:
                os.mkdir(files_dir) 
    
    
        print("")
        print("Getting main data...")
        event_data = []
        input_field = "%s (%s)" % (number, number_type)
        
        url = "https://register.epo.org/smartSearch?searchMode=smart&query=%s" \
            % number
        
        bs_content = self._get_bs_content(url)
        
        if "No documents found" in str(bs_content):
            raise Exception("Document not found")
        
        div = bs_content.find("div", {"class": "blockMe"})
        if div:
            div = div.find("div", {"class": "epoBarItem"})
            resp = div.text.replace("\\n", " ").strip()
            resp = re.sub(" +", " ", resp)
            raise Exception("Server response: %s" % resp)
        
        table = bs_content.find("table", {"class": "printTable"})
        
        if not table:
            raise Exception("Failed to process number: %s (%s)" %
                                                        (number, number_type))
        
        trs = table.find_all("tr", recursive=False)
        
        i = -1
        rspan = 0
        data = {
            "Alias": alias,
        }
        cur_title = "" 
        while i+1 < len(trs):
            i += 1
            if rspan > 0:
                rspan -= 1
            
            tds = trs[i].find_all("td", recursive=False)
            
            if not tds or len(tds) <= 1 or "th" not in tds[0].get('class', []) \
                    or rspan != 0:
                
                
                
                if cur_title and tds and \
                        "former" not in trs[i].get('class', []):
                    line = "\t"
                    
                    for td in tds:
                        line += "%s\t" % self._get_tag_content(td)
                        
                    data[cur_title] += "\n%s" % line[1:-1]
                    
                continue
            
            rspan =  int(tds[0].get('rowspan', 0))
            
            
            title = tds[0].text.strip()
            if "Most recent event" in title:
                title = "Most recent event"
                
            if "Lapses during opposition" in title:
                title = "Lapses during opposition"
            
            if title.strip():
                cur_title = title
                data[cur_title] = "\t"
            else:
                data[cur_title] += "\n\n"
            
            for j in range(1, len(tds)):
                data[cur_title] += "%s\t" % self._get_tag_content(tds[j])
            data[cur_title] = data[cur_title][1:-1]
            
        for key in data:
            data[key] = data[key].replace("\\r\\n", "")
            data[key] = self._normalize_date_str(
                                        re.sub(" +", " ", data[key]).strip())
            
            if "title" in key.lower():
                try:
                    data[key] = re.search("English:\t([^\n]*)", data[key]) \
                        .group(1).strip()
                except:
                    data[key] = ""
                    
                    
        if "Lapses during opposition" in data:
            data["Lapses during opposition."] = data["Lapses during opposition"] 
            d = ""
            lines = data["Lapses during opposition"].split("\n")
            for line in lines:
                line = line.strip().split()
                if len(line) != 2:
                    continue
                d += ", " + line[0]
            
            if d:
                d = d[2:]
                
            data["Lapses during opposition"] = d
                        
            
                    
        data["About this file"] = bs_content \
            .find("div", {"id": "epoContentLeft"}).find("span").text
            
        
        for key in ["Entry into regional phase", "Examination procedure",
                "Fees paid", "Opposition(s)", "Appeal following opposition",
                "Lapses during opposition."]:
            
            if key not in data:
                continue
            
            lines = data[key].split("\n")
            
            for line in lines:
                line = line.strip().split("\t")
                
                if len(line) != 2:
                    continue
                
                date_key = 0
                value_key = 1
                if key == "Lapses during opposition.":
                    date_key = 1
                    value_key = 0
                
                line[date_key] = line[date_key].strip()
                if len(line[date_key]) != 10 or line[date_key][2] != "/" or \
                        line[date_key][5] != "/":
                    continue
                
                category = key
                if category[-1] == '.':
                    category = category[:-1]
                    
                event_data.append({
                    "Alias": alias,
                    "Input": input_field,
                    "Date": line[date_key],
                    "Action": line[value_key].strip(),
                    "Category": category,
                })
        
        link = bs_content.find("a", text="Legal status")["href"]
        link = urlparse.urljoin(self.SITE_URL, link)
        bs_content = self._get_bs_content(link)
        table = bs_content.find("table", {"class": "tableType3"})
        
        design_collect = False
        design_list = []
        for tr in [table] + table.find_all("tr", recursive=False):
            tds = tr.find_all("td", recursive=False)
            
            if tds[0].text.strip() == "Designated contracting states":
                design_collect = True
                tds = tds[1:]
            elif "t2" not in tds[0]["class"]:
                design_collect = False
                
            if design_collect:
                lapse = tds[1].text.strip()
                if lapse:
                    lapse = self._normalize_date_str(lapse[-10:])
                
                design_dict = {
                        "Alias": alias,
                        "Country Code": tds[0].text.strip(),
                        "Lapse": lapse,
                    }
                
                try:
                    design_dict["Link"] = tds[0].find("a")["href"]
                except:
                    pass
                
                design_list.append(design_dict)
                
            
            if tds[0].text.strip() == "European patent granted":
                data["Grant Date"] = \
                    self._normalize_date_str(tds[1].text.strip()) 
            
            
        self._saver.save_design_data(design_list)
        self._saver.save_main_data(data)
        
        print("")
        print("Getting patent family data...")
        get_patent_family(self._driver, number, files_dir,
            self._fetcher, self._saver, self._do_download, alias)
        
        
        print("")
        print("Getting Citations...")
        
        url = bs_content.find("a", text="Citations")
        
        if not url:
            print("No Citations data.")
        
        else:
            url = urlparse.urljoin(self.SITE_URL, url["href"])
            
            bs_content = self._get_bs_content(url)
            table = bs_content.find("table", {"class": "tableType3"})
            
            type_ = None
            data = []
            for tr in table.find_all("tr", recursive=False):
                tds = tr.find_all("td")
                
                if tds[0].text == "Type:":
                    type_ = tds[1].text.strip()
                    continue
                
                if tds[0].text == "Publication No.:" and type_ is not None:
                    data.append({
                        "Alias": alias,
                        "Document Type": type_,
                        "Reference": tds[1].text.strip(),
                        "Category": tds[2].text.strip() if len(tds) >= 3 else ""
                    })
    
                type_ = None
                
            self._saver.save_citations_data(data)

        
        print("")
        print("Getting Event history...")
        
        url = bs_content.find("a", text="Event history")
        
        if not url:
            print("No Event history data...")
        else:
            
            url = urlparse.urljoin(self.SITE_URL, url["href"])
            bs_content = self._get_bs_content(url)
            
            table = bs_content.find("table", id="row")
            
            for tr in table.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) != 3:
                    continue
                
                b_date = ""
                num = ""
                if tds[2].text.strip():
                    line = tds[2].text.strip()
                    num = re.search("\[[^\]]*\]", line).group(0)
                    b_date = self._normalize_date_str(line[:-len(num)])
                    b_date = re.sub("\s+", " ", b_date)
                
                event_data.append({
                    "Alias": alias,
                    "Input": input_field,
                    "Date": self._normalize_date_str(tds[0].text),
                    "Action": self._normalize_date_str(tds[1].text),
                    "European Patent Bulletin date": b_date,
                    "Issue number": num,
                })
                
            self._saver.save_evt_history_data(event_data)
        
        
        print("")
        print("Getting Documents...")
        url = bs_content.find("a", text="All documents")
        
        if not url:
            print("No Documents data.")
            return
        
        url = urlparse.urljoin(self.SITE_URL, url["href"])
        
        bs_content = self._get_bs_content(url)
        table = bs_content.find("table", id="row")
    
        data = []
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) != 5:
                continue
            
            link = tds[2].find("a")["href"]
            doc_id = re.search("documentId=([^&]*)", link).group(1)
            app_num = re.search("number=([^&]*)", link).group(1)
            
            data.append({
                "Alias": alias,
                "Date": self._normalize_date_str(tds[1].text.strip()),
                "Document type": tds[2].text.strip(),
                "Number of pages": tds[4].text.strip(),
                "Procedure": tds[3].text.strip(),
                "Link": "https://register.epo.org/application?showPdfPage=all" \
                    "&documentId=%s&appnumber=%s" % (doc_id, app_num,)
            })
                
        self._saver.save_documents_data(data)
        
        if not self._do_download:
            print("Download is turned off.")
            return
        
        print("Downloading files...")
        
        files_dir = os.path.dirname(os.path.realpath(__file__))
        files_dir = os.path.join(files_dir, "../../Output/%s" % alias)
        
        try:
            os.stat(files_dir)
        except:
            os.mkdir(files_dir)
            
        for doc, file_no in zip(data, range(1, len(data)+1)):
            filename = fs.clean_filename(doc["Document type"])
            filename = "%d - %s.pdf" % (file_no, filename)
            
            print("Downloading file number %d: %s..." %
                                                (file_no, filename))
            
            src = doc["Link"]
                
            self._fetcher.download_file(src,
                os.path.join(files_dir.strip(), filename))
        


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    