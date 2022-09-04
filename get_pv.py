from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


def GetPV(email,password,select_column_dict):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://nao-consulting.net/wp-admin/edit.php')
    driver.find_element(By.ID, 'user_login').send_keys(email)
    driver.find_element(By.ID, 'user_pass').send_keys(password)
    driver.find_element(By.ID, 'wp-submit').click()    
    
    #setting display options
    sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/ul/li[2]/a').send_keys(Keys.ENTER)
    get_num = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/div[1]/div[3]/span[1]').text
    get_num = int(get_num.replace('個の項目',''))
    driver.find_element(By.ID, 'show-settings-link').click()
    for column_id, true_or_false in select_column_dict.items():
        now_true_or_false = driver.find_element(By.ID, column_id).is_selected()
        if str(now_true_or_false) == str(true_or_false):
            pass
        else:
            driver.find_element(By.ID, column_id).click()

    driver.find_element(By.ID,'edit_post_per_page').clear()
    driver.find_element(By.ID,'edit_post_per_page').send_keys(get_num)
    if driver.find_element(By.ID,'list-view-mode').is_selected() == True:
        pass
    else:
        driver.find_element(By.ID,'list-view-mode').click()
    if driver.find_element(By.ID,'excerpt-view-mode').is_selected() == True:
        driver.find_element(By.ID,'excerpt-view-mode').click()
    else:
        pass
    driver.find_element(By.ID,'screen-options-apply').click()
    
    #getting data
    title_list = []
    author_list = []
    category_list = []
    tags_list = []
    date_list = []
    views_list = []
    post_id_list = []
    word_count_list = []
    thumbnail_list = []
    for i in range(get_num):
            i += 1
            title = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{i}]/td[1]/strong/a').text
            title_list.append(title)
    for get_column, true_or_false in select_column_dict.items():
        #その他の項目は選択
        if true_or_false == 'True':
            if get_column == 'author-hide':
                for i in range(get_num):
                    i += 1
                    author_list.append(driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{i}]/td[2]/a').text)

            if get_column == 'categories-hide':
                for i in range(get_num):
                    i += 1
                    category_list.append(driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{i}]/td[3]/a').text)
            if get_column == 'tags-hide':
                for i in range(get_num):
                    i += 1
                    tags_list.append(driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{i}]/td[4]/a').text)
            if get_column == 'date-hide':
                for i in range(get_num):
                    i += 1
                    date = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{i}]/td[6]').text
                    date = date.split()
                    date_list.append(date[1])
            if get_column == 'views-hide':
                for i in range(get_num):
                    i += 1
                    views = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{i}]/td[7]').text
                    views = views.replace(' ビュー','')
                    views_list.append(views)
            if get_column == 'post-id-hide':
                for i in range(get_num):
                    i += 1
                    post_id_list.append(driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{i}]/td[8]').text)
            if get_column == 'word-count-hide':
                for i in range(get_num):
                    i += 1
                    word_count_list.append(driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{i}]/td[9]/div/div[2]/span[2]').text)
            if get_column == 'thumbnail-hide':
                for i in range(get_num):
                    i += 1
                    thumbnail_list.append(driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{i}]/td[11]/img').get_attribute('src'))
        else:
            pass

    driver.quit()
    return title_list,author_list,category_list,tags_list,date_list,views_list,post_id_list,word_count_list,thumbnail_list