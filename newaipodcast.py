# 假设这段代码是你的更新脚本，它需要定期运行
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
        link="http://yourwebsite.com/custom_rss.xml",  # 更改为实际的访问URL
        description="自动更新，包含关键词AI或OpenAI的播客单集",
        lastBuildDate=datetime.datetime.now(),
        items=all_filtered_episodes
    )

    save_path = "/path/to/your/webserver/directory/custom_rss.xml"  # 更改为实际的保存路径
    new_rss.write_xml(open(save_path, "w", encoding='utf-8'), encoding='utf-8')

# 假设你将这个函数设置为定期执行，例如每天运行一次
update_custom_rss()
