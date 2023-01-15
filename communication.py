from connection import Connector

class Communicator:
    def __init__(self):
        self.base = Connector()
        self.state_dict = dict()

    BUTTONS = {
        'ADMIN': ["Получить информацию", "Выйти из аккаунта"],
        'USER': ["Отправить информацию", "Выйти из аккаунта"]
    }

    @staticmethod
    def send_all_teachers():
        return Connector().get_all_teacher_ids(), 'Уже 8.10! Время заполнить информацию для столовой!'

    @staticmethod
    def send_all_admins():
        a = Connector()
        return a.get_all_admin_ids(), a.get_all_info()

    @staticmethod
    def clear_all_msgs():
        return Connector().clear_all_msgs()

    def login(self, tg_id):
        login = self.state_dict[tg_id]['login']
        password = self.state_dict[tg_id]['password']
        if self.base.auth(login, password, tg_id):
            acc = self.base.find_id(tg_id)[0]
            self.state_dict[tg_id] = {'auth': "ADMIN" if acc["is_admin"] else "USER", 'login': False, 'password': False}
            return tg_id, 'Авторизация прошла успешно', self.BUTTONS[self.state_dict[tg_id]['auth']]
        self.state_dict[tg_id] = {'auth': False, 'login': True, 'password': False}
        return tg_id, 'Похоже что-то пошло не так, попробуйте снова.\nВведите логин: ', None

    def read_msg(self, msg):
        tg_id = msg.chat.id
        txt = msg.text
        if txt == '/start' or tg_id not in self.state_dict.keys():
            acc = self.base.find_id(tg_id)
            if acc:
                acc = acc[0]
                self.state_dict[tg_id] = {'auth': "ADMIN" if acc["is_admin"] else "USER",
                                          'login': False, 'password': False}
                return tg_id, f'Здравствуйте, ваш id привязан к аккаунту {acc["login"]}', \
                       self.BUTTONS[self.state_dict[tg_id]['auth']]
            self.state_dict[tg_id] = {'auth': False, 'login': True, 'password': False}
            return tg_id, 'Здравствуйте, Вас приветствует ...bot. Для продолжения работы введите свой логин: ', ['-']
        elif self.state_dict[tg_id].get('auth', False):
            if txt == "Выйти из аккаунта":
                return tg_id, "Вы уверены, что хотите выйти с аккаунта?", ["ДА", "НЕТ"]
            elif txt == "Получить информацию":
                return tg_id, [self.base.get_all_info(), ""], self.BUTTONS[self.state_dict[tg_id]['auth']]
            elif txt == "Отправить информацию.":
                self.state_dict[tg_id]['spec'] = True
                return tg_id, "Введите информацию о присутствующих для столовой: ", None
            elif self.state_dict[tg_id].get('spec', False):
                self.base.add_msg(tg_id, txt)
                del self.state_dict[tg_id]['spec']
                return tg_id, "Информация успешно записана", self.BUTTONS[self.state_dict[tg_id]['auth']]
            elif txt == "ДА":
                self.base.exit(tg_id)
                del self.state_dict[tg_id]
                return tg_id, "Вы успешно вышли из аккаунта", ['/start']
            elif txt == "НЕТ":
                return tg_id, "Хорошо, продолжим работу", self.BUTTONS[self.state_dict[tg_id]['auth']]
        elif self.state_dict[tg_id]['login'] == True:
            self.state_dict[tg_id] = {'auth': False, 'login': txt, 'password': True}
            return tg_id, 'Хорошо, теперь введите свой пароль: ', None
        elif self.state_dict[tg_id]['password'] == True:
            self.state_dict[tg_id]['password'] = txt
            return self.login(tg_id)
        return tg_id, "Извините, я Вас не понял", None
