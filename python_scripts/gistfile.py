#! /usr/bin/python3
#gpt4 
#写一个 爬虫 爬取 https://www4.bestjavporn.com/video/fc2-ppv-3187558/ 提取 class entry-title  下 title 信息   
#提取 class  video-description  Date       Duration: 信息   提取 class tags-list 下所有 tag信息

#gpt4 
#把python dict {'title': title, 'date': date, 'duration': duration, 'tags': tags } list 写入到 excel 中 按照对应的 key 


import requests
from bs4 import BeautifulSoup
import pandas as pd


def page_list(page_num):
    url = f"https://www4.bestjavporn.com/category/uncensored/page/{page_num}/"
    print("url", url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="thumb-block")
    rets = []

    for article in articles:
        a_tag = article.find("a")
        video_id = a_tag["href"].split("/")[-2]
        detail_url = f"https://www4.bestjavporn.com/video/{video_id}/"
        # print(detail_url)
        rets.append(detail_url)
    return rets


def get_video_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # 提取标题
        title = soup.find('h1', {'class': 'entry-title'}).get_text()
        print("title", title)

        # 提取日期和时长
        video_description = soup.find('div', {'id': 'video-about'})
        # print("video_description", video_description)
        date_duration = video_description.find_all(
            'div', {'id': 'video-date'})
        # print("date_duration", date_duration)
        date = date_duration[0].get_text()
        duration = date_duration[1].get_text()

        # 提取标签
        tags_list = soup.find('div', {'class': 'tags-list'})
        # print("tags_list", tags_list)
        tags = [tag.get_text() for tag in tags_list.find_all('a')]

        return {
            'title': title,
            'date': date,
            'duration': duration,
            'tags': tags,
            "url": url
        }

    else:
        print(
            f"Error: Failed to fetch the page. Status code: {response.status_code}")
        return None


def write_dict_list_to_excel(dict_list, filename):
    # 将字典列表转换为DataFrame
    df = pd.DataFrame(dict_list)

    # 将tags列中的列表转换为逗号分隔的字符串
    df['tags'] = df['tags'].apply(lambda x: ', '.join(x))

    # 将DataFrame写入Excel文件
    df.to_excel(filename, index=False)


dict_list = []
for page_num in range(1, 2):

    rets = page_list(page_num)
    for url in rets:
        video_info = get_video_info(url)
        if video_info:
            #     print(video_info)
            dict_list.append(video_info)
write_dict_list_to_excel(dict_list, 'video_data.xlsx')