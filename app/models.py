# ##
#
# "name": "李俊锋",
# "age": 22,
# "gender": 1,
# "avatar": 2130837590,
# "description": "非常牛逼",
# "duration": 1,
# "career": "软件工程师",
# "graduateFrom": "中国科学技术大学",
# "jobExp": "一家企业",
# "projectExp": "非常多的项目",
# "skill": "JAVA C++ Python "
#
# ##
class User:
    def __init__(self, name, age, gender, degree, avatar, description, duration, career, graduateExp, jobExp,
                 projectExp, skill,
                 change_job_fre):
        self.name = name
        self.age = age
        self.gender = gender
        self.degree = degree
        self.avatar = avatar
        self.description = description
        self.duration = duration
        self.career = career
        self.graduateExp = graduateExp
        self.jobExp = jobExp
        self.projectExp = projectExp
        self.skill = skill
        self.change_job_fre = change_job_fre

    def __repr__(self):
        return repr(
            (self.name, self.age, self.gender, self.degree, self.avatar, self.description, self.duration, self.career,
             self.graduateExp, self.jobExp, self.projectExp, self.skill))


class Result:
    code = 0
    msg = ""
    data = ""

    def __init__(self):
        self.code = 0
        self.msg = ""
        self.data = ""

    def __repr__(self):
        return repr((self.code, self.msg, self.data))

    def SUCCESS(self, data):
        self.data = data
        return self

    def ERROR(self, msg, code):
        self.code = code
        self.msg = msg
        return self
