from requests import Session
from bs4 import BeautifulSoup
import time
from domeventlistener.utils import unidiff_output


EVENT_CHANGED = 'changed'
EVENT_EMPTIED = 'emptied'


class Listener(object):

    def __init__(
        self,
        domain,
        query,
        event_handler=None,
        read_element=None,
        write_element=None
    ):
        self.domain = domain
        self.query = query
        self.event_handler = event_handler
        self.read_element = read_element
        self.write_element = write_element
        self.session = Session()
        self.element_str = str(self.find_element())

    def find_element(self):
        resp = self.session.get(self.domain)
        document = BeautifulSoup(resp.text, 'html.parser')

        return document.select(self.query)

    def read_element_str(self):
        ''' fetch stored old element '''

        return self.element_str if not self.read_element\
            else self.read_element()

    def write_element_str(self, element_str):
        ''' write to store '''

        if not self.write_element:
            self.element_str = str(element_str)
        else:
            return self.write_element(element_str)

    def poll_change(self):
        ''' Returns a tuple (has_changed, new_element_str) '''

        new_element = self.find_element()

        return str(new_element) != self.read_element_str(), str(new_element)

    def start(self, sleep_time=5):
        while True:
            has_changed, new_element_str = self.poll_change()

            if has_changed:
                if self.event_handler:
                    self.event_handler(
                        EVENT_CHANGED if new_element_str else EVENT_EMPTIED,
                        unidiff_output(
                            self.read_element_str(),
                            new_element_str
                        )
                    )

                self.write_element_str(new_element_str)
                time.sleep(sleep_time)
