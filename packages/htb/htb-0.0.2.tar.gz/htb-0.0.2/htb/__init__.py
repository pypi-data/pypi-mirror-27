import requests
from bs4 import BeautifulSoup

class HTB:

    def __init__(self, email, password):
        self.session = requests.Session()
        login_page = self.session.get('https://www.hackthebox.eu/login').text
        login_parse = BeautifulSoup(login_page, 'html.parser')
        csrf_token = login_parse.find('meta',  {'name': 'csrf-token'})['content']
        post_data = {'_token': csrf_token, 'email': email, 'password': password}
        logged_in_page = self.session.post('https://www.hackthebox.eu/login', data=post_data).text
        if 'These credentials do not match our records.' in logged_in_page:
            raise Exception('Login Failed')

    def _get_machines(self, url):
        page = self.session.get(url).text
        parse = BeautifulSoup(page, 'html.parser')
        table = parse.find('table')
        # Ignore the first entry, it's the header
        entries = table.findAll('tr')[1:]
        machines = {}
        for entry in entries:
            name, machine = HTB.__parse_machine_row(entry)
            machines[name] = machine
        return machines

    def get_active_machines(self):
        return self._get_machines('https://www.hackthebox.eu/home/machines/list')

    def get_retired_machines(self):
        return self._get_machines('https://www.hackthebox.eu/home/machines/retired')

    @staticmethod
    def __parse_machine_row(soup_tr):
        machine = {}
        soup_tds = soup_tr.findAll('td')
        name = soup_tds[0].find('a').getText()
        machine['id'] = soup_tds[0].find('a')['href'].split('/')[-1]
        machine['author'] = soup_tds[1].find('a').getText()
        machine['os'] = soup_tds[2].getText().strip()
        machine['ip'] = soup_tds[3].getText().strip()
        return name, machine
