from common import BaseTest
from c7n.credentials import SessionFactory


class SessionSubscriberTest(BaseTest):

    def test_session(self):
        factory = SessionFactory('us-east-1')
        found = []

        def subscriber(s):
            found.append(s)

        factory.set_subscribers([subscriber])
