
import requests
import pymongo
def getPage(page=1):
    #json请求的数据地址
    httpUrl = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1583543459901&countryId=&cityId=&bgIds=&productId=&categoryId=40001001&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    httpUrl = httpUrl.format(1)
    #请求数据
    result = requests.get(httpUrl)
    #获取招聘岗位列表
    posts = result.json()['Data']['Posts']
    for (i,item) in enumerate(posts):
        #获取每个照片信息的POSTID
        postid = item['PostId']
        #获取详细信息
        get_info(postid)
        print(postid)
def get_info(postid):
    httpUrl = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1583543509457&postId={}&language=zh-cn'
    httpUrl = httpUrl.format(postid)
    #获取详细工作岗位的数据
    result = requests.get(httpUrl)
    data = result.json()['Data']
    #将数据插入数据库
    insert_data(data)
    print(result.json()['Data']['RecruitPostName'])
    print(data)
    
#get_info(1123178083830992896)


def insert_data(data):
    #连接mongodb数据库
    client = pymongo.MongoClient('mongodb://localhost:27017')
    #创建laochen数据库
    db = client['laochen']
    #创建jobs集合
    col = db['jobs']
    #插入数据
    col.insert_one(data)
# for i in range(1,20):
#     print(i)
#     getPage(i)


client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['laochen']
col = db['jobs']
options = {
    'RecruitPostName':{
        '$regex':"后台"
    }
}
for item in col.find(options):
    print(item)
