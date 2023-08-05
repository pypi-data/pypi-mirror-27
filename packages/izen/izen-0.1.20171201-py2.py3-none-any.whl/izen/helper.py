# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = 'lihe <imanux@sina.com>'
__date__ = '06/09/2017 5:15 PM'
__description__ = '''
'''

import binascii
import datetime
import json
import os
import requests
import socket
import struct
import subprocess
import sys
import time
import platform
import base64
import getpass
import pickle
import random

app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_root)
if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

import psutil
import click
from logzero import logger as log

""" 交互选择功能 """


def num_choice(choices, depth=1):
    """
        传入数组, 返回正确的 index

    :param depth:
    :param choices:
    :type choices:
    :return:
    :rtype:
    """
    if not choices:
        return None

    with textui.indent(4, quote=' {}'.format(icons.icons[depth - 1])):
        # if len(choices) < 20:
        for i, choice in enumerate(choices, start=1):
            textui.puts(textui.colored.green('{}. {}'.format(i, choice)))
        # else:
        #     click.echo_via_pager('\n'.join('{}'.format(x) for x in choices))

    _valid = [str(x + 1) for x in range(0, len(choices))]
    c = click.prompt(click.style('[Depth: ({})]Your Choice(q-quit/b-back)?', fg='cyan').format(depth))

    if str(c) in 'qQ':
        os._exit(-1)
    elif str(c) in 'bB':
        return c
    elif c not in _valid:
        log.error('Invalid input :( [{}]'.format(c))
        return num_choice(choices)
    else:
        return int(c) - 1


def yn_choice(msg):
    """
    传入 msg , 返回 True/False
    :param msg:
    :type msg:
    :return:
    :rtype:
    """
    click.secho('{}? [yn]'.format(msg), nl=False, fg='green')
    c = click.getchar()
    click.echo()
    if c in 'yYnN':
        return 'yYnN'.index(c) < 2
    else:
        click.secho('only yYnN allowed :( [{}]'.format(c), fg='red')
        return yn_choice(msg)


