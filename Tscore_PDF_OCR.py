#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 00:03:36 2022

@author: alyion
"""

from PIL import Image
import pytesseract 
import os
import re
import fitz
#搜索資料夾內pdf檔案
def DFS_file_search(dict_name):
    stack = []
    result_txt = []
    stack.append(dict_name)
    while len(stack) != 0:  #所有目錄是否以搜索完畢
        temp_name = stack.pop()
        try:
            temp_name2 = os.listdir(temp_name) # list ["","",...]
            for eve in temp_name2:
                stack.append(temp_name + "/" + eve)  #維持絕對路徑
        except NotADirectoryError:
            if temp_name.endswith(".pdf"):
                result_txt.append(temp_name)
    return result_txt
#pdf轉img
def pdf_image(pdfPath,imgPath,zoom_x,zoom_y,rotation_angle):
  # 打開PDF文件
  pdf = fitz.open(pdfPath)
  # 逐頁讀取PDF
  for pg in range(0, pdf.page_count):
    page = pdf[pg]
    # 設置縮放和旋轉系數
    trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
    pm = page.get_pixmap(matrix=trans, alpha=False)
    img = pdfPath[pdfPath.rindex('/') + 1:pdfPath.rindex(r'.')]
    pm.save(imgPath + str(img) + str(pg) + ".png")
    # 開始寫圖像
  pdf.close()

#img切割
def png_crop(imgPath,cropPath,filename,zoom_x = 4, zoom_y = 4):
   im = Image.open(imgPath+".png")
   im1 = im.crop((800*(zoom_x/7.5), 640*(zoom_y/7.5), (4590-3020)*(zoom_x/7.5), (5940-5080)*(zoom_y/7.5)))
   im2 = im.crop((3125*(zoom_x/7.5), 2600*(zoom_y/7.5), (4590-920)*(zoom_x/7.5), (5940-2800)*(zoom_y/7.5)))
   im1 = im1.resize((im1.width//2,im1.height//2))
   im1.save(cropPath+'/'+filename.rstrip('.png')+"_name.png")
   im2.save(cropPath+'/'+filename.rstrip('.png')+"_score.png")


pdfPath =[]
dirPath = input('请輸入pdf轉存為png輸出之路徑：')#/Users/alyion/Desktop/111 8月OA/DXA
pdfPath = DFS_file_search(dirPath)
os.makedirs(dirPath+'/'+"pic")

for i in range(0,len(pdfPath)):
    pdf_image(
        pdfPath[i],
        dirPath+'/'+"pic"+'/', 4, 4, 0)
patient_tscore_dic = {}
os.makedirs(dirPath + '/' + 'crop')
for filename in os.listdir(dirPath+'/'+"pic"+'/'):
    f = os.path.join(dirPath+'/'+"pic"+'/',filename).rstrip(".png")
    png_crop(f,dirPath+'/' + 'crop', filename)  
    text1 = pytesseract.image_to_string(Image.open(dirPath+'/' + 'crop/'+filename.rstrip('.png')+"_name.png"),lang = 'chi_tra')
    text2 = pytesseract.image_to_string(Image.open(dirPath+'/' + 'crop/'+filename.rstrip('.png')+"_score.png"),lang = 'chi_tra')
    print(text1[0]+text1[3]+text1[4])
    name = text1[0]+text1[3]+text1[4]
    if re.search(u'[\u4e00-\u9fff]', name):
        name = re.sub('/','', name)
    else:
        name = filename
    print(text2)
    score = text2
    patient_tscore_dic.setdefault(name,score)
    os.rename(dirPath+'/' + 'pic/'+filename.rstrip('.png')+".png", dirPath+'/' + 'pic/'+ name +".png")
    os.rename(dirPath+'/' + 'crop/'+filename.rstrip('.png')+"_name.png", dirPath+'/' + 'crop/'+ name +"_name.png")
    os.rename(dirPath+'/' + 'crop/'+filename.rstrip('.png')+"_score.png", dirPath+'/' + 'crop/'+ name +"_score.png")
print(patient_tscore_dic)

with open('/Users/alyion/Desktop/111 8月OA/DXA/八月tscore.csv', 'w') as f:
    for key in patient_tscore_dic.keys():
        f.write("%s, %s\n" % (key, patient_tscore_dic[key].replace('\n\n','\n').replace('\n',',')))
        
        
#調整參數區域/Users/alyion/Desktop/111 8月OA/DXA/4m80hr7ipc.dfx00.png
# pdfID = "4m80hr7ipc"
# pdf_image("/Users/alyion/Desktop/111 8月OA/DXA/"+pdfID+".dfx00/"+pdfID+".pdf","/Users/alyion/Desktop/",4, 4, 0)
# png_crop("/Users/alyion/Desktop/"+pdfID+"0","/Users/alyion/Desktop/",pdfID+"0",4, 4)
# im1 = Image.open("/Users/alyion/Desktop/"+pdfID+"0_name.png")
# im2 = Image.open("/Users/alyion/Desktop/"+pdfID+"0_score.png")
# im1 = im1.resize((im1.width//2,im1.height//2))
# text1 = pytesseract.image_to_string(im1,lang = 'chi_tra')
# text2 = pytesseract.image_to_string(im2,lang = 'chi_tra')
# print(text1[0]+text1[3]+text1[4])
# name = text1[0]+text1[3]+text1[4]
# if re.search(u'[\u4e00-\u9fff]', name):
#     name = re.sub('/','', name)
# else:
#     name = filename
# print(text2)
# score = text2
    
    
    
    
    
    