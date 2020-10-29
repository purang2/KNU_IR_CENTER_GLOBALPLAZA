import json
from collections import OrderedDict
import sqlite3


def get_school_names():
    global school_names
    school_names = set()
    conn = sqlite3.connect("학부생자료_0611.db")
    cur = conn.cursor()


    semester = ["2015_2", "2016_1", "2016_2", "2017_1", "2017_2", "2018_1", "2018_2", "2019_1", "2019_2", "2020_1"]

    for i in range(0, len(semester)):
        sql = "select distinct 소속학과명 from '" + semester[i] + "'"
        cur.execute(sql)

        rows = cur.fetchall()

        for i in range(0, len(rows)):
            tmp = str(rows[i])
            tmp = tmp[2:-3]
            if tmp != 'None':
                school_names.add(tmp)

    conn.close()

    conn = sqlite3.connect("대학원생자료_0611.db")
    cur = conn.cursor()
    for i in range(0, len(semester)):
        sql = "select distinct 소속학과명 from '" + semester[i] + "'"

        cur.execute(sql)

        rows = cur.fetchall()

        for i in range(0, len(rows)):
            tmp = str(rows[i])
            tmp = tmp[2:-3]
            if tmp != 'None':
                school_names.add(tmp)

    conn.close()


def get_major_types(major):
    global major_types
    major_types = dict()
    conn = sqlite3.connect("계열분류DB.db")

    row = ["first_pro","second_pro","third_pro"]

    for i in range(0,len(row)):
        cur = conn.cursor()
        sql = "select 학과 from '" + row[i] + "'"
        cur.execute(sql)

        name = cur.fetchall()
        cur = conn.cursor()
        sql = "select 계열명 from '" + row[i] + "'"
        cur.execute(sql)
        value = cur.fetchall()

        #print(name)
        #print(value)
        imsy_type=dict()
        for j in range(0, len(name)):
            #print(value[j][0])

            imsy_type[name[j][0]] = value[j][0]
        if i==0:
            major_types= imsy_type
            #print(major_types)
            #print()
        else:
            major_types.update(imsy_type)
            #print(imsy_type)
            #print()
    conn.close()

    if major in major_types:
        if str(major_types[major]).find("예능") > -1 or str(major_types[major]).find("체능")>-1:
            return "art" #설명: html/js파일에서 예체능 계열을 art로 읽고 있어서 art로 받았습니다. -은찬-
        elif str(major_types[major]).find("자연과학") > -1:
            return "science"
        elif str(major_types[major]).find("인문사회") > -1:
            return "social"
        elif str(major_types[major]).find("공학") > -1:
            return "engineering"
        elif str(major_types[major]).find("의학") > -1:
            return "medicine"
    else:
        return 'etc'

def get_bechleor(tablename, schoolname, sex):
    sexcode = "3"
    if sex == "여":
        sexcode = "2"
    elif sex == "남":
        sexcode = "1"

    conn = sqlite3.connect("학부생자료_0611.db")
    cur = conn.cursor()

    if schoolname == "의학과" or schoolname == "전자공학부":
        sql = "select count(*) from '" + tablename + "' where 소속학과명 ='" + schoolname + "' and 졸업연월일 is not 'None' and 성별 = '" + sexcode + "'"
        #        print(sql)
    else:
        sql = "select count(*) from '" + tablename + "' where 소속학과명 LIKE '%" + schoolname + "%' and 졸업연월일 is not 'None' and 성별 = '" + sexcode + "'"

    '''
    if schoolname == "경영학부":
        sql = "select count(*) from '" + tablename + "' where 소속학과명 LIKE'" + "경영학부" + "' and 졸업연월일 is not 'None' and 성별 = '" + sexcode + "'"
    elif schoolname == "지구시스템과학부":
        sql = "select count(*) from '" + tablename + "' where 소속학과명 LIKE'" + "지구시스템과학부" + "' and 졸업연월일 is not 'None' and 성별 = '" + sexcode + "'"
    else:
        sql = "select count(*) from '" + tablename + "' where 소속학과명 ='" + schoolname + "' and 졸업연월일 is not 'None' and 성별 = '" + sexcode + "'"
    '''
    if schoolname=="경영학전공" or schoolname=="회계학전공":
        return 0
    else:
        cur.execute(sql)
        temp = cur.fetchall()
        conn.close()
        return int(str(temp)[2:-3])


def get_master(tablename, schoolname, sex):
    sexcode = "3"
    if sex == "여":
        sexcode = "2"
    elif sex == "남":
        sexcode = "1"

    conn = sqlite3.connect("대학원생자료_0611.db")
    cur = conn.cursor()
    if schoolname == "의학과":
        sql = "select count(*) from '" + tablename + "' where 소속학과명 ='" + schoolname + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '1'"
    else:
        sql = "select count(*) from '" + tablename + "' where 소속학과명 LIKE '%" + schoolname + "%' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '1'"

#    sql = "select count(*) from '" + tablename + "' where 소속학과명 LIKE'" + "schoolname" + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '1'"


    '''
    if schoolname=="경영학부":
        sql = "select count(*) from '" + tablename + "' where 소속학과명 LIKE'" + "경영학부" + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '1'"
    elif schoolname == "지구시스템과학부":
        sql = "select count(*) from '" + tablename + "' where 소속학과명 LIKE'" + "지구시스템과학부" + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '1'"
    else:
        sql = "select count(*) from '" + tablename + "' where 소속학과명 ='" + schoolname + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '1'"
    '''


