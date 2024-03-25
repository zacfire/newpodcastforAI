import os
import feedparser
import PyRSS2Gen
import datetime

def update_custom_rss():
    rss_urls = [
        "https://feed.xyzfm.space/evgg6xle9rdc",
        "https://feed.xyzfm.space/xxg7ryklkkft",
    ]
    include_keywords = ["AI", "OpenAI", "LLM", "大模型", "AIGC"]
    exclude_phrases = ["AI创业公司打工人", "AI私董会"]
    all_filtered_episodes = []

    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            content = entry.title + " " + entry.get("description", "")
            if any(keyword.lower() in content.lower() for keyword in include_keywords):
                if not any(phrase in content for phrase in exclude_phrases):
                    audio_url = None
                    audio_length = 0
                    audio_type = 'audio/mpeg'  # 默认MIME类型
                    for link in entry.links:
                        if link.rel == 'enclosure':
                            audio_url = link.href
                            audio_length = link.length if hasattr(link, 'length') else 0
                            audio_type = link.type if hasattr(link, 'type') else 'audio/mpeg'
                            break  # 假设每个条目只有一个音频文件链接
                    if audio_url:
                        episode = PyRSS2Gen.RSSItem(
                            title=entry.title,
                            link=entry.link,
                            description=entry.get("description", ""),
                            guid=PyRSS2Gen.Guid(entry.id),
                            pubDate=datetime.datetime(*entry.published_parsed[:6]),
                            enclosure=PyRSS2Gen.Enclosure(url=audio_url, length=audio_length, type=audio_type)
                        )
                        all_filtered_episodes.append(episode)

    new_rss = PyRSS2Gen.RSS2(
        title="与AI有关",
        link="https://emmmme.com/",
        description="自动更新，42章经和on board！播客里包含关键词AI或OpenAI的播客单集",
        lastBuildDate=datetime.datetime.now(),
        language="zh-CN",
        items=all_filtered_episodes,
        image=PyRSS2Gen.Image(url="https://raw.githubusercontent.com/zacfire/newpodcastforAI/main/AI%20Logo%20Raw.png", title="与AI有关", link="https://emmmme.com/")
    )

    save_path = "./rss/filtered_podcast_rss.xml"  # 更改为实际的保存路径

    # 确保目录存在
    dir_name = os.path.dirname(save_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # 保存修改后的RSS文件
    with open(save_path, "w", encoding='utf-8') as f:
        new_rss.write_xml(f, encoding='utf-8')

# 运行更新函数
update_custom_rss()
