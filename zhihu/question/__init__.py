import os
import re
import logging
from json.decoder import JSONDecodeError

from bs4 import BeautifulSoup

import zhihu
from util import const
from util import document
from util import net
from util.timer import timer

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s %(message)s')

__all__ = ['answer', 'answers', 'make_answers_as_book']

template = '''
{} {}    {} / {}  👍 {}
    {}
    评分：{:<.2f}
    收录：{}
'''


def answer(answer_id, warehouse):
    response = net.answer_spider(answer_id)
    if response is not None:
        answer_content = response.json()
        content = BeautifulSoup(answer_content['content'], 'lxml').body
        # # TODO DEBUG TAG CLEAR AFTER FINISH!
        # with open(answer_id + '.html', 'w', encoding='utf8') as foo:
        #     foo.write(content.prettify())
        msg = answer_msg(answer_content)
        an = document.Answer(content, msg)
        an.make_markdown(warehouse)
        return an.answer_msg()
    else:
        raise ValueError('Response is None')


def answers(question_id, warehouse):
    offset = zhihu.Controller(collect_all=True)
    warehouse = question_warehouse(question_id, warehouse)
    logger.info("开始抓取问题 %s 的回答，输出目录：%s", question_id, warehouse)
    while not offset.is_end():
        response = fetch_answers_page(question_id, offset.next_offset())
        try:
            response_json = response.json()
            offset.totals = response_json['paging']['totals']
            database: list = response_json['data']
            offset.increase(len(database))
            logger.info("批次 offset=%d，获取 %d 条，目标总数=%s", offset.next_offset(), len(database), offset.totals)
            for answer_content in database:
                msg = answer_msg(answer_content)
                if not offset.to_collect(answer_content):
                    continue
                content = parse_answer_body(answer_content)
                if content is None:
                    logger.warning("回答内容为空或无法解析，question=%s, answer=%s，已跳过",
                                   question_id, answer_content.get('id'))
                    continue
                an = document.Answer(content, msg)
                an.set_file_name(template='%a-%v')
                an.make_markdown(warehouse)
                print(an.answer_msg())
            timer.sleep_for(zhihu.SLEEP)
        except JSONDecodeError as e:
            debug_response(response)
            raise e


def answer_msg(answer_content):
    author = answer_content['author']['name']
    voteup = answer_content['voteup_count']
    title = answer_content['question']['title']
    question_id = answer_content['question']['id']
    answer_id = answer_content['id']
    original_url = const.ANSWER_URL.format(question_id, answer_id)
    author_page = const.AUTHOR_PAGE_URL.format(answer_content['author']['url_token'])
    avatar = answer_content['author']['avatar_url_template'].replace(const.AVATAR_SIZE_R,
                                                                     const.AVATAR_SIZE_A)
    date = timer.timestamp_to_date(answer_content['created_time'])
    answer_dict = {'author': author, 'author_avatar_url': avatar, 'author_page': author_page, 'title': title,
                   'original_url': original_url, 'created_date': date, 'voteup': voteup}
    return document.Meta(**answer_dict)


def question_warehouse(question_id, warehouse):
    response = net.question_msg_spider(question_id)
    if response is not None:
        response_json = response.json()
        name = response_json['title']
        name = re.sub(r'[\\/]', '、', name)
        name = re.sub(r'[？?*:<>|]', '', name)
        warehouse = os.path.join(warehouse, name)
        if not os.path.exists(warehouse):
            os.makedirs(warehouse)
            logger.info("创建输出目录：%s", warehouse)
        return warehouse
    else:
        raise ValueError('Response is None')