#    sql = "select count(*) from '" + tablename + "' where 소속학과명 ='" + schoolname + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '1'"

    cur.execute(sql)
    temp = cur.fetchall()
    conn.close()
    return int(str(temp)[2:-3])


def get_phd(tablename, schoolname, sex):
    sexcode = "3"
    if sex == "여":
        sexcode = "2"
    elif sex == "남":
        sexcode = "1"

    conn = sqlite3.connect("대학원생자료_0611.db")
    cur = conn.cursor()

    # sql = "select count(*) from '" + tablename + "' where 소속학과명 ='" + schoolname + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '2'"
    if schoolname == "의학과":
        sql = "select count(*) from '" + tablename + "' where 소속학과명 ='" + schoolname + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '2'"
    else:
        sql = "select count(*) from '" + tablename + "' where 소속학과명 LIKE '%" + schoolname + "%' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '2'"


    '''
    if schoolname=="경영학부":
        sql = "select count(*) from '" + tablename + "' where 소속학과명 LIKE'" + "경영학부" + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '2'"
    elif schoolname == "지구시스템과학부":
        sql = "select count(*) from '" + tablename + "' where 소속학과명 LIKE'" + "지구시스템과학부" + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '2'"
    else:
        sql = "select count(*) from '" + tablename + "' where 소속학과명 ='" + schoolname + "' and 학위취득일 is not 'None' and 성별 = '" + sexcode + "' and 학위종류 = '2'"
    '''

    cur.execute(sql)
    temp = cur.fetchall()
    conn.close()
    return int(str(temp)[2:-3])



def change_school_name(schoollist):
    for i in range(0, len(schoollist)):
        temp = str(schoollist[i])
        if temp == '센서 및 디스플레이공학과 학과간 협동과정':
            schoollist[i] = '센서 및 디스플레이공학과'
            continue
        temp = temp.replace("(", " ")
        temp_list = temp.split(" ")
        schoollist[i] = temp_list[0]
        for k in range(0, len(temp_list)):
            if temp_list[k].find("학과") != -1 or temp_list[k].find("학부") != -1:
                schoollist[i] = temp_list[k]
                break

    return list(set(schoollist))


def create_Json_grade_Top10(file_name):
    global school_names
    get_school_names()
    school_name_list = list(school_names)
    school_name_list = change_school_name(school_name_list)

    #To see every major
    #list.sort(school_name_list)
    #print(school_name_list)

    jsonfile = file_name + ".json"
    json_list = list()

    for year in range(2016, 2021):
        print(year)
        json_list = list()

        for i in range(0, len(school_name_list)):

            #if school_name_list[i].find("학과") == -1 and school_name_list[i].find("학부") == -1 and school_name_list[i].find("예과") == -1 and school_name_list[i].find("교육과") == -1:
                #print(school_name_list[i])
             #   continue

            male_bech = 0
            female_bech = 0
            male_master = 0
            female_master = 0
            male_phd = 0
            female_phd = 0
            major_type=''
            sn=school_name_list[i]


            tablename = str(year) + "_1"
            if tablename != '2015_1':
                male_bech = get_bechleor(tablename, school_name_list[i], "남")
                female_bech = get_bechleor(tablename, school_name_list[i], "여")
                male_master = get_master(tablename, school_name_list[i], "남")
                female_master = get_master(tablename, school_name_list[i], "여")
                male_phd = get_phd(tablename, school_name_list[i], "남")
                female_phd = get_phd(tablename, school_name_list[i], "여")

            tablename = str(year-1) + "_2"
            if tablename != '2020_2':
                male_bech += get_bechleor(tablename, school_name_list[i], "남")
                female_bech += get_bechleor(tablename, school_name_list[i], "여")
                male_master += get_master(tablename, school_name_list[i], "남")
                female_master += get_master(tablename, school_name_list[i], "여")
                male_phd += get_phd(tablename, school_name_list[i], "남")
                female_phd += get_phd(tablename, school_name_list[i], "여")

            # print(school_name_list[i], "::", year, ":::", male_bech+ female_bech)

            temp_dictonary = {
                              "major": school_name_list[i],
                              "college": get_major_types(school_name_list[i]),
                              "bachelor_all": int(male_bech)+int(female_bech),
                              "bachelor_man": int(male_bech),
                              "bachelor_woman": int(female_bech),
                              "master_all": int(male_master)+int(female_master),
                              "master_man": int(male_master),
                              "master_woman": int(female_master),
                              "phd_all": int(male_phd)+int(female_phd),
                              "phd_man": int(male_phd),
                              "phd_woman": int(female_phd)}
            if int(male_bech)+int(female_bech)>=10 or int(male_master)+int(female_master)>=10 or int(male_phd)+int(female_phd)>=10:
                json_list.append(temp_dictonary)

        with open('4_'+str(year)+'_degree.json', 'w', encoding='UTF-8') as make_file:
            json.dump(json_list, make_file, indent="\t", ensure_ascii=False)


create_Json_grade_Top10('s')

