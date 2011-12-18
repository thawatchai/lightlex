import re
import os
from pysqlite2 import dbapi2 as sqlite

class Lexitron(object):
    NOT_ENG_RE = re.compile("[^a-z '-]", re.IGNORECASE)

    def __init__(self, abs_dir):
        db = '%s/pylexitron/lexitron.db' % abs_dir
        os.stat(db)
        sqlite.enable_shared_cache(True)
        self.con = sqlite.connect(db)
        self.con.row_factory = sqlite.Row

    def __make_thai_senses(self, rows):
        l = []
        for row in rows:
            l.append(row['tentry'])
            if row['ethai']:
                l.append(row['ethai'])
        return ', '.join(l)

    def __make_eng_senses(self, rows):
        return ', '.join([row['eentry'] for row in rows])

    @classmethod
    def iseng(cls, str):
        if not cls.NOT_ENG_RE.search(str):
            return True
        else:
            return False

    def search(self, str):
        if self.iseng(str):
            return self.search_et(str)
        else:
            return self.search_te(str)

    def list(self, str):
        if self.iseng(str):
            return self.list_et(str)
        else:
            return self.list_te(str)

    def search_et(self, str):
        rows = self.con.execute('SELECT * FROM etlex WHERE esearch LIKE ?', [str]).fetchall()
        return {'type': 'et', 'items': rows, 'senses': self.__make_thai_senses(rows)}

    def list_et(self, str):
        rows = self.con.execute('SELECT esearch FROM etlex WHERE esearch LIKE ? GROUP BY esearch', ['%s%%' % str]).fetchall()
        return {'type': 'et', 'items': [row['esearch'] for row in rows]} 

    def search_te(self, str):
        rows = self.con.execute('SELECT * FROM telex WHERE tsearch = ?', [str]).fetchall()
        return {'type': 'te', 'items': rows, 'senses': self.__make_eng_senses(rows)}

    def list_te(self, str):
        rows = self.con.execute('SELECT tsearch FROM telex WHERE tsearch LIKE ? GROUP BY tsearch', ['%s%%' % str]).fetchall()
        return {'type': 'te', 'items': [row['tsearch'] for row in rows]}

