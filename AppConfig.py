#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-09 16:16:21
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

# 定义个人测试公众号的配置
myWeChat = {
    'appID': 'wx89*********ba6',
    'appsecret': 'c69b71**********9ec1e'
}

weChat_api = {
    'send_temp_msg': 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s',  # 发送模板消息
}

# 定义redis配置
myRedis = {'host': '127.0.0.1', 'port': 6379, 'db': 5}

redisKey = {
    'access_token': 'wechat_access_token',  # 微信token
    'token_tmp': 'wechat_token_tmp',  # 微信token临时储存
    'ticket': 'wechat_ticket',  # 微信token
    'ticket_tmp': 'wechat_ticket_tmp',  # 微信ticket临时储存
}
