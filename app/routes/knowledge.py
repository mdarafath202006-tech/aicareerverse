"""app/routes/knowledge.py — Knowledge Base V5"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.decorators import login_required
from app.models import db, KnowledgeEntry, User

knowledge_bp = Blueprint("knowledge", __name__)


@knowledge_bp.route("/")
@login_required
def index():
    category = request.args.get("category", "")
    q        = request.args.get("q", "")
    query    = KnowledgeEntry.query.filter_by(is_approved=True)
    if category:
        query = query.filter_by(category=category)
    if q:
        query = query.filter(
            KnowledgeEntry.title.ilike(f"%{q}%") |
            KnowledgeEntry.content.ilike(f"%{q}%") |
            KnowledgeEntry.company.ilike(f"%{q}%")
        )
    entries = query.order_by(KnowledgeEntry.created_at.desc()).all()
    # Attach author names
    result = []
    for e in entries:
        d = e.to_dict()
        d["author_name"]   = e.author.name if e.author else "Anonymous"
        d["author_avatar"] = e.author.avatar_url if e.author else None
        d["author_role"]   = e.author.role if e.author else "alumni"
        result.append(d)
    categories = [
        ("success_story", "🌟 Success Stories"),
        ("interview_experience", "💬 Interview Experiences"),
        ("placement_story", "🎓 Placement Stories"),
        ("career_guide", "🗺️ Career Guides"),
        ("company_review", "🏢 Company Reviews"),
        ("tips_and_tricks", "💡 Tips & Tricks"),
    ]
    return render_template("knowledge/index.html",
                           entries=result, categories=categories,
                           selected_category=category, q=q)


@knowledge_bp.route("/<int:entry_id>")
@login_required
def detail(entry_id):
    entry = KnowledgeEntry.query.filter_by(id=entry_id, is_approved=True).first_or_404()
    entry.views += 1
    db.session.commit()
    related = (KnowledgeEntry.query
               .filter_by(category=entry.category, is_approved=True)
               .filter(KnowledgeEntry.id != entry_id)
               .limit(4).all())
    return render_template("knowledge/detail.html", entry=entry, related=related)


@knowledge_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title    = request.form.get("title", "")[:300]
        category = request.form.get("category", "career_guide")
        content  = request.form.get("content", "")[:10000]
        company  = request.form.get("company", "")[:150]
        role     = request.form.get("role", "")[:150]
        tags     = request.form.get("tags", "")[:500]
        if not title or not content:
            flash("Title and content are required.", "warning")
            return redirect(request.url)
        e = KnowledgeEntry(
            author_id=session["user_id"], title=title, category=category,
            content=content, company=company, role=role, tags=tags, is_approved=True
        )
        db.session.add(e)
        db.session.commit()
        flash("Your story has been published! 🎉", "success")
        return redirect(url_for("knowledge.index"))
    return render_template("knowledge/create.html")


@knowledge_bp.route("/<int:entry_id>/helpful", methods=["POST"])
@login_required
def mark_helpful(entry_id):
    entry = KnowledgeEntry.query.get_or_404(entry_id)
    entry.helpful_count += 1
    db.session.commit()
    return redirect(request.referrer or url_for("knowledge.index"))
