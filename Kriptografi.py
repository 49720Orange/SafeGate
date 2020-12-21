import hashlib
from Crypto import Random
from cryptography.fernet import Fernet
from flask_mail import Message
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class kriptografi:
    anahtar=""
    def __init__(self):
        self.anahtar=Fernet.generate_key()

    def aesSifreleme(self,veri):
        encoded_veri = veri.encode()
        f = Fernet(self.anahtar)
        sifreliMesaj = f.encrypt(encoded_veri)
        return sifreliMesaj, self.anahtar

    def aesDesifreleme(self, veri, anahtar):
        anahtar = Fernet(anahtar.encode())
        mesaj = anahtar.decrypt(veri.encode())
        return mesaj

    def md5Sifreleme(self, veri):
        sifreleyici = hashlib.sha256()
        sifreleyici.update(veri.encode("utf-8"))
        hash = sifreleyici.hexdigest()
        return hash

    def generate_keys(self):
        x = RSA.generate(1024)
        my_private_key = x.export_key()  # private key
        my_public_key = x.publickey().export_key()  # public key
        return my_public_key, my_private_key

    def rsaSifreleme(self,mesaj):
        pubKey, priKey=self.generate_keys()
        cipher = PKCS1_v1_5.new(RSA.importKey(pubKey))
        sonuc = cipher.encrypt(mesaj.encode())
        return sonuc, priKey

    def rsaDesifreleme(self, mesaj, priKey):
        # Post-private key decryption

        prikey=str(priKey).replace("\n","").replace("\\n","")
        priKey="""-----BEGIN RSA PRIVATE KEY-----
               """+prikey+"""
                -----END RSA PRIVATE KEY-----"""
        #dsize =256 #SHA.digest_size
        sentinel = Random.new().read(256)

        cipher = PKCS1_v1_5.new(RSA.importKey(priKey))
        mesaj = str.encode(mesaj)
        sonuc = cipher.decrypt(mesaj, sentinel)
        return sonuc.decode()


class mailSent():
    mail=None
    def __init__(self,mail):
        self.mail = mail

    def mailGondermeSifreleme(self, ad, alici, mesaj, anahtar, sonuc, metod):
        mailMetni = f'Sayın {ad} \nYazdığınız mesaj seçtiğiniz {metod} ile şifrelenmiştir. \nŞifrelediğiniz mesajınız= {mesaj} \nŞifreleme Anahtarınız= {anahtar} \nŞifrelenmiş Mesajınız= {sonuc}'
        msg = Message('Şifreleme Bilgileriniz', sender='SafeGate', recipients=[alici])
        msg.body = (mailMetni)
        self.mail.send(msg)

    def mailGondermeDesifreleme(self,ad,alici,mesaj, sonuc, metod):
        mailMetni = f'Sayın {ad} \nYazdığınız şifrelenmiş mesaj {metod} ile deşifrelenmiştir. \nDeşifrelediğiniz mesajınız= {mesaj} \nDeşifrelenmiş Mesajınız= {sonuc}'
        msg = Message('Deşifreleme Bilgileriniz', sender='SafeGate', recipients=[alici])
        msg.body = (mailMetni)
        self.mail.send(msg)

