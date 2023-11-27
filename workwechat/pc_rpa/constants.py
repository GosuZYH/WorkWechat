import os

ROAMING_PATH = os.getenv("APPDATA")
DATA_PATH = os.path.join(ROAMING_PATH, "SMR")
LOG_PATH = os.path.join(DATA_PATH, "log")
PHOTO_PATH = os.path.join(LOG_PATH, "photo")
DB_PATH = os.path.join(DATA_PATH, "data")
RSA_PATH = os.path.join(DATA_PATH, "rsa")
UI_PATH = os.path.join(DATA_PATH, "ui")
# PUBLIC_PATH = RSA_PATH + '\\api_public_key.key'
# PRIVATE_PATH = RSA_PATH + '\\api_private_key.key'

pubkey = '''-----BEGIN RSA PUBLIC KEY-----
MEgCQQDP8W17Y7a+FiRNKvedtOnV+jpkjUdLMM7G/Q7CWLWjDNZtaWGC728/903s
EHniA5KA0GV08breeibcT7oj+9OJAgMBAAE=
-----END RSA PUBLIC KEY-----
'''
prikey = '''-----BEGIN RSA PRIVATE KEY-----
MIIBPAIBAAJBAM/xbXtjtr4WJE0q95206dX6OmSNR0swzsb9DsJYtaMM1m1pYYLv
bz/3TewQeeIDkoDQZXTxut56JtxPuiP704kCAwEAAQJAG0VreVo7djSLMD+pV9qJ
LFHz5IoOxpKxG7HGhMCDe8HRZxOBUFM/LEJ3U6F6RdgW89Nwc8qV1QAvF1Zzpa/b
MQIjAOUakEis+fuKK48JgvPjwMieHxW6YH5KU3ywnygqL1wISF0CHwDoWue7iTk0
dGHbWpzEHOVmfVEb7tr7HnVnXevMFR0CIgQUYANbSSxIfpQSeEl9gb5Qyn7pjbRS
AICU6JCfh65c22UCHg+BCVdtJ6EFZwYw/KblWrVFBWV8waXh+WmFTdeXTQIjALMW
G4J719wdkZTPhCHb+xCs6oIsfcmBOzA2WZ3I/EoudNU=
-----END RSA PRIVATE KEY-----
'''



PUBLIC_KEY = '-----BEGIN RSA PUBLIC KEY-----\
MEgCQQCUy8zzHoTc+xf6XgD6UEMSmnSDPUuWiorCQVONz/AOAalKYPGGFpC16kzK\
RfyYYC5qCC91TxlTv0j/2j+WLMVXAgMBAAE=\
-----END RSA PUBLIC KEY-----'
PRIVATE_KEY = '-----BEGIN RSA PRIVATE KEY-----\
MIIBPAIBAAJBAJTLzPMehNz7F/peAPpQQxKadIM9S5aKisJBU43P8A4BqUpg8YYW\
kLXqTMpF/JhgLmoIL3VPGVO/SP/aP5YsxVcCAwEAAQJBAItbEDkGdUMNe5iF3/6P\
mzHaLJMZniiA2pIyYpGnlCccx1ke1sSjXvmdfz6iZdo4sHyvlsA6VOi29n6qezzE\
nZkCIwC+T5yb0K9+kn4GYTn2ppYy4rwkOG9msDhRbgzNMILMray7Ah8AyCfSerYN\
Vs/NHQ9qdIfIvtCewlwDqj9mAXqobC4VAiIuAweFMJZNjtODbVxbQvmLggAk7bQZ\
ar+jCG116qWlINRjAh5Q/DPgrMqm5nuSl4s2TT5/Xn/uGjbtaquGS6/b3aUCIjIv\
V/6VofiYjSJGT6MmlEYj3KZA9EckSoT/nXRk6LN/Aa4=\
-----END RSA PRIVATE KEY-----'

#企微窗口list
'''
,'无法打开小程序','请假','出差','外出','加班','会议室预定','物品领用','物品维修',
             '用章','用车','公文流转','报销','费用','付款','合同审批','采购','活动经费','入职','转正','离职',
             '绩效','招聘需求','汇报','店面检查表','营业报告','拜访记录','销售单','邀约到访','销售业绩',
             '月报','周报','日报','选择管理员','预约会议','预约直播'
'''
WINDOW_LIST= ['企业微信-工作台', '选择客户','SOP消息','朋友圈','向我的客户发消息','群发助手','客户联系','客户群','新建群发','素材管理','全部群发记录','待发送的企业消息','详情']