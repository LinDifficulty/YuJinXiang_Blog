from models.user import PermissionModel, PermissionEnum, RoleModel, UserModel
from models.post import BoardModel, PostModel
import click
from exts import db
from faker import Faker
import random


def create_permission():
    for permission_name in dir(PermissionEnum):
        if permission_name.startswith("__"):
            continue
        permission = PermissionModel(name=getattr(PermissionEnum, permission_name))
        db.session.add(permission)
    db.session.commit()
    click.echo("权限添加成功")


def create_role():
    # 管理员
    administrator = RoleModel(name="管理员", desc="负责网站的所有工作")
    administrator.permissions = PermissionModel.query.all()

    db.session.add(administrator)
    db.session.commit()
    click.echo("角色添加成功")


@click.option("--username", '-u')
@click.option("--email", '-e')
@click.option("--password", '-p')
def create_admin(username, email, password):
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    admin_user = UserModel(username=username,
                           email=email,
                           password=password,
                           is_staff=True,
                           role=admin_role)
    db.session.add(admin_user)
    db.session.commit()
    click.echo("管理员添加成功")


def create_board():
    board_names = ['C/C++', 'Python', '前端']
    for board_name in board_names:
        board = BoardModel(name=board_name)
        db.session.add(board)
    db.session.commit()
    click.echo("板块添加成功")


def create_test_post():
    fake = Faker(locale="zh_CN")
    author = UserModel.query.first()
    boards = BoardModel.query.all()

    click.echo("开始生成测试帖子....")
    for x in range(10000):
        title = fake.sentence()
        content = fake.paragraph(nb_sentences=10)
        random_index = random.randint(0, 2)
        board = boards[random_index]
        post = PostModel(title=title, content=content, board=board, author=author)
        db.session.add(post)
    db.session.commit()
    click.echo("测试帖子生成成功！")