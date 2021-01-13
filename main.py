import os
import time
import urllib

from requests import Response

import util
from douyin import Douyin
from util import logger


def generate_archive_md(searches, stars, lives, musics):
    """生成今日readme
    """
    def search(item):
        word = item['word']
        return '1. {}'.format(word)

    def star(item):
        name = item['user_info']['nickname']
        uid = item['user_info']['uid']
        suid = item['user_info']['sec_uid']
        url = 'https://www.iesdouyin.com/share/user/{}?sec_uid={}'.format(
            uid, suid)
        return '1. [{}]({})'.format(name, url)

    def live(item):
        uid = item['user']['id']
        suid = item['user']['sec_uid']
        nickname = item['user']['nickname']
        title = item['room']['title']
        roomid = item['room']['id']
        user_url = 'https://www.iesdouyin.com/share/user/{}?sec_uid={}'.format(
            uid, suid)
        live_url = 'https://webcast.amemv.com/webcast/reflow/'+str(roomid)
        if not title:
            title = '看直播'
        return '1. [{}]({}) - [{}]({})'.format(title, live_url, nickname, user_url)

    def music(item):
        info = item['music_info']
        title = info['title']
        author = info['author']
        if 'play_url' in info:
            play_url = info['play_url']['uri']
            return '1. [{}]({}) - {}'.format(title, play_url, author)
        return '1. {} - {}'.format(title, author)

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    starMd = '暂无数据'
    if stars:
        starMd = '\n'.join([star(item) for item in stars])

    liveMd = '暂无数据'
    if lives:
        liveMd = '\n'.join([live(item) for item in lives])

    musicMd = '暂无数据'
    if musics:
        musicMd = '\n'.join([music(item) for item in musics])

    readme = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        readme = f.read()

    today = util.current_date()
    now = util.current_time()
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{searches}", searchMd)
    readme = readme.replace("{stars}", starMd)
    readme = readme.replace("{lives}", liveMd)
    readme = readme.replace("{musics}", musicMd)

    filename = '{}-brand.md'.format(today)
    brandMd = '[{}]({})'.format(filename, filename)
    readme = readme.replace("{brands}", brandMd)

    return readme


def generate_readme(searches, stars, lives, musics):
    """生成今日readme
    """
    def search(item):
        word = item['word']
        return '1. {}'.format(word)

    def star(item):
        name = item['user_info']['nickname']
        uid = item['user_info']['uid']
        suid = item['user_info']['sec_uid']
        url = 'https://www.iesdouyin.com/share/user/{}?sec_uid={}'.format(
            uid, suid)
        return '1. [{}]({})'.format(name, url)

    def live(item):
        uid = item['user']['id']
        suid = item['user']['sec_uid']
        nickname = item['user']['nickname']
        title = item['room']['title']
        roomid = item['room']['id']
        user_url = 'https://www.iesdouyin.com/share/user/{}?sec_uid={}'.format(
            uid, suid)
        live_url = 'https://webcast.amemv.com/webcast/reflow/'+str(roomid)
        if not title:
            title = '看直播'
        return '1. [{}]({}) - [{}]({})'.format(title, live_url, nickname, user_url)

    def music(item):
        info = item['music_info']
        title = info['title']
        author = info['author']
        if 'play_url' in info:
            play_url = info['play_url']['uri']
            return '1. [{}]({}) - {}'.format(title, play_url, author)
        return '1. {} - {}'.format(title, author)

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    starMd = '暂无数据'
    if stars:
        starMd = '\n'.join([star(item) for item in stars])

    liveMd = '暂无数据'
    if lives:
        liveMd = '\n'.join([live(item) for item in lives])

    musicMd = '暂无数据'
    if musics:
        musicMd = '\n'.join([music(item) for item in musics])

    readme = ''
    file = os.path.join('template', 'README.md')
    with open(file) as f:
        readme = f.read()

    today = util.current_date()
    now = util.current_time()
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{searches}", searchMd)
    readme = readme.replace("{stars}", starMd)
    readme = readme.replace("{lives}", liveMd)
    readme = readme.replace("{musics}", musicMd)

    filename = '{}-brand.md'.format(today)
    file = os.path.join('archives', filename)
    brandMd = '[{}]({})'.format(filename, file)
    readme = readme.replace("{brands}", brandMd)

    return readme


def save_readme(md):
    logger.info('today md:%s', md)
    util.write_text('README.md', md)


def save_archive_md(md):
    logger.info('archive md:%s', md)
    name = util.current_date()+'.md'
    file = os.path.join('archives', name)
    util.write_text(file, md)


def saveRawResponse(resp: Response, filename: str):
    """保存原始响应内容
    """
    if resp:
        content = resp.text
        filename = '{}.json'.format(filename)
        logger.info('save response:%s', filename)
        date = util.current_date()
        file = os.path.join('raw', date, filename)
        util.write_text(file, content)


def saveBrandRawResponse(resp: Response, category: str):
    """保存品牌榜响应内容
    """
    if resp:
        content = resp.text
        date = util.current_date()
        filename = '{}.json'.format(category)
        logger.info('save response:%s', filename)
        file = os.path.join('raw', date, 'brand', filename)
        util.write_text(file, content)


def generate_brand_md(brand_map: map):
    """品牌榜md
    """
    def brand(item):
        name = item['name']
        logo_url = item['logo_url']['uri']
        key = urllib.parse.quote(name)
        search_url = 'https://www.baidu.com/s?wd={}'.format(key)
        return '1. [{}]({})'.format(name, search_url)

    md = '# 品牌榜单\n\n`最后更新时间：{updateTime}`\n\n'
    md = md.replace("{updateTime}", util.current_time())

    for category in brand_map:
        items = brand_map[category]
        group = '## {category}\n\n{brands}\n\n'
        brands = '暂无数据'
        if items:
            brands = '\n'.join([brand(item) for item in items])
        group = group.replace('{category}', category)
        group = group.replace('{brands}', brands)
        md += group

    return md


def handle_hot_brands(dy: Douyin):
    """热门品牌
    """
    categories, resp = dy.get_brand_category()
    saveRawResponse(resp, 'brand-category')
    time.sleep(1)
    brand_map = {}
    for category in categories:
        id = category['id']
        category = category['name']
        brands, resp = dy.get_hot_brand(int(id))
        time.sleep(1)
        saveBrandRawResponse(resp, category)
        brand_map[category] = brands
    md = generate_brand_md(brand_map)
    filename = '{}-brand.md'.format(util.current_date())
    file = os.path.join('archives', filename)
    util.write_text(file, md)


def run():
    # 获取数据
    dy = Douyin()
    # 热搜
    searches, resp = dy.get_hot_search()
    saveRawResponse(resp, 'hot-search')
    time.sleep(1)
    # 明星
    stars, resp = dy.get_hot_star()
    saveRawResponse(resp, 'hot-star')
    time.sleep(1)
    # 直播
    lives, resp = dy.get_hot_live()
    saveRawResponse(resp, 'hot-live')
    time.sleep(1)
    # 音乐
    musics, resp = dy.get_hot_music()
    saveRawResponse(resp, 'hot-music')
    time.sleep(1)
    # 品牌单独归档
    handle_hot_brands(dy)

    # 最新数据
    todayMd = generate_readme(searches, stars, lives, musics)
    save_readme(todayMd)
    # 归档
    archiveMd = generate_archive_md(searches, stars, lives, musics)
    save_archive_md(archiveMd)


if __name__ == "__main__":
    run()
