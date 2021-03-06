
import pytest
import os

from masonite import env
from masonite.environment import LoadEnvironment

LoadEnvironment()



from masonite.app import App
from masonite.exceptions import DriverNotFound
from masonite.view import View
from masonite.managers.MailManager import MailManager
from masonite.drivers.MailSmtpDriver import MailSmtpDriver as MailDriver
from masonite.drivers.MailMailgunDriver import MailMailgunDriver as Mailgun
from config import mail

if os.getenv('MAILGUN_SECRET'):

    class UserMock:
        pass

    class TestMailgunDriver:

        def setup_method(self):
            self.app = App()
            self.app.bind('Container', self.app)

            self.app.bind('Test', object)
            self.app.bind('MailConfig', mail)
            self.app.bind('MailSmtpDriver', MailDriver)
            self.app.bind('MailMailgunDriver', Mailgun)
            self.app.bind('View', View(self.app))

        def test_mailgun_driver(self):
            user = UserMock
            user.email = 'test@email.com'

            assert MailManager(self.app).driver('mailgun').to(user).to_address == 'test@email.com'

        def test_mail_renders_template(self):
            assert 'MasoniteTesting' in MailManager(self.app).driver('mailgun').to(
                'idmann509@gmail.com').template('mail/welcome', {'to': 'MasoniteTesting'}).message_body

        def test_mail_sends_with_queue_and_without_queue(self):
            if env('RUN_MAIL'):
                assert MailManager(self.app).driver('mailgun').to('idmann509@gmail.com').send('test queue') == None
                assert MailManager(self.app).driver('mailgun').queue().to('idmann509@gmail.com').send('test queue') == None
