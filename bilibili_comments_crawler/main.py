import os
import requests
from fake_useragent import UserAgent
import re
import json
import time
import execjs
import browser_cookie

SAVE_DATA_PATH = 'data'

cookie = ""

headers = {
    # 获取桌面版UA
    'User-Agent': UserAgent().random,
    'Accept': '*/*',
    'Cookie': cookie,
    'Origin': 'https://www.bilibili.com',
    'Referer': 'https://www.bilibili.com',
    # 'Referer': 'https://www.bilibili.com/video/BV1WiAKeWEPc/?vd_source=9835ba5eb63174bbd7f82307d86ddbc2',
}

node = execjs.get()

author_url = 'https://www.bilibili.com/video/{video_id}/'
comments_url = f'https://api.bilibili.com/x/v2/reply/wbi/main'
nav_url = 'https://api.bilibili.com/x/web-interface/nav'


# 获取oid
def get_oid(author_url):
    rsp = requests.get(author_url, headers=headers)
    # print(rsp.text)
    oid = re.findall(r'"aid":(\d+),', rsp.text)[0]
    return oid


def get_nav_wbi_img():
    rsp = requests.get(nav_url, headers=headers)
    wbi_img = rsp.json()['data']['wbi_img']
    print('获取 nav 图片路径：\n', json.dumps(wbi_img, indent=2, ensure_ascii=False))
    if not wbi_img:
        print('获取 nav 图片路径失败')
        raise ValueError('获取 nav 图片路径失败')
    return wbi_img


def get_w_rid(params):
    nodejs_ctx = node.compile(open('crypto.js').read())
    nav_wbi_img = get_nav_wbi_img()
    js_str = 'get_w_rid({mode: %s, oid: "%s", pagination_str: `%s`, plat: %s, seek_rpid: "", type: %s, web_location: %s}, "%s-%s")'
    if 'seek_rpid' not in params:
        js_str = 'get_w_rid({mode: %s, oid: "%s", pagination_str: `%s`, plat: %s, type: %s, web_location: %s}, "%s-%s")'
    # 如何参数 pagination_str 有单个反斜杠，需要在js字符串中使用两个反斜杠
    pagination_str = params['pagination_str'].replace('\\', '\\\\')
    run_js = (
            js_str %
            (params['mode'], params['oid'], pagination_str, params['plat'], params['type'],
             params['web_location'], nav_wbi_img['img_url'], nav_wbi_img['sub_url']))
    print(f'加密获取 w_rid 参数: {run_js}')
    crypto_result = nodejs_ctx.eval(run_js)
    print(f'加密获取 w_rid 结果: {crypto_result}')
    if not crypto_result:
        print('加密获取 w_rid 失败')
        raise ValueError('加密获取 w_rid 失败')
    return crypto_result


def get_comment_list(url, params):
    rsp = requests.get(url=url, headers=headers, params=params)
    print('请求地址：', rsp.request.url)
    if rsp.json()['code'] != 0:
        raise ValueError('获取评论列表失败', rsp.json())
    return rsp.json()


def get_next_page_offset(params):
    if not params:
        print('get_next_page_offset 参数为空')
        return
    pagination_reply = params['data']['cursor']['pagination_reply']
    # 检查 pagination_reply 是否存在 next_offset 字段
    if 'next_offset' in pagination_reply:
        return pagination_reply['next_offset']
    else:
        return None


def save_data(name, data, path):
    if not data:
        print('save_data 数据为空')
        return
    if not os.path.exists(path):
        os.makedirs(path)
    # 如果文件已存在，直接覆盖原文件
    with open(f'{path}/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_comments_by_bv(video_id='BV1WiAKeWEPc'):
    # 创建保存的目录
    if not os.path.exists(SAVE_DATA_PATH):
        os.makedirs(SAVE_DATA_PATH)
    video_data_path = f'{SAVE_DATA_PATH}/{video_id}'
    if not os.path.exists(video_data_path):
        os.makedirs(video_data_path)

    # 获取oid
    oid = get_oid(author_url.format(video_id=video_id))
    print('oid:', oid)
    if not oid:
        print('获取oid失败')
        return

    next_offset = ''
    params = {
        'oid': oid,
        'type': 1,
        'mode': 3,
        'pagination_str': '{"offset":""}',
        'seek_rpid': '',
        'plat': 1,
        'web_location': 1315875,
        'w_rid': '',
        'wts': '',
    }

    # 获取评论列表
    page_count = 0
    while next_offset is not None:
        page_count += 1
        print(f'========= 第{page_count}页 =========')
        params['pagination_str'] = '{"offset":%s}' % (json.dumps(next_offset))
        if page_count > 1 and 'seek_rpid' in params:
            # 移除seek_rpid参数
            params.pop('seek_rpid')
        # 获取 w_rid 和 wts 参数
        w_rid_obj = get_w_rid(params)
        params['w_rid'] = w_rid_obj['w_rid']
        params['wts'] = w_rid_obj['wts']
        comment_data = get_comment_list(comments_url, params)
        next_offset = get_next_page_offset(comment_data)
        # 保存数据
        print('保存数据：', f'comments_data_{page_count}')
        save_data(f'comments_data_{page_count}', comment_data, video_data_path)
        print('下一个分页的参数:', next_offset)
        # 随机延时 0.5s-1.0s
        time.sleep(0.5 + 0.5 * time.time() % 1)

    print('获取评论列表完成')


if __name__ == '__main__':
    cookie = browser_cookie.get_bilibili_cookie()
    print('获取到的 Cookie 信息：', cookie)
    get_comments_by_bv('BV1WiAKeWEPc')
