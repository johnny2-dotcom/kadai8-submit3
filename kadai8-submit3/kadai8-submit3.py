from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
import time 
import pandas as pd
from datetime import  datetime
from webdriver_manager.chrome import ChromeDriverManager
import threading


def find_table_target_word(th_elms,td_elms,target:str):
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text



def calc_total_pages_num(search_keyword):

    url = 'https://tenshoku.mynavi.jp/'

    driver = Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(2)

    try:
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(3)
    except:
        pass

    driver.find_element_by_class_name('topSearch__text').send_keys(search_keyword)
    driver.find_element_by_class_name('topSearch__button').click()

    num = int(driver.find_element_by_css_selector('body > div.wrapper > div:nth-child(5) > div.result > div > p.result__num > em').text)
    return -(-num//50)

    driver.quit()



def search(search_keyword,i):

    page_url = f'https://tenshoku.mynavi.jp/list/kw{search_keyword}/pg{i}/?jobsearchType=14&searchType=18'

    driver = Chrome(ChromeDriverManager().install())
    driver.get(page_url)
    time.sleep(2)

    try:
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(3)
    except:
        pass

    exp_name_list = []
    exp_copy_list = []
    exp_status_list = []
    exp_first_year_fee_list = []
    
    name_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__name")
    copy_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__copy")
    status_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .labelEmploymentStatus")
    table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition") # テーブル全体を取得

    for name,copy,status,table in zip(name_list,copy_list,status_list,table_list):
        exp_name_list.append(name.text)
        exp_copy_list.append(copy.text)
        exp_status_list.append(status.text)

        first_year_fee = find_table_target_word(table.find_elements_by_tag_name("th"),table.find_elements_by_tag_name("td"), "初年度年収")
        exp_first_year_fee_list.append(first_year_fee)
    
    driver.quit()

    EXP_CSV_PATH = 'exp_list_{search_keyword}_{datetime}.csv'

    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df = pd.DataFrame({"企業名":exp_name_list,"キャッチコピー":exp_copy_list,"ステータス":exp_status_list,"初年度年収":exp_first_year_fee_list})
    df.to_csv(EXP_CSV_PATH.format(search_keyword=search_keyword,datetime=now), encoding="utf-8-sig")




search_keyword = 'プログラマー'

total_pages_num = calc_total_pages_num(search_keyword)

t_list = []
for  i in range(1,total_pages_num+1):
     t = threading.Thread(target=search, args=[search_keyword, i])
     t_list.append(t)

for t in t_list:
    t.start()
    
for t in t_list:
    t.join()