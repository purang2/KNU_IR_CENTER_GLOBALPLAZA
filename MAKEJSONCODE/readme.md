

## readme!!


코드 함수들 모음

---


### 학과,성별 별 학부생,대학원생의 수를 카운팅하는 함수 

```python


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



```



### 데이터를 열고 연도별 인원수 상위 10개 학과만 추출하는 함수 코드 

```python


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

        json_list=sorted(json_list, key=(lambda x: x['Male']), reverse=True)
        json_list=json_list[0:11]
        #print(json_list)

        json_list2 = sorted(json_list2, key=(lambda x: x['Male']), reverse=True)
        json_list2 = json_list2[0:11]
        #print(json_list2)
        json_dict ={
            "bachelor":json_list,
            "phdmaster":json_list2
        }
    with open('result_summary_top_graduate_male_'+str(n)+'.json', 'w', encoding='UTF-8') as make_file:
        json.dump(json_dict, make_file, indent="\t", ensure_ascii=False)


```
