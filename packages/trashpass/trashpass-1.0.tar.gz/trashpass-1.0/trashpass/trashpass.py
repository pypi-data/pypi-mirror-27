import re
import requests
from bs4 import BeautifulSoup


class Trashpass(object):
    def __init__(self):
        """
        initial session from trash-mail
        """
        self.session = {}
        self.singlemail_headers = {
            'User-Agent': (
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0)"
                " Gecko/20100101 Firefox/57.0"
            ),
            'Accept': "text/html, */*; q=0.01",
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate",
            'Referer': "https://www.trash-mail.com/inbox/",
            'X-Requested-With': "XMLHttpRequest",
            'DNT': '1'
        }
        self.headers = {
            'User-Agent': (
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0)"
                " Gecko/20100101 Firefox/57.0"
            ),
            'Accept': (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,*/*;q=0.8"
            ),
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate",
            'Referer': "https://www.trash-mail.com/inbox/",
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1'
        }
        self.url = "https://www.trash-mail.com"

    def refresh_session(self):
        response_cookies = requests.get(
            self.url, headers=self.headers).headers['set-cookie']
        phpsessid = re.search(
            r"PHPSESSID=(\w+);", response_cookies).group(1)
        self.session = {'PHPSESSID': phpsessid}

    def read_inbox(self, start=1, end=3):
        """
        send GET request to /inbox/ and parsing it into JSON
        """
        mainmail = BeautifulSoup(
            requests.get(
                "{}/inbox".format(self.url),
                headers=self.headers,
                cookies=self.session
            ).text,
            'html.parser'
        )
        messages = {}

        """
        visit every message and parse images and link
        """
        for msg in mainmail.find_all('td', 'message-td'):
            index = int(msg.a['nr'])
            if index > end:
                continue
            elif index < start:
                break

            messages[index] = {
                'from': msg.find(
                    id="message-from-{}".format(index)).text,
                'subject': msg.find(
                    id="message-subject-{}".format(index)).text,
                'date': msg.find(
                    id="message-date-{}".format(index)
                    ).text
            }

            singlemail = BeautifulSoup(
                requests.get(
                    "{}/en/mail/message/id/{}".format(self.url, index),
                    headers=self.singlemail_headers,
                    cookies=self.session
                ).text,
                'html.parser'
            )
            links = {}
            attachments = {}
            message_content = singlemail.find(class_='message-content')

            chunks = message_content.find_all('a')
            if chunks:
                count_id = 1
                for link in chunks:
                    if link.has_attr('href'):
                        links[count_id] = {
                            'title': link.text,
                            'url': link['href']
                        }
                        count_id += 1
                messages[index]['links'] = links

            chunks = singlemail.find_all('p', class_='attachment')
            if chunks:
                count_id = 1
                for att in chunks:
                    att = att.find('a')
                    if att.has_attr('href'):
                        attachments[count_id] = {
                            'title': att.text.lstrip(),
                            'url': att['href']
                        }
                        count_id += 1
                messages[index]['attachments'] = attachments
            messages[index]['text'] = message_content.text

        return messages

    def refresh_inbox(self):
        """
        send POST request to /refresh-inbox/
        """
        url = "https://www.trash-mail.com/refresh-inbox/"
        cookies = self.session
        headers = {
            'User-Agent': (
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) "
                "Gecko/20100101 Firefox/57.0"
            ),
            'Accept': (
                "text/html,application/xhtml+xml,application/xml"";"
                "q=0.9,*/*;q=0.8"
            ),
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate",
            'Referer': "https://www.trash-mail.com/inbox/",
            'Content-Type': (
                "multipart/form-data; boundary=------------------"
                "---------887797712456155301704285384"
                ),
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1'
        }
        mail_data = (
            "-----------------------------88779771"
            "2456155301704285384--\r\n"
        )
        requests.post(url, headers=headers, cookies=cookies, data=mail_data)

    def set_target(self, mail_address):
        """
        refresh session and send POST request
        to /inbox/ containing email parameter
        """
        self.refresh_session()
        url = "https://www.trash-mail.com/inbox/"
        cookies = self.session
        headers = {
            'User-Agent': (
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0)"
                " Gecko/20100101 Firefox/57.0"
            ),
            'Accept': (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,*/*;q=0.8"
            ),
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate",
            'Referer': "https://www.trash-mail.com/inbox/",
            'Content-Type': (
                "multipart/form-data; boundary=----------------"
                "-----------29685118913426370411117460603"
            ),
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1'
        }
        mail_data = (
            "-----------------------------296851189134263704111174"
            "60603\r\nContent-Disposition: form-data; name=\"form-"
            "postbox\"\r\n\r\n{}\r\n-----------------------------2"
            "9685118913426370411117460603\r\nContent-Disposition: "
            "form-data; name=\"form-domain\"\r\n\r\ntrash-mail.com"
            "---0\r\n-----------------------------2968511891342637"
            "0411117460603\r\nContent-Disposition: form-data; name"
            "=\"form-password\"\r\n\r\n\r\n-----------------------"
            "------29685118913426370411117460603--\r\n"
        ).format(mail_address)
        requests.post(url, headers=headers, cookies=cookies, data=mail_data)
