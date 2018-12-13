# -*- coding:utf-8 -*-
import base64
from json import JSONDecoder
import simplejson
import requests

key="oJAdSkbO1z-1fS0CXR98q-1R5t6SgP7g"
secret="s5BR5q-l4P7yjMXThBhnwc48M1lgNLse"

def find_face(imgpath):
    print("finding")
    http_url="https://api-cn.faceplusplus.com/facepp/v3/detect"
    data={"api_key":key,"api_secret":secret,"image_url":imgpath,"return_landmak":1}
    files={"image_file":open(imgpath,"rb")}
    response=requests.post(http_url,data=data,files=files)
    req_con=response.content.decode('utf-8')
    req_dict=JSONDecoder().decode(req_con)

    this_json=simplejson.dumps(req_dict)
    this_json2=simplejson.loads(this_json)

    faces=this_json2['faces']
    list0=faces[0]
    rectangle=list0['face_rectangle']
    return rectangle

def add_face(image_url_1,image_url_2,image_url,number):
    ff1=find_face(image_url_1)
    ff2=find_face(image_url_2)

    rectangle1=str(ff1['top'])+","+str(ff1['left'])+","+str(ff1['width'])+","+str(ff1['height'])
    rectangle2=str(ff2['top'])+","+str(ff2['left'])+","+str(ff2['width'])+","+str(ff2['height'])

    url_add='https://api-cn.faceplusplus.com/imagepp/v1/mergeface'

    f1=open(image_url_1,'rb')
    f1_64=base64.b64encode(f1.read())
    f1.close()
    f2=open(image_url_2,'rb')
    f2_64=base64.b64encode(f2.read())
    f2.close()

    data={"api_key": key, "api_secret": secret, "template_base64": f1_64, "template_rectangle": rectangle1,
            "merge_base64": f2_64, "merge_rectangle": rectangle2, "merge_rate": number}

    response=requests.post(url_add,data=data)
    req_con=response.content.decode('utf-8')
    req_dict=JSONDecoder().decode(req_con)
    #print(req_dict)
    result=req_dict['result']
    imgdata=base64.b64decode(result)
    file=open(image_url,'wb')
    file.write(imgdata)
    file.close()
    
image_url_2=r'/home/hj/Desktop/hj.jpg'
image_url_1=r'/home/hj/Desktop/lhz1.jpg'
image_url=r'/home/hj/Desktop/add1.jpg'
add_face(image_url_1,image_url_2,image_url,50)