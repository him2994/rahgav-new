from bs4 import BeautifulSoup


class SiteBase:

    
    def _get_bs_content(self, url):
        content = self._fetcher.get_content(url)
        return BeautifulSoup(content)
    
    
    def _post_bs_content(self, url, data):
        content = self._fetcher.post_content(url, data)
        return BeautifulSoup(content)