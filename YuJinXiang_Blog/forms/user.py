from wtforms import Form, StringField, BooleanField, ValidationError
from wtforms.validators import Email, EqualTo, Length
from exts import cache
from models.user import UserModel
from .baseform import BaseForm


class RegisterForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式错误!")])
    email_captcha = StringField(validators=[Length(min=6, max=6, message="验证码格式错误!")])
    username = StringField(validators=[Length(min=2, max=20, message="用户名验证错误")])
    password = StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
    confirm_password = StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # 自定义验证
    # 1.邮箱是否已经注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise ValidationError(message="该邮箱已经被注册")

    # 2.验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        cache_captcha = cache.get(email)
        if not cache_captcha or captcha != cache_captcha:
            raise ValidationError(message="邮箱或验证码错误!")


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式错误!")])
    password = StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
    remember = BooleanField()