# -*- coding:utf-8 -*-
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as CPK


# 加密方法
def rsa_encrypt(pubkey, string):
	rsaKey = RSA.importKey(pubkey)
	cipher = CPK.new(rsaKey)
	res = base64.b64encode(cipher.encrypt(string.encode(encoding="utf-8")))
	return res.decode(encoding='utf-8')


# 解密方法
def rsa_decrypt(prikey, enCode):
	rsaKey = RSA.importKey(prikey)
	cipher = CPK.new(rsaKey)
	res = cipher.decrypt(base64.b64decode(enCode), "ERROR")
	return res.decode(encoding='utf-8')
