"""app/routes/communities.py"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.decorators import login_required
from app.models import db, Community, CommunityMember, User

communities_bp = Blueprint("communities", __name__)


@communities_bp.route("/communities")
@login_required
def list_communities():
    all_comms = Community.query.filter_by(is_active=True).order_by(Community.member_count.desc()).all()
    # Get user's joined communities
    joined_ids = set()
    if session.get("user_id"):
        memberships = CommunityMember.query.filter_by(user_id=session["user_id"]).all()
        joined_ids = {m.community_id for m in memberships}
    return render_template("communities.html", communities=all_comms, joined_ids=joined_ids)


@communities_bp.route("/communities/join/<int:comm_id>", methods=["POST"])
@login_required
def join_community(comm_id):
    comm = Community.query.get_or_404(comm_id)
    existing = CommunityMember.query.filter_by(community_id=comm_id, user_id=session["user_id"]).first()
    if not existing:
        member = CommunityMember(community_id=comm_id, user_id=session["user_id"])
        db.session.add(member)
        comm.member_count = (comm.member_count or 0) + 1
        db.session.commit()
        flash(f"Joined {comm.name}! 🎉", "success")
    return redirect(url_for("communities.list_communities"))


@communities_bp.route("/communities/leave/<int:comm_id>", methods=["POST"])
@login_required
def leave_community(comm_id):
    comm = Community.query.get_or_404(comm_id)
    existing = CommunityMember.query.filter_by(community_id=comm_id, user_id=session["user_id"]).first()
    if existing:
        db.session.delete(existing)
        comm.member_count = max(0, (comm.member_count or 1) - 1)
        db.session.commit()
        flash(f"Left {comm.name}.", "info")
    return redirect(url_for("communities.list_communities"))
