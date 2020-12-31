from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import img2pdf 
from PIL import Image
import os
import urllib
import time
import urllib3
import requests
import PyPDF2
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

for b in range(101,510,50):
    pdf = PyPDF2.PdfFileWriter()
    a = 1
    for i in range(b,b+50):
        img_old = None
        page = 1
        while(True):
            imgTemp = BytesIO()
            link = "https://www.mangareader.net/noblesse/"+str(i)+"/"+str(page)
            hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            try:
                req = Request(link,headers=hdr)
                webpage = urlopen(req)
            except:
                print("Error occured in connection with page retrying in 2 seconds")
                time.sleep(2)
                continue
            webpage_html_parsing = webpage.read()
            webpage_html = soup(webpage_html_parsing,'html.parser')
            img = "https:"+webpage_html.findAll('img')[2]["src"]
            if(img == img_old):
                break
            img_old = img
            try:
                r = requests.get(img)
            except:
                print("Error occured in connection with image retrying in 2 seconds")
                time.sleep(2)
                continue
            with open("./Noblesse1/"+str(a)+".jpg", 'wb') as outfile:
                outfile.write(r.content)
            try:
                im = Image.open("./Noblesse1/"+str(a)+".jpg")
                imgDoc = canvas.Canvas(imgTemp, pagesize=im.size)
                imgDoc.drawImage("./Noblesse1/{}.jpg".format(a),0,0)
                a = a+1
                imgDoc.save()
                pdf.addPage(PyPDF2.PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))
            except:
                print("problem at chapter"+str(i)+" image "+str(page))
            page = page+1
        print("Chapter "+str(i)+" Completed")
    output_path = "chapter{}-{}.pdf"
    pdf.write(open(output_path.format(b,b+49),"wb"))
    print(b)