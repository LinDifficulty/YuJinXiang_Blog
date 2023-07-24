from flask import Blueprint, request, render_template, g, redirect, flash
from flask_paginate import current_app, Pagination

from decorators import login_required
from exts import db, csrf
from forms.post import PublicPostForm, DeletePostForm, EditPostForm
from models.post import BoardModel, PostModel

bp = Blueprint('front', __name__, url_prefix='')


@bp.route("/")
def index():
    boards = BoardModel.query.all()
    # 获取页码参数
    page = request.args.get("page", type=int, default=1)

    # 获取板块参数
    board_id = request.args.get("board_id", type=int, default=0)

    # 获取搜索关键字
    q = request.args.get("q")

    # 当前page下的起始位置
    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
    # 当前page下的结束位置
    end = start + current_app.config.get("PER_PAGE_COUNT")
    # 查询对象
    query_obj = PostModel.query.order_by(PostModel.create_time.desc())

    # 过滤帖子
    if board_id:
        query_obj = query_obj.filter_by(board_id=board_id)
    if q:
        query_obj = query_obj.filter(PostModel.title.contains(q))

    # 总共有多少帖子
    total = query_obj.count()

    # 当前page下的帖子列表
    posts = query_obj.slice(start, end)

    # 分页对象
    pagination = Pagination(bs_version=4, page=page, total=total,
                            outer_window=0, inner_window=2, alignment="center")

    context = {
        "posts": posts,
        "boards": boards,
        "pagination": pagination,
        "current_board": board_id
    }

    return render_template("front/index.html", **context)


@bp.get("/post/detail/<int:post_id>")
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    boards = BoardModel.query.all()
    post.read_count += 1
    db.session.commit()
    return render_template("front/detail.html", post=post, boards=boards)


@bp.route("/post/public", methods=['POST', 'GET'])
@login_required
def public_post():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template("front/post.html", boards=boards)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            post = PostModel(title=title, content=content, board_id=board_id, author=g.user)
            db.session.add(post)
            db.session.commit()
            return redirect("/")
        else:
            for message in form.messages:
                flash(message)
            boards = BoardModel.query.all()
            return render_template("front/post.html", boards=boards)


@csrf.exempt
@bp.route("/post/public/delete_post", methods=["GET", "POST"])
def delete_post():
    form = DeletePostForm(request.form)
    post_id = form.post_id.data
    post = PostModel.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")


@csrf.exempt
@bp.route("/post/public/edit_post", methods=["GET", "POST"])
def edit_post():
    boards = BoardModel.query.all()
    form = DeletePostForm(request.form)
    post_id = form.post_id.data
    post = PostModel.query.get(post_id)
    return render_template("front/post_edit.html", post=post, boards=boards)

@csrf.exempt
@bp.route("/post/public/edit_post_post", methods=["GET", "POST"])
def edit_post_post():
    boards = BoardModel.query.all()
    form = EditPostForm(request.form)
    post_id = form.post_id.data
    new_title = form.new_title.data
    new_content = form.new_content.data
    post = PostModel.query.get(post_id)
    db.session.query(PostModel).filter_by(id=post_id).update({"title": new_title, "content": new_content})
    db.session.commit()
    post = PostModel.query.get(post_id)
    return render_template("front/detail.html", post=post, boards=boards)


@bp.route("/resource")
def resource():
    return render_template("front/resource.html")


@bp.route("/friends")
def friends():
    return render_template("front/friends.html")