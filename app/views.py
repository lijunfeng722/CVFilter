# encoding: utf-8
from datetime import datetime
import cut_words as cut
import vectorized as vec
from app import myapp
from app.models import User, Result
from flask import render_template
from flask import request
import json
import pandas as pd
from config import *
from cv.MandatorySelect import mandatorySelect

'''
{
    "ageTop":22,          // 年龄限制上界(可选，默认不限制)
    "ageBottom":24,       // 年龄限制下界(可选，默认不限制)
    "duration":[["博士",-1,99],["硕士",-1,3],["本科",3,8],["大专",5,10]],
    "gender":1,            // 性别(可选，默认不限制)
    "isPublic":"否",          // 要求公立(可选，默认不限制)
    "leaveRate":3,     // 离职率(可选，默认不限制)
    "career":"Java",          // 岗位（必选）
    "description":"具有..."   // 描述(必填)
}'''


@myapp.route('/postProperties', methods=["POST"])
def filterCV():
    # ageTop = request.json.get('ageTop')
    # ageBottom = request.json.get('ageBottom')
    # duration = request.json.get('duration')
    # gender = request.json.get('gender')
    # isPublic = request.json.get('isPublic')
    # leaveRate = request.json.get('leaveRate')
    # career = request.json.get('career')
    # description = request.json.get('description')

    post_params = {}

    for para in POST_PROPERTIES_PARAMS.keys():
        value = request.json.get(para, None)
        if value is not None:  # 若值不为空
            post_params[para] = request.json.get(para)

    print("post_params-->", post_params)

    career = post_params["career"]
    dataList = list()
    for x in range(len(CVFile[career])):
        file = CVFILEPATH + CVFile[career][x]
        data = pd.read_excel(file, usecols=USECOLS).fillna("null")
        dataList.append(data)
    data = pd.concat(dataList)

    # save_file = "result.csv"
    data['离职率'] = int(99)
    data = mandatorySelect(data, **post_params)
    data = data.fillna(-1)

    if "description" in post_params.keys():
        print('正在切词...')  # 切词,中间结果会保存成csv文件，所以改函数无需返回值
        data = cut.execute(data)
        print('正在匹配模型...')
        data = vec.execute(data,career)

    # 将筛选结果存入resultCV
    resultCV = list()
    for x in range(len(data)):
        name = data.iloc[x]["姓名"]
        birthday = data.iloc[x]["生日"]
        age = data.iloc[x]["age"]
        if age is None and birthday != "null":
            birthday = birthday if type(birthday).__name__ == "str" else data.iloc[x]["生日"].strftime("%Y.%m.%d")
            age = datetime.now().year - datetime.strptime(birthday, "%Y.%m.%d").year
        gender = 1 if data.iloc[x]["性别"] == '男' else 0
        degree = data.iloc[x]["学历"]
        avatar = "avatar"
        description = data.iloc[x]["自我介绍"]
        duration = int(data.iloc[x]["工作年限（年）"])
        # career = data["工作经历"].iloc[x]
        graduateExp = data.iloc[x]["教育经历"]
        jobExp = data.iloc[x]["工作经历"]
        projectExp = data.iloc[x]["项目经历"]
        skill = data.iloc[x]["技能"]
        change_job_fre = int(data.iloc[x]["离职率"])
        cv = User(name, age, gender, degree, avatar, description, duration, career, graduateExp, jobExp, projectExp,
                  skill,
                  change_job_fre)
        resultCV.append(cv)

    # 返回json
    result = Result().SUCCESS(resultCV)
    resultStr = json.dumps(result, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    return resultStr


@myapp.route('/getProperties', methods=['GET'])
def getJobCategories():
    result = Result().SUCCESS(JOB_POSITION)
    resultStr = json.dumps(result, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    return resultStr


@myapp.route('/cv/<id>', methods=["GET"])
def findCVById(id):
    user = User('李俊锋', 22, 1, '2130837590', '非常牛逼', 2, '软件工程师', '中国科学技术大学', '一家企业', '非常多的项目', 'JAVA C++ Python ')
    result = Result().SUCCESS(user)
    result_str = json.dumps(result, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    return result_str


@myapp.route('/cv', methods=["POST"])
def saveCV():
    age = request.json.get("age")
    description = request.json.get("description")
    duration = request.json.get("duration")
    job = request.json.get("career")
    name = request.json.get("name")
    gender = request.json.get("gender")
    avatar = request.json.get("avatar")
    graduateFrom = request.json.get("graduateFrom")
    jobExp = request.json.get("jobExp")
    projectExp = request.json.get("projectExp")
    skill = request.json.get("skill")
    new_user = User(name, age, gender, avatar, description, duration, job, graduateFrom, jobExp, projectExp, skill)
    # TODO saveCV
    return "success"


@myapp.route('/')
@myapp.route('/index')
def index():
    return render_template('index.html')


myapp.run(host='0.0.0.0', debug=True)
