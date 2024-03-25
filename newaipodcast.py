import os
import feedparser
import PyRSS2Gen
import datetime
import xml.etree.ElementTree as ET
from io import BytesIO

def update_custom_rss():
    rss_urls = [
        "https://feed.xyzfm.space/evgg6xle9rdc",
        "https://feed.xyzfm.space/xxg7ryklkkft",
    ]
    keywords = ["AI", "OpenAI"]
    all_filtered_episodes = []

    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if any(keyword.lower() in (entry.title + " " + entry.description).lower() for keyword in keywords):
                episode = PyRSS2Gen.RSSItem(
                    title=entry.title,
                    link=entry.link,
                    description=entry.description,
                    guid=PyRSS2Gen.Guid(entry.link),
                    pubDate=datetime.datetime(*entry.published_parsed[:6])
                )
                all_filtered_episodes.append(episode)

    new_rss = PyRSS2Gen.RSS2(
        title="AI相关的播客集合",
        link="https://emmmme.com/aipodcast",  # 确保这是你的RSS feed最终托管的URL
        description="自动更新，包含关键词AI或OpenAI的播客单集",
        lastBuildDate=datetime.datetime.now(),
        items=all_filtered_episodes
    )

    save_path = "./rss/filtered_podcast_rss.xml"  # 更改为实际的保存路径

    # 生成并修改RSS XML以添加atom:link元素
    rss_xml = BytesIO()
    new_rss.write_xml(rss_xml, encoding='utf-8')
    rss_xml.seek(0)  # 回到BytesIO对象的开始位置
    rss_tree = ET.parse(rss_xml)
    rss_root = rss_tree.getroot()

    ET.register_namespace('atom', 'http://www.w3.org/2005/Atom')
    atom_link = ET.Element("{http://www.w3.org/2005/Atom}link", {
        "href": "https://zacfire.github.io/newpodcastforAI/rss/filtered_podcast_rss.xml",  # RSS文件的实际URL
        "rel": "self",
        "type": "application/rss+xml"
    })
    rss_root.find('channel').insert(0, atom_link)

    # 确保目录存在
    dir_name = os.path.dirname(save_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # 保存修改后的RSS文件
    rss_tree.write(save_path, encoding='utf-8', xml_declaration=True)

# 运行更新函数
update_custom_rss()
