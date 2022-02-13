# FBGroupCrawler

說明
* 主要以python3.7版本
* chrome版本為98.0.4758.82
* 自動點擊「顯示更多」、「查看先前回覆」、「檢視更多回覆」等隱藏所需抓取內容的按鈕
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
* 直接執行(如環境已有bs4、selenium、pandas等套件，可省略第一行)
```
python setup.py install
python FbGroupCrawler/FbGroupCrawler.py
```
執行後會跳出提示訊息依照提示訊息輸入網址及日期
