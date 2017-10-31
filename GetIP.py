'''
各种获取 IP 的方法
'''
import socket
import random
import requests
from ddnslogger import ddns_logger


class GetIP():
    ''' 各种获取 IP 的方法 '''

    def __init__(self):
        self.dlog = ddns_logger('IP_logger')

    def get_ip_local(self):
        ''' 获取内网ip '''
        try:
            self.dlog.info_msg('try to get local ip ...')
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(('8.8.8.8', 80))
                ip_local = s.getsockname()[0]
        except Exception:
            self.dlog.warning_msg('fail to get local ip!')
            return None
        self.dlog.info_msg('get local ip %s', ip_local)
        return ip_local

    def get_ip_ex_ifconfig(self):
        ''' get ip_ex from [ifconfig.me/ip] [Sometimes it's slow, more timeout!]'''
        try:
            self.dlog.info_msg('try to get ip_ex from ifconfig ...')
            with requests.session() as ipsess:
                ip_ex_ifconfig = ipsess.get(
                    'http://ifconfig.me/ip', timeout=12).text
        except Exception:
            self.dlog.warning_msg('fail to get ip_ex from ifconfig!')
            return None
        self.dlog.info_msg(
            'get ip_ex %s from ifconfig', ip_ex_ifconfig)
        return ip_ex_ifconfig

    def get_ip_ex_ip138(self):
        ''' get ip_ex from [ip138.com] '''
        import lxml.html
        try:
            self.dlog.info_msg('try to get ip_ex from ip138 ...')
            with requests.session() as ipsess:
                r = ipsess.get('http://2017.ip138.com/ic.asp', timeout=8)
                r.encoding = 'gb2312'
                page = lxml.html.document_fromstring(r.text)
                ip_ex_ip138 = page.xpath("//body/center/text()")[0][7:21]
        except Exception:
            self.dlog.warning_msg('fail to get ip_ex from ip138!')
            return None
        self.dlog.info_msg('get ip_ex %s from ip138', ip_ex_ip138)
        return ip_ex_ip138

    def get_ip_ex_ns1(self):
        '''  get ip_ex from [ns1.dnspod.net], best reliability'''
        try:
            self.dlog.info_msg('try to get ip_ex from ns1 ...')
            with socket.create_connection(address=('ns1.dnspod.net', 6666), timeout=8) as sk:
                ip_ex_ns1 = str(sk.recv(32), 'utf-8')
        except Exception:
            self.dlog.warning_msg('fail to get ip_ex from ns1!')
            return None
        self.dlog.info_msg('get ip_ex %s from ns1', ip_ex_ns1)
        return ip_ex_ns1

    def get_ip_ex(self):
        '''  '''
        ip_ex = self.get_ip_ex_ns1()
        if ip_ex:
            return ip_ex
        ip_ex = self.get_ip_ex_ifconfig()
        if ip_ex:
            return ip_ex
        ip_ex = self.get_ip_ex_ip138()
        if ip_ex:
            return ip_ex
        else:
            self.dlog.error_msg('fail to get ip_ex!')
            return None

    def get_ip_random(self):
        ''' 获取随机ip '''
        randomlist = []
        for i in range(4):
            randomlist.append(str(random.randrange(0, 256, 1)))
        ip_random = '.'.join(randomlist)
        self.dlog.info_msg('get random ip %s', ip_random)
        return ip_random

    def get_ip_static(self):
        ''' 获取固定ip '''
        ip_static = '180.128.12.36'
        self.dlog.info_msg('get static ip %s', ip_static)
        return ip_static

    def get_ip_none(self):
        ''' 获取none '''
        ip_none = None
        self.dlog.info_msg('get %s', ip_none)
        return ip_none


def test():
    ''' test '''
    get_ip = GetIP()

    ip = get_ip.get_ip_none()
    ip = get_ip.get_ip_static()
    ip = get_ip.get_ip_random()
    ip = get_ip.get_ip_local()
    ip = get_ip.get_ip_ex_ifconfig()
    ip = get_ip.get_ip_ex_ip138()
    ip = get_ip.get_ip_ex_ns1()

    print(ip)


if __name__ == '__main__':
    test()
