from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import Qt, QThread, pyqtSlot

import time
import ctypes
import threading
from client import Client
from handlers import GuiReciever
from repo.server_repo import DbRepo
from repo.server_models import Base
import sys


class MyWindow(QtWidgets.QPushButton):
    def __init__(self):
        QtWidgets.QPushButton.__init__(self)

    def load_data(self, sp):
        for i in range(1, 11):
            time.sleep(0.1)
            sp.showMessage("Загрузка данных...{}%".format(i * 10), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom,
                           QtCore.Qt.black)
            QtWidgets.qApp.processEvents()


class AuthWindow(object):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        splash = QtWidgets.QSplashScreen(QtGui.QPixmap('img.jpg'))
        splash.showMessage("Загрузка данных...{}%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
        splash.show()
        QtWidgets.qApp.processEvents()
        window = MyWindow()
        window.load_data(splash)
        window = uic.loadUi('auth.ui')

        main_window = uic.loadUi('main.ui')
        main_window.show()
        main_window.hide()

        window.show()
        splash.finish(window)

        cl_list = []

        repo = DbRepo('server.db', Base)
        tess = repo.get_clients()
        for el in tess:
            cl_list.append(el.Name)

        def match(self):
            text = window.textEditMessage.toPlainText()
            print(text)
            print(cl_list)
            try:
                if cl_list.index(text):
                    ctypes.windll.user32.MessageBoxW(0, "Здравствуйте, {}".format(text), "Приветствие", 0)
                    print('hello')
                    # main_window.show()
                    print('yes')
                    window.close()
                    ter = MainWindow(text, main_window)
                    # ter()
            except Exception as e:
                print(e)
                print('Нет такого пользователя')
                ctypes.windll.user32.MessageBoxW(0, "Нет такого пользователя", "Ошибка", 0)

        window.pushOk.clicked.connect(match)
        quitAction = QtWidgets.QAction("Quit", None)
        quitAction.triggered.connect(app.quit)
        window.pushOk.addAction(quitAction)
        sys.exit(app.exec())


class MainWindow(object):
    def __init__(self, name, form):
        self.name = name
        self.window = form

        # def __call__(self, *args, **kwargs):

        # app = QtWidgets.QApplication(sys.argv)
        print(self.name)
        self.window.setWindowTitle(self.name)
        client = Client(name=self.name)
        # получаем список контактов с сервера, которые лежат у нас - не надежные
        client.connect()

        listener = GuiReciever(client.socket, client.request_queue)

        # Связываем сигнал и слот
        # слот обновление данных в списке сообщений

        @pyqtSlot(str)
        def update_chat(data):
            ''' Отображение сообщения в истории
            '''
            try:
                msg = data
                self.window.listWidgetMessages.addItem(msg)
            except Exception as e:
                print(e)

        # сигнал мы берем из нашего GuiReciever
        print('Привязываем сингнал слот')
        listener.gotData.connect(update_chat)
        print('Типо привязали')

        # Используем QThread так рекомендуется, но можно и обычный
        # th_listen = threading.Thread(target=listener.poll)
        # th_listen.daemon = True
        # th_listen.start()
        self.th = QThread()
        # pool_th = QThread()

        listener.moveToThread(self.th)

        # # ---------- Важная часть - связывание сигналов и слотов ----------
        # При запуске потока будет вызван метод search_text
        # pool_th.started.connect(listener.poll)
        # pool_th.start()
        self.th.started.connect(listener.poll)
        self.th.start()

        contact_list = client.get_contacts()

        def load_contacts(contacts):
            """загрузка контактов в список"""
            # чистим список
            self.window.listWidgetContacts.clear()
            # добавляем
            for contact in contacts:
                self.window.listWidgetContacts.addItem(contact)

        # грузим контакты в список сразу при запуске приложения
        load_contacts(contact_list)

        def add_contact():
            """Добавление контакта"""
            # Получаем имя из QTextEdit
            username = self.window.textEditUsername.toPlainText()
            if username:
                # добавляем контакт - шлем запрос на сервер ...
                client.add_contact(username)
                # добавляем имя в QListWidget
                self.window.listWidgetContacts.addItem(username)

        # Связываем сигнал нажатия кнопки добавить со слотом функцией добавить контакт
        self.window.pushButtonAddContact.clicked.connect(add_contact)

        def del_contact():
            """Удаление контакта"""
            # получаем выбранный элемент в QListWidget
            current_item = self.window.listWidgetContacts.currentItem()
            # получаем текст - это имя нашего контакта
            username = current_item.text()
            # удаление контакта (отправляем запрос на сервер)
            client.del_contact(username)
            # удаляем контакт из QListWidget
            # window.listWidgetContacts.removeItemWidget(current_item) - так не работает
            # del current_item
            # Так норм удаляется, может быть можно как то проще
            current_item = self.window.listWidgetContacts.takeItem(self.window.listWidgetContacts.row(current_item))
            del current_item

        # связываем сигнал нажатия на кнопку и слот функцию удаления контакта
        self.window.pushButtonDelContect.clicked.connect(del_contact)

        def open_chat():
            try:
                # грузим QDialog чата
                dialog = uic.loadUi('chat.ui')

                @pyqtSlot(str)
                def update_chat(data):
                    ''' Отображение сообщения в истории
                    '''
                    try:
                        msg = data
                        dialog.listWidgetMessages.addItem(msg)
                    except Exception as e:
                        print(e)

                # сигнал мы берем из нашего GuiReciever
                listener.gotData.connect(update_chat)

                # получаем выделенного пользователя
                selected_index = self.window.listWidgetContacts.currentIndex()
                # получаем имя пользователя
                user_name = selected_index.data()
                # выставляем имя в название окна
                dialog.setWindowTitle('Чат с {}'.format(user_name))

                # отправка сообщения
                def send_message():
                    text = dialog.textEditMessage.toPlainText()
                    if text:
                        print(client)
                        client.send_message(user_name, text)
                        # # будем выводить то что мы отправили в общем чате
                        msg = '{} >>> {}'.format(self.name, text)
                        dialog.listWidgetMessages.addItem(msg)

                # связываем отправку с кнопкой ОК
                dialog.pushOk.clicked.connect(send_message)
                # запускаем в модальном режиме
                # привязываем события модального окна (для демонстрации)
                # dialog.pushOk.clicked.connect(dialog.accept)
                dialog.exec()
            except Exception as e:
                print(e)

        # Пока мы не можем передать элемент на который нажали - сделать в следующий раз через наследование
        self.window.listWidgetContacts.itemDoubleClicked.connect(open_chat)

        # Контекстное меню при нажатии правой кнопки мыши (пока тестовый вариант для демонстрации)
        # Создаем на листе
        self.window.listWidgetContacts.setContextMenuPolicy(Qt.CustomContextMenu)
        self.window.listWidgetContacts.setContextMenuPolicy(Qt.ActionsContextMenu)
        quitAction = QtWidgets.QAction("Quit", None)
        # quitAction.triggered.connect(app.quit)
        self.window.listWidgetContacts.addAction(quitAction)
        print('КОнец')
        # рисуем окно
        self.window.show()
        # точка запуска приложения
        # sys.exit(app.exec_())


if __name__ == '__main__':
    auth = AuthWindow()
    auth()