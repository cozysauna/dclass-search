import requests
from bs4 import BeautifulSoup
import traceback
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import chromedriver_binary
from time import sleep

# PlaneData

###
eng_faculty_name = 'Letters'
###

open_f = open(f'syllabus_plane_data/{eng_faculty_name}/2021_2.txt')
write_f = open(f'final_data/{eng_faculty_name}.txt', 'a')
# FACULTY = 'グローバル地域文化学部'
# FACULTY = 'グローバル・コミュニケーション学部'
# FACULTY = '心理学部'
# FACULTY = 'スポーツ健康科学部'
# FACULTY = '生命医科学部'
# FACULTY = '理工学部'
# FACULTY = '文化情報学部'
# FACULTY = '政策学部'
# FACULTY = '商学部'
# FACULTY = '経済学部'
# FACULTY = '法学部'
# FACULTY = '社会学部'
FACULTY = '文学部'
# FACULTY = '神学部'
# FACULTY = '一般教養'
YEAR = '2021'
data = open_f.read()
soup = BeautifulSoup(data, 'html.parser')
tables = soup.select("table")[2].select("tr")[2:]


def mold_txt(txt):
    if len(txt.select('a')) >= 1: 
        txt = txt.select_one('a')
        if txt.find('br') != None:
            txt.br.replace_with(' ')
            txt = txt.text.split(' ')[0][1:]
        else:
            txt = txt.text[1:]
        idx = txt.find('(')
        if idx != -1:
            txt = txt[:idx]
        idx = txt.find('（')
        if idx != -1:
            txt = txt[:idx]
        txt = [txt]
    else:
        new_txt = str(txt.string).split('\n')
        if new_txt == ['None']:
            new_txt = [e.text for e in txt]
        txt = new_txt


    #要素解除
    remove_elems = [' ', '\t', '\xa0', '\n']
    for remove_elem in remove_elems:
        txt = [tx.replace(remove_elem, '') for tx in txt]

    #空白置換
    txt = [tx.replace('\u3000', ' ') for tx in txt]
    txt = [tx for tx in txt if tx]

    if len(txt) >= 1 and '曜日' in txt[0]: 
        txt[0] = txt[0].split('曜日')

    if len(txt) >= 1 and '集中' in txt[0]:
        txt = [[['集中講義'], '0']]

    if len(txt) >= 1 and 'インターネット' in txt[0]:
        txt = [[['インターネット'], '0']]


    return txt

def dict_to_str(dic):
    return '@'.join(str(v) for v in dic.values())

def str_to_dict(st):
    columns =  [
        'class_name',
        'grade_distribution',
        'average_evaluation',
        'a_ratio_history',
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
        'credit'
    ]
    st = st.split('@')
    ret = dict()
    list_columns = ['grade_distribution', 'a_ratio_history', 'textbook', 'teacher']
    for i, column in enumerate(columns):
        if column in list_columns:
            ret[column] = eval(st[i])
        else:
            ret[column] = st[i]
    return ret

def get_syllabus_link(code, year):
    if '-' not in code: code += '-000'
    faculty_number = code[1:5]
    url = 'https://syllabus.doshisha.ac.jp/html/'+ year +'/'+ faculty_number + '/' + code.replace('-', '') + '.html'
    return url

def get_syllabus_data(url):
    term = '春'
    class_form = '対面授業'
    test_ratio = 0
    report_ratio = 0
    participation_ratio = 0

    try:
        data = requests.get(url).text
        soup = BeautifulSoup(data, 'html.parser')
        head = soup.find_all('td', class_='show__content-in')[0].select("tbody")
        grades = soup.find('table', class_='show__grades').select('td')
        txt = []
        for grade in grades:
            grade = [elem for elem in grade.text.split('\n') if elem]
            grade = [elem.replace('\xa0', '') for elem in grade][0]
            txt.append(grade)

        for i, tx in enumerate(txt):
            if '%' in tx:
                try:
                    percent = int(tx[:-1])
                except:
                    percent = 0
                if i == 0: continue
                if 'テスト' in txt[i-1] or 'Test' in txt[i-1]:
                    test_ratio += percent
                elif 'レポート' in txt[i-1] or 'Report' in txt[i-1]:
                    report_ratio += percent
                elif '平常点' in txt[i-1] or 'Participation' in txt[i-1]:
                    participation_ratio += percent
                else: pass
    
        for elem in head:
            txt = elem.text.split('\n')
            for tx in txt:
                if '秋学期' in tx:
                    term = '秋'
                if 'ネット' in tx:
                    class_form = 'オンライン授業'


        text_book_flag = False
        textbook = []
        for elem in soup.select_one('body'):
            txt = elem.text 
            for tx in txt.split('\n'):
                for t in tx.split('\n'):
                    if not t: continue
                    if '＜参考文献/Reference Book＞' in t or '＜備考/Remarks＞' in t: text_book_flag = False 
                    if text_book_flag: 
                        for e in t.split('\n'):
                            e = e.replace('\xa0', '')
                            if not e: continue 
                            if '『' not in e: continue
                            textbook.append(e)
                    if '＜テキスト/Textbook＞' in t: text_book_flag = True 

        textbook = [book for book in textbook if '使用しない' not in book]
        if textbook == []: textbook = None

        return term, class_form, test_ratio, report_ratio, participation_ratio, textbook
    except:
        return False
    
