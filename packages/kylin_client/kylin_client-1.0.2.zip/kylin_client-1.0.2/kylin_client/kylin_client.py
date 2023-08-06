# -*- coding: utf-8 -*-

__author__ = 'chenglei'


import json
import base64
import requests


class KylinClient(object):

    def __init__(self, host, user, password):

        self.host = host
        self.user = user
        self.password = password

        auth_url = 'http://{0}/kylin/api/user/authentication'.format(self.host)

        self.s = requests.session()
        self.s.post(auth_url, headers={
            'Authorization': 'Basic {0}'.format(base64.b64encode(':'.join([self.user, self.password]))),
            'Content-Type' : 'application/json'
        })

    def query(self, sql, project='kylin_test', limit=5000):
        query_url = 'http://{0}/kylin/api/query'.format(self.host)
        r = self.s.post(query_url, data=json.dumps({
            'sql': '{0}'.format(sql),
            'offset': 0,
            'limit': limit,
            'project': '{0}'.format(project),
            'acceptPartial': False
        }), headers={'Content-Type': 'application/json'})
        return r.json()

    def build(self, cubename, start, end, buildtype='BUILD'):
        build_url = 'http://{0}/kylin/api/cubes/{1}/build'.format(self.host, cubename)
        r = self.s.put(build_url, data=json.dumps({
            'startTime': '{0}'.format(start),
            'endTime': '{0}'.format(end),
            'buildType': buildtype
        }), headers={'Content-Type': 'application/json'})
        return r.json()