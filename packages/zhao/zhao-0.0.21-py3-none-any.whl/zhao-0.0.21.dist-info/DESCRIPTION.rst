大家读我
========

尽管一直以来我坚守着 Python2 这个阵地，但如今我也离她而去了。

所以，我推荐大家和我一样将 **Python3.6** 作为 2018 年的新起点！

也因此本包使用了某些 Python3.6 的特性，且仅发布了 Python3 的版本。

包包简介
========

可能您会觉得这个包里面东西五花八门，但我真心希望其中的某些代码对您有用。

比如，如果您可能也使用小米路由器，可能您也发现它会不时掉线，只有手动断开ADSL并重新拨号才能恢复上网？

那么，您可以试试 `zhao.xin_api.MiWiFi` 对象::

    from zhao.xin_api import MiWiFi
    MIWIFI = MiWiFi(password='您自己的小米路由器WEB登录密码')
    if MIWIFI.is_offline:
        if MIWIFI.reconnect():
            printf('自动重新拨号成功')
        else:
            printf('自动重新拨号失败')


