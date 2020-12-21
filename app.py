import Kriptografi, Hacking
from flask import Flask, render_template, request
from flask_mail import Mail
import socket
from SafeGateDB import safegateDB

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'orange49720@gmail.com'
app.config['MAIL_PASSWORD'] = 'Oran4558ge.'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/')
def anasayfa():
    c=Hacking.ipscan()
    rslt=c.my_ip_adresses()
    sg=safegateDB()
    sg.tabloOlusturma()
    sg.veriEkleme()
    rs=sg.get_hocalar()
    return render_template('index.html',rslt=rslt,rs=rs)


@app.route('/port_scan', methods=['POST'])
def port_scan():
    c=Hacking.port_scan()
    target = str(request.form.get('ip'))
    rslt=c.port_tarayıcı(target)
    return render_template('portscan.html',rslt=rslt)


@app.route('/ip_scan', methods=['POST'])
def ip_scan():
    c=Hacking.ipscan()
    target = str(request.form.get('ip2'))
    rslt=c.pingfonk(target)
    return render_template('ipscan.html',rslt=rslt)


def dom2ip(target):
    rslt=[]
    rslt.append(socket.gethostbyname(target))
    return rslt


@app.route('/domaintoip', methods=['POST'])
def domaintoip():
    target = str(request.form.get('domain'))
    rslt=dom2ip(target)
    return render_template('domaintoip.html',rslt=rslt, target=target)


@app.route('/sifreleme', methods=['GET', 'POST'])
def sifreleme():
    anahtar="Bu şifreleme yönteminde şifreleme anahtarı kullanılmamaktadır!.."
    isim = request.form.get('isim')
    mesaj = request.form.get('mesaj')
    metod=request.form.get('sifre')
    alici = request.form['email']
    kripto=Kriptografi.kriptografi()
    if metod=="AES":
        sonuc, anahtar =kripto.aesSifreleme(mesaj)
        anahtar = anahtar.decode("utf-8")
        sonuc = sonuc.decode("utf-8")
    elif metod=="RSA":
        sonuc, anahtar=kripto.rsaSifreleme(mesaj)
        sonuc=sonuc.hex()

        anahtar=anahtar.decode("utf-8")
        anahtar=str(anahtar).replace("-----BEGIN RSA PRIVATE KEY-----","").replace("-----END RSA PRIVATE KEY-----","").replace("\n","")
    elif metod=="MD5":
        sonuc=kripto.md5Sifreleme(mesaj)

    ms=Kriptografi.mailSent(mail)
    ms.mailGondermeSifreleme(isim,alici, mesaj, anahtar, sonuc, metod)

    return render_template("sifrelemesonuc.html", isim=isim, mesaj=mesaj, sonuc=sonuc, metod=metod)

@app.route('/aesdesifreleme', methods=['GET', 'POST'])
def aesdesifreleme():
    isim = request.form.get('isim')
    mesaj = request.form.get('mesaj')
    anahtar = request.form.get('anahtar')
    alici = request.form['email']
    kripto = Kriptografi.kriptografi()
    sonuc=kripto.aesDesifreleme(mesaj, anahtar)
    sonuc=sonuc.decode("utf-8")
    ms = Kriptografi.mailSent(mail)
    ms.mailGondermeDesifreleme(isim, alici, mesaj, sonuc, metod="AES")
    return render_template("desifrelemesonuc.html", isim=isim, mesaj=str(mesaj), sonuc=(sonuc), metod="AES")

@app.route('/rsadesifreleme', methods=['GET', 'POST'])
def rsadesifreleme():
    isim = request.form.get('isim')
    mesaj = request.form.get('mesaj')
    anahtar = request.form.get('anahtar')
    alici = request.form['email']
    kripto = Kriptografi.kriptografi()
    sonuc=kripto.rsaDesifreleme(mesaj, anahtar)
    print("sonuc",sonuc)
    return render_template("desifrelemesonuc.html", isim=isim, mesaj=str(mesaj), sonuc=(sonuc), metod="RSA")

if __name__ == '__main__':
    app.run(debug=True)
