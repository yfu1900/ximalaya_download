import requests
from bs4 import BeautifulSoup

# 伪装请求头
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

# 通过分析唐诗三百首页面 https://www.ximalaya.com/renwen/2776000/ 得知，其实际url字段为 albumId=字段&pageNum=页码，故初始化页码为1
p = 1
# 创建空列表，用来存放每首唐诗的真实ID
list_poem_url = []

# 创建循环，爬取一共11页的唐诗
for p in range(1,12):
    # 爬取网页
    res = requests.get('https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=2776000&pageNum='+ str(p), headers=headers)
    # 把爬到的页面进行.json()
    json_poem = res.json()
    # 分析得知，每首唐诗页面真实url隐藏于 data - tracks 下
    list_poem = json_poem['data']['tracks']

    # 创建循环，获取每首唐诗的页面
    for poem in list_poem:
        # 获取每首唐诗真实url
        poem_url = poem['url']
        # 由于每首唐诗真实url变动仅为最后的唐诗ID，故对url进行切片，切除前面的 /renwen/27760000/，留下最后的ID
        poem_url_id = poem_url[16:]
        # 把ID加入list_poem_url列表
        list_poem_url.append(poem_url_id)

# 检查列表list_poem_url 是否正常
# print(list_poem_url)

# 创建循环，对每首诗进行命名、获取下载地址、自动命名下载
for i in list_poem_url:
    # 使用列表list_poem_url中的ID和每首诗所在网页的前缀进行拼接，得到每首诗的网页
    res_poem_name_url = 'https://www.ximalaya.com/renwen/2776000/'+ str(i)
    # 使用列表list_poem_url中的ID和每首诗真实url前半段和后半段进行拼接
    res_poem_url = 'https://www.ximalaya.com/revision/play/v1/audio?id='+ str(i) + '&ptype=1'
    # 爬取网页内容
    res_poem_page = requests.get(res_poem_name_url, headers=headers)
    res_poem = requests.get(res_poem_url, headers=headers)
    # 解析网页，目的是提取诗的名字
    res_poem_name = BeautifulSoup(res_poem_page.text, 'lxml')
    # 把爬到的页面进行.json()，目的是提取每首诗的真实可下载url
    json_res_poem = res_poem.json()
    # 获取诗的名字
    poem_name = res_poem_name.find('h1', class_='title-wrapper _Td').text
    # 拼接后，获得每首诗真实可下载url，位于 data - src
    download_url = json_res_poem['data']['src']
    
    # 打印，作用只是为了运行时知道下载到哪一首了 =.=
    print(poem_name)
    print(download_url + '\n')

    # 把获得的诗的真实可下载url下载到本地
    download_file = requests.get(download_url, headers=headers)
    download_file_content = download_file.content

    # 自动根据诗的名称命名下载的诗
    with open (poem_name + '.m4a', 'wb') as file1:
        # 写入
        file1.write(download_file_content)
        
