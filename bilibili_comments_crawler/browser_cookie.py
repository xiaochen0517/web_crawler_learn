import json

from playwright.sync_api import sync_playwright

# B站首页
BILIBILI_URL = 'https://www.bilibili.com'
# 存储 localStorage 的路径，json文件自行创建，文件内容默认为空对象 {}
STORAGE_JSON_PATH = 'browser_data/bilibili_storage.json'
# 5分钟等待登录超时
WAIT_TIME_SEC = 60 * 5


def get_playwright_page():
    playwright = sync_playwright()
    if not playwright:
        raise ValueError('playwright sync_playwright() 初始化失败')
    playwright_start = playwright.start()
    if not playwright_start:
        raise ValueError('playwright start() 启动失败')
    chromium = playwright_start.chromium.launch(headless=False)
    if not chromium:
        raise ValueError('playwright chromium 启动失败')
    return chromium


def track_local_storage_changes(page, key_to_watch):
    changes = []

    # 暴露 Python 函数以接收变化
    def record_change(key, value):
        changes.append({"key": key, "value": value})

    page.expose_function("pyRecordStorageChange", record_change)

    # 注入监听脚本
    page.evaluate(
        """(keyToWatch) => {
            // 监听跨页面的 storage 事件
            window.addEventListener('storage', (e) => {
                if (e.key === keyToWatch) {
                    window.pyRecordStorageChange(e.key, e.newValue);
                }
            });

            // 劫持当前页面的 localStorage.setItem 以捕获同页面修改
            const originalSetItem = localStorage.setItem;
            localStorage.setItem = function(key, value) {
                if (key === keyToWatch) {
                    window.pyRecordStorageChange(key, value);
                }
                originalSetItem.apply(this, arguments);
            };
        }""",
        key_to_watch
    )

    return changes


def check_login_status(chromium_page):
    # 获取localStorage
    local_storage_json = chromium_page.evaluate("() => JSON.stringify(window.localStorage)")
    local_storage = json.loads(local_storage_json)
    if 'bili-login-state' in local_storage:
        return int(local_storage['bili-login-state']) % 2 == 0


def get_cookie(chromium_page):
    # 获取 Cookie
    cookies = chromium_page.context.cookies()
    # key和value之间使用等于号，key-value对之间使用分号加空格
    result_str = ''
    for index, cookie_item in enumerate(cookies):
        result_str += f'{cookie_item["name"]}={cookie_item["value"]}{"; " if index < len(cookies) - 1 else ""}'
    return result_str


def save_state_close_browser(chromium, context):
    context.storage_state(path=STORAGE_JSON_PATH)
    chromium.close()


def get_bilibili_cookie():
    chromium = get_playwright_page()
    context = chromium.new_context(
        storage_state=STORAGE_JSON_PATH,
    )
    chromium_page = context.new_page()
    chromium_page.goto(BILIBILI_URL, wait_until='networkidle')

    # 获取 Cookie
    # cookies = context.cookies()
    # for cookie_item in cookies:
    #     print(f'key: {cookie_item["name"]}; value: {cookie_item["value"]}')
    # print('cookie: ', context.cookies())

    # 检查是否已经是登录状态
    if check_login_status(chromium_page):
        # 已登录
        cookie = get_cookie(chromium_page)
        save_state_close_browser(chromium, context)
        return cookie

    # 监听 localStorage 变化
    change = track_local_storage_changes(chromium_page, 'bili-login-state')
    # 等待直到登录状态变化
    for sec in range(WAIT_TIME_SEC):
        chromium_page.wait_for_timeout(1000)
        if len(change) > 0 and int(change[-1]['value']) % 2 == 0:
            # 当前是登录状态
            cookie = get_cookie(chromium_page)
            save_state_close_browser(chromium, context)
            return cookie
        if sec >= WAIT_TIME_SEC - 1:
            raise ValueError('登录状态未变化')