def copy_to_clipboard(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(to_bytes(data))
    p.stdin.close()
    p.communicate()


""" 时间处理 """


def now(fmt='%Y-%m-%d %H:%M:%S'):
    """
        获取当前时间的字符串表示

    :param fmt: ``默认(%Y-%m-%d %H:%M:%S)``
    :type fmt: str
    :return:
    :rtype: str
    """
    return datetime.datetime.now().strftime(fmt)


def str2unixtime(ts, fmt='%Y-%m-%d %H:%M:%S'):
    """
        将固定格式的字符串转换成对应的时间戳到秒级别

    - 使用:

    >>> str2unixtime('2016-01-01 01:01:01')
    1451581261

    :param ts:
    :type ts:
    :param fmt:
    :type fmt:
    :return:
    :rtype:
    """
    t = time.strptime(ts, fmt)
    return int(time.mktime(t))


def unixtime2str(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    """
    将 ``秒级别的时间戳`` 转换成字符串

    .. warning:
        时间戳是以 ``秒`` 为单位的

    :param timestamp: unix timestamp
    :type timestamp: int
    :param fmt: show format
    :type fmt: str
    :return:
    :rtype: str
    """
    dt = None
    try:
        timestamp = time.localtime(timestamp)
        dt = time.strftime(fmt, timestamp)
    except Exception as err:
        print(err)
    return dt


"""文件处理"""


def mkdir_p(pathin, is_dir=False):
    """
        分隔pathin, 并以此创建层级目录

    - ``is_dir == True``: 则将所有 ``/ 分隔`` 的pathin 当前文件夹
    - 否则, 将分隔的最后一个元素当做是文件处理

    >>> # 创建一个目录 /tmp/a/b/c
    >>> mkdir_p('/tmp/a/b/c/001.log')

    :param is_dir: ``是否目录``
    :type is_dir: bool
    :param pathin: ``待创建的目录或者文件路径``
    :type pathin: str
    """
    h, _ = os.path.split(pathin)
    if is_dir:
        h = pathin
    try:
        if not os.path.exists(h):
            os.makedirs(h)
    except Exception as err:
        raise err


def walk_dir_with_filter(pth, prefix=None, suffix=None):
    """
        默认情况下,会遍历目录下所有文件,写入数组返回.

    - ``prefix`` 会过滤以 其开头的所有文件
    - ``suffix`` 结尾

    :param pth:
    :type pth:
    :param prefix:
    :type prefix:
    :param suffix:
    :type suffix:
    :return:
    :rtype:
    """
    if suffix is None or type(suffix) != list:
        suffix = []
    if prefix is None or type(prefix) != list:
        prefix = []

    r = []
    for root_, dirs, files in os.walk(pth):
        for file_ in files:
            full_pth = os.path.join(root_, file_)

            # 排除 \.开头文件, 及 .pyc .md 结尾文件
            c = False
            for x in prefix:
                if file_.startswith(x):
                    c = True
                    break
            if c:
                continue
            # if runs here , c is False
            for x in suffix:
                if file_.endswith(x):
                    c = True
                    break
            if c:
                continue

            r.append(full_pth)
    return r


def write_file(dat, pth, append=True, is_abs_path=True):
    """
        将 dat 内容写入 pth 中, 如果写入成功, 返回为空, 否则返回失败信息

    :param is_abs_path: ``是否是全局路径``
    :type append: ``bool``
    :param append: 写入模式
    :type append: ``bool``
    :param dat: 待写入内容
    :type dat: ``str``
    :param pth:
    :type pth: ``str``
    :return:
    :rtype:
    """
    err = None

    # 如果是全局路径, 则创建目录
    if is_abs_path:
        _d, _nm = os.path.split(pth)
        if not os.path.exists(_d):
            os.makedirs(_d)

    try:
        mode = 'ab' if append else 'wb'

        with open(pth, mode) as _fp:
            dat = to_bytes(dat)
            _fp.write(dat)
    except Exception as _err:
        err = _err
    return err


def read_file(pth):
    """
        读取文件, 并返回内容,
        如果读取失败,返回None

    :param pth:
    :type pth:
    :return:
    :rtype:
    """
    cont = None
    try:
        with open(u'' + pth, 'rb') as fp:
            cont = fp.read()
    except Exception as err:
        print(err)
    return cont


def is_file_ok(fpth):
    """
        判断文件是否为空, 如果不存在, 或者大小为0, 则返回0, 否则返回文件大小.

    :param fpth:
    :type fpth:
    :return:
    :rtype:
    """
    try:
        return os.path.getsize(fpth)
    except FileNotFoundError as _:
        return 0


def b64_file(src_file):
    """
    打包当前程序目录中的所有程序文件 生成 tgz 文件, 读取 base64编码后, 使用aes加密数据,并附加rsa签名
    :return:
    :rtype:
    """
    z = None
    i = 0
    while not z and i < 3:
        z = read_file(src_file)
        time.sleep(0.1)
        i += 1

    if not z:
        log.warning('cannot open {} '.format(src_file))
        return z

    c = base64.b64encode(z)
    return c


def pickle_m2f(dat, pth):
    """
        将 dat 内容同步到文件存储中

    :param dat:
    :type dat:
    :param pth:
    :type pth:
    :return:
    :rtype:
    """
    mkdir_p(pth)
    # 为了2与3兼容, 设置 dump 的协议为 2
    with open(pth, 'wb') as f:
        pickle.dump(dat, f, 2)


def pickle_f2m(pth, rt=None):
    """
        获取文件内容并返回, 如果文件不存在, 则返回 rt

    :param pth:
    :type pth:
    :param rt: ``如果需要指定返回值, 请设置该值``
    :type rt:
    :return:
    :rtype:
    """
    r = rt
    try:
        with open(pth, 'rb') as f:
            r = pickle.load(f)
    except Exception as err:
        sys.stderr.write('pickle_f2m(pth={}) with error: {}\n'.format(pth, err))
    return r


""" 数据校验 """


def l_endian(v):
    """ 小端序 """
    w = struct.pack('<H', v)
    return str(binascii.hexlify(w), encoding='gbk')


def b_endian(v):
    """ 大端序 """
    w = struct.pack('>H', v)
    return str(binascii.hexlify(w), encoding='gbk')


def xorsum(t):
    """
    异或校验
    :param t:
    :type t:
    :return:
    :rtype:
    """
    _b = t[0]
    for i in t[1:]:
        _b = _b ^ i
        _b &= 0xff
    return _b


def xorsum_counter(t):
    """
    异或取反
    :param t:
    :type t:
    :return:
    :rtype:
    """
    return ~xorsum(t) & 0xff


def check_sum(buf, csum):
    """
    检查数据的校验和
    :param buf:
    :type buf:
    :param csum:
    :type csum:
    :return:
    :rtype:
    """
    csum = csum.encode('utf-8')
    _csum = ord(buf[0])
    for x in buf[1:]:
        _csum ^= ord(x)

    _csum = binascii.b2a_hex(chr(_csum).encode('utf-8')).upper()
    if _csum != csum:
        sys.stderr.write('csum not matched: ({} {})\n'.format(_csum, csum))
    return _csum == csum


"""系统命令"""


def debug(users=None):
    """
        是一种方便的测试模式, 用于 ``全局开启`` 或者关闭测试功能

    - 如果当前用户存在在users列表中, 则设定程序运行于debug模式

    """
    if not users:
        return False
    users = users if isinstance(users, list) else [users]
    return True if getpass.getuser() in users else False


def get_addr(iface='lo0'):
    """
        获取网络接口 ``iface`` 的 ``mac``

    - 如果系统类型为 ``mac``, 使用 ``psutil``
    - 其他使用 ``socket``

    :param iface: ``网络接口``
    :type iface: str
    :return: ``mac地址/空``
    :rtype: str/None
    """
    if platform.system() in ['Darwin', 'Linux']:
        _AF_FAMILY = psutil.AF_LINK
    else:
        raise SystemExit('Unsupported System. Only Mac/Linux Supported')

    addrs = psutil.net_if_addrs()
    for n in addrs[iface]:
        if n.family == _AF_FAMILY:
            return n.address


def uniqid(iface='wlan0', is_hex=True):
    """
        使用网卡的物理地址 ``默认wlan0`` 来作为标识

    - 置位 ``is_hex``, 来确定返回 ``16进制/10进制格式``

    :param iface: ``网络接口(默认wlan0)``
    :type iface: str
    :param is_hex: ``True(返回16进制)/False(10进制)``
    :type is_hex: bool
    :return: ``mac地址/空``
    :rtype: str
    """
    # return str(appid.getnode()) if not is_hex else str(hex(appid.getnode()))[2:-1]
    m_ = get_addr(iface)
    m_ = ''.join(m_.split(':')) if m_ else m_
    if m_ and not is_hex:
        m_ = str(int(m_.upper(), 16))
    return m_


def app_id(iface=''):
    """ 依据指定的 ``iface`` 名, 来获取程序运行需要的唯一ID

    - iface 为空, 则自动从系统选择第一个可用的网络接口 mac
    - 顺序,自动获取编号最小的网络接口:
        + macosx: en0~n
        + linux: eth/wlan(0~n)

    :param iface: ``系统中的网络接口名``
    :type iface: str
    :return:
    :rtype:
    """
    if iface:
        return uniqid(iface)

    if platform.system() == 'Darwin':
        _ava_start = ['en']
    elif platform.system() == 'Linux':
        _ava_start = ['eth', 'wla']
    else:
        return None

    nics = psutil.net_if_addrs()
    _ifces = list(nics.keys())
    _ifces.sort()

    for _ in _ifces:
        if _[:len(_ava_start[0])] in _ava_start:
            return uniqid(_)


def get_sys_cmd_output(cmd):
    """
        通过 ``subprocess`` 运行 ``cmd`` 获取系统输出

    - ``cmd`` 为数组形式
    - 需要符合 ``subprocess`` 调用标准
    -  返回

       -  err信息,
       -  使用 ``换行符\\n`` 分隔的数组

    :param cmd:
    :type cmd: list, str
    :return:
    :rtype:
    """
    _e, op = None, ''
    if not isinstance(cmd, list):
        cmd = cmd.split(' ')

    try:
        op = subprocess.check_output(cmd)
        if sys.version_info[0] >= 3:
            op = to_str(op)
        op = op.split('\n')
    except Exception as err:
        _e = err

    return _e, op


"""程序控制 线程/定期运行"""


def block_here(duration=0):
    """
    如果 duration 为0, 则一直阻塞程序运行
    :param duration:
    :type duration:
    :return:
    :rtype:
    """
    try:
        while not duration:
            time.sleep(0.001)

        while duration:
            time.sleep(0.001)
            duration -= 1
    except KeyboardInterrupt as err:
        raise SystemExit(1)


""" http get/post """


def do_get(url, params, to=3):
    """
    使用 ``request.get`` 从指定 url 获取数据

    :param params: ``输入参数, 可为空``
    :type params: dict
    :param url: ``接口地址``
    :type url:
    :param to: ``响应超时返回时间``
    :type to:
    :return: ``接口返回的数据``
    :rtype: dict
    """
    try:
        rs = requests.get(url, params=params, timeout=to)
        if rs.status_code == 200:
            try:
                return rs.json()
            except Exception as __e:
                # log.error(__e)
                return rs.text
    except Exception as er:
        log.error('get {} ({}) with err: {}'.format(url, params, er))
        time.sleep(0.5)
    return {}


def do_post(url, payload, to=3, use_json=True):
    """
    使用 ``request.get`` 从指定 url 获取数据

    :param use_json: 是否使用 ``json`` 格式, 如果是, 则可以直接使用字典, 否则需要先转换成字符串
    :type use_json: bool
    :param payload: 实际数据内容
    :type payload: dict
    :param url: ``接口地址``
    :type url:
    :param to: ``响应超时返回时间``
    :type to:
    :return: ``接口返回的数据``
    :rtype: dict
    """
    try:
        if use_json:
            rs = requests.post(url, json=payload, timeout=to)
        else:
            rs = requests.post(url, data=payload, timeout=to)
        if rs.status_code == 200:
            log.warn(rs.text)
            return rs.json()
    except Exception as er:
        log.error('post to {} ({}) with err: {}'.format(url, payload, er))
        time.sleep(0.5)
    return {}


""" 进制, str/bytes 转换 """


def b2h(bins):
    return ''.join(["%02X" % x for x in bins]).strip()


def to_str(str_or_bytes, charset='utf-8'):
    """
        转换 str_or_bytes 为 str

        - if hasattr(str_or_bytes, 'decode'), 转换

    :param str_or_bytes:
    :type str_or_bytes:
    :param charset:
    :type charset:
    :return:
    :rtype:
    """
    return str_or_bytes.decode(charset) if hasattr(str_or_bytes, 'decode') else str_or_bytes


def to_bytes(str_or_bytes):
    """
        转换 str_or_bytes 为 bytes

        - if hasattr(str_or_bytes, 'encode'), 转换

    :param str_or_bytes:
    :return:
    """
    return str_or_bytes.encode() if hasattr(str_or_bytes, 'encode') else str_or_bytes


""" 实用功能 """


def randint(start=0, end=100):
    return random.randint(start, end)


def words(fpth):
    """
    ww = words(os.path.join(app_root, 'ig/helper.py'))
    for k, v in (ww.most_common(3)):
        print(k, v)

    :param fpth:
    :type fpth:
    :return:
    :rtype:
    """
    from collections import Counter
    words__ = Counter()
    with open(fpth) as fp:
        for line in fp:
            words__.update(line.strip().split(' '))
    return words__
