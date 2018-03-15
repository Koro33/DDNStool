# DDNStool for Raspberry pi

## 介绍

`ddnstool.py` 是基于 DNSPod 服务的 **动态 DNS**（DDNS）脚本，用于检测 IP 变化并更新至 DNSPod。

## 特性

* 使用 DNSPod 的 [API](https://www.dnspod.cn/docs/index.html)，并有检测 API 版本的功能，防止重复错误提交导致账号被锁。

* 多外网 IP 获取方式，有效防止因 IP 获取不到而引起的错误。

* 详细日志记录，自动清理。

* 暂时只支持 Linux

> 暂时只支持 Linux 是 Crontab 的原因，理论上 Windows 平台使用计划任务也可以实现间隔运行。

## 版本要求

* python >= 3.5
* requests >= 2.18.4
* python-crontab >= 2.2.8

都可通过 `pip install` 命令安装

## 安装和配置

使用 **git** 获取 DDNStool

```bash
git clone https://github.com/ycg1024/DDNStool.git DDNStool
```

定位到目录，执行 `install.py`

```bash
cd DDNStool
python3 ./install.py # linux
```

使用模板建立配置文件

```bash
cp -p ./ddns_config.template.json ./ddns_config.json
leafpad ./ddns_config.json
```

打开的json文件按下面的说明进行修改，其中注释前加*的是必须要改的

```json
{
    "headers": {
        "User-Agent": "DDNStool for ras/1.1.0 (ycg1024@qq.com)" // 默认不用改
    },
    "comm_parm": {
        "login_token": "00000,00000000000000000000", // *完整的 API Token，是由 ID,Token 组合而成的，用英文的逗号分割
        "format": "json", // 默认不用改
        "lang": "en", // 默认不用改
        "error_on_empty": "no" // 默认不用改
    },
    "record_list": {
        "domain": "xxxx.xx" // *填入域名
    },
    "update_record": {
        "domain": "xxxx.xx", // *填入域名
        "record_id":"123456", //*填入记录id
        "sub_domain":"@", //默认全部解析
        "record_type":"A", //默认记录类型A
        "record_line_id":"0", //默认记录线路0
        "value":"0.0.0.0" // 占位字段不用改
    }
}
```

>* "comm_parm" -> "login_token": 完整的 API Token，是由 ID,Token 组合而成的，用英文的逗号分割
>* "record_list" -> "domain": 填入域名
>* "update_record" -> "domain": 填入域名
>* "update_record" -> "record_id": 填入记录id

## TODO List

[] 安装时自动获取 "update_record" 字段

## 更新

* **1.1.0**
  * 简化安装步骤
  * 修复部分IP获取方式失效的问题
  * 去除lxml库，改用Re的方式匹配IP地址

* **1.0.0**
  * 初始版本
  * 完成大部分功能

## License

[MIT](https://github.com/ycg1024/DDNStool/blob/master/LICENSE)
