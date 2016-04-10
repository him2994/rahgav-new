import re
import os
from datetime import datetime
from bs4 import BeautifulSoup
from utils.simple_requests_fetcher import SimpleRequestsFetcher
from utils import fs


try:
    # Pyhton2
    import urlparse
except ImportError:
    # Python3
    import urllib.parse as urlparse


class SiteFIProcessor:

    HOST = "patent.prh.fi"
    SITE_URL = "http://patent.prh.fi"


    def __init__(self, saver, requests_per_minute=5,
            max_proxy_use_number=15, do_download=True, proxy_list=None):
        print("Init [FIA, FIP] processor...")

        self._saver = saver
        self._do_download = do_download

        self._fetcher = SimpleRequestsFetcher(requests_per_minute,
                        max_proxy_use_number, proxy_list=proxy_list,
                        use_session=True, init_fetcher_func=self._init_fetcher)

        self._fetcher.update_headers({ "Host": self.HOST })



    def _get_bs_content(self, url):
        content = self._fetcher.get_content(url)
        return BeautifulSoup(content)


    def _post_bs_content(self, url, data):
        content = self._fetcher.post_content(url, data)
        return BeautifulSoup(content)


    def process_number(self, number, number_type, alias, *args, **kwargs):

        if number_type in ("FIA", "FIP"):
            self._process_number(number, number_type, alias)

        else:
            raise Exception("Unknown number type: %s" % number_type)



    def _init_fetcher(self, r_fetcher):
        data = {
                "Etsi1": "Etsi+/+Search",
                "Lng": "ENG",
            }
        url = "http://patent.prh.fi/patinfo/default2.asp"
        r_fetcher.post(url, data)



    def _element_to_str(self, element):

        def _normalize_date_str(date_str):
            try:
                date = datetime.strptime(date_str, '%d.%m.%Y')
                date_str = date.strftime("%d/%m/%Y")
            except:
                pass

            return date_str


        content = element.decode_contents(formatter=None)
        content = content.replace("<br/>", "\r\n")
        content = content.replace("&nbsp;", " ")
        content = re.sub("<[^>]*>", "", content)
        return _normalize_date_str(content.strip())


    def _get_tag_content(self, tag):
        content = tag.decode_contents(formatter=None)
        content = re.sub("\r?\n", "", content)
        content = content.replace("<br/>", "\r\n").replace("<BR/>", "\r\n")
        content = content.replace("&nbsp;", " ")
        content = re.sub("<[^>]*>", " ", content).strip()


    def _process_number(self, number, number_type, alias):
        print("Processing number: %s (%s)" % (number, number_type))


        payload = self.BIG_POST.copy()
        if number_type == "FIP":
            payload["idpatent"] = number
        elif number_type == "FIA":
            payload["extidappli"] = number
        else:
            raise Exception("Unknown number type: %s." % number_type)

        # getting application number
        self._fetcher.get("http://patent.prh.fi/patinfo/default2.asp")

        bs_content = self._post_bs_content(
            urlparse.urljoin(self.SITE_URL, "/patinfo/tulos.asp"), payload)


        found_link = False
        for link in bs_content.find_all("a"):
            if "JavaScript:Katso('tiedot.asp'" in link["href"]:
                match = re.search("'([^']*)','([^']*)','([^']*)',(\d+)",
                                                                link["href"])
                found_link = True
                break

        if not found_link:
            if "No search result" in str(bs_content):
                raise Exception("Server says: No search result")

            raise Exception("Failed to find link to the data page")


        # main data
        print("")
        print("Getting main data...")

        url_template = "/patinfo/%s?NroParam=%s&NID=&offset=&ID=%s&Inx=%s"
        url = urlparse.urljoin(self.SITE_URL, url_template % match.groups())

        bs_content = self._get_bs_content(url)

        data = {
                "Alias": alias,
            }

        for tr in bs_content.find_all("tr"):
            tds = tr.find_all("td", { "class": "luettelo" }, recursive=False)

            if not tds or len(tds) != 2:
                continue

            data[tds[0].text.strip()] = self._element_to_str(tds[1])


        if "Parent application:" not in data or \
                not data["Parent application:"]:
            if "Stock application:" in data:
                data["Parent application:"] = data["Stock application:"]

        self._saver.save_main_data(data)

        # setting up input field
        input_field = "%s (%s)" % (number, number_type)


        print("")
        print("Getting history...")

        link = bs_content.find("a", {"href": re.compile("toimenpide.asp.*")})
        if not link:
            print("No history data.")

        else:
            url = urlparse.urljoin(self.SITE_URL, "/patinfo/")
            url = urlparse.urljoin(url, link["href"])

            data = []
            bs_content = self._get_bs_content(url)


            table1 = bs_content.find("table",
                                    { "cellpadding": "3", "width": "769" })
            table2 = None
            for t in bs_content.find_all("table",
                                        { "cellpadding": "3", "width": "770" }):
                td = t.find("td")
                if not td:
                    continue

                if "Asiakirjan" in td.text:
                    table2 = t
                    break

            for table in (table1, table2):
                if not table:
                    continue

                for tr in table.find_all("tr"):
                    if tr.has_attr("bgcolor"):
                        continue # it's a caption

                    tds = tr.find_all("td", { "class": "luettelo" })

                    if len(tds) != 2:
                        continue

                    data.append({
                        "Alias": alias,
                        "Input": input_field,
                        "Date": self._element_to_str(tds[0]),
                        "Action": tds[1].text.strip(),
                    })

            self._saver.save_evt_history_data(data)



            # pto event
            data = []
            table = bs_content.find("table",
                                    { "cellpadding": "3", "width": "770" })

            for tr in table.find_all("tr"):
                if tr.has_attr("bgcolor"):
                    continue # it's a caption

                tds = tr.find_all("td", { "class": "luettelo" })

                if len(tds) != 4:
                    continue
                
                data.append({
                    "Alias": alias,
                    "Input": input_field,
                    "Viraston päätöksen lähettämispvm":self._element_to_str(tds[0]),
                    "Hakijan määräaika vastata": self._element_to_str(tds[1]),
                    "Hakijan vastauspvm": self._element_to_str(tds[2]),
                    "Kirjeen nimi": tds[3].text.strip(),
                })

            self._saver.save_pto_event_data(data)


        print("")
        print("Getting fees due (within 6 months)...")

        link = bs_content.find("a", {"href": re.compile("maksutiedot.asp.*")})
        if not link:
            print("No info about fee dues.")

        else:

            url = urlparse.urljoin(self.SITE_URL, "/patinfo/")
            url = urlparse.urljoin(url, link["href"])

            bs_content = self._get_bs_content(url)

            if "Ei maksutietoja" in str(bs_content):
                print("No data about fee dues.")
            else:

                data = []
                table = bs_content.find("table",
                                        { "width": "770", "cellpadding": "3" })

                for tr in table.find_all("tr"):
                    if tr.has_attr("bgcolor"):
                        continue # it's a caption

                    tds = tr.find_all("td", { "class": "luettelo" })

                    if len(tds) == 0:
                        continue

                    data.append({
                        "Alias": alias,
                        "Input": input_field,
                        "Due Date": self._element_to_str(tds[0]),
                        "The sum of [EUR]": tds[1].text.strip(),
                        "Payment Type": tds[2].text.strip(),
                        "Payment reference": tds[3].text.strip(),
                        "Account Number": tds[4].text.strip(),
                        "Payment In order No.": tds[5].text.strip(),
                        "Customer reference": tds[6].text.strip(),
                    })

                self._saver.save_fees_data(data)


        print("")
        print("Getting documents data...")

        link = bs_content.find("a", text=re.compile(" *Documents *"))

        if not link:
            print("No documents.")

        else:
            bs_content = self._get_bs_content(link["href"])

            if "No public documents found in document archive" in \
                    str(bs_content):
                print("No public documents found in document archive")
                return

            if "Application documents are not public" in str(bs_content):
                print("Application documents are not public")
                return

            data = []
            form = bs_content.find("form", { "name": "documents"})
            for tr in form.find("table", { "cellpadding": "3"})\
                                                        .find_all("tr")[1:]:
                tds = tr.find_all("td", { "class": "luettelo" })

                if len(tds) == 0:
                    continue

                src = tds[3].find("a")["href"].replace("public-doc.jsp", "public-doc-pdf.jsp")
                docs_url = urlparse.urljoin(self.SITE_URL, "/patdocs/")
                src = urlparse.urljoin(docs_url, src)

                data.append({
                        "Alias": alias,
                        "Date": self._element_to_str(tds[1]),
                        "Number of pages": tds[2].text.strip(),
                        "Document type": tds[3].text.strip(),
                        "Link": src,
                    })

            print("Got this number of documents: %d." % len(data))
            self._saver.save_documents_data(data)

            print("")
            if not self._do_download:
                print("Download turned off.")
                return

            print("Downloading files...")


            files_dir = os.path.dirname(os.path.realpath(__file__))
            files_dir = os.path.join(files_dir, "../Output/%s" % alias)

            try:
                os.stat(files_dir)
            except:
                os.mkdir(files_dir)

            for link, file_no in zip((row["Link"] for row in data),
                                                    range(1, len(data)+1)):

                filename = fs.clean_filename(data[file_no-1]["Document type"])

                filename = "%d - %s.pdf" % (file_no, filename)

                print("Downloading file number %d: %s..." %
                                                    (file_no, filename))
                src = link
                self._fetcher.download_file(src,
                                        os.path.join(files_dir, filename))



    BIG_POST = {
        "TpPat": "1,2,3",
        "TpHM": "8,9,10",
        "TpSPC": "6,7",
        "extidappli": "",
        "mnuextidappli": "",
        "extidappli2": "",
        "idpatent": "",
        "mnuidpatent": "",
        "idpatent2": "",
        "tuote": "",
        "peruspatentti": "",
        "myyntilupa": "",
        "title": "",
        "mnutitle": " ",
        "title2": "",
        "rbtitle": "AND",
        "engtitle": "",
        "mnuengtitle": " ",
        "engtitle2": "",
        "rbengtitle": "AND",
        "pctno": "",
        "rbpctno": "AND",
        "mnupctno": "",
        "pctno2": "",
        "noprio": "",
        "mnunoprio": "",
        "noprio2": "",
        "rbnoprio": "AND",
        "hakpvm1": "",
        "hakpvm2": "",
        "rbhakpvm": "AND",
        "dtoriginal1": "",
        "dtoriginal2": "",
        "rboriginalpvm": "AND",
        "pvm1": "",
        "pvm2": "",
        "rbpvm": "AND",
        "patpvm1": "",
        "patpvm2": "",
        "rbpatpvm": "AND",
        "ipcclass": "",
        "mnuipcclass": "",
        "ipcclass2": "",
        "rbipcclass": "AND",
        "fnowner": "",
        "nmowner": "",
        "mnunmowner": "",
        "nmowner2": "",
        "rbnmowner": "AND",
        "fninventor": "",
        "mnufninventor": "",
        "fninventor2": "",
        "rbfninventor": "AND",
        "nminventor": "",
        "mnunminventor": "",
        "nminventor2": "",
        "rbnminventor": "AND",
        "AgentId": "",
        "AgentId2": "",
        "mnuAgentId": "",
        "claim": "",
        "etsi": "  Search  ",
        "PP": "0",
        "Haku": "FIRST",
        "DateCheck": "",
        "Lng": "",
        "Etsi1": "Etsi / Search",
    }
