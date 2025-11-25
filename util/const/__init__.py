JSON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/142.0.0.0 Safari/537.36',
    'Referer': 'https://www.zhihu.com/question/800718032',
    'Host': 'www.zhihu.com',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': '_zap=dc65c8de-2eaa-4c6f-890b-4e50e52deb8a; d_c0=ATASYAzg_BmPTicbhYE-3tVoWEZZYhVtxBY=|1739246896; '
              '__snaker__id=JehzPV5AsowyJ0yd; q_c1=87fbbfd5c1b34e85ad9c108f72fad01e|1739246957000|1739246957000; '
              '_xsrf=0tVJ4nSVaEt7uBKgnynGxotBeGLH4Wl8; HMACCOUNT=E3AE090E6106D59B; '
              'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1761909849; '
              'z_c0=2|1:0|10:1763436246|4:z_c0|92:Mi4xa1hZMkFRQUFBQUFCTUJKZ0RPRDhHU1lBQUFCZ0FsVk4xalFKYWdEMmM0NGRMV3VaZ1ZEeHFvbW5mUWJqN3ZZdVJ3|1561305d29b4e4b52c9b08904743b4cb769eb65f31ae5c78eb3020e51bc2a2ac; '
              '__zse_ck=004_RNhw77FlrKFnaO4ae9UlW9iJkAnJ0kMLc9R8qTb=XTrs3ri1lqNJOi1dJB96Fy9YHfUWo4RtUmHifNm77eH48mrf753jfLI2ELQH5J4tnwZfgEzyQ32f3U279TraG2zI-zkDUc6ew7mOoOZYp28GA8kq2O1Hj8nXHyBMwe+5C2qGd60JO6TWCxQ/N1WDblIlJ0tImNgp7zU3Z1t2ylmhIc0hbFYWkf+S6BdawRPp5xX+44noa3sUhvDUVQsz9mQVE; '
              'SESSIONID=V75WHFeQ8XKO9jMc9Hi9kit26y1MD4upA7kspcXyVov; '
              'JOID=UlsUB0pkr0r9uSS2K2KdGW61wEgzMZp6r_Bh0X9d9AO3hU_4Siveb5C7JbErKUcWf1UcBKExsfSUUlCJF-u5rjA=; '
              'osd=VlwcBkpgqEL8uSCxI2OdHWm9wUg3NpJ7r_Rm2X5d8AS_hE_8TSPfb5S8LbArLUAeflUYA6kwsfCTWlGJE-yxrzA=; '
              'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1764062821; BEC=5725bc0a8a749d6bef30389b0155cdd0',
    'x-requested-with': 'fetch',
    'x-zse-93': '101_3_3.0',
    'x-zse-96': '2.0_51B/KU0fyhasazPlV/maU3MPA1g9Ty9zusYOgi7q03M9Gf2X=/IeO4A5Xtjl2Nsu',
    'x-udid': 'ATASYAzg_BmPTicbhYE-3tVoWEZZYhVtxBY=',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin'
}

USER_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
                'authority': 'www.zhihu.com',
                "Referer": ""}


def get_user_headers(user_id):
    ref = r'https://www.zhihu.com/people/{}/posts'
    USER_HEADERS['Referer'] = ref.format(user_id)
    return USER_HEADERS


HTML_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
                'authority': 'zhuanlan.zhihu.com'}

COLLECTION_HEADERS = {
    'User-Agent': JSON_HEADERS['User-Agent'],
    'Referer': JSON_HEADERS['Referer'],
    'Host': 'api.zhihu.com',
    'accept': JSON_HEADERS['accept'],
    'accept-encoding': JSON_HEADERS['accept-encoding'],
    'accept-language': JSON_HEADERS['accept-language'],
    'cookie': JSON_HEADERS['cookie'],
    'x-requested-with': JSON_HEADERS['x-requested-with'],
    'x-zse-93': JSON_HEADERS['x-zse-93'],
    'x-zse-96': JSON_HEADERS['x-zse-96'],
    'x-udid': JSON_HEADERS['x-udid'],
    'sec-ch-ua': JSON_HEADERS['sec-ch-ua'],
    'sec-ch-ua-mobile': JSON_HEADERS['sec-ch-ua-mobile'],
    'sec-ch-ua-platform': JSON_HEADERS['sec-ch-ua-platform'],
    'sec-fetch-dest': JSON_HEADERS['sec-fetch-dest'],
    'sec-fetch-mode': JSON_HEADERS['sec-fetch-mode'],
    'sec-fetch-site': 'same-site'
}

SORT_BY_DEF = 'default'
SORT_BY_VOT = 'voteups'
SORT_BY_DAT = 'created'
PLATFORM = 'desktop'

# 作者头像
AVATAR_SIZE_R = '{size}'
AVATAR_SIZE_A = 'l'  # is L
# size: r, m, b, l, xs, is, s

# 作者主页 format(url_token)
AUTHOR_PAGE_URL = 'https://www.zhihu.com/people/{}'

# 答案原文链接 format: question_id, answer_id
# 没有考虑到 question_id，先前爬取的答案原文链接都不对    2019-05-02 更正
ANSWER_URL = r'https://www.zhihu.com/question/{}/answer/{}'

# 文章原文链接
ARTICLE_URL = 'https://zhuanlan.zhihu.com/p/{}'

# 设置休眠时长（秒）
TIME_SLEEP = 6

LIMITLESS = -1

LIMIT_SIZE = 20  # 每次获取答案的数量
