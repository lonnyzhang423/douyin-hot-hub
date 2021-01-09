import json
import os
import traceback

import util
from util import logger


def generateArchiveMd(items):
    """生成归档markdown
    """
    def search(item):
        return '1. [{}]({})'.format(item['title'], item['url'])

    searchs = '暂无数据'
    if items:
        searchs = '\n'.join([search(item) for item in items])

    readme = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        readme = f.read()

    date = util.current_date()
    now = util.current_time()
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
    file = os.path.join('template', 'README.md')
    with open(file) as f:
        readme = f.read()

    now = util.current_time()
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{searches}", searchs)

    return readme


def handleTodayMd(md):
    logger.debug('today md:%s', md)
    util.write_text('README.md', md)


def handleArchiveMd(md):
    logger.debug('archive md:%s', md)
    name = util.current_date()+'.md'
    file = os.path.join('archives', name)
    util.write_text(file, md)


def handleRawContent(content: str):
    logger.debug('raw content:%s', content)
    name = util.current_date()+'.json'
    file = os.path.join('raw', name)
    util.write_text(file, content)


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
