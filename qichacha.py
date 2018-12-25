import requests
from gongju import format_headers
from pprint import pprint
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
import time

headers = format_headers("""
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: max-age=0
referer: https://m.qichacha.com/firm_6bc7e7ccdb755391651316a0227c059b.shtml
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
""")

company_url = 'https://m.qichacha.com/firm_6bc7e7ccdb755391651316a0227c059b.shtml'
session = HTMLSession()
resp = session.get(company_url, headers=headers)
resp.encoding = 'utf-8'
soup = BeautifulSoup(resp.text,'lxml')
"""头部信息"""
toubuxinxi = soup.find('div',class_="content-block")
t_gongsimingzi = toubuxinxi.find('div',class_="company-name").next_element
t_cunxuzhuangtai = toubuxinxi.find('span',class_="company-status status-normal").text
t_zerenren = toubuxinxi.find('a',class_="oper").text
t_zerenrenzhiwei = toubuxinxi.find('span',class_="oper-desc").text.strip()
t_lianxifangshi = toubuxinxi.find('div',class_="contact-info-wrap").text
t_dizhi = toubuxinxi.find('div',class_="address").text.strip()
toubuxinxi_dict = {'公司名':t_gongsimingzi,t_zerenrenzhiwei:t_zerenren,'联系方式':t_lianxifangshi,'地址':t_dizhi}

"""基本信息"""
jibenxinxi_dict = {}
jibenxinxi = soup.find('div',class_="basic-wrap")
jibenxinxi_list = jibenxinxi.find_all(class_="basic-item")
for _ in jibenxinxi_list:
    jibenxinxi_key = _.find('div',class_="basic-item-left").text.strip()
    jibenxinxi_value = _.find('div',class_="basic-item-right").text.strip()
    _jbxx_dict = {jibenxinxi_key:jibenxinxi_value}
    jibenxinxi_dict.update(_jbxx_dict)
gudongxinxi = soup.find('div',id="partners")
gudongxinxi_list = gudongxinxi.find_all('div',class_="stock-wrap")
gdxx_dict_all = {}
for _ in gudongxinxi_list:
    gdxx_gufenleixing = _.find(class_="text-blue a-decoration").text
    gdxx_gufenchiyouren = _.find(class_="company-status status-normal").text
    gdxx_dict = {gdxx_gufenleixing:gdxx_gufenchiyouren}
    gdxx_stock_subtitle = _.find_all(class_="stock-subtitle")
    gdxx_stock_text = _.find_all(class_="stock-text")
    for i in range(len(gdxx_stock_subtitle)):
        gdxx_temporary_dict = {gdxx_stock_subtitle[i].text.strip():gdxx_stock_text[i].text.strip()}
        gdxx_dict.update(gdxx_temporary_dict)
    _gdxx_dict = {gdxx_gufenleixing:gdxx_dict}
    gdxx_dict_all.update(_gdxx_dict)

"""主要人员"""
zhuyaorenyuan = soup.find('div',id="employees")
zhuyaorenyuan_list = zhuyaorenyuan.find_all('div',class_="stock-wrap")
zyry_ds = []
zyry_dsz = []
zyry_fdsz = []
zyry_js = []
zyry_zjl = []
for _ in zhuyaorenyuan_list:
    zhuyaorenyuan_key = _.find('div',class_="employee-job").text
    zhuyaorenyuan_value = _.find('div',class_="employee-name").text
    if zhuyaorenyuan_key == '董事':
        zyry_ds.append(zhuyaorenyuan_value)
    if zhuyaorenyuan_key == '董事长':
        zyry_dsz.append(zhuyaorenyuan_value)
    if zhuyaorenyuan_key == '副董事长':
        zyry_fdsz.append(zhuyaorenyuan_value)
    if zhuyaorenyuan_key == '监事':
        zyry_js.append(zhuyaorenyuan_value)
    if zhuyaorenyuan_key == '总经理':
        zyry_zjl.append(zhuyaorenyuan_value)
