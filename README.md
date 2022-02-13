# FBGroupCrawler

說明
* 主要以python3.7版本
* 自動登入設定的FB帳密
* 自動點擊社團內「顯示更多」、「查看先前回覆」、「檢視更多回覆」等隱藏所需抓取內容的按鈕
* 可爬各FB社團內的文章、發文者、按讚數、評論內容
* 英文版本FB(待更新)
* csv檔案輸出，輸出至./FbGroupCrawler/output

格式
```
post:文章內容
poster:發文者
num_good:按讚數量
comment:[評論內容1,評論內容2,評論內容3...]
```

使用方式
* 請先至fb-acoount.txt更改成您的帳密(第一行為FB帳號、第二行為FB密碼)
* 直接執行(如環境已有bs4、selenium、pandas等套件，可省略第一行)
```commandline
pip3 install -r requirements.txt 
python FbGroupCrawler/FbGroupCrawler.py
```
執行後會跳出提示訊息依照提示訊息輸入FB社團網址網址及日期(你想要爬何時以後發布的文章)。

```commandline
Please input the URL you wanna scrape:

Please input the creation date of the group or the date when you wanna stop scraping.
input format is %Y-%m-%d, like 2016-6-12.
input:
```

***
由於使用selenium進行爬蟲，速度偏慢，在評論數偏多的狀況下，也須衡量電腦記憶體是否足夠。
