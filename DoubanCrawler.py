import expanddouban
import csv
import codecs
from bs4 import BeautifulSoup


def getMovieUrl(category, location=''):
    url = "https://movie.douban.com/tag/#/?sort=S&range=0,10&tags={},{}".format(category, location)
    # expanddouban.getHtml(getMovieUrl("电影","美国"))是页面的html,expanddouban.getHtml()中参数loadmore点击加载更多。
    return url


class Movie(object):
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    def show(self):
        return self.name,self.rate,self.location,self.category,self.info_link,self.cover_link


def getMovie(category, location):
    movie_list = []
    html = expanddouban.getHtml(getMovieUrl(category,location),loadmore=True)        # loadmore=True
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', attrs={'class': 'item'}):            #attrs 参数定义一个字典参数来搜索包含特殊属性的tag
        info_link = link.get('href')
        cover_link = link.find('img').get('src')
        name = link.find('p').find(class_='title').get_text()
        rate = link.find('p').find(class_='rate').get_text()
        m = Movie(name, rate, location, category, info_link, cover_link)
        if float(m.rate) >= 9.0:                        # 后续改进：将9.0形成变量，用户可输入控制删选。
            movie_list.append(m.show())
    return movie_list           # 列表格式：Movie，Movie

# 选取剧情类别，统计剧情的电影总数、统计剧情中哪三个地区数量最多。
#   统计每个类别的电影个数type_num、统计每个类别每个地区的电影个数=count，排序找max
def type_loc_num(category, location):
    html = expanddouban.getHtml(getMovieUrl(category,location),loadmore=True)    # loadmore=True
    soup = BeautifulSoup(html,'html.parser')
    count = len(soup.find_all('a', attrs={'class': 'item'}))
    return count


national = ("中国大陆","美国","香港","台湾","日本","韩国","英国","法国","德国",
            "意大利","西班牙","印度","加拿大","澳大利亚","爱尔兰","瑞典","巴西","丹麦")
type_loc_num_list = [type_loc_num("剧情",x) for x in national]
type_loc_num_dic = zip(type_loc_num_list, national)
sort_dic = sorted(type_loc_num_dic)

# print("第一多的地区是：{}，数量为{}".format(sort_dic[-1][1],sort_dic[-1][0]))
# print("第二多的地区是：{}，数量为{}".format(sort_dic[-2][1],sort_dic[-2][0]))
# print("第三多的地区是：{}，数量为{}".format(sort_dic[-3][1],sort_dic[-3][0]))
def type_num(category):
    html = expanddouban.getHtml(getMovieUrl(category),loadmore=True)      # loadmore=True
    soup = BeautifulSoup(html,'html.parser')
    count = len(soup.find_all('a', attrs={'class': 'item'}))
    return count


type_num_total = type_num("剧情")
first = float(sort_dic[-1][0]/type_num_total)*100
second = float(sort_dic[-2][0]/type_num_total)*100
third = float(sort_dic[-3][0]/type_num_total)*100
with open('output.txt','w') as f_txt:
    f_txt.write("第一多的地区是：{}，数量为{},同类占比{}".format(sort_dic[-1][1],sort_dic[-1][0],str(first)))
    f_txt.write("第二多的地区是：{}，数量为{}，同类占比{}".format(sort_dic[-2][1],sort_dic[-2][0],str(second)))
    f_txt.write("第三多的地区是：{}，数量为{},同类占比{}".format(sort_dic[-3][1],sort_dic[-3][0],str(third)))

with codecs.open('movies.csv', 'w', 'utf_8_sig') as f:
     wr = csv.writer(f)
     wr.writerow(['影片名', '评分', '地区', '影片类型', '页面链接', '图片链接'])
     wr.writerows(getMovie("喜剧", "香港"))
     wr.writerows(getMovie("科幻", "美国"))
     wr.writerows(getMovie("动作", "韩国"))