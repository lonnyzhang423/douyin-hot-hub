import os
import time
import urllib

from requests import Response

import util
from douyin import Douyin
from util import logger


def generate_archive_md(searches, stars, lives, musics, brands):
    """生成今日readme
    """
    def search(item):
        word = item['word']
        url = 'https://www.douyin.com/search/' + urllib.parse.quote(word)
        return '1. [{}]({})'.format(word, url)

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

    brandsMd = '暂无数据'
    if brands:
        brandsMd = generate_brand_table_md(brands)

    readme = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        readme = f.read()

    now = util.current_time()
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{searches}", searchMd)
    readme = readme.replace("{stars}", starMd)
    readme = readme.replace("{lives}", liveMd)
    readme = readme.replace("{musics}", musicMd)
    readme = readme.replace("{brands}", brandsMd)

    return readme


def generate_readme(searches, stars, lives, musics, brands):
    """生成今日readme
    """
    def search(item):
        word = item['word']
        url = 'https://www.douyin.com/search/' + urllib.parse.quote(word)
        return '1. [{}]({})'.format(word, url)

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

    brandsMd = '暂无数据'
    if brands:
        brandsMd = generate_brand_table_md(brands)

    readme = ''
    file = os.path.join('template', 'README.md')
    with open(file) as f:
        readme = f.read()

    now = util.current_time()
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{searches}", searchMd)
    readme = readme.replace("{stars}", starMd)
    readme = readme.replace("{lives}", liveMd)
    readme = readme.replace("{musics}", musicMd)
    readme = readme.replace("{brands}", brandsMd)

    return readme


def save_readme(md):
    logger.info('today md:%s', md)
    util.write_text('README.md', md)


def save_archive_md(md):
    logger.info('archive md:%s', md)
    name = util.current_date()+'.md'
    file = os.path.join('archives', name)
    util.write_text(file, md)


def save_raw_response(resp: Response, filename: str):
    """保存原始响应内容
    """
    if resp:
        content = resp.text
        filename = '{}.json'.format(filename)
        logger.info('save response:%s', filename)
        date = util.current_date()
        file = os.path.join('raw', date, filename)
        util.write_text(file, content)


def save_brand_raw_response(resp: Response, category: str):
    """保存品牌榜响应内容
    """
    if resp:
        content = resp.text
        date = util.current_date()
        filename = '{}.json'.format(category)
        logger.info('save response:%s', filename)
        file = os.path.join('raw', date, 'brand', filename)
        util.write_text(file, content)


def generate_brand_table_md(brand_map: map):
    """品牌榜md
    """
    fake_brand = {'name': '-'}

    def column(item):
        if item is fake_brand:
            return fake_brand['name']

        name = item['name']
        key = urllib.parse.quote(name)
        search_url = 'https://www.baidu.com/s?wd={}'.format(key)
        return '[{}]({})'.format(name, search_url)

    def ensure_same_len(brand_map: map):
        max_len = 0
        for category in brand_map:
            max_len = max(max_len, len(brand_map[category]))
        for category in brand_map:
            brands: list = brand_map[category]
            if len(brands) < max_len:
                brands.extend([fake_brand for _ in range(max_len-len(brands))])
        return max_len

    # 确保品牌列表长度相同
    max_len = ensure_same_len(brand_map)

    # 表头
    table_header = '|'
    for category in brand_map:
        table_header += ' {} |'.format(category)
    table_header += '\n'
    table_header += '|'
    for _ in range(len(brand_map)):
        table_header += ' --- |'
    # 表行
    table_rows = ''
    for i in range(max_len):
        row = '|'
        for category in brand_map:
            brands: list = brand_map[category]
            row += ' {} |'.format(column(brands[i]))
        table_rows += row + '\n'

    return table_header + '\n' + table_rows


def get_all_brands(dy: Douyin):
    """热门品牌
    """
    categories, resp = dy.get_brand_category()
    save_raw_response(resp, 'brand-category')
    time.sleep(1)

    brand_map = {}
    for category in categories:
        # 分类名称
        cname = category['name']
        cid = int(category['id'])
        brands, resp = dy.get_hot_brand(cid)
        save_brand_raw_response(resp, cname)
        brand_map[cname] = brands
        time.sleep(1)

    return brand_map


def run():
    # 获取数据
    dy = Douyin()
    # 热搜
    searches, resp = dy.get_hot_search()
    save_raw_response(resp, 'hot-search')
    time.sleep(1)
    # 明星
    stars, resp = dy.get_hot_star()
    save_raw_response(resp, 'hot-star')
    time.sleep(1)
    # 直播
    lives, resp = dy.get_hot_live()
    save_raw_response(resp, 'hot-live')
    time.sleep(1)
    # 音乐
    musics, resp = dy.get_hot_music()
    save_raw_response(resp, 'hot-music')
    time.sleep(1)
    # 品牌
    brands = get_all_brands(dy)
    time.sleep(1)

    # 最新数据
    todayMd = generate_readme(searches, stars, lives, musics, brands)
    save_readme(todayMd)
    # 归档
    archiveMd = generate_archive_md(searches, stars, lives, musics, brands)
    save_archive_md(archiveMd)


if __name__ == "__main__":
    try:
        run()
    except:
        logger.exception('run failed')
