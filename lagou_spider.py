#!/home/fy/.virtualenvs/spider_py2/bin/python2.7
# coding=utf-8
import requests,json,time,random
import pymongo,sys,urllib2,threading
import page_num
import proxy


reload(sys)
sys.setdefaultencoding('utf-8')
client = pymongo.MongoClient('localhost', 27017)
client.lagou.authenticate('root', 'root', mechanism='MONGODB-CR')
lagou = client['lagou']
item_info = lagou['item_info']


# 将需要的数据写入mongodb
def write_file(result, category):
    for item in result["content"]["positionResult"]["result"]:
        data = {
            "category": category,
            "companyId": item["companyId"],
            "positionName": item["positionName"],
            "workYear": item["workYear"],
            "education": item["education"],
            "jobNature": item["jobNature"],
            "positionId": item["positionId"],
            "createTime": item["createTime"],
            "city": item["city"],
            "industryField": item["industryField"],
            "positionAdvantage": item["positionAdvantage"],
            "salary": item["salary"],
            "companySize": item["companySize"],
            "companyFullName": item["companyFullName"],
            "financeStage": item["financeStage"]
        }
        item_info.insert_one(data)


def load_data(url, data, headers):
    while True:
    	# 从代理池获取代理，若代理连续5次不能使用，从池中删除
        pro = proxy.get_proxy()
        proxies = {"http": "http://{}".format(pro)}
        print proxies["http"]
        retry_count = 5
        while retry_count > 0:
            try:
                t = random.randint(1, 5)
                time.sleep(t)
                # 发起请求
                response = requests.post(
                    url, data=data, headers=headers, proxies=proxies)
                text = response.text                
                result = json.loads(text)
                return result
            except Exception:
                retry_count -= 1
        proxy.delete_proxy(pro)


# 拼接headers
def pre_work(url, category, num):
    for i in range(1, num + 1):
        if i == 1:
            first = 'true'
        else:
            first = 'false'
        data = {
            'first': first,
            'pn': str(i),
            'kd': category,
        }
        user_list = [
            'Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        ]
        user_agent = random.choice(user_list)
        cookie_list = [
            'user_trace_token=20170504145147-247f6c9a-3096-11e7-9695-525400f775ce; LGUID=20170504145147-247f73e8-3096-11e7-9695-525400f775ce; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=7; gate_login_token=d52e941c3bbe0b8bcb2c5a0ef88b521d3b77d553dbbd46d3; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAAAIAACBI5A2D13FBA002401EDED81C3EF5AD0671; X_HTTP_TOKEN=c8cd50fd33fb9fc986d045b950b85d50; TG-TRACK-CODE=index_navigation; _gat=1; LGSID=20180130164920-766b4722-059a-11e8-a0fc-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FC%252B%252B%2F%3FlabelWords%3Dlabel; LGRID=20180130164920-766b4880-059a-11e8-a0fc-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1517293637; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1517302161; _ga=GA1.2.1407291709.1517293637; _gid=GA1.2.2122956848.1517293637; SEARCH_ID=16d077744b4a45b4a45e2f7310aa3b47',
            'user_trace_token=20180128133936-28f494de-e8ef-4aaf-9957-a05a6a7516e0; JSESSIONID=ABAAABAACDBABJBF02BB9683C0CD9B7327322D83E3C1A36; _ga=GA1.2.910212977.1517120107; LGUID=20180128141504-94dfc9f2-03f2-11e8-abb7-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1517120107; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.513659644.1517277081; TG-TRACK-CODE=index_navigation; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1517302067; _gat=1; LGSID=20180130164745-3d9c24e7-059a-11e8-abd5-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_HTML5%3Fpx%3Ddefault%26city%3D%25E5%2585%25A8%25E5%259B%25BD; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_HTML5%3Fpx%3Ddefault%26city%3D%25E5%258C%2597%25E4%25BA%25AC; LGRID=20180130164745-3d9c27cf-059a-11e8-abd5-5254005c3644; SEARCH_ID=6702e5532ebc4e4ca8ff9b8f1b9bb91f',
        ]
        cookie = random.choice(cookie_list)
        headers = {
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_' + category + '?city=全国',
            'User-Agent': user_agent,
            'Cookie': cookie,
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest',
        }
        result = load_data(url, data, headers)        
        write_file(result, category)


def start_p():
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    #获取类目名称
    with open('/home/fy/workspaces/spider/lagou_spider/category.txt', 'r')as f:
        text = f.read()
    categorys = text.split(' ')
    for category in categorys:
        print category
        # 获取每个类目的页数
        num = page_num.get_num(category)
        print num        
        pre_work(url, category, num)
