from datetime import datetime
from PIL import Image
import pytesseract
import os
import pandas as pd
import numpy as np

ROAMING_PATH = os.getenv("APPDATA")
DATA_PATH = os.path.join(ROAMING_PATH, "SMR")
UI_PATH = os.path.join(DATA_PATH, "ui")
img_path = UI_PATH + '\\test.png'

s_time = datetime.now()
data = pytesseract.image_to_data(Image.open(img_path),lang='chi_sim',output_type='dict')
e_time = datetime.now()
print(data)
print('用时：',(e_time-s_time).total_seconds())

share_list = []
reply_list = []

# share_list.append(data.loc[data['text']=='一'])
# share_list.append(data.loc[data['text']=='键'])
# share_list.append(data.loc[data['text']=='分'])
# share_list.append(data.loc[data['text']=='享'])
# share_list.append(data.loc[data['text']=='朋友'])
# share_list.append(data.loc[data['text']=='圈'])

# reply_list.append(data.loc[data['text']=='回'])
# reply_list.append(data.loc[data['text']=='执'])
# reply_list.append(data.loc[data['text']=='回执'])

# print(np.array(share_list))
# print(np.array(reply_list))

# max_pos_y = 0
# for i in share_list:
#     print(i.loc[i['top']])
#     # if i['top'] > max_pos_y:
#         max_pos_y = i['top']

for i in data.series:
    print(i)
df_stitched = pd.DataFrame()
for i in range(len(data)):
    if data.loc[i]['text'] == '一':
        df_stitched = pd.concat([data.loc[i]])
    elif data.loc[i]['text'] == '键':
        df_stitched = pd.concat(df_stitched,data.loc[i])
    elif data.loc[i]['text'] == '分':
        df_stitched = pd.concat(df_stitched,data.loc[i])
    elif data.loc[i]['text'] == '享':
        df_stitched = pd.concat(df_stitched,data.loc[i])
    elif data.loc[i]['text'] == '朋':
        df_stitched = pd.concat(df_stitched,data.loc[i])
    elif data.loc[i]['text'] == '友':
        df_stitched = pd.concat(df_stitched,data.loc[i])
    elif data.loc[i]['text'] == '朋友':
        df_stitched = pd.concat(df_stitched,data.loc[i])
    elif data.loc[i]['text'] == '圈':
        df_stitched = pd.concat(df_stitched,data.loc[i])
    elif data.loc[i]['text'] == '回':
        df_stitched = pd.concat(df_stitched,data.loc[i])
    elif data.loc[i]['text'] == '执':
        df_stitched = pd.concat(df_stitched,data.loc[i])
    elif data.loc[i]['text'] == '回执':
        df_stitched = pd.concat(df_stitched,data.loc[i])

for i in range(len(data['text'])):
    if data['text'][i] == '一' or data['text'][i] =='键' or data['text'][i] =='分' or data['text'][i] =='享' or data['text'][i] =='朋友' or data['text'][i] =='圈':
        share_list.append(i)
    elif data['text'][i] == '回' or data['text'][i] == '执' or data['text'][i] == '回执' or data['text'][i] == '已':
        reply_list.append(i)

print(share_list)
print(reply_list)

share_top = []
for i in share_list:
    share_top.append(data['top'][i])

reply_top = []
for i in reply_list:
    reply_top.append(data['top'][i])

print(max(share_top))       #一键分享朋友圈坐标
print(max(reply_top))       #回执坐标

# print(share_list)
# df_stitched = pd.DataFrame([series_1, series_2, series_3,series_4,series_7,series_8])
# for i in share_list:
#     print(i)
#     # print(i.top>1500)



