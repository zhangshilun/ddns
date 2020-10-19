from apscheduler.schedulers.blocking import BlockingScheduler
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import DescribeSubDomainRecordsRequest, AddDomainRecordRequest, \
    UpdateDomainRecordRequest
import json
import urllib


def sync():
    # AccessKey 和 Secret  建议使用 RAM 子账户的 KEY 和 SECRET 增加安全性
    AccessKeyID = ''
    AccessKeySecret = ''

    # 地区节点 可选地区取决于你的阿里云帐号等级，普通用户只有四个，分别是杭州、上海、深圳、河北，具体参考官网API
    regionId = 'cn-hangzhou'

    # 配置认证信息
    client = AcsClient(AccessKeyID, AccessKeySecret, regionId)

    # 设置主域名
    mainDomain = 'aaa.com'

    # 子域名列表  列表参数可根据实际需求增加或减少值
    subDomainList = ['nas']

    IP = getIp()

    # 循环子域名列表进行批量操作
    for subDomain in subDomainList:
        setDomainRecord(client, IP, subDomain, mainDomain)

    # 删除记录测试
    # delDomainRecord(client,'b.jsoner.com')

    # 新增或更新记录测试
    # setDomainRecord(client,'192.168.3.222','a',DomainName)

    # 获取记录测试
    # print (getDomainInfo(DomainName, 'y'))

    # 批量获取记录测试
    # for x in SubDomainList:
    #     print (getDomainInfo(DomainName, x))

    # 获取外网ip地址测试
    # print ('(' + getIp() + ')')


# 获取外网IP
def getIp():
    return json.load(urllib.request.urlopen('https://ipv4.jsonip.com/'))['ip']


# 查询记录
def getDomainInfo(client, subDomain):
    request = DescribeSubDomainRecordsRequest.DescribeSubDomainRecordsRequest()
    request.set_accept_format('json')

    # 设置要查询的记录类型为 A记录   官网支持A / CNAME / MX / AAAA / TXT / NS / SRV / CAA / URL隐性（显性）转发  如果有需要可将该值配置为参数传入
    request.set_Type("A")

    # 指定查记的域名 格式为 'test.example.com'
    request.set_SubDomain(subDomain)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')

    # 将获取到的记录转换成json对象并返回
    return json.loads(response)


# 新增记录 (默认都设置为A记录，通过配置set_Type可设置为其他记录)
def addDomainRecord(client, ip, subDomain, mainDomain):
    request = AddDomainRecordRequest.AddDomainRecordRequest()
    request.set_accept_format('json')

    # request.set_Priority('1')  # MX 记录时的必选参数
    request.set_TTL('600')  # 可选值的范围取决于你的阿里云账户等级，免费版为 600 - 86400 单位为秒
    request.set_Value(ip)  # 新增的 ip 地址
    request.set_Type('A')  # 记录类型
    request.set_RR(subDomain)  # 子域名名称
    request.set_DomainName(mainDomain)  # 主域名

    # 获取记录信息，返回信息中包含 TotalCount 字段，表示获取到的记录条数 0 表示没有记录， 其他数字为多少表示有多少条相同记录，正常有记录的值应该为1，如果值大于1则应该检查是不是重复添加了相同的记录
    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    relsult = json.loads(response)
    return relsult


# 更新记录
def updateDomainRecord(client, ip, subDomain, record_id):
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_accept_format('json')

    # request.set_Priority('1')
    request.set_TTL('600')
    request.set_Value(ip)  # 新的ip地址
    request.set_Type('A')
    request.set_RR(subDomain)
    request.set_RecordId(record_id)  # 更新记录需要指定 record_id ，该字段为记录的唯一标识，可以在获取方法的返回信息中得到该字段的值

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    return response


# 有记录则更新，没有记录则新增
def setDomainRecord(client, ip, subDomain, mainDomain):
    info = getDomainInfo(client, subDomain + '.' + mainDomain)
    if info['TotalCount'] == 0:
        print('准备添加新记录')
        add_result = addDomainRecord(client, ip, subDomain, mainDomain)
        print(add_result)
    elif info["TotalCount"] == 1:
        print('准备更新已有记录')
        record_id = info["DomainRecords"]["Record"][0]["RecordId"]
        old_ip = info["DomainRecords"]["Record"][0]["Value"]
        if ip == old_ip:
            print("新ip与原ip相同，无法更新！")
        else:
            update_result = updateDomainRecord(client, ip, subDomain, record_id)
            print('更新成功，返回信息：')
            print(update_result)
    else:
        # 正常不应该有多条相同的记录，如果存在这种情况，应该手动去网站检查核实是否有操作失误
        print("存在多个相同子域名解析记录值，请核查删除后再操作！")


if __name__ == '__main__':
    # 定时任务
    scheduler = BlockingScheduler()
    scheduler.add_job(sync, 'interval', seconds=10)
    scheduler.start()
    print("__main__")
