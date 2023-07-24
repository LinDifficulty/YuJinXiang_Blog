from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length

from .baseform import BaseForm


class PublicPostForm(BaseForm):
    title = StringField(validators=[Length(min=2, max=15, message="请输入正确长度的标题")])
    content = StringField(validators=[Length(min=2, message="请输入正确长度的内容！")])
    board_id = IntegerField(validators=[InputRequired(message="请输入板块id")])


class DeletePostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message="请输入文章id")])


class EditPostForm(BaseForm):
    post_id = IntegerField(validators=[InputRequired(message="请输入文章id")])
    new_title = StringField(validators=[Length(min=2, max=100, message="请输入正确长度的标题")])
    new_content = StringField(validators=[Length(min=2, message="请输入正确长度的内容！")])