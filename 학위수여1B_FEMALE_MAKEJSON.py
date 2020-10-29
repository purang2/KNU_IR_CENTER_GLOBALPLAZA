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
            return "예체능"
        elif str(major_types[major]).find("자연과학") > -1:
            return "자연과학"
        elif str(major_types[major]).find("인문사회") > -1:
            return "인문사회"
        elif str(major_types[major]).find("공학") > -1:
            return "공학"
        elif str(major_types[major]).find("의학") > -1:
            return "의학"
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

    if schoolname == "의학과":
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


def create_Json_grade_Top10(n):
    global school_names
    get_school_names()
    school_name_list = list(school_names)
    school_name_list = change_school_name(school_name_list)

    #To see every major
    #list.sort(school_name_list)
    #print(school_name_list)

    json_list = list()
    json_list2 = list()

    for year in range(n,n+1):
        print(year)
        for i in range(0, len(school_name_list)):


            male_bech = 0
            female_bech = 0
            male_master = 0
            female_master = 0
            male_phd = 0
            female_phd = 0
            major_type=''
            sn=school_name_list[i]

            if sn == '에너지공학부':
                continue

            tablename = str(year) + "_1"
            if tablename != '2015_1':
                male_bech += get_bechleor(tablename, school_name_list[i], "남")
                female_bech += get_bechleor(tablename, school_name_list[i], "여")
                male_master+= get_master(tablename, school_name_list[i], "남")
                female_master += get_master(tablename, school_name_list[i], "여")
                male_phd += get_phd(tablename, school_name_list[i], "남")
                female_phd += get_phd(tablename, school_name_list[i], "여")

            tablename = str(year-1) + "_2"
            if tablename != '2020_2':
                male_bech += get_bechleor(tablename, school_name_list[i], "남")
                female_bech += get_bechleor(tablename, school_name_list[i], "여")
                male_master += get_master(tablename, school_name_list[i], "남")
                female_master += get_master(tablename, school_name_list[i], "여")
                male_phd += get_phd(tablename, school_name_list[i], "남")
                female_phd += get_phd(tablename, school_name_list[i], "여")

            # print(school_name_list[i], "::", year, ":::", male_bech+ female_bech)

            ref_dict={"bachelor","phdmaster"};
            temp_dictonary1 = {
                              "major": school_name_list[i],
                              "All": int(male_bech) +int(female_bech),
                              "Male": int(male_bech),
                              "Female": int(female_bech),
                              }

            json_list.append(temp_dictonary1)
            temp_dictonary2 = {
                "major": school_name_list[i],
                "All": int(male_master) + int(female_master)+ int(male_phd)+ int(female_phd),
                "Male": int(male_master)+int(male_phd),
                "Female": int(female_master)+int(female_phd),
            }
            json_list2.append(temp_dictonary2)

        json_list=sorted(json_list, key=(lambda x: x['Female']), reverse=True)
        json_list=json_list[0:11]
        #print(json_list)

        json_list2 = sorted(json_list2, key=(lambda x: x['Female']), reverse=True)
        json_list2 = json_list2[0:11]
        #print(json_list2)
        json_dict ={
            "bachelor":json_list,
            "phdmaster":json_list2
        }
    with open('result_summary_top_graduate_female_'+str(n)+'.json', 'w', encoding='UTF-8') as make_file:
        json.dump(json_dict, make_file, indent="\t", ensure_ascii=False)



for year in range(2016,2021):
    create_Json_grade_Top10(year)

# OUTPUT 타입 "result_summary_top_graduate_201n.json

