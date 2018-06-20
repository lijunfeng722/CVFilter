import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
DEBUG = True

JOB_POSITION = list(["Java", "FrontEnd", "Mechanical"])
USECOLS = ['姓名', '来源', '所在地', '自我介绍', '期望地区', '工作年限（年）',
           '学历', '性别', '生日', '当前公司', '当前职位', '当前状态', '目前年薪',
           '期望行业', '期望职位', '邮箱', 'marriagestate', '技能', '手机号',
           '期望年薪', '工作经历', '教育经历', '语言能力', '项目经历']
CVFILEPATH = "../cv/简历训练/"
CVFile = {
    "Java": ["01430317(java通过简历库).xlsx", "01430318（Java未通过简历库）.xlsx"],
    "FrontEnd": ["01430319（前端通过简历库）.xlsx", "01430320（前端未通过简历库）.xlsx"],
    "Mechanical": ["01430321（机械通过简历库）.xlsx", "01430322（机械未通过简历库）.xlsx"]
}

POST_PROPERTIES_PARAMS = {
    "ageTop": None,  # 年龄限制上界(可选，默认不限制)
    "ageBottom": None,  # 年龄限制下界(可选，默认不限制)
    "duration": None,
    "gender": None,  # 性别(可选，默认不限制)
    "isPublic": None,  # 要求公立(可选，默认不限制)
    "leaveRate": None,  # 离职率(可选，默认不限制)
    "career": "",  # 岗位（必选）
    "description": ""  # 描述(必填)
}
