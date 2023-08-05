#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__=""

"""顶层包引入"""
import sys
sys.path.append("/root/Downloads/Pscc")

"""引入基本包，受__all__限制"""
from pscc import QS, Item, XS


# def test_item_define():
def item_define():
    class User(Item):
        username = QS(".username")

    assert "username" in User.selectors
    assert isinstance(User.selectors["username"],QS)


def item_parser():
    class User(Item):
        username = XS('//title')
        karma = QS('.karma')

    html = '<title class="username">tom</title><div class="karma">15</div>'
    user = User(html)

    assert 'username' in user.results
    assert 'karma' in user.results
    assert user.username == 'tom'
    assert user.karma == '15'


item_define()
item_parser()
# test_item_define()
# assert 1==1