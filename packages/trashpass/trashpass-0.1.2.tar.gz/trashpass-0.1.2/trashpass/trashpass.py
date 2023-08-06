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
            'DNT': '1',
            "Upgrade-Insecure-Requests": '1'
        }
        response_cookies = requests.get(
            url, headers=headers).headers['set-cookie']
        PHPSESSID = re.search(
            r"PHPSESSID=(\w+);", response_cookies).group(1)
        self.session = {'PHPSESSID': PHPSESSID}

    def read_inbox(self, start=1, end=3):
        """
        send GET request to /inbox/ and parsing it into JSON
        """
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
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1'
        }
        req = requests.get(url, headers=headers, cookies=cookies)
        mainmail = BeautifulSoup(req.text, 'html.parser')
        messages = {}
        messages_parsed = mainmail.find_all('td', 'message-td')
        singlemail_headers = {
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

        """
        visit every message and parse images and link
        """
        for m in messages_parsed:
            index = int(m.a['nr'])
            if index > end:
                continue
            elif index < start:
                break

            messages[index] = {
                'from': m.find(
                    id="message-from-{}".format(index)).text,
                'subject': m.find(
                    id="message-subject-{}".format(index)).text,
                'date': m.find(
                    id="message-date-{}".format(index)
                    ).text
            }
            url = (
                "https://www.trash-mail.com/en/mail/message/id/{}"
            ).format(index)
            req = requests.get(
                url, headers=singlemail_headers, cookies=self.session)
            singlemail = BeautifulSoup(req.text, 'html.parser')
            links = {}
            attachments = {}
            message_content = singlemail.find(class_='message-content')

            html_links = message_content.find_all('a')
            if html_links:
                link_id = 1
                for link in html_links:
                    if link.has_attr('href'):
                        links[link_id] = {
                            'title': link.text,
                            'url': link['href']
                        }
                        link_id += 1
                messages[index]['links'] = links

            html_attachments = singlemail.find_all('p', class_='attachment')
            if html_attachments:
                attachment_id = 1
                for att in html_attachments:
                    att = att.find('a')
                    if att.has_attr('href'):
                        attachments[attachment_id] = {
                            'title': att.text.lstrip(),
                            'url': att['href']
                        }
                        attachment_id += 1
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
