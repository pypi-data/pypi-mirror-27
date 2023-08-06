from requests import Session
from bs4 import BeautifulSoup
import time
from domeventlistener.utils import unidiff_output


EVENT_CHANGED = 'changed'


class Listener(object):

    def __init__(
        self,
        domain,
        query,
        event_handler,
        read_element=None,
        write_element=None
    ):
        self.domain = domain
        self.query = query
        self.event_handler = event_handler
        self.read_element = read_element
        self.write_element = write_element
        self.session = Session()
        self.element_str = None

    def read_element_str(self):
        if not self.read_element:
            return str(self.element_str)

        return self.read_element

    def write_element_str(self, element_str):
        if not self.write_element:
            self.element_str = str(element_str)
        else:
            return self.write_element(element_str)

    def on_event(self, event_type, data):
        return self.event_handler(event_type, data)

    def start(self, sleep_time=5):
        while True:
            resp = self.session.get(self.domain)
            document = BeautifulSoup(resp.text, 'html.parser')
            _element = document.select(self.query)

            if str(_element) != self.read_element_str():
                self.on_event(
                    EVENT_CHANGED,
                    unidiff_output(self.read_element_str(), str(_element))
                )

            self.write_element_str(str(_element))
            time.sleep(sleep_time)
