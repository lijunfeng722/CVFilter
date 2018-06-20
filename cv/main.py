import pandas as pd

from cv.MandatorySelect import mandatorySelect

if __name__=="__main__":
    usecols = ['姓名', '来源', '所在地', '自我介绍', '期望地区', '工作年限（年）',
               '学历', '性别', '生日', '当前公司', '当前职位', '当前状态', '目前年薪',
               '期望行业', '期望职位', '邮箱', 'marriagestate', '技能', '手机号',
               '期望年薪', '工作经历', '教育经历', '语言能力', '项目经历']

    # data1 = pd.read_excel(path+"01430319（前端通过简历库）.xlsx", usecols=usecols)
    # data2 = pd.read_excel(path+"01430320（前端未通过简历库）.xlsx", usecols=usecols)
    # save_file = path+"qianduan_test.csv"

    # data1 = pd.read_excel(path+"01430317(java通过简历库).xlsx", usecols=usecols)
    # data2 = pd.read_excel(path+"01430318（Java未通过简历库）.xlsx", usecols=usecols)
    # save_file = path+"java_test.csv"
    #

    file1 = input("通过简历 file name")
    file2 = input("未通过简历 file name")
    data1 = pd.read_excel(file1, usecols=usecols)
    data2 = pd.read_excel(file2, usecols=usecols)
    save_file = "result.csv"


    # data['年龄'] = data['生日'].apply\
    #     (lambda x: 2018 - int(str(x)[:4]) if str(x)[:4] != 'NaT' else 0)

    data1['label'] = 1
    data2['label'] = 0
    data = pd.concat([data1, data2])
    mandatorySelect(data, save_file)