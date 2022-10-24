import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineIconListItem

from database import DataBase1
from databaseClient import DataBaseClient

Window.size = (350, 550)


class LoginScreen(Screen):
    email = ObjectProperty(None)
    passw = ObjectProperty(None)
    n = ObjectProperty(None)

    def loginBtn(self):

        if db.validate(self.ids.email.text, self.ids.passw.text) == VALID:
            LoginScreen.email = self.ids.email.text
            LoginScreen.passw = self.ids.passw.text

            self.manager.current = 'menu'

        else:
            close = MDFlatButton(text="Kapat", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Geçersiz kullanıcı adı veya şifre", size_hint=(0.5, 1),
                                   buttons=[close])
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
        self.manager.current = 'login'


class MenuScreen(Screen):
    """"""

    def logout(self):
        self.manager.current = 'login'

    def addClient(self):
        self.manager.current = 'add'

    def clientList(self):
        self.manager.current = 'list'

    def send(self):
        self.manager.current = 'message'

    def settings(self):
        self.manager.current = 'set'


class CreateScreen(Screen):
    def createAccount(self):
        if self.passw.text != self.passw2.text:
            close = MDFlatButton(text="Kapat", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Şifre onayı yanlış", size_hint=(0.5, 1),
                                   buttons=[close])
            self.dialog.open()

        elif self.n.text != "" and self.email.text != "" and \
                self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if db.add_user(self.n.text, self.email.text, self.passw.text) == VALID:

                self.manager.current = 'login'
            else:
                close = MDFlatButton(text="Kapat", on_release=self.close_dialog)
                self.dialog = MDDialog(title="Böyle hesap zaten var", size_hint=(0.5, 1),
                                       buttons=[close])
                self.dialog.open()
        else:
            close = MDFlatButton(text="Kapat", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Lütfen tüm girişleri geçerli\nbilgilerle doldurunuz", size_hint=(0.5, 1),
                                   buttons=[close])
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
        self.manager.current = 'create'


class AddClientScreen(Screen):
    """Müşteri ekleme"""

    def submit(self):
        userId = db.userId(LoginScreen.email, LoginScreen.passw)
        if self.n.text != "" and self.email.text != "" and \
                self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if dbc.add_client(self.n.text, self.surname.text,
                              self.email.text, self.tcno.text, self.telno.text, userId) == VALID:
                self.manager.current = 'menu'
            else:
                close = MDFlatButton(text="Kapat", on_release=self.close_dialog)
                self.dialog = MDDialog(title="Böyle hesap zaten var", size_hint=(0.5, 1),
                                       buttons=[close])
                self.dialog.open()

        else:
            close = MDFlatButton(text="Kapat", on_release=self.close_dialog)
            self.dialog = MDDialog(title="Lütfen tüm girişleri geçerli\nbilgilerle doldurunuz", size_hint=(0.5, 1),
                                   buttons=[close])
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
        self.manager.current = 'add'

    def dialogs(self):
        close = MDFlatButton(text="Kapat", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Müşteri başarıyla\neklendi", size_hint=(0.5, 1),
                               buttons=[close])
        self.dialog.open()


class SendMessage(Screen):
    """"""
    subject = ObjectProperty(None)
    fromm = ObjectProperty(None)
    to = ObjectProperty(None)
    text = ObjectProperty(None)

    def button(self):
        me = LoginScreen.email
        my_password = LoginScreen.passw
        you = self.to.text

        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject.text
        msg['From'] = me
        msg['To'] = you

        html = self.text.text
        part2 = MIMEText(html, 'html')

        msg.attach(part2)
        s = smtplib.SMTP_SSL('smtp.gmail.com')
        s.login(me, my_password)

        s.sendmail(me, you, msg.as_string())
        s.quit()

        close = MDFlatButton(text="Kapat", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Müşteriye mesaj gönderildi", size_hint=(0.5, 1),
                               buttons=[close])
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
        self.manager.current = 'menu'


class ClientsList(Screen):
    """"""
    def on_enter(self):
        self.remove()
        userId = db.userId(LoginScreen.email, LoginScreen.passw)
        arr = dbc.getClientsInfo(userId)
        for i in arr:
            self.ids.container.add_widget(
                ThreeLineIconListItem(text=f'{i[0]} {i[2]}',secondary_text = i[1],
                tertiary_text = i[4])
            )

    def remove(self):
        self.ids.container.clear_widgets()

class Setting(Screen):
    """"""
    n = ObjectProperty(None)

    email = ObjectProperty(None)
    password = ObjectProperty(None)
    def on_enter(self,*args):
        """"""
    def on_arrange_passw(self):
        id = db.userId(LoginScreen.email,LoginScreen.passw)
        db.update(id, self.password.text)
        LoginScreen.passw = self.password.text
    def on_arrange_email(self):
        id = db.userId(LoginScreen.email, LoginScreen.passw)
        db.updateE(id, self.email.text)
        LoginScreen.email=self.email.text
class WindowScreen(ScreenManager):
    pass


sm = WindowScreen()
db = DataBase1()
dbc = DataBaseClient()

VALID = 1
INVALID = -1
screens = [LoginScreen(name="login"), CreateScreen(name="create"), MenuScreen(name="menu"),
           AddClientScreen(name='add'), ClientsList(name='list'), SendMessage(name='message'),Setting(name="set")]
for screen in screens:
    sm.add_widget(screen)


class Client(MDApp):
    def build(self):
        return Builder.load_file("my.kv")


Client().run()
