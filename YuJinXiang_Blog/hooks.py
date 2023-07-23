from flask import session, g, render_template

from models.user import UserModel


# 将user设置为全局变量
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)



def my_context_processor():
    return {"user": g.user}

# 错误提示
def bbs_404_error(error):
    return render_template("errors/404.html"), 404


def bbs_401_error(error):
    return render_template("errors/401.html"), 401


def bbs_500_error(error):
    return render_template("errors/500.html"), 500
