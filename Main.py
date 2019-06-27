#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-06-19 23:55:52
# @Author  : Your Name (you@example.org)
# @Link    : link
# @Version : 1.0.0

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from AppLoggin import logging
from AppConfig import myRedis, redisKey, weChat_api, myWeChat
import redis
import requests
import json


app = Flask(__name__)
api = Api(app)

pool = redis.ConnectionPool(**myRedis)
r = redis.Redis(connection_pool=pool)

# 空方法
class Emptys(Resource):
    def get(self):
        return {'errcode': 404, 'errmsg': '页面不存在'}
    
    def post(self):
        return {'errcode': 404, 'errmsg': '页面不存在'}

        
# 获取微信token
class AccessToken(Resource):
    def get(self):
        access_token = r.get(redisKey['access_token'])
        return {'errcode': 0, 'errmsg': '获取成功', 'value': access_token.decode('utf-8') if access_token else ''}


# 获取微信token
class Ticket(Resource):
    def get(self):
        ticket = r.get(redisKey['ticket'])
        return {'errcode': 0, 'errmsg': '获取成功', 'value': ticket.decode('utf-8') if ticket else ''}

# 发送模板消息
class SendTemplateMessage(Resource):
    def post(self):
        url = 'http://127.0.0.1:5000/access_token'
        res = requests.get(url).json()
        access_token = res['value']
        if access_token:
            send_url = weChat_api['send_temp_msg'] % access_token

            parser = reqparse.RequestParser()

            parser.add_argument('openid', type=str)
            parser.add_argument('template_id', type=str)
            parser.add_argument('url', type=str)
            parser.add_argument('first_val', type=str)
            parser.add_argument('keyword1_val', type=str)
            parser.add_argument('keyword2_val', type=str)
            parser.add_argument('remark_val', type=str)

            args = parser.parse_args()
            if not args['openid']:
                return {'errcode': 2, 'errmsg': 'openid不能为空'}
            
            if not args['template_id']:
                return {'errcode': 2, 'errmsg': 'template_id不能为空'}

            if not args['first_val'] or not args['keyword1_val'] or not args['keyword2_val'] or not args['remark_val']:
                return {'errcode': 2, 'errmsg': '模板消息不能为空'}

            temp_data = {
                'touser': args['openid'],
                'template_id': args['template_id'],
                'url': args['url'],
                'data': {
                    'first': {
                        'value': args['first_val'],
                    },
                    'keyword1': {
                        'value': args['keyword1_val'],
                    },
                    'keyword2': {
                        'value': args['keyword2_val'],
                    },
                    'remark': {
                        'value': args['remark_val'],
                    }
                }
            }

            send_result = requests.post(send_url, verify=False, json=temp_data)
            res = send_result.json()

            logging.info('[data] %s ,res %s' % (json.dumps(temp_data, ensure_ascii=False), send_result.text))
            
            return {'errcode': res['errcode'], 'errmsg':  res['errmsg']}
        else:
            return {'errcode': 1, 'errmsg': 'access_token获取失败'}


api.add_resource(Emptys, '/')
api.add_resource(AccessToken, '/access_token')
api.add_resource(Ticket, '/ticket')
api.add_resource(SendTemplateMessage, '/send_template_message')

if __name__ == '__main__':
    # app.config['JSON_AS_ASCII'] = False
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    app.run(host='127.0.0.1', port='5000', debug=True)