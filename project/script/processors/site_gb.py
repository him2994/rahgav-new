import os
import urllib
import re

from utils.simple_requests_fetcher import SimpleRequestsFetcher
from processors import CapchaRequiredException
from utils.sleeper import Sleeper
from utils import fs


try:
    # Pyhton2
    import urlparse
except ImportError:
    # Python3
    import urllib.parse as urlparse
    
from datetime import datetime
from bs4 import BeautifulSoup


class SiteGBProcessor:
    
    HOST = "www.ipo.gov.uk"
    SITE_URL = "http://www.ipo.gov.uk"

    PUBLICATION_URL = "http://www.ipo.gov.uk/p-ipsum/Case/PublicationNumber/"
    APPLICATION_URL = "http://www.ipo.gov.uk/p-ipsum/Case/ApplicationNumber/"    
    
    
    
    def __init__(self, saver, requests_per_minute=5,
                max_proxy_use_number=15, do_download=True, proxy_list=None):
        print("Init [GBA, GBP] processor...")
        
        self._sleeper = Sleeper(interval=3)
        
        self._saver = saver
        self._do_download = do_download
        
        self._fetcher = SimpleRequestsFetcher(requests_per_minute,
                max_proxy_use_number, use_session=False, proxy_list=proxy_list)
        
        self._fetcher.update_headers({ "Host": self.HOST })
    
    
    
    def _get_bs_content(self, url):
        # for some reason some pages are not retrieved without '/' at the end 
        content = self._fetcher.get_content(url + '/')
        
        if "checks that ensure you are a genuine user" in str(content):
            try:
                print("SITE REQUIRES CAPTCHA, TRYING TO CHANGE PROXY")
                self._fetcher.change_proxy()
                return self._get_bs_content(url)
            except Exception as e:
                raise CapchaRequiredException("Site requires captcha and"
                        " failed to change proxy because: %s." % str(e))
        
        return BeautifulSoup(content)
    
    
    
    def process_number(self, number, number_type, alias, *args, **kwargs):
        if number_type in ("GBA", "GBP"):
            self._process_number(number, number_type, alias)
            
        else:
            raise Exception("Unknown number type: %s" % number_type)
    
    
    
    def _normalize_date_str(self, date_str):
        try:
            date = datetime.strptime(date_str, '%d %B %Y')
            date_str = date.strftime("%d/%m/%Y")
        except:
            pass
        
        return date_str
    
    
    
    def _normalize_dates(self, input_dict):
        """ Converts all dates in the input dictionary into format:
            "dd/mm/yyyy"
        """
        
        for key in input_dict.keys():
            input_dict[key] = self._normalize_date_str(input_dict[key])
        
        return input_dict
        
    
    
    def _extract_tag_text(self, key, bs_wrapped_tag):
        str_data = ''
        
        for child in bs_wrapped_tag:
            
            try:
                if child.name == 'br':
                    str_data += "\r\n"
                    '''
                    if str_data[-1] != " ":
                        str_data += "; "
                    elif str_data[-1] != "\n":
                        str_data += "\r\n"
                    ''' 
            except:
                str_data += self._normalize_date_str(str(child).strip())
        
        return str_data



    def _get_info_from_horizontal_table(self, bs_content, **kwargs):
        
        #id_ = "MainContent_BibliographyViewUserControl_BibliographyTable"
        tag_table = bs_content.find("table", {"class": "BibliographyTable"})
        result = {}
        
        td_titles = tag_table.find_all("td", { "class" : "CaseDataItemHeader"})
        td_data = tag_table.find_all("td", { "class" : "CaseDataItemValue"})
        
        for data in zip(td_titles, td_data):
            key = data[0].text.strip()
            result[key] = self._extract_tag_text(key, data[1])
        
        result.update(kwargs)
        self._normalize_dates(result)

        return result
    
    
    
    def get_info_from_vertical_table(self, bs_content, table_id, **kwargs):
        result = []
        
        table_tag = bs_content.find(id=table_id)
        captions = []
        for th in table_tag.find_all("th"):
            captions.append(th.text.strip())
        
        for tr in table_tag.find_all("tr", { "class": ["even", "odd"] }):
            new_row = kwargs.copy()
            for caption, td in zip(captions, tr.find_all("td")):
                new_row[caption] = self._normalize_date_str(td.text.strip())
                
            result.append(new_row)
            
        return result
        
    
    

    def _process_number(self, number, number_type, alias):
        
        if number_type == "GBA":
            print("Processing application number: %s (%s)" %
                                                        (number, number_type))
            url = os.path.join(self.APPLICATION_URL, number)
        elif number_type == "GBP":
            print("Processing publication number: %s (%s)" %
                                                        (number, number_type))
            url =  os.path.join(self.PUBLICATION_URL, number)
        else:
            raise Exception("Unknown number type: %s." % number_type) 
        
        self._sleeper.next_step()
        
        # GETTING MAIN DATA
        print("Getting main data...")
        bs_content = self._get_bs_content(url)
        error_msg = bs_content.find("p", id="AsyncErrorMessage")
        
        
        if error_msg and error_msg.text.strip():
            error_msg = error_msg.text
            if re.search("Please enter a valid [^ ]+ number\.", error_msg):
                raise Exception("Not a valid number: %s (%s)" %
                                                        (number, number_type))
            
            if "case was not found" in error_msg:
                raise Exception("A case was not found matching this number")
            
            raise Exception("Site message: %s." % error_msg)
        
        '''
        page_title = bs_content.find("title").text
        if "Intellectual Property Office" not in page_title:
            raise Exception("Got page with this title: \"%s\""
                " (error messages come to foreign proxies in other languages)" %
                    page_title)
        '''
        
        data = self._get_info_from_horizontal_table(bs_content, Alias=alias)
        
        # correcting data
        key1 = "Grant of Patent (Notification under Section 18(4)):"
        key2 = "Publication of notice in the Patents and Designs Journal " \
                                                            "(Section 25(1)):"
        key_source = "Grant Date"
        
        if key_source in data:
            try:
                if key1 not in data or not data[key1]:
                    pattern = key1.replace("(", "\(").replace(")", "\)")
                    pattern += "\r\n(\d+/\d+/\d+)"
                    match = re.search(pattern, data[key_source])
                    data[key1] = match.group(1)
            except:
                pass
            
            try:    
                if key2 not in data or not data[key2]:
                    pattern = key2.replace("(", "\(").replace(")", "\)")
                    pattern += "\r\n(\d+/\d+/\d+)"
                    match = re.search(pattern, data[key_source])
                    data[key2] = match.group(1)
            except:
                pass
        
        #print("Got this main data:")
        #print(data)
        self._saver.save_main_data(data)
        
        # GETTING FORMS FIELD DATA
        id_ = "SideContent_caseViewLinkPanel1_FormsLinkListItem_ViewHyperLink"
        a_formsfield = bs_content.find(id=id_)
        
        print("") # empty row for  better view
        if a_formsfield is not None:
            print("Getting Forms Field data...")
            formfields_url = urlparse.urljoin(
                                            self.SITE_URL, a_formsfield['href'])
            bs_content = self._get_bs_content(formfields_url)
            
            data = self.get_info_from_vertical_table(bs_content,
                "MainContent_FiledFormsViewUserControl_FormsTable", Alias=alias)
            print("Got number of rows: %d" % len(data))
            self._saver.save_formfields_data(data)
        else:
            print("No Forms Field data found.")
            
        
        # GETTING CITATIONS DATA
        id_="SideContent_caseViewLinkPanel1_CitationsLinkListItem_ViewHyperLink"
        a_formsfield = bs_content.find(id=id_)
        
        print("") # empty row for  better view
        if a_formsfield is not None:
            print("Getting Citations data...")
            formfields_url = urlparse.urljoin(
                                            self.SITE_URL, a_formsfield['href'])
            bs_content = self._get_bs_content(formfields_url)
            
            if "There are no citations to be viewed for this case." in \
                    str(bs_content):
                print("There are no citations to be viewed for this case.")
            else:
                data = self.get_info_from_vertical_table(
                    bs_content,
                    "MainContent_CitationsViewUserControl_PatentCitationsTable",
                    Alias=alias)
                print("Got number of rows: %d" % len(data))
                self._saver.save_citations_data(data)
        else:
            print("No Citations data found.")
        
        
        # GETTING DOCUMENTS DATA
        has_documents = True
        id_="SideContent_caseViewLinkPanel1_DocumentsLinkListItem_ViewHyperLink"
        a_documents = bs_content.find(id=id_)
        print("") # empty row for  better view
        if a_documents is not None:
            print("Getting Documents data...")
            documents_url = urlparse.urljoin(self.SITE_URL, a_documents['href'])
            bs_content = self._get_bs_content(documents_url)
            
            data = self.get_info_from_vertical_table(
                bs_content,
                "DossierTable",
                Alias=alias)
            
            links = bs_content.find_all("a", title="Click to view "
                            "this document in PDF format (opens in new window)")
            for d, l in zip(data, links):
                d["Link"] = urllib.parse.urljoin(documents_url +'/', l["href"])
            
            print("Got number of rows: %d" % len(data))
            self._saver.save_documents_data(data)
        else:
            has_documents = False
            print("No Documents data found.")
        
        
        if not has_documents:
            return
        
        
        if not self._do_download:
            print("") # empty line
            print("File download is turned off.")
            return
            
            
        print("Downloading files: ...")
        
        links = bs_content.find_all("a", title="Click to view "
                            "this document in PDF format (opens in new window)")
        
        if len(links) == 0:
            print("No links to download.")
            return
        
        files_dir = os.path.dirname(os.path.realpath(__file__))
        files_dir = os.path.join(files_dir, "../Output/%s" % alias)
        
        try:
            os.stat(files_dir)
        except:
            os.mkdir(files_dir)     
        
        tr_tags = bs_content.find("table", id="DossierTable").find_all("tr")
        
        file_no = 0
        for a, tr in zip(links, tr_tags[1:]):
            file_no += 1
            
            src = urllib.parse.urljoin(documents_url +'/', a["href"])
            
            _, file_extension = os.path.splitext(a["href"])
            filename = fs.clean_filename(tr.find_all("td")[1].text)
            filename = "%d - %s%s" % (file_no, filename, file_extension)
            
            print("Downloading file number %d: %s..." % (file_no, filename))
            
            self._fetcher.download_file(src, os.path.join(files_dir, filename))
            
            #self._fetcher.do_interval()
            #urllib.request.urlretrieve(src, os.path.join(files_dir, filename))
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    