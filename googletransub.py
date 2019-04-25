import requests
import json
import os
import shutil
import execjs #必须，需要先用pip 安装，用来执行js脚本
import time
class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072;       
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f";    
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
        };      
        function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
        } 
        """)
    def getTk(self,text):
        return self.ctx.call("TL", text)
def buildUrl(text,tk):
    """构建url，主要是传入文本和tk值，sl指要翻译的文本语言类型，tl指想要翻译成的语言类型"""
    tk = str(tk)
    baseUrl= f'https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=en&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk={tk}&q={text}'
    # print(baseUrl)
    return baseUrl
def translate(text):
      header={
        'authority':'translate.google.cn',
        'method':'GET',
        'path':'',
        'scheme':'https',
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        'cookie':'',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'x-client-data':'CKq1yQEIi7bJAQiitskBCMG2yQEIqZ3KAQioo8oBCLGnygEI4qjKAQjxqcoB'
      }
      url=buildUrl(text, js.getTk(text))
      res=''
      try:
          requests.adapters.DEFAULT_RETRIES = 5  # 增加重试次数
          s = requests.session()
          s.keep_alive = False    # 关闭多余连接
          #time.sleep(1)  # 需要时加个延时，避免短时间请求太多
          # s.proxies = {"https": "60.205.229.126:80"}  # 使用代理
          # 上面主要是为了防止" Max retries exceeded with url"报错，
          r=s.get(url)
          result=json.loads(r.text)
          if result[7]!=None:
          # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
              try:
                  correctText=result[7][0].replace('<b><i>',' ').replace('</i></b>','')
                  print(correctText)
                  correctUrl=buildUrl(correctText,js.getTk(correctText))
                  correctR=requests.get(correctUrl)
                  newResult=json.loads(correctR.text)
                  res=newResult[0][0][0]
              except Exception as e:
                  print(e)
                  res=result[0][0][0]
          else:
              res=result[0][0][0]
      except Exception as e:
          res=''
          print(url)
          print("翻译"+text+"失败")
          print("错误信息:")
          print(e)
      finally:
          return res


def translate_file(filepath, filetype = ''):

    n = 0
    for root, dirs, files in os.walk(filepath):
            for file in files:
                if file.endswith(filetype):  # 指定文件类型，后缀为 .vtt
                    newfile = file.replace(filetype, ".txt")
                    src_file = os.path.join(root, file)
                    new_file = os.path.join(root, newfile)
                    if os.path.exists(new_file):
                        os.remove(new_file)
                    shutil.copyfile(src_file, new_file)
                    with open(new_file, "r", encoding="utf-8") as f:
                        text = f.readlines()
                        for sentence in text:
                            if sentence != "\n":
                                if "-->" in sentence:   # 时间直接返回，不进行翻译
                                    res = sentence
                                else:
                                    n += 1
                                    res = translate(sentence)
                                    print(n, res)
                                    res = res + "\n"
                                newsub = new_file.replace(".txt", f"_{filetype}")
                                sub = open(newsub, "a+", encoding='utf-8')
                                sub.write(res)
                            else:
                                continue
                    sub.close()
                    os.remove(new_file)






if __name__ == '__main__':
  js=Py4Js() # 执行js 生成tk值
  # res=translate('Par exemple, vous pouvez')
  # print(res)
  translate_file(r"C:\Users\DH107000\Downloads\[FreeCourseSite.com] Udemy - Complete Python Bootcamp Go from zero to hero in Python 3", ".vtt")  # 文件路径, 文件类型