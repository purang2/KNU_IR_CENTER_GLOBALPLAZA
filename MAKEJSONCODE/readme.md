

## readme!!


코드 예시

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