zhuyaorenyuan_dict = {'董事':zyry_ds,'董事长':zyry_dsz,'副董事长':zyry_fdsz,'监事':zyry_js,'总经理':zyry_zjl}

"""变更信息"""
biangengjilu = soup.find('div',id="changeRecord")
biangengjilu_list = biangengjilu.find_all('div',class_="change-wrap")
bgjl_dict_all = {}
len(biangengjilu_list)
for _ in biangengjilu_list:
    bgjl_biangengxiangqing_list = []
    bgjl_biangengshijian_list = []
    bgjl_biangengqian_list = []
    bgjl_biangenghou_list = []
    bgjl_biangengshixiang = _.find('div',class_="change-date").text.strip()
    bgjl_biangengshijian = _.find_all('div',class_="change-title")
    [bgjl_biangengshijian_list.append(i.text.strip().replace(' ', '').replace('\n', '')) for i in bgjl_biangengshijian]
    bgjl_biangengqian = _.find(class_="change-left").find_all(class_="change-item-content")
    [bgjl_biangengqian_list.append(i.text.strip().replace(' ', '').replace('\n', '')) for i in bgjl_biangengqian]
    bgjl_biangenghou = _.find(class_="change-right").find_all(class_="change-item-content")
    [bgjl_biangenghou_list.append(i.text.strip().replace(' ', '').replace('\n', '')) for i in bgjl_biangenghou]
    bgjl_dict = {'变更详情':bgjl_biangengshixiang,'变更时间':bgjl_biangengshijian_list,'变更前':bgjl_biangengqian_list,'变更后':bgjl_biangenghou_list}
    _bgjl_dict = {bgjl_biangengshixiang:bgjl_dict}
    bgjl_dict_all.update(_bgjl_dict)

"""底部信息"""
diduanxinxi = resp.html.find('div.content-block')[-1]
diduanxinxi_list = diduanxinxi.find('a')
diduanxinxi_dict_all = {}
for _ in diduanxinxi_list:
    ddxx_mingzi = _.text.replace('\n','条 ')
    ddxx_links = [i for i in _.absolute_links][0]
    diduanxinxi_dict = {ddxx_mingzi:ddxx_links}
    diduanxinxi_dict_all.update(diduanxinxi_dict)