def mold_table(table, year, faculty):
    table = [mold_txt(txt) for txt in table]
    try:
        class_data = {
            'class_name': table[2][0].translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})),
            # ratio a, b, c, d, f, o
            'grade_distribution':[-1, -1, -1, -1, -1, -1],
            'average_evaluation': -1,
            'a_ratio_history': [-1, -1, -1],
            'term': None, # シラバス
            'year': year,
            'place': table[4][0],
            'class_form': None, # シラバス
            'day': table[6][0][0][0],
            'time': table[6][0][1][0],
            'textbook': None, # シラバス
            'code': table[0][0],
            'faculty ': faculty,
            'teacher': table[3],
            'syllabus_link': get_syllabus_link(table[0][0], YEAR), # シラバス
            'test_ratio': None, # シラバス
            'report_ratio': None, # シラバス
            'participation_ratio': None, # シラバス
            # 'num_student': None, # シラバス
            'credit': table[5][0][0]
        }
    except:
        return False
    try:
        term, class_form, test_ratio, report_ratio, participation_ratio, textbook = get_syllabus_data(class_data['syllabus_link'])
    except: 
        return False
    class_data['term'] = term 
    class_data['class_form'] = class_form
    class_data['test_ratio'] = test_ratio
    class_data['report_ratio'] = report_ratio
    class_data['participation_ratio'] = participation_ratio
    class_data['textbook'] = textbook
    return class_data

# 成績評価(得点分布検索)
URL = 'https://duet.doshisha.ac.jp/kokai/html/fi/fi020/FI02001G.html'
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

#########################################
DATA_NUM = 0
log = DATA_NUM
# END = 200
for table in tables[DATA_NUM:]:
    log += 1
    table = table.select("td")
    class_data = mold_table(table, year=YEAR, faculty=FACULTY)
    if not class_data:
        print(f'Disable_Data{log}')
        continue
    code = class_data['code']
    print(log)

    for i in range(2, -1, -1):
        driver.get(URL)
        sleep(0.3)

        #年度
        dropdown = driver.find_element(by=By.ID, value='form1:kaikoNendolist')
        select = Select(dropdown)
        select.select_by_value(str(2020-i))

        # code
        if '-' in code:
            code_forward = code[:code.index('-')]
            code_back = code[code.index('-')+1:]
            code_f = driver.find_element(by=By.NAME, value='form1:_id90')
            code_f.send_keys(code_forward)


            code_b = driver.find_element(by=By.NAME, value='form1:_id92')
            code_b.send_keys(code_back)
        else:
            code_forward = code
            code_f = driver.find_element(by=By.NAME, value='form1:_id90')
            code_f.send_keys(code_forward)

        #検索ボタン
        search_btn = driver.find_element(by=By.ID, value='form1:enterDodoZikko')
        search_btn.click()
        sleep(0.2)


        txts = driver.find_element(by=By.CLASS_NAME, value="sortable")
        txts = txts.find_element(by=By.CSS_SELECTOR, value="tbody")
        txts_by_tr = txts.find_elements(by=By.CSS_SELECTOR, value="tr")[::2]

        if len(txts_by_tr) == 0: continue
        txt = txts_by_tr[0]
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
        a_ratio = a_ratio if a_ratio else -1
        b_ratio = b_ratio if b_ratio else -1 
        c_ratio = c_ratio if c_ratio else -1
        d_ratio = d_ratio if d_ratio else -1
        f_ratio = f_ratio if f_ratio else -1
        o_ratio = o_ratio if o_ratio else -1

        if i == 0:
            class_data['grade_distribution'] = [a_ratio, b_ratio, c_ratio, d_ratio, f_ratio, o_ratio]
            class_data['average_evaluation'] = txts_by_td[11].get_attribute('innerHTML')
            if not class_data['average_evaluation']: class_data['average_evaluation'] = -1

        class_data['a_ratio_history'][i] = a_ratio

    class_data = dict_to_str(class_data)
    write_f.write(class_data + '\n')