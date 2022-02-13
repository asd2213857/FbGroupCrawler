import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import os


def time_dealing(timetext):
    struct_time = time.localtime(int(time.time()))
    nowYear = time.strftime("%Y", struct_time)  # 將時間轉換成想要的字串
    nowmonth = time.strftime("%m", struct_time)
    nowday = time.strftime("%d", struct_time)

    if '昨天' in timetext:
        timetext = nowYear + '-' + nowmonth + '-' + str(int(nowday) - 1)

    elif '小時' not in timetext and '分' not in timetext and '天' not in timetext:
        if '年' not in timetext:
            timetext = nowYear + '-' + timetext
        else:
            timetext = timetext.replace('年', '-')

        timetext = timetext.replace('月', '-')
        timetext = timetext.replace('日', '')

        if '午' in timetext:
            timetext = timetext[:timetext.index('午') - 1]
    else:
        timetext = time.strftime("%Y-%m-%d", struct_time)

    return timetext


def click_all(issue, driver, elements):
    # print(issue," len:",len(elements))
    if len(elements) > 0:
        count = 0
        for i in elements:
            action = ActionChains(driver)
            try:
                action.move_to_element(i).click().perform()
                # 滑鼠移動點擊
                count += 1
            except:
                try:
                    # try js 方式點擊
                    driver.execute_script("arguments[0].click();", i)
                    count += 1
                except:
                    continue
            time.sleep(2)
            # 可防止滑鼠誤擊頭像或圖片
        if len(elements) - count > 0:
            print(issue + ' issue:', len(elements) - count)
        time.sleep(1)
    else:
        pass


def click_seemores(driver):
    seemores = driver.find_elements(By.XPATH,
                                    "//div[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p' and contains(text(),'顯示更多')]")
    click_all('click_seemores', driver, seemores)


def click_comments(driver):
    comments = driver.find_elements(By.XPATH,
                                    "//div[@class='oajrlxb2 g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb n00je7tq arfg74bv qs9ysxi8 k77z8yql pq6dq46d btwxx1t3 abiwlrkh lzcic4wl bp9cbjyn m9osqain buofh1pr g5gj957u p8fzw8mz gpro0wi8']")
    click_all('comments', driver, comments)


def click_more_comments(driver):
    more_comments = driver.find_elements(By.XPATH,
                                         "//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v lrazzd5p m9osqain' and contains(text(),'回覆')]")
    click_all('more_comment', driver, more_comments)


def getBack(driver, URL):
    if driver.current_url != URL:
        # print('redirected!!!')
        driver.back()
        # print('got back!!!')


def time_translate(timetext):
    struct_time = time.strptime(timetext, "%Y-%m-%d")
    time_stamp = int(time.mktime(struct_time))  # 轉成時間戳
    return time_stamp


def ouput_file(data):
    if not os.path.isdir("./output"):
        os.makedirs("./output")
    df = pd.DataFrame(data=data)
    df.to_csv('./output/output.csv', index=False, encoding='utf-8-sig')


def scraping(driver, cards, poster, post, posttime, num_good, comment):
    for i in cards:
        ####發文者####
        name = i.find("h2").text
        poster.append(name)
        #############

        ####發文時間####
        timeclass = "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"
        timepoint = time_dealing(i.find(class_=timeclass).text)
        posttime.append(timepoint)
        ###############

        ####貼文####
        # 不明原因i.find(attrs={"data-ad-comet-preview": "message"}).text錯誤

        tclass = "dati1w0a ihqw7lf3 hv4rvrfc ecm0bbzt"
        normal_texts = i.find_all(class_=tclass)
        clicked_texts = i.find_all(attrs={"data-ad-comet-preview": "message"})

        if clicked_texts != []:
            posttext = ''.join([x.text for x in clicked_texts])
        elif normal_texts != []:
            posttext = ''.join([x.text for x in normal_texts])
        else:
            posttext = '特殊文章'

        post.append(posttext)
        ###########

        ####按讚數####
        # 考慮按讚數為零
        try:
            n_good = i.find(class_='bzsjyuwj ni8dbmo4 stjgntxs ltmttdrg gjzvkazv').text

        except:
            n_good = 0
        num_good.append(n_good)
        #############

        ####評論####
        # c_class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8"
        commenttext = i.find_all(class_="ecm0bbzt e5nlhep0 a8c37x1j")
        if commenttext == []:
            comment.append([])

        else:
            comment.append([x.text for x in commenttext])
            ###########

    return poster, post, posttime, num_good, comment


def crawler(URL, Group_creation_date):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless') #不顯示瀏覽器
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不顯示圖片
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(executable_path="../chromedriver", options=chrome_options)

    # 是否需要登入
    with open('../fb-account.txt') as file:
        EMAIL = file.readline()
        PASSWORD = file.readline()
    driver.get("http://facebook.com")
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)
    email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
    email_field.send_keys(EMAIL)
    pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
    pass_field.send_keys(PASSWORD)
    pass_field.send_keys(Keys.RETURN)
    time.sleep(5)

    driver.get(URL)
    time.sleep(5)

    poster = []
    posttime = []
    post = []
    num_good = []
    comment = []
    count = 1

    #####先爬一次以啟動迴圈#####

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    for i in range(3):
        click_comments(driver)
        getBack(driver, URL)

    for i in range(3):
        click_more_comments(driver)
        getBack(driver, URL)

    click_seemores(driver)
    getBack(driver, URL)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "lxml")
    cards = soup.find_all(class_="du4w35lb k4urcfbm l9j0dhe7 sjgh65i0")[0:]
    poster, post, posttime, num_good, comment = scraping(driver, cards, poster, post, posttime, num_good, comment)
    startpoint = len(post)
    ##########################

    # 爬至社團創始日期
    while time_translate(posttime[-1]) >= Group_creation_date:

        print('count:', count)

        ###頁面滾動###
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        #############

        ####點擊####
        for i in range(3):
            click_comments(driver)
            getBack(driver, URL)
        time.sleep(5)

        for i in range(3):
            click_more_comments(driver)
            getBack(driver, URL)
        time.sleep(5)

        click_seemores(driver)
        getBack(driver, URL)
        time.sleep(5)
        ############

        ####載入HTML####
        soup = BeautifulSoup(driver.page_source, "lxml")
        cards = soup.find_all(class_="du4w35lb k4urcfbm l9j0dhe7 sjgh65i0")[startpoint:]
        ###########

        ####爬蟲####
        poster, post, posttime, num_good, comment = scraping(driver, cards, poster, post, posttime, num_good, comment)
        ###########

        ####輸出####
        ouput_file({'poster': poster, 'post': post, 'time': posttime, 'num_good': num_good, 'comment': comment})
        ###########

        startpoint = len(post)
        print('post_len:', startpoint)

        time.sleep(5)
        count += 1
    driver.quit()

if __name__ == '__main__':
    URL = str(input('Please input the URL you wanna scrape:'))
    # FB社團網址
    # https://www.facebook.com/groups/1260448967306807
    Group_creation_date =str(input('Please input the creation date of the group or the date when you wanna stop scraping. \n input format is %Y-%m-%d, like 2016-6-12. \n input:'))
    Group_creation_date = time_translate(Group_creation_date)
    # FB社團創始日期 OR 你想爬到的日期
    crawler(URL, Group_creation_date)