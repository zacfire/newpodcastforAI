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
            if any(keyword.lower() in (entry.title + " " + entry.get("description", "")).lower() for keyword in keywords):
                if 'links' in entry:
                    for link in entry.links:
                        if link.rel == 'enclosure':
                            episode = PyRSS2Gen.RSSItem(
                                title=entry.title,
                                link=entry.link,
                                description=entry.get("description", ""),
                                guid=PyRSS2Gen.Guid(entry.id),
                                pubDate=datetime.datetime(*entry.published_parsed[:6]),
                                enclosure=PyRSS2Gen.Enclosure(url=link.href, length=str(link.length), type=link.type)
                            )
                            all_filtered_episodes.append(episode)
                            break  # 假设每个条目只有一个音频文件链接

    new_rss = PyRSS2Gen.RSS2(
        title="AI相关的节目",
        link="https://emmmme.com/",  # 更改为你的RSS feed托管的URL
        description="自动更新，42章经和on board！播客里包含关键词AI或OpenAI的播客单集",
        lastBuildDate=datetime.datetime.now(),
        language="zh-CN",
        items=all_filtered_episodes
    )

    save_path = "./rss/filtered_podcast_rss.xml"  # 更改为实际的保存路径

    # 生成并修改RSS XML以添加额外的播客元素
    rss_xml = BytesIO()
    new_rss.write_xml(rss_xml, encoding='utf-8')
    rss_xml.seek(0)
    rss_tree = ET.parse(rss_xml)
    rss_root = rss_tree.getroot()

    # 添加命名空间
    ET.register_namespace('atom', 'http://www.w3.org/2005/Atom')
    ET.register_namespace('itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')

    # 添加atom:link元素
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
    with open(save_path, "wb") as f:
        rss_tree.write(f, encoding='utf-8', xml_declaration=True)

# 运行更新函数
update_custom_rss()
