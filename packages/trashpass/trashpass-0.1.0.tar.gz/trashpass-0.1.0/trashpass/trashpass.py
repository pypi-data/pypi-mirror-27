import requests
import re
from bs4 import BeautifulSoup

class Trashpass:
    def __init__(self):
        """
        initial session from trash-mail
        """
        self.session = {}

    def refresh_session(self):
        url = "https://www.trash-mail.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0", 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
            "Accept-Language": "en-US,en;q=0.5", 
            "Accept-Encoding": "gzip, deflate", 
            "DNT": "1", 
            "Upgrade-Insecure-Requests": "1"
        }
        response_cookies = requests.get(url, headers=headers).headers["set-cookie"]
        PHPSESSID = re.search(
            r"PHPSESSID=(\w+);", response_cookies).group(1)     
        self.session = {"PHPSESSID" :  PHPSESSID}

    def read_inbox(self):
        """ 
        send GET request to /inbox/ and parsing it into JSON
        """
        url = "https://www.trash-mail.com/inbox/"
        cookies = self.session
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0", 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
            "Accept-Language": "en-US,en;q=0.5", 
            "Accept-Encoding": "gzip, deflate", 
            "Referer": "https://www.trash-mail.com/inbox/", 
            "DNT": "1", 
            "Upgrade-Insecure-Requests": "1"}
        req = requests.get(url, headers=headers, cookies=cookies)
        
        soup = BeautifulSoup(req.text, 'html.parser')
        
        messages = {}

        messages_parsed = soup.find_all("td", "message-td")

        for m in messages_parsed:
            index = m.a['nr']
            messages[index] = {
                'from' : m.find(id="message-from-{}".format(index)).string,
                'subject' : m.find(id="message-subject-{}".format(index)).string,
                'date' : m.find(id="message-date-{}".format(index)).string,
                'text' : m.find(id="message-text-{}".format(index)).string
            }

        return messages

    
    def refresh_inbox(self):
        """
        send POST request to /refresh-inbox/
        """
        url = "https://www.trash-mail.com/refresh-inbox/"
        cookies = self.session
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0", 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
            "Accept-Language": "en-US,en;q=0.5", 
            "Accept-Encoding": "gzip, deflate", 
            "Referer": "https://www.trash-mail.com/inbox/", 
            "Content-Type": "multipart/form-data; boundary=---------------------------887797712456155301704285384", 
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1"
        }
        mail_data="-----------------------------887797712456155301704285384--\r\n"
        requests.post(url, headers=headers, cookies=cookies, data=mail_data)
    
    def set_target(self, mail_address):
        """
        refresh session and send POST request to /inbox/ containing email parameter
        """
        self.refresh_session()
        url = "https://www.trash-mail.com/inbox/"
        cookies = self.session
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
            "Accept-Language": "en-US,en;q=0.5", 
            "Accept-Encoding": "gzip, deflate", 
            "Referer": "https://www.trash-mail.com/inbox/", 
            "Content-Type": "multipart/form-data; boundary=---------------------------29685118913426370411117460603", 
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1"
        }
        mail_data = "-----------------------------29685118913426370411117460603\r\nContent-Disposition: "  \
                    "form-data; name=\"form-postbox\"\r\n\r\n{}\r\n-----------------------------296851189" \
                    "13426370411117460603\r\nContent-Disposition: form-data; name=\"form-domain\"\r\n\r\n" \
                    "trash-mail.com---0\r\n-----------------------------29685118913426370411117460603\r\n" \
                    "Content-Disposition: form-data; name=\"form-password\"\r\n\r\n\r\n------------------" \
                    "-----------29685118913426370411117460603--\r\n".format(mail_address)
        requests.post(url, headers=headers, cookies=cookies, data=mail_data)
