# coding=utf-8

"""
Example:
~~~~~~~~
    zafw = SendMsg(agentid=agentid, corpid='corpid', corpsecret='corpsecret')
    ret = zafw.send_text_msg(touser=['user1', 'user2'], toparty=['party1', 'party2'], content='content')
"""


import os
import requests
import json
import pickle
import logging
from datetime import datetime
from WeChatTool.exception import *
from WeChatTool.utils import check_msg_params

__all__ = ["SendMsg"]
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(funcName)s: %(message)s')


class SendMsg:
    def __init__(self, agentid=None, corpid=None, corpsecret=None):
        self.sendmsg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?'
        self.gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.cache_file = '/tmp/.{}.pick'.format(self.corpid)

    def get_token_from_server(self):
        token_info = {}
        timestamp = int(datetime.timestamp(datetime.now()))
        args = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret,
            'token_file': self.cache_file
        }
        try:
            resp = requests.get(self.gettoken_url, params=args, timeout=6)
            token_info['ctime'] = timestamp
            token_info['token'] = resp.json()['access_token']
            token_info['expires_in'] = resp.json()['expires_in']
            logging.info('get token from server success')
            with open(self.cache_file, 'wb') as fb:
                logging.info('write token to cache file')
                pickle.dump(token_info, fb)
            return token_info
        except Exception:
            logging.info('get token from server failed')
            raise GetTokenError()

    def _get_token_from_cache(self):
        timestamp = int(datetime.timestamp(datetime.now()))
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as fb:
                    token_info = pickle.load(fb, errors='ignore')
                    ctime = int(token_info['ctime'])
                    expires_in = int(token_info['expires_in'])
                    if ctime + expires_in > timestamp - 10:
                        logging.info('get token from cache file')
                        return token_info
                    raise HitTokenError('cache token failure')
            except Exception:
                raise HitTokenError('read cache file error')
        raise HitTokenError('cache file not exist')

    def get_token(self):
        try:
            token = self._get_token_from_cache()['token']
        except HitTokenError:
            token = self.get_token_from_server()['token']
        except Exception:
            raise Exception('get token failed')
        return token

    @check_msg_params
    def send_text_msg(self, **kwargs):
        args = {
            "touser": '|'.join(str(x) for x in kwargs.get('touser')),
            "toparty": '|'.join(str(x) for x in kwargs.get('toparty')),
            "agentid": self.agentid,
            "msgtype": "text",
            "text": {
                "content": kwargs.get('content')
            },
            "safe": 0
        }
        try:
            token = self.get_token()
            resp = requests.post('{0}access_token={1}'.format(self.sendmsg_url, token), data=json.dumps(args))
            logging.debug('{}-->{}'.format(args, resp.json()))
            if resp.json()['errcode'] == 0:
                logging.info('send msg successed')
                return {'code': 0, 'msg': 'send msg successed'}
            return {'code': 1, 'msg': 'send msg failed'}
        except Exception:
            logging.info('send msg failed')
            return {'code': 1, 'msg': 'send msg failed'}
