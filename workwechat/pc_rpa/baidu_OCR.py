import base64
import requests
from airtest.aircv import *

class CodeDemo:
    def __init__(self,img_path):
        self.AK='9dKOpkrRB7GrnRbGxAlFOaNy'
        self.SK='bglCiyBDUk8sMgV3jXuRXhHC4Fzno4GU'
        self.code_url='https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
        self.img_path=img_path
        self.access_token=self.get_access_token()

    def get_access_token(self):
        token_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={ak}&client_secret={sk}'.format(ak=self.AK,sk=self.SK)
        header={'Content-Type': 'application/json; charset=UTF-8'}
        response=requests.post(url=token_host,headers=header)
        content = response.json()
        access_token=content.get("access_token")
        return access_token

    def getCode(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        def read_img():
            with open(self.img_path, "rb")as f:
                return base64.b64encode(f.read()).decode()

        image = read_img()
        response=requests.post(url=self.code_url,data={"image":image,"access_token":self.access_token},headers=header)
        return response.json()


class SMROCR:
    def __init__(self) :
        self.code_url='http://192.168.200.90:7000/ocr'

    def request_ocr(self,file_path,file_name):
        '''
        request POST to outline SDK.
        '''
        file = {'img_file':(file_name,open(file_path,'rb'),'png/jpg')}
        response = requests.post(url=self.code_url, files=file)
        resjson = response.json()
        print(resjson)
        return resjson

if __name__ == '__main__':
    # local = aircv.imread(filename=img_path)
    # show_origin_size(img = local)

    # code_obj=CodeDemo(img_path=img_path)
    # res=code_obj.getCode()
    # words_result=res.get("words_result")
    # words_list = [words.get('words') for words in words_result]
    # words_str = str(words_list)

    # print('——response——:',res)
    # print('——res——:',words_result)
    # print('——list——:',words_list)
    # print('——string——:',words_str)

    ocr = SMROCR()
    name = 'test3'
    ocr.request_ocr(file_name=name)