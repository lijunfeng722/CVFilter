# -*- coding: utf-8 -*-

import re
from cv.Colleage import CollegeUtils
from datetime import datetime


def get_year(content):
    return int(content[:4])


# 筛选民办学学校
def minban(data):
    data['民办'] = 0
    pattern1 = "[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{4}-[0-9]{2}-[0-9]{2}\s[^\d]+?\s"  # 2005-09-01 2009-07-01 青岛理工大学
    pattern2 = "[0-9]{4}-[0-9]{2}-[0-9]{2}\s1\s[^\d]+?\s"  # 2008-08-01 1 青岛理工大学 机械设计制造及其自动化  1：表示至今
    pattern3 = "[0-9]{4}-[0-9]{2}-[0-9]{2}\s至今\s[^\d]+?\s"  # 2008-08-01 至今 青岛理工大学 机械设计制造及其自动化
    re1 = re.compile(pattern1)
    re2 = re.compile(pattern2)
    re3 = re.compile(pattern3)
    cu = CollegeUtils()
    for x in range(len(data['姓名'])):
        line = data['教育经历'].iloc[x]
        print(line, x)
        college = re2.search(line)
        if college is not None:  # 2008-08-01 1 青岛理工大学 机械设计制造及其自动化  1：表示至今
            college = college.group().strip()[13:]
            college_nature = cu.getCollege_nature(college)
        else:
            # 2008-08-01 至今 青岛理工大学 机械设计制造及其自动化
            college = re3.search(line)
            if college is not None:
                college = college.group().strip()[14:]
                college_nature = cu.getCollege_nature(college)
            else:
                # 2005-09-01 2009-07-01 青岛理工大学
                college = re1.search(line)
                if college is not None:
                    college = college.group().strip()[22:]
                    college_nature = cu.getCollege_nature(college)
                else:
                    college_nature = "error"
        print(college)

        if college_nature.find("民办") >= 0 or college_nature == "error":
            data['民办'].iloc[x] = 1
            print("民办", data['姓名'].iloc[x], college)
            continue
    cu.close()

    result = data[data['民办'] != 0]
    print("minban result", result)
    return result


def meetDuration(data, durationNeed):
    print(durationNeed)
    data.loc[(data['学历'] == durationNeed[0])
             & (data['工作年限（年）'] >= durationNeed[1])
             & (data['工作年限（年）'] <= durationNeed[2]), '学历+年限'] = 1


# 筛选学历与年限
def filterWorkYear(data, durationNeed):
    data['学历+年限'] = 0
    # p1 = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    # pattern_date = re.compile(p1)
    # for x in range(len(data['姓名'])):
    #     # 毕业时间筛选
    #     dateString = str(data['教育经历'].iloc[x])
    #     b = pattern_date.findall(dateString)
    #     graduateYear = max(list(map(get_year, b)))
    #     data['毕业时长'] = datetime.now().year-graduateYear
    #     # if datetime.now().year-graduateYear >= edu_workYear:
    #     #     data['学历+年限'].iloc[x] = 0
    #     #     continue

    """
    "duration":[["doctor",-1,-1],["master",0,3],["bachelor",1,3],["normal",3,5]]
    """

    for restrict in durationNeed:
        meetDuration(data, restrict)

    result = data[data['学历+年限'] == 1]
    return result


# 筛选离职频率
def change_job_fre(data, minInterval):
    """

    :param data:
    :param minInterval: 能容忍能小跳槽间隔，比如低于平均2年跳一次就剔除
    :return:
    """

    data['离职率'] = minInterval
    for x in range(len(data['姓名'])):
        exp = str(data['工作经历'].iloc[x])

        p1 = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
        pattern_date = re.compile(p1)
        date = pattern_date.findall(exp)

        p2 = r'[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{4}-[0-9]{2}-[0-9]{2}\s[^\d]+?(实习)|(兼职)'
        pattern_shixi = re.compile(p2)
        shixi = pattern_shixi.findall(exp)

        work_year = data['工作年限（年）'].iloc[x]
        change_time = (len(date) + 1) // 2 - len(shixi)
        if change_time > 0:
            data['离职率'].iloc[x] = work_year / change_time
            # if len(shixi) != 0 and data['离职率'].iloc[x] < min:
            #     print(x, data['姓名'].iloc[x], "实习或兼职 =", len(shixi), "fre =", data['离职率'].iloc[x],
            #           "work_year =", work_year, "change_time =", change_time, data['工作经历'].iloc[x])

    result = data[data['离职率'] >= minInterval]
    return result


def genderFilter(data, gender):
    result = data[data['性别'] == gender]
    return result


def olderThan(data, age):
    return data[data['age'] >= age]


def youngerThan(data, age):
    return data[data['age'] <= age]


def mandatorySelect(data, **kwargs):
    if "gender" in kwargs.keys():
        # 筛选性别
        data.loc[data['性别'] == '男', '性别'] = 1
        data.loc[data['性别'] == '女', '性别'] = 0
        gender = kwargs.get("gender")
        data = genderFilter(data, gender)

    data["age"] = -1

    def countAge(birthday):
        if birthday != "null":
            birthday = birthday if type(birthday).__name__ == "str" else birthday.strftime("%Y.%m.%d")
            return datetime.now().year - datetime.strptime(birthday, "%Y.%m.%d").year

    data["age"] = data["生日"].map(countAge)

    if "ageTop" in kwargs.keys():
        # 筛选年龄最大值
        age = kwargs.get("ageTop")
        data = youngerThan(data, age)

    if "ageBottom" in kwargs.keys():
        # 筛选年龄最小值
        age = kwargs.get("ageBottom")
        data = olderThan(data, age)

    if "duration" in kwargs.keys():
        # 筛选学历与年限
        duration = kwargs.get("duration")

        """
        "duration":[["doctor",0,0],["master",0,3],["bachelor",1,3],["normal",3,5]]
        """
        data = filterWorkYear(data, duration)

    if "isPublic" in kwargs.keys() and kwargs.get("isPublic") == "是":
        # 筛选民办学学校
        data = minban(data)

    if "leaveRate" in kwargs.keys():
        # 筛选离职频率
        leaveRate = kwargs.get("leaveRate")
        data = change_job_fre(data, leaveRate)

    if "save_file" in kwargs.keys():
        data.to_csv(kwargs.get("save_file"), index=False)

    return data
