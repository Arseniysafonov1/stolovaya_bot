from seatable_api import Base

class Connector:
    __api = "7e4294f86c76c2a62665ad6fdf031c129a5d8c02"
    __server_url = 'https://cloud.seatable.io'

    def __init__(self):
        self.base = Base(Connector.__api, Connector.__server_url)
        self.base.auth()
        self.arr = []
        self.refresh()

    def refresh(self):
        self.arr = self.base.list_rows('Teachers')

    def find_id(self, id):
        self.refresh()
        return list(filter(lambda x: str(id) in x.get('tg_ids', '').split(';'), self.arr))

    def auth(self, login, password, tg_id):
        self.refresh()
        a = lambda x: x['login'] == login and x['password'] == password
        arr = list(filter(a, self.arr))
        if len(arr) != 1:
            return None
        arr = arr[0]
        if str(tg_id) in arr.get('tg_ids', '').split(';'):
            return arr
        arr['tg_ids'] = arr.get('tg_ids', '') + str(tg_id) + ';'
        self.base.update_row('Teachers', arr['_id'], {'tg_ids': arr['tg_ids']})
        return arr

    def exit(self, tg_id):
        self.refresh()
        row = self.find_id(tg_id)[0]
        self.base.update_row('Teachers', row['_id'], {'tg_ids': row['tg_ids'].replace(str(tg_id) + ';', '')})

    def get_all_teacher_ids(self):
        self.refresh()
        l = []
        for i in list(filter(lambda x: not x['is_admin'], self.arr)):
            l += i.get('tg_ids', '').split(';')[:-1]
        return l

    def get_all_admin_ids(self):
        self.refresh()
        l = []
        for i in list(filter(lambda x: x['is_admin'], self.arr)):
            l += i.get('tg_ids', '').split(';')[:-1]
        return l

    def get_all_info(self):
        self.refresh()
        txt =  "\n".join([f"{x.get('class', '')}: {x.get('msg', 'Нет данных')}" for x in list(filter(lambda y: not y['is_admin'], self.arr))])
        with open("info.txt", 'w', encoding='utf-8') as f:
            f.write(txt)
        with open("info.txt", "rb") as f:
            return f.read()
        return None

    def add_msg(self, tg_id, msg):
        self.refresh()
        a = self.find_id(tg_id)[0]
        if a['is_admin']:
            return False
        self.base.update_row('Teachers', a['_id'], {'msg': msg})
        return True
    def clear_all_msgs(self):
        for i in self.get_all_teacher_ids():
            self.add_msg(i, '')