"""遍历底端链接"""
for _ in diduanxinxi_dict_all.values():
    # print(_)
    if re.search('Branch',_):
        branch_dict_all = {}
        branch_resp = requests.get(_, headers=headers)
        fenzhijiegou_chushiye = str(re.search('class="top-bar-title">(.*?)<script type="text/javascript">',branch_resp.text,re.S).group())
        branch_gsm = re.findall('class="list-item" >(.*?)</div>',fenzhijiegou_chushiye)
        branch_links = re.findall('a href="(.*?)"',fenzhijiegou_chushiye)
        branch_links = ['https://m.qichacha.com/'+i for i in branch_links]
        for i in range(len(branch_gsm)):
            _branch_dict = {'分支机构-公司名':branch_gsm[i],'分支机构-公司链接':branch_links[i]}
            branch_dict = {branch_gsm[i]:_branch_dict}
            branch_dict_all.update(branch_dict)


        # for i in branch_dict_all.values():
        #     """容易出错 响应网页为空"""
        #     fenzhijiegou_dict = {}
        #     new_resp = requests.get(i,headers=headers)
        #     new_soup = BeautifulSoup(new_resp.text,'lxml')
        #     fenzhijigou = new_soup.find('div', class_="content-block")
        #     fenzhijigou_qiyemingcheng = fenzhijigou.find('div', class_="company-name").next_element
        #     fenzhijigou_zhucezhuangtai = fenzhijigou.find('span', class_="company-status status-normal").text
        #     fenzhijigou_zhuceshijian = re.search('\s*(\d.*-\d\d-\d\d)',str(new_soup.find('div',class_="basic-wrap"))).group(1)
        #     fenzhijigou_faren = re.search('basic-item-right text-blue".*?">(.*?)</div>',str(new_soup.find('div',class_="basic-wrap"))).group(1)
        #     _fzjg_dict = {'分支结构-公司名':fenzhijigou_qiyemingcheng,'分支结构-注册时间':fenzhijigou_zhuceshijian,
        #                   '分支结构-注册状态':fenzhijigou_zhucezhuangtai,'分支结构-法人':fenzhijigou_faren}
        #     fenzhijiegou_dict = {fenzhijigou_qiyemingcheng:_fzjg_dict}
        #     fenzhijiegou_dict_all.update(fenzhijiegou_dict)
        # time.sleep(10)

    if re.search('Investment',_):
        pass
    if re.search('Report',_):
        report_list_all = []
        report_resp = requests.get(_, headers=headers)
        qiyenianbao_chushiye = str(re.search('<div class="top-bar-title">(.*?)<div class="ft">', report_resp.text, re.S).group())
        report_niandu = re.findall('class="item-title">(.*?)</div>', qiyenianbao_chushiye)
        report_riqi = re.findall('class="item-subtitle">(.*?\d)</div>', qiyenianbao_chushiye)
        report_links = re.findall('a href="(.*?)".class="a-decoration"', qiyenianbao_chushiye)
        report_links = ['https://m.qichacha.com/'+i for i in report_links]
        for i in range(len(report_niandu)):
            _report_dict = {'年度报表名': report_niandu[i], '公示日期': report_riqi[i], '年度报表链接': report_links[i]}
            report_dict = {report_niandu[i]:_report_dict}
            report_list_all.append(report_dict)
        for i in report_links:
            """i = qiyenianbao_xiangqing_dict_all"""
            qiyenianbao_xiangqing_dict_all = {}
            report_next_resp = requests.get(i, headers=headers)
            report_next_soup = BeautifulSoup(report_next_resp.text,'lxml')
            key = report_next_soup.find('div',class_="top-bar-title").text
            qiyenianbao_cijiye = report_next_soup.find_all('div',class_="company-essential-information")
            for k in qiyenianbao_cijiye:
                qiyenianbao_xiangqing_dict = {}
                qiyenianbao_cijiye_title = k.find('div', class_="title-font").text
                right = k.select('.company-col .company-subtitle > div')[::2]
                left = k.select('.company-col .company-subtitle > div')[1::2]
                qiyenianbao_cijiye_left = [_.text.strip() for _ in left]
                qiyenianbao_cijiye_right = [_.text.strip() for _ in right]
                for _k in range(len(qiyenianbao_cijiye_left)):
                    _qiyenianbao_xiangqing_dict = {qiyenianbao_cijiye_left[_k]: qiyenianbao_cijiye_right[_k]}
                    qiyenianbao_xiangqing_dict.update(_qiyenianbao_xiangqing_dict)
                _qiyenianbao_xiangqing_dict_all = {qiyenianbao_cijiye_title: qiyenianbao_xiangqing_dict}
                qiyenianbao_xiangqing_dict_all.update(_qiyenianbao_xiangqing_dict_all)
            qiyenianbao_xiangqing_dict_all = {'data':qiyenianbao_xiangqing_dict_all}
            for _k in report_list_all:
                if _k.get(key):
                    _k.get(key).update(qiyenianbao_xiangqing_dict_all)
                else:
                    continue
                print(_k)
            # exit()

            """
            nianbao = [
                {'name':'2017年'
                 'time':'2018-06-22',
                 'data':{
                    '网站或网店信息'："无"
                    }
                 },
                 {'name':'2016年'
                 'time':'2018-06-22',
                 'data':{
                    '网站或网店信息'："无"
                    }
                 },
            ]
            
            """

    if re.search('ShangBiao',_):
        pass
    if re.search('Patent',_):
        pass
    if re.search('JudgementType',_):
        pass



