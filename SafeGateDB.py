import sqlite3
import pandas as pd


class safegateDB():
    def dbOlusturma(self):
        baglanti = sqlite3.connect('safegateDB.db')
        return baglanti
    def get_query(self,query):
        df = pd.read_sql_query(query, self.dbOlusturma())
        return df
    def set_query(self,query):
        db=self.dbOlusturma()
        bag=db.cursor()
        bag.execute(query)
        db.commit()
    def tabloOlusturma(self):
        if self.kontrol():
            q='CREATE TABLE IF NOT EXISTS hocaBilgileri ([id] INTEGER PRIMARY KEY,[ad] text, [soyad] text,[okuladi] text,[email] text)'
            self.set_query(q)

    def veriEkleme(self):
        if self.kontrol_table():
            q='INSERT INTO hocaBilgileri(id, ad, soyad,okuladi,email) ' \
              'VALUES(1, "Neslihan","Genç","Dilek Sabancı MTAL","neslihan.karacakurt@gmail.com"),' \
              '(2, "Emine","Aydoğmuş","Dilek Sabancı MTAL","orangeemi@gmail.com"),' \
              '(3, "İsmail Ersin","Turan","Dr. Nurettin Erk Perihan Erk MTAL","ismailersin@gmail.com")'
            self.set_query(q)

    def kontrol(self):
        q="select count(*) as count from sqlite_master where type='table' and name='hocaBilgileri';"
        rs=self.get_query(q)
        if rs["count"][0]>0:
            return False
        return True
    def kontrol_table(self):
        q="select count(*) as count from hocaBilgileri ;"
        rs=self.get_query(q)
        if rs["count"][0]>0:
            return False
        return True
    def get_hocalar(self):
        return self.get_query("select ad, soyad,okuladi,email from hocaBilgileri;")






