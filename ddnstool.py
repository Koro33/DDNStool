'''
使用 DNSPod 的 API 来实现 DDNS 功能
It works in both WinX and Linux
'''
import os
import json
import requests

from GetIP import GetIP
from ddnslogger import ddns_logger

API_VERSION = '4.6'

dlog = ddns_logger()


def dnspod_conf_read():
    '''
    read information from json files
    '''
    dlog.info_msg('try to Read ddns_config.json ...')
    try:
        with open("ddns_config.json", "r") as f1:
            text = f1.read()
        jsonData = json.loads(text)
    except Exception:
        dlog.warning_msg(
            'Read failed! Please check if the file [ddns_config.json] is existed...')
        print('Read config files failed! Please check if the file [dns_config.json] is existed...')
        exit()
    dlog.info_msg('Read config files succesful ...')

    return jsonData


class Last(object):
    '''  '''

    def __init__(self, tag):
        self.fn = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), tag)

    def Read(self):
        try:
            with open(self.fn, "r") as fp:
                return fp.read()
        except FileNotFoundError:  # 首次
            with open(self.fn, "w") as fp:
                fp.write('123.123.123.123')
        except Exception:
            return None

    def Write(self, value):
        with open(self.fn, "w") as fp:
            fp.write(value)


class DNSPod():
    '''  '''

    def __init__(self, dnspod_jsonData):
        self.dnspod_data = dnspod_jsonData
        self.last_ip = Last('last.ip').Read()

    def run(self):

        self.checkAPIversion()

        get_ip = GetIP()
        # ip = get_ip.get_ip_random()
        ip = get_ip.get_ip_ex()

        if ip and ip != self.last_ip:
            dlog.info_msg('IP changed from %s to %s ', self.last_ip, ip)
            print('[info] IP changed from {!r} to {!r} '.format(self.last_ip, ip))
            self.modifyRecord(ip)
            Last('last.ip').Write(ip)

        elif ip == None:
            dlog.error_msg('can not get your ip!')
            print('can not get your ip!')
            exit()
        elif ip == self.last_ip:
            dlog.info_msg('IP(%s) not changed', ip)
            print('[info] IP({!r}) not changed'.format(ip))

    def checkAPIversion(self):
        APIversion = self.getAPIversion()

        if APIversion != API_VERSION:
            dlog.error_msg(
                'APIversion not match, current APIversion is %s', APIversion)
            print('APIversion not match, current APIversion is {!r}'.format(APIversion))
            exit()

    def getAPIversion(self):
        ''' Get Version '''
        post_data = self.dnspod_data['comm_parm']
        post_headers = self.dnspod_data['headers']

        try:
            with requests.session() as dnspodsess:
                resjson = dnspodsess.post(
                    'https://dnsapi.cn/Info.Version', data=post_data, headers=post_headers, timeout=8)
            # print(resjson.text)
            res = resjson.json()
            code = res['status']['code']
        except Exception:
            dlog.error_msg('getAPIversion response ERROR')

        if code == '1':  # 注意返回值数字是数值型
            version = res['status']['message']
            dlog.info_msg(
                'getAPIversion action successful, version = %s', version)
            return version
        else:
            dlog.error_msg('getAPIversion action ERROR! errorcode = %s', code)
            print('getAPIversion action ERROR! errorcode = {!r}'.format(code))
            return None

    def getRecordList(self):
        ''' get record list (just for test)'''
        post_data = dict(
            self.dnspod_data['comm_parm'], **self.dnspod_data['record_list'])
        post_headers = self.dnspod_data['headers']
        with requests.session() as dnspodsess:
            resjson = dnspodsess.post(
                'https://dnsapi.cn/Record.List', data=post_data, headers=post_headers, timeout=8)
        return resjson.text

    def modifyRecord(self, ip):
        ''' modify record '''
        self.dnspod_data['update_record']['value'] = ip
        post_data = dict(
            self.dnspod_data['comm_parm'], **self.dnspod_data['update_record'])
        post_headers = self.dnspod_data['headers']
        try:
            with requests.session() as dnspodsess:
                resjson = dnspodsess.post(
                    'https://dnsapi.cn/Record.Modify', data=post_data, headers=post_headers, timeout=8)
            # print(resjson.text)
            res = resjson.json()
            code = res['status']['code']
        except Exception:
            dlog.error_msg('modifyRecord response ERROR')

        if code == '1':  # 注意返回值数字是数值型
            dlog.info_msg('modifyRecord action successful')
            return 1
        else:
            dlog.error_msg('modifyRecord action ERROR! errorcode = %s', code)
            dlog.error_msg('response: %s', res['status']['message'])
            return 0

    def print_postdata(self):
        ''' print post data (just for test) '''
        post = dict(self.dnspod_data['comm_parm'], **
                    self.dnspod_data['record_list'], **self.dnspod_data['update_record'])
        print(post)


def test():
    ''' for test '''
    dnspod_jsonData = dnspod_conf_read()
    dnspod = DNSPod(dnspod_jsonData)

    dnspod.print_postdata()

    ver = dnspod.getAPIversion()
    print(ver)

    recordlist = dnspod.getRecordList()
    print(recordlist)


def main():
    ''' main function '''
    dnspod_jsonData = dnspod_conf_read()
    dnspod = DNSPod(dnspod_jsonData)
    dnspod.run()


if __name__ == '__main__':
    main()
