import socket, requests
import netifaces
from pythonping import ping

class ipscan():

    def get_host_list(self,target):
        fark = 3 - target.count(".")
        stg = []
        stg.append(target)
        for i in range(fark):
            stg2 = []
            if i == fark - 1:
                for s in stg:
                    for j in range(1, 256):
                        stg2.append(s + '.' + str(j))
            else:
                for s in stg:
                    for j in range(256):
                        stg2.append(s + '.' + str(j))
            stg = stg2
        return stg

    def get_ipscan(self,target):
        rslt=[]
        s = ""
        #host_list=[]
        host_list=self.get_host_list(target)

        for i in host_list:
            d=ping(i,timeout=0.1,count=1,size=1, verbose=False)
            if d.success():
                rslt.append(i)

        print("rslt",rslt,flush=True)
        return rslt
        # s = ""
        # for i in range(3 - target.count(".")):
        #     s += ".0"
        # s = target + s + "/24"
        # print(s)
        # scan = networkscan.Networkscan(s)
        # scan.run()
        # return scan.list_of_hosts_found
    def pingfonk(self, target=""):
        rslt = []
        ips = ipscan()
        if target=="":
            for i in netifaces.interfaces():
                addrs = netifaces.ifaddresses(i)
                if 2 in addrs.keys():
                    d = addrs[2][0]['addr']
                    if not str(d).startswith("192.168.56") and not str(d).startswith("127."):
                        d=d.split(".")
                        d=str(d[0])+"."+str(d[1])+"."+str(d[2])
                        target=d
        if target!="":
            rslt = ips.get_ipscan(target)
            return rslt
        return []

    def my_ip_adresses(self):
        NAT_ip = requests.get("http://wtfismyip.com/text").text.strip()
        host_name = socket.gethostname()
        # host_ip = socket.gethostbyname(host_name+ ".local")
        rs = []
        for i in netifaces.interfaces():
            addrs = netifaces.ifaddresses(i)
            if 2 in addrs.keys():
                d = addrs[2][0]['addr']
                if not str(d).startswith("192.168.56") and not str(d).startswith("127."):
                    rs.append(d)
        from getmac import get_mac_address as gma
        mac_address=gma()
        rslt=[NAT_ip, rs, host_name, mac_address]
        return rslt



class port_scan():

    def port_tarayıcı(self, target):
        result = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        # ports=[1,4,5,7,9,13,17,18,19,20,21,22,23,25,26,37,38,39,41,42,49,53,57,67,68,69,70,79,80,88,101,107,109,110,113,115,118,119,123,137,138,139,143,152,153,156,158,161,162,179,194,201,209,213,218,220,259,264,318,323,366,369,384,387,389,401,411,427,443,444,445,464,465,500,513,514,515,524,530,531,540,542,546,547,554,563,587,591,593,604,631,636,639,646,647,648,652,654,666,674,691,692,695,698,699,700,701,702,706,711,712,720,829,860,873,901,981,989,990,991,992,993,995,1080,1099,1194,1198,1214,1223,1337,1352,1387,1414,1433,1434,1494,1521,1547,1723,1761,1863,1900,1935,1984,2000,2030,2031,2082,2083,2086,2087,2095,2096,2181,2222,2427,2447,2710,2809,2967,3050,3074,3128,3306,3389,3396,3689,3690,3724,3784,3785,4500,4662,4672,4894,4899,5000,5003,5121,5190,5222,5223,5269,5432,5517,5800,5900,6000,6112,6346,6347,6600,6667,9009,9715,9714,9987]
        ports = [23, 25, 26, 37, 38, 39, 41, 42, 49, 53, 57, 67, 68, 69, 70, 79, 80, 88, 101]
        for port in ports:
            stg = {}
            print(port, flush=True)
            if s.connect_ex((target, port)) == 0:
                stg["port"] = port
                stg["result"] = "Açık"
                result.append(stg)
        return result

