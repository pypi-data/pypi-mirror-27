"""
Функции ​​сервера:​
- принимает ​с​ообщение ​к​лиента;
- формирует ​​ответ ​к​лиенту;
- отправляет ​​ответ ​к​лиенту;
- имеет ​​параметры ​к​омандной ​с​троки:
- -p ​​<port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт ​​7777);
- -a ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса).
"""
import sys
from socket import socket, AF_INET, SOCK_STREAM
import select
import logging
import log.server_log_config
from log.decorators import Log
from jim.config import *
from jim.protocol import JimMessage, JimResponse
from repo.server_repo import DbRepo
from repo.server_models import Base
import time

# Получаем серверный логгер по имени, он уже объявлен в log_config и настроен
logger = logging.getLogger('server')
log = Log(logger)


class Server:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        # запускаем сервер
        self.socket = self._start()
        # формируем список клиентов
        self._clients = []
        # создаем репозиторий
        self.repo = DbRepo('server.db', Base)
        self.names = {}

    def _start(self):
        """
        Запуск сервера
        :param addr: адрес
        :param port: порт
        :return: серверный сокет
        """
        # Создает сокет TCP
        s = socket(AF_INET, SOCK_STREAM)
        # Присваиваем адрес и порт
        s.bind((self.addr, self.port))
        # Максимум 15 клиентов
        s.listen(15)
        # Задаем задержку для обработки событий
        s.settimeout(0.2)
        # Возвращаем серверный сокет
        return s

    @log
    def _read_requests(self, r_clients):
        """
        Чтение сообщений, которые будут посылать клиенты
        :param r_clients: клиенты которые могут отправлять сообщения
        :return: список сообщений
        """
        # Список входящих сообщений
        messages = []

        for sock in r_clients:
            try:
                # Получаем входящие сообщения
                bdata = sock.recv(1024)
                jm = JimMessage.create_from_bytes(bdata)
                # Добавляем в список пару сообщение и сокет который его прислал
                messages.append((jm, sock))
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                self._clients.remove(sock)

        # Возвращаем словарь сообщений
        return messages

    @log
    def _write_responses(self, messages):
        """
        Теперь будем отправлять сообщения только конкретному пользователю
        """

        for message, sender in messages:
            # Теперь клиенты отправляют сообщения с разными ключами
            if message.action == ADD_CONTACT:
                # нужно добавить контакт клиенту
                # имя клиента
                client_username = message.user
                # имя контакта
                contact_username = message.user_id
                # сохраняем данные в базу
                self.repo.add_contact(client_username, contact_username)
                self.repo.commit()
                response = JimResponse(**{RESPONSE: OK})
                # отправляем пока ответ всем
                sender.send(bytes(response))
            elif message.action == DEL_CONATCT:
                # нужно добавить контакт клиенту
                # имя клиента
                client_username = message.user
                # имя контакта
                contact_username = message.user_id
                # сохраняем данные в базу
                self.repo.del_contact(client_username, contact_username)
                self.repo.commit()
                response = JimResponse(**{RESPONSE: OK})
                # отправляем пока ответ всем
                sender.send(bytes(response))
            elif message.action == GET_CONTACTS:
                # отдаем список контактов клиенту
                client_username = message.user
                # получаем список контактов
                contact_list = self.repo.get_contacts(client_username)
                # отправляем ответ что всё ок
                response = JimResponse(**{RESPONSE: ACCEPTED, QUANTITY: len(contact_list)})
                # отправляем пока ответ всем
                sender.send(bytes(response))
                # формируем второе сообщение со списком
                jm = JimMessage(action=contact_list, time=time.time())
                sender.send(bytes(jm))
            elif message.action == MSG:
                # получаем кому отправить сообщение
                to = message.to
                # на надо только переслать сообщение этому пользователю
                # получаем сокет по имени
                # можно даже обойти тут список контактов и отправлять напрямую
                sock = self.names[to]
                sock.send(bytes(message))
                # отвечам тому кто прислал сообщение что все хорошо
                sender.send(bytes(JimResponse(**{RESPONSE: ACCEPTED})))


    def _get_connection(self):
        try:
            conn, addr = self.socket.accept()  # Проверка подключений
            # Должно прийти сообщение о присутствии
            presence_msg_bytes = conn.recv(1024)
            presence_msg = JimMessage.create_from_bytes(presence_msg_bytes)
            if presence_msg.action == PRESENCE:
                # Получаем имя пользователя
                client_name = presence_msg.user[ACCOUNT_NAME]
                print('К нам подключился {}'.format(client_name))
                # если клиента нету в базе
                print(self.repo.client_exists(client_name))
                if not self.repo.client_exists(client_name):
                    # мы его добавляем
                    print('Добавляем клиента')
                    self.repo.add_client(client_name)
                    print('Сохраняем')
                    self.repo.commit()
                # добавляем историю подключения
                self.repo.add_history(client_name, addr[0])
                self.repo.commit()
                # отправляем ответ
                presence_response = JimResponse(**{RESPONSE: OK})
                conn.send(bytes(presence_response))
            else:
                presence_response = JimResponse(**{RESPONSE: WRONG_REQUEST})
                conn.send(bytes(presence_response))
        except OSError as e:
            pass  # timeout вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            # Добавляем клиента в список
            self._clients.append(conn)
            # Добавляем в словарь имя клиента и соответствующий ему сокет
            # Мы это делаем, чтобы знать в будующем кому пересылать сообщение
            self.names[client_name] = conn
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(self._clients, self._clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился

            requests = self._read_requests(r)  # Получаем входные сообщения
            self._write_responses(requests)  # Выполним отправку входящих сообщений

    def main_loop(self):
        """
        Главный цикл работы сервера
        :return: None
        """
        while True:
            self._get_connection()


if __name__ == '__main__':
    print('Запуск сервера')
    # Получаем аргументы скрипта
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)

    serv = Server(addr, port)
    serv.main_loop()
