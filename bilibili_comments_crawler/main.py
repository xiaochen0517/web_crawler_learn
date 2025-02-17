import requests
from fake_useragent import UserAgent
import re
import csv
import json
import time
import execjs
from urllib.parse import quote

cookie = "buvid3=D1C8F3F4-ED22-8D0C-90D5-6512ED983DC321434infoc; b_nut=1739763621; _uuid=CD1CE346-41CE-103EB-7D103-15D7B3103415222112infoc; buvid4=6B943605-04E3-5A23-E8ED-13AC5095AE8522169-025021703-pBn7cxoPJbzyelLrTzKACg%3D%3D; enable_web_push=DISABLE; enable_feed_channel=DISABLE; buvid_fp=b3d2bcf15966e04d3a182ecab6b5c04a; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDAwMjI4MjMsImlhdCI6MTczOTc2MzU2MywicGx0IjotMX0.oI26AgrzX3ELa6uLg0yjTjzo8HHhezISQVg5MnG2ZvU; bili_ticket_expires=1740022763; home_feed_column=4; browser_resolution=1324-1916; CURRENT_FNVAL=4048; rpdid=|(umku))l)u)0J'u~Jm~YJYlY; SESSDATA=63db2eac%2C1755315725%2Cecc19%2A21CjATSTw0T9KnUdc0vej1_aKpq6FeS-n0nxBYHKTUvAIFa2nIfjnVPt_8u0IIZqlCugUSVl9nMWpaWXAxNlY3ZEo2UEFPX1lsdWxmc2NrczBQa0ZBQVBRcVMzTFlJSklmcnF6ZU1KaXhFcGlIczdvb3pJQWk3WGFGb2VFcHBDWks1Z3lCOVlka2RBIIEC; bili_jct=ef95d20db689c0e85aedfe4dcd944bf4; DedeUserID=286915431; DedeUserID__ckMd5=5e3bbb8008303cf6; sid=8nwzom1x; b_lsid=8AF217C6_19512713163; bp_t_offset_286915431=1034805866697588736"

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


# 获取oid
def get_oid(author_url):
    rsp = requests.get(author_url, headers=headers)
    # print(rsp.text)
    oid = re.findall(r'"aid":(\d+),', rsp.text)[0]
    return oid


def get_nav():
    nav_url = 'https://api.bilibili.com/x/web-interface/nav'
    rsp = requests.get(nav_url, headers=headers)
    wbi_img = rsp.json()['data']['wbi_img']
    print('获取 nav 图片路径：\n', json.dumps(wbi_img, indent=2, ensure_ascii=False))
    return wbi_img


def get_w_rid(mode=3, oid='', pagination_str='{"offset":""}', plat=1, seek_rpid='', type=1,
              web_location=1315875):
    nodejs_ctx = node.compile(open('crypto.js').read())
    nav_wbi_img = get_nav()
    run_js = (
                'get_w_rid({mode: %s, oid: "%s", pagination_str: `%s`, plat: %s, seek_rpid: "", type: %s, web_location: %s}, "%s-%s")' %
                (mode, oid, pagination_str, plat, type, web_location, nav_wbi_img['img_url'], nav_wbi_img['sub_url']))
    print(f'加密获取 w_rid 参数: {run_js}')
    crypto_result = nodejs_ctx.eval(run_js)
    print(f'加密获取 w_rid 结果: {crypto_result}')
    return crypto_result


def main(video_id='BV1WiAKeWEPc'):
    # 获取oid
    oid = get_oid(author_url.format(video_id=video_id))
    print('oid:', oid)
    if not oid:
        print('获取oid失败')
        return

    # 获取评论接口参数构建
    pagination_str = '{"offset":""}'
    # 将 pagination_str 中的花括号和双引号转义
    pagination_str = quote(pagination_str)
    print(f'转义后的 pagination_str: {pagination_str}')
    mode = 3
    type = 1
    pagination_str = '{"offset":""}'
    plat = 1
    web_location = 1315875
    w_rid_obj = get_w_rid(mode=mode, oid=oid, pagination_str=pagination_str, plat=plat, type=type,
                          web_location=web_location)
    w_rid = w_rid_obj['w_rid']
    wts = w_rid_obj['wts']

    params = {
        'oid': oid,
        'type': type,
        'mode': mode,
        'pagination_str': pagination_str,
        'seek_rpid': '',
        'plat': plat,
        'web_location': web_location,
        'w_rid': w_rid,
        'wts': wts,
    }
    print('请求参数:', params)
    comments_url = f'https://api.bilibili.com/x/v2/reply/wbi/main'

    # 将 comments_url 拼接 params
    # request_url = comments_url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
    # print('请求url:', request_url)
    # return

    rsp = requests.get(comments_url, headers=headers, params=params)
    # 打印http请求头
    print(rsp.request.headers)
    # 打印请求完整的请求url
    print(rsp.request.url)
    data = rsp.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    # f = open('data.csv', mode='w', encoding='utf-8-sig', newline='')  # 创建文件对象，保存数据
    # csv_writer = csv.DictWriter(f, fieldnames=[
    #     '昵称',
    #     '性别',
    #     'IP',
    #     '评论',
    #     '点赞',
    # ])
    # csv_writer.writeheader()


if __name__ == '__main__':
    main()
    # get_nav()
