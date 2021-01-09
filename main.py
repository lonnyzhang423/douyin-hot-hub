import json
import logging
import os
import traceback
import urllib.parse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import util

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(level=logging.INFO)

# HOT_UR='https://is-lq.snssdk.com/api/suggest_words/?business_id=10016'
HOT_URL = "https://i-lq.snssdk.com/api/feed/hotboard_online/v1/?category=hotboard_online&count=50"

retries = Retry(total=2,
                backoff_factor=0.1,
                status_forcelist=[k for k in range(400, 600)])


def getContent(url: str) -> str:
    try:
        with requests.session() as s:
            s.mount("http://", HTTPAdapter(max_retries=retries))
            s.mount("https://", HTTPAdapter(max_retries=retries))
            return s.get(url).text
    except:
        log.error(traceback.format_exc())


def parseSearchList(content):
    """解析话题
    """
    def search(item):
        content = json.loads(item['content'])
        title = content['raw_data']['title']
        url = 'https://so.toutiao.com/search?keyword={}'.format(
            urllib.parse.quote(title))
        info = {'title': title, 'url': url}
        return info

    result = []
    try:
        data = json.loads(content)['data']
        result = [search(item) for item in data]
    except:
        log.error(traceback.format_exc())

    return result


def generateArchiveMd(items):
    """生成归档markdown
    """
    def search(item):
        return '1. [{}]({})'.format(item['title'], item['url'])

    searchs = '暂无数据'
    if items:
        searchs = '\n'.join([search(item) for item in items])

    readme = ''
    file = os.path.join('template','archive.md')
    with open(file) as f:
        readme = f.read()

    date = util.currentDateStr()
    now = util.currentTimeStr()
    readme = readme.replace("{date}", date)
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{searches}", searchs)

    return readme


def generateReadme(items):
    """生成今日readme
    """
    def search(item):
        return '1. [{}]({})'.format(item['title'], item['url'])

    searchs = '暂无数据'
    if items:
        searchs = '\n'.join([search(item) for item in items])

    readme = ''
    file = os.path.join('template','README.md')
    with open(file) as f:
        readme = f.read()

    now = util.currentTimeStr()
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{searches}", searchs)

    return readme


def handleTodayMd(md):
    log.debug('today md:%s', md)
    util.writeText('README.md', md)


def handleArchiveMd(md):
    log.debug('archive md:%s', md)
    name = util.currentDateStr()+'.md'
    file = os.path.join('archives', name)
    util.writeText(file, md)


def handleRawContent(content: str):
    log.debug('raw content:%s', content)
    name = util.currentDateStr()+'.json'
    file = os.path.join('raw', name)
    util.writeText(file, content)


def run():
    # 获取数据
    content = getContent(HOT_URL)
    searches = parseSearchList(content)

    # 最新数据
    todayMd = generateReadme(searches)
    handleTodayMd(todayMd)
    # 归档
    archiveMd = generateArchiveMd(searches)
    handleArchiveMd(archiveMd)
    # 原始数据
    handleRawContent(content)


if __name__ == "__main__":
    run()
