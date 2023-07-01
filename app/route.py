from flask import render_template, request, url_for, redirect
from config import db, app
from model import Group, Bookmark


# ---------- General ----------
@app.route("/")
def index():
    groups = Group.query.filter(Group.parent_id == 0).order_by(Group.name).all()
    return render_template("index.html", groups=groups)


# ---------- Group ----------
@app.route("/group/<int:id>/")
def group(id):
    group = Group.query.get_or_404(id)
    return render_template("group/group.html", group=group)


@app.route("/group/new/", methods=("GET", "POST"))
def new_group():
    groups = Group.query.filter(Group.parent_id == 0).order_by(Group.name).all()
    if request.method == "POST":
        # parent_id = request.form.get("group")
        name = request.form.get("name")

        db.session.add(
            Group(
                # parent_id=parent_id,
                parent_id=0,
                name=name,
            )
        )
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("group/new.html", groups=groups)


@app.route("/group/<int:id>/edit/", methods=("GET", "POST"))
def edit_group(id):
    group = Group.query.get_or_404(id)
    # groups = Group.query.filter(Group.parent_id == 0).all()
    if request.method == "POST":
        group.parent_id = 0
        group.name = request.form.get("name")
        db.session.add(group)
        db.session.commit()
        return redirect(url_for("group", id=group.id))
    return render_template("group/edit.html", group=group)


@app.route("/group/<int:id>/delete/")
def delete_group(id):
    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for("index"))


# ---------- Bookmark ----------
@app.route("/bookmark/new/", defaults={"group_id": 0}, methods=("GET", "POST"))
@app.route("/bookmark/new/<int:group_id>", methods=("GET", "POST"))
def new_bookmark(group_id):
    groups = Group.query.filter(Group.parent_id == 0).all()
    if request.method == "POST":
        title = request.form.get("title")
        group_id = request.form.get("group")
        url = request.form.get("url")
        description = request.form.get("description")
        db.session.add(
            Bookmark(
                group_id=group_id,
                title=title,
                url=url,
                description=description,
            )
        )
        db.session.commit()
        return redirect(url_for("group", id=group_id))
    return render_template("bookmark/new.html", groups=groups, group_id=group_id)


@app.route("/bookmark/<int:id>/edit/", methods=("GET", "POST"))
def edit_bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)
    groups = Group.query.filter(Group.parent_id == 0).all()
    if request.method == "POST":
        bookmark.title = request.form.get("title")
        bookmark.group_id = request.form.get("group")
        bookmark.url = request.form.get("url")
        bookmark.description = request.form.get("description")
        db.session.add(bookmark)
        db.session.commit()
        return redirect(url_for("group", id=bookmark.group_id))
    return render_template("bookmark/edit.html", groups=groups, bookmark=bookmark)


@app.route("/bookmark/<int:id>/delete/")
def delete_bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)
    db.session.delete(bookmark)
    db.session.commit()
    return redirect(url_for("group", id=bookmark.group_id))