def make_answers_as_book(question_id, warehouse):
    offset = zhihu.Controller(collect_all=True)
    response = net.question_msg_spider(question_id)
    if response is not None:
        response_json = response.json()
        name = response_json['title']
        name = re.sub(r'[\\/]', '、', name)
        title = re.sub(r'[？?*:<>|]', '', name)
    else:
        raise ValueError('Response is None')
    book_path = os.path.join(warehouse, title + '.md')
    logger.info("开始抓取问题 %s，生成合集：%s", question_id, book_path)
    book = open(book_path, 'a', encoding='utf8')
    while not offset.is_end():
        response = fetch_answers_page(question_id, offset.next_offset())
        try:
            response_json = response.json()
            offset.totals = response_json['paging']['totals']
            database: list = response_json['data']
            offset.increase(len(database))
            logger.info("批次 offset=%d，获取 %d 条，目标总数=%s", offset.next_offset(), len(database), offset.totals)
            for answer_content in database:
                msg = answer_msg(answer_content)
                if not offset.to_collect(answer_content):
                    continue
                content = parse_answer_body(answer_content)
                if content is None:
                    logger.warning("回答内容为空或无法解析，question=%s, answer=%s，已跳过", question_id,
                                   answer_content.get('id'))
                    continue
                an = document.Answer(content, msg)
                an.set_file_name(template='%a-%v')
                book.write(an.to_markdown())
                book.write('\n---\n')
                print(an.answer_msg())
            timer.sleep_for(zhihu.SLEEP)
        except JSONDecodeError as e:
            debug_response(response)
            book.close()
            logger.error("解析失败，已保留当前文件：%s，错误：%s", book_path, e)
            raise e
    book.close()
    logger.info("问题 %s 抓取完成，文件已写入：%s", question_id, book_path)


def debug_response(response):
    """打印接口调试信息，辅助定位 403/非 JSON 响应"""
    if response is None:
        print('response is None')
        return
    print('debug status/url:', getattr(response, 'status_code', '?'), getattr(response, 'url', '?'))
    try:
        print('debug headers snippet:', {k: response.headers.get(k) for k in ['content-type', 'content-encoding', 'x-req-id', 'x-api-version']})
    except Exception:
        pass
    try:
        text = response.text
        print('debug body snippet:', text[:400])
    except Exception as err:
        print('debug body read error:', err)


def ensure_response_ok(response, question_id, offset):
    """确保响应有效，便于定位 403/401/空响应"""
    if response is None:
        msg = f"question={question_id}, offset={offset}: response is None，可能被限流或鉴权失效"
        logger.error(msg)
        raise RuntimeError(msg)
    status = getattr(response, 'status_code', 200)
    if status != 200:
        debug_response(response)
        msg = f"question={question_id}, offset={offset}: status {status}，请更新请求头或放慢频率"
        logger.error(msg)
        raise RuntimeError(msg)


def fetch_answers_page(question_id, offset):
    """携带重试的回答列表请求，降低 403/429 造成的中断"""
    last_resp = None
    for attempt in range(1, 4):
        resp = net.answers_spider(question_id, offset, const.SORT_BY_VOT)
        last_resp = resp
        if resp is None:
            wait = zhihu.SLEEP * attempt
            logger.warning("尝试 %d/3: question=%s offset=%d 响应 None，等待 %ss 重试", attempt, question_id, offset, wait)
            timer.sleep_for(wait)
            continue
        status = getattr(resp, 'status_code', 200)
        if status != 200:
            wait = zhihu.SLEEP * attempt
            logger.warning("尝试 %d/3: question=%s offset=%d 状态 %s，等待 %ss 重试", attempt, question_id, offset, status, wait)
            debug_response(resp)
            timer.sleep_for(wait)
            continue
        return resp
    # 重试后仍失败，抛出详细错误
    ensure_response_ok(last_resp, question_id, offset)
    return last_resp


def parse_answer_body(answer_content):
    """解析回答主体的 HTML，若无 body 则返回 None"""
    content_html = answer_content.get('content') if isinstance(answer_content, dict) else None
    if not content_html:
        return None
    soup = BeautifulSoup(content_html, 'lxml')
    return soup.body


"""
说明：
    这里实现了对单个回答或问题的所有回答的爬取，其中单个回答的爬取需要的是answer_id，而问题的所有回答需要的是
question_id。通过相应的id发起网络请求，返回的json文件中包含的内容的主体，通过解析json文件获得文章的基本信息，生
成一个msg对象，再将内容主体解析成BeautifulSoup对象，连同msg一起交给document下的有关类解析生成markdown文件
"""
