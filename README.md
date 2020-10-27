# ddns

#### 介绍

    ddns_aliyun.py
        通过阿里云提供的SDK，然后自己编写程序新增或者修改域名的解析，达到动态解析域名的目的；
        主要应用于pppoe拨号的环境。

#### 软件逻辑

    1.  获取阿里云的accessKeyId和accessSecret
        建议新建RAM用户赋予 AliyunDNSFullAccess 权限即可
    2.  获取外网ip
    3.  判断外网ip是否与之前一致
    4.  外网ip不一致时，新增或者更新域名解析记录

#### 安装教程

    1.  pip3 install APScheduler
    2.  pip3 install aliyun-python-sdk-core
    3.  pip3 install aliyun-python-sdk-domain
    4.  pip install aliyun-python-sdk-alidns

#### 使用说明
        
    1.  定时执行间隔
    
        scheduler.add_job(sync, 'interval', seconds=10)
        定时器默认10秒执行一次，按自己需求在__main__方法修改即可
        
    2.  执行
    
        python ddns_aliyun.py
