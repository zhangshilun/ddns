# ddns

#### 介绍
    ddns_aliyun
        通过阿里云提供的SDK，然后自己编写程序新增或者修改域名的解析，达到动态解析域名的目的；主要应用于pppoe拨号的环境，比如家里设置了服务器，但是外网地址经常变化的场景；再比如公司的pppoe网关，需要建立vpn的场景。

#### 软件架构
    一、获取阿里云的accessKeyId和accessSecret
    二、获取外网ip
    三、判断外网ip是否与之前一致
    四、外网ip不一致时，新增或者更新域名解析记录

#### 安装教程
    1.  pip3 install APScheduler
    2.  pip3 install aliyun-python-sdk-core
    3.  pip3 install aliyun-python-sdk-domain
    4.  pip install aliyun-python-sdk-alidns

#### 使用说明
    1.  ./start.py