import os
import feedparser
import PyRSS2Gen
import datetime

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
        link="https://emmmme.com/aipodcast.xml",  # 更改为实际的访问URL
        description="自动更新，包含关键词AI或OpenAI的播客单集",
        lastBuildDate=datetime.datetime.now(),
        items=all_filtered_episodes
    )

    save_path = "./rss/filtered_podcast_rss.xml"  # 更改为实际的保存路径

    # 确保目录存在
    dir_name = os.path.dirname(save_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # 保存RSS文件
    new_rss.write_xml(open(save_path, "w", encoding='utf-8'), encoding='utf-8')

# 运行更新函数
update_custom_rss()
