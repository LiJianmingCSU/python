# -*- coding: UTF-8 -*-
from analysispcap.analysisPcap import TcpData


def test_get_appoint_tcp_stream():
    """测试指定方向的tcpstream"""
    client = ['192.168.43.158', 64343]
    server = ['183.232.24.222', 80]
    metas = ['192.168.43.157', '183.232.24.221', 64343, 80, 0, 0, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 1, 18, None,
             '145.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a', ]
    example = TcpData(metas, client, server).get_appoint_tcp_stream(metas, client, server)
    assert example == ['183.232.24.222', '192.168.43.158', 80, 64343, 1, 1, 18, None, 'S->C',
                       '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a',  'C->S']


def test_find_start_flags():
    """测试第三次握手时的循环数i"""
    client = ['192.168.43.158', 64343]
    server = ['183.232.24.222', 80]
    metas = ['192.168.43.158', '183.232.24.222', 64343, 80, 0, 0, 16, None, 'C->S',
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 1, 18, None, 'S->C',
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 16, None, 'C->S', ]
    example = TcpData(metas, client, server).find_start_flags(metas)
    assert example == 18


def test_reassemble_tcp():
    """测试正常情况下的tcpstream"""
    client = ['192.168.43.158', 64343]
    server = ['183.232.24.222', 80]
    metas = ['192.168.43.158', '183.232.24.222', 64343, 80, 0, 0, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 1, 18, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a',
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc',
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 3, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 3, 17, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 3, 3, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 5, 3, 17, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 6, 16, None,
             ]
    example = TcpData(metas, client, server).reassemble_tcp()
    assert example == ['192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a', 'C->S',
                       '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc', 'S->C', ]


def test_reassemble_tcp_missing_frame_1():
    """测试丢包的tcpstream"""
    client = ['192.168.43.158', 64343]
    server = ['183.232.24.222', 80]
    # 丢失内容‘a’包
    metas = ['192.168.43.158', '183.232.24.222', 64343, 80, 0, 0, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 1, 18, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc',
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 3, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 3, 17, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 3, 3, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 5, 3, 17, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 6, 16, None,
             ]
    example = TcpData(metas, client, server).reassemble_tcp()
    assert example == ['183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc', 'S->C', ]


def test_reassemble_tcp_missing_frame_2():
    """测试丢包后重传的tcpstream"""
    client = ['192.168.43.158', 64343]
    server = ['183.232.24.222', 80]
    # 丢失内容‘a’包后重传
    metas = ['192.168.43.158', '183.232.24.222', 64343, 80, 0, 0, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 1, 18, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc',
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 3, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a',
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 3, 17, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 3, 3, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 5, 3, 17, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 6, 16, None,
             ]
    example = TcpData(metas, client, server).reassemble_tcp()
    assert example == ['183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc', 'S->C',
                       '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a', 'C->S', ]


def test_reassemble_tcp_repeat_frame():
    """测试重传的tcpstream"""
    client = ['192.168.43.158', 64343]
    server = ['183.232.24.222', 80]
    metas = ['192.168.43.158', '183.232.24.222', 64343, 80, 0, 0, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 1, 18, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a',
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a',
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc',
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc',
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 3, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 3, 17, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 3, 3, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 5, 3, 17, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 6, 16, None,
             ]
    example = TcpData(metas, client, server).reassemble_tcp()
    assert example == ['192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a', 'C->S',
                       '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc', 'S->C', ]


def test_reassemble_tcp_differ_time_frame():
    """测试一段时间后的同一地址的tcpstream"""
    client = ['192.168.43.158', 64343]
    server = ['183.232.24.222', 80]
    metas = ['192.168.43.158', '183.232.24.222', 64343, 80, 0, 0, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 1, 18, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a',
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc',
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 3, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 3, 17, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 3, 3, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 5, 3, 17, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 3, 6, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 0, 0, 16, None,
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 1, 18, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'ccc',
             '183.232.24.222', '192.168.43.158', 80, 64343, 1, 5, 16, None,
             '192.168.43.158', '183.232.24.222', 64343, 80, 5, 3, 17, None,
             ]
    example = TcpData(metas, client, server).reassemble_tcp()
    assert example == ['192.168.43.158', '183.232.24.222', 64343, 80, 2, 1, 24, 'a', 'C->S',
                       '183.232.24.222', '192.168.43.158', 80, 64343, 1, 3, 24, 'cc', 'S->C', ]