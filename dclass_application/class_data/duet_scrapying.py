import traceback
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import chromedriver_binary
from time import sleep

# 成績評価(得点分布検索)
URL = 'https://duet.doshisha.ac.jp/kokai/html/fi/fi020/FI02001G.html'


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)


data_columns = [
    'class_name',
    'a_ratio',
    'b_ratio',
    'c_ratio',
    'd_ratio',
    'f_ratio',
    'o_ratio',
    'average_evaluation',
    'term',
    'year',
    'place',
    'class_form',
    'day',
    'time',
    'textbook',
    'code',
    'faculty',
    'teacher',
    'syllabus_link',
    'test_ratio',
    'report_ratio',
    'participation_ratio',
]


data = {
    'class_name':'',
    'grade_distribution':{
        'a_ratio': 0, 
        'b_ratio': 0, 
        'c_ratio': 0, 
        'd_ratio': 0, 
        'f_ratio': 0, 
        'o_ratio': 0, 
    },
    'average_evaluation': 0,
    'term': '',
    'year': '',
    'place': '',
    'class_form': '', 
    'day': '',
    'time': '',
    'textbook': '',
    'code': '',
    'faculty ': '',
    'teacher': [],
    'syllabus_link': '',
    'test_ratio': 0,
    'report_ratio': 0,
    'participation_ratio': 0,
}

FACULTY = 'General_Education'
YEAR = '2020'
faculty_num = {
    '神学部': '11001', # Theology
    '文学部': '11002', # Letters
    '法学部': '11003', # Law
    '経済学部': '11004',# Economics
    '商学部': '11005', # Commerce
    '政策学部': '11007', # Policy
    '文化情報学部': '11008',# Culture_Information_Science
    '社会学部': '11009', # Social
    '生命医科学部': '11014', # Life_Medical_Science
    'スポーツ健康科学部': '11015',# Health_Sports_Science
    '理工学部': '11016', # Science_Enginnering
    '心理学部': '11017', # Psychology
    'グローバル・コミュニケーション学部': '11019', # Global_Communication
    '国際教養インスティチュート学部': '11020', # International_Institute
    'グローバル地域文化学部': '11022', # Global_Regional
    '全学共通教養教育科目（外国語教育科目・保健体育科目以外）': '11060', # General_Education
    '全学共通教養教育科目（保健体育科目）': '11061', # General_Education(PE)
    '全学共通教養教育科目（外国語教育科目）': '11065', # General_Education(Language)
    '日本語・日本文化教育科目': '11090'
}

FACURUTY_NUM = '11060'


def scrape(year, faculty):
    ret_data = []
    txts = driver.find_element(by=By.CLASS_NAME, value="sortable")
    txts = txts.find_element(by=By.CSS_SELECTOR, value="tbody")
    txts_by_tr = txts.find_elements(by=By.CSS_SELECTOR, value="tr")[::2]
    for txt in txts_by_tr:
        txts_by_td = txt.find_elements(by=By.CSS_SELECTOR, value="td")
        teacher = txts_by_td[3].get_attribute('innerHTML').split('\n')
        teacher = [elm.strip(' ').replace('\u3000', ' ')for elm in teacher]
        teacher = [elm for elm in teacher if elm and elm != '<span><br></span>']

        a_ratio = txts_by_td[5].get_attribute('innerHTML')
        b_ratio = txts_by_td[6].get_attribute('innerHTML')
        c_ratio = txts_by_td[7].get_attribute('innerHTML')
        d_ratio = txts_by_td[8].get_attribute('innerHTML')
        f_ratio = txts_by_td[9].get_attribute('innerHTML')
        o_ratio = txts_by_td[10].get_attribute('innerHTML')
        a_ratio = a_ratio if a_ratio else None
        b_ratio = b_ratio if b_ratio else None
        c_ratio = c_ratio if c_ratio else None
        d_ratio = d_ratio if d_ratio else None
        f_ratio = f_ratio if f_ratio else None
        o_ratio = o_ratio if o_ratio else None


        class_data = {
            'class_name': txts_by_td[2].get_attribute('innerHTML'),
            # ratio a, b, c, d, f, o
            'grade_distribution':[
                a_ratio, b_ratio, c_ratio, d_ratio, f_ratio, o_ratio
            ],
            'average_evaluation': txts_by_td[11].get_attribute('innerHTML'),
            'a_ratio_history': [None, None, None],
            'term': txts_by_td[1].get_attribute('innerHTML'),
            'year': year,
            'place': None,
            'class_form': None, 
            'day': None,
            'time': None,
            'textbook': None,
            'code': txts_by_td[0].get_attribute('innerHTML'),
            'faculty ': faculty,
            'teacher': teacher,
            'syllabus_link': None,
            'test_ratio': None,
            'report_ratio': None,
            'participation_ratio': None,
            # 'num_student': txts_by_td[4].get_attribute('innerHTML'),
            'credit': None
        }
        ret_data.append(class_data)
    return ret_data

try:
    # file_name = YEAR + FACULTY + '.json'
    # open_file = open(file_name, 'w')
    driver.get(URL)
    sleep(1)

    #年度
    dropdown = driver.find_element(by=By.ID, value='form1:kaikoNendolist')
    select = Select(dropdown)
    select.select_by_value(YEAR)

    #学部
    dropdown = driver.find_element(by=By.NAME, value='form1:_id86')
    select = Select(dropdown)
    select.select_by_value(FACURUTY_NUM)

    #検索ボタン
    # search_btn = driver.find_element_by_id('')
    search_btn = driver.find_element(by=By.ID, value='form1:enterDodoZikko')
    search_btn.click()
    sleep(0.2)

    #データ数取得
    data_num = int(driver.find_element(by=By.CLASS_NAME, value="pagectl-title").text.split()[-1][1:-1])
    # page_num = (data_num + 50 -1) // 50 
    page_num = 1
    sleep(2)
    now_page = 1
    while now_page <= page_num:
        data = scrape(year=YEAR, faculty=FACULTY)
        for one_data in data:
            print(one_data)
            # pass
            # open_file.write(dumps(one_data)+'\n')

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(0.3)
        now_page += 1
        nx = driver.find_element(by=By.LINK_TEXT, value=str(now_page))
        nx.click()

    sleep(3)


finally:
    driver.quit()