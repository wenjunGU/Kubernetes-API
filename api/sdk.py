#/usr/bin/env python
# --*-- coding:utf-8 --*--

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

class AliyunAccount(object):
    def __init__(self, access_key_id, access_key_secret):
        self.client = AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
        self.request = CommonRequest()
        self.request.set_accept_format('json')
        self.request.set_domain('business.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_version('2017-12-14')

    def query_account_balance(self, **kwargs):
        self.request.set_action_name('QueryAccountBalance')
        for key, value in kwargs.items():
            self.request.add_query_param(key, value)
        response = self.client.do_action_with_exception(self.request)
        return response

    def query_product_list(self, **kwargs):
        """
        查询阿里云产品列表
        :param kwargs:
        :return:
        """
        self.request.set_action_name('QueryProductList')
        for key, value in kwargs.items():
            self.request.add_query_param(key, value)
        response = self.client.do_action_with_exception(self.request)
        return response

    def get_all_aliyun_product_code(self):
        page_size = 100
        page_number = 1
        self.request.set_action_name('QueryProductList')
        produce_code_list = []
        while True:
            self.request.add_query_param('PageNum', page_number)
            self.request.add_query_param('PageSize', page_size)
            self.request.add_query_param('QueryTotalCount', True)
            response = self.client.do_action_with_exception(self.request)
            produce_list = json.loads(response)['Data']['ProductList']['Product']
            for produce in produce_list:
                produce_code_list.append(produce['ProductCode'])
            page_number += 1
            if page_size * page_number >= int(json.loads(response)['Data']['TotalCount']):
                break
        print produce_code_list
        return list(set(produce_code_list))

    def QuerySettlementBill(self, **kwargs):
        self.request.set_action_name('QuerySettlementBill')
        for key, value in kwargs.items():
            if key == 'QuerySettlementBill':
                continue
            self.request.add_query_param(key, value)
        response = self.client.do_action_with_exception(self.request)
        # print response
        return response

    @staticmethod
    def ramalias(access_key_id, access_key_secret):
        client = AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('ram.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2015-05-01')
        request.set_action_name('GetAccountAlias')

        response = client.do_action_with_exception(request)
        return json.loads(response)['AccountAlias']
