"""app/routes/feed.py — Social Feed for Students & Alumni"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.utils.decorators import login_required
from app.models import db, Post, Comment, Like, User, Notification
from datetime import datetime

feed_bp = Blueprint("feed", __name__)


def _feed_posts(limit=30):
    """Return posts with author info, newest first."""
    rows = (
        db.session.query(Post, User)
        .join(User, Post.user_id == User.id)
        .order_by(Post.created_at.desc())
        .limit(limit)
        .all()
    )
    result = []
    for post, user in rows:
        d = post.to_dict()
        d["author_name"]   = user.name
        d["author_role"]   = user.role
        d["author_avatar"] = user.avatar_url
        result.append(d)
    return result


@feed_bp.route("/student/feed")
@login_required
def student_feed():
    posts = _feed_posts()
    return render_template("feed.html", posts=posts, user_role="student")


@feed_bp.route("/alumni/feed")
@login_required
def alumni_feed():
    posts = _feed_posts()
    return render_template("feed.html", posts=posts, user_role="alumni")


@feed_bp.route("/feed/post", methods=["POST"])
@login_required
def create_post():
    content   = request.form.get("content", "").strip()[:2000]
    post_type = request.form.get("post_type", "text")
    tags      = request.form.get("tags", "")[:500]
    if not content:
        flash("Post content cannot be empty.", "warning")
        return redirect(request.referrer or url_for("feed.student_feed"))
    post = Post(
        user_id=session["user_id"], content=content,
        post_type=post_type, tags=tags,
    )
    db.session.add(post)
    db.session.commit()
    flash("Post shared! 🎉", "success")
    return redirect(request.referrer or url_for("feed.student_feed"))


@feed_bp.route("/feed/like/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):
    existing = Like.query.filter_by(post_id=post_id, user_id=session["user_id"]).first()
    post = Post.query.get_or_404(post_id)
    if existing:
        db.session.delete(existing)
        post.likes_count = max(0, post.likes_count - 1)
        liked = False
    else:
        like = Like(post_id=post_id, user_id=session["user_id"])
        db.session.add(like)
        post.likes_count += 1
        liked = True
    db.session.commit()
    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"liked": liked, "count": post.likes_count})
    return redirect(request.referrer or url_for("feed.student_feed"))


@feed_bp.route("/feed/comment/<int:post_id>", methods=["POST"])
@login_required
def comment_post(post_id):
    content = request.form.get("content", "").strip()[:1000]
    if not content:
        return redirect(request.referrer or url_for("feed.student_feed"))
    post    = Post.query.get_or_404(post_id)
    comment = Comment(post_id=post_id, user_id=session["user_id"], content=content)
    db.session.add(comment)
    post.comments_count += 1
    db.session.commit()
    return redirect(request.referrer or url_for("feed.student_feed"))
