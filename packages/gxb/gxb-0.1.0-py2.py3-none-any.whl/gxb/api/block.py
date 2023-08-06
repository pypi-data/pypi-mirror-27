#!/usr/bin/env python
# coding=utf-8

import base64
import requests
from gxb.exceptions import GxbRequestException
from functools import wraps

class BlockAPI(object):
  API_URL = "http://block.gxb.io/api"

  def wrap_request(request):
    @wraps(request)
    def wrapper(self, *args, **kwargs):
      try:
        return request(self, *args, **kwargs)
      except ValueError:
        raise GxbRequestException('Invalid Response For Request: %s' % request.__doc__)
    return wrapper

  @wrap_request
  def get_supply(self):
    """block.gxb.io/api/supply"""
    return requests.get("%s/%s" % (self.API_URL, "supply")).json()

  @wrap_request
  def get_block_info(self, block_height):
    """https://block.gxb.io/api/block/:block_height"""
    return requests.get("%s/%s/%s" % (self.API_URL, "block", block_height)).json()

  @wrap_request
  def get_transaction_info(self, tx_id):
    """https://block.gxb.io/api/transaction/:tx_id"""
    return requests.get("%s/%s/%s" % (self.API_URL, "transaction", tx_id)).json()

  @wrap_request
  def get_account_info(self, account_id_or_name):
    """https://block.gxb.io/api/account/:account_id_or_name"""
    return requests.get("%s/%s/%s" % (self.API_URL, "account", account_id_or_name)).json()

  @wrap_request
  def get_account_balance(self, account_id_or_name):
    """https://block.gxb.io/api/account_balance/:account_id_or_name"""
    return requests.get("%s/%s/%s" % (self.API_URL, "account_balance", account_id_or_name)).json()

  @wrap_request
  def get_account_avatar(self, account_name):
    """https://block.gxb.io/api/header/:account_name"""
    img = b''
    resp = requests.get("%s/%s/%s" % (self.API_URL, "header", account_name))
    for chunk in resp.iter_content(chunk_size=128):
      img += chunk

    return base64.b64encode(img)

  @wrap_request
  def get_product_info(self, product_id):
    """https://block.gxb.io/api/product/:product_id"""
    return requests.get("%s/%s/%s" % (self.API_URL, "product", product_id)).json()
