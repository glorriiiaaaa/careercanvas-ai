# app/skill_tracker/routes.py
#
# WHY THIS FILE EXISTS:
# Unlike our AI-powered modules, Skill Tracker is standard CRUD
# (Create, Read, Update, Delete) on user-owned records - no AI calls.
# Every route that touches a specific skill checks skill.user_id ==
# current_user.id BEFORE allowing access/edit/delete - this is the
# same "insecure direct object reference" protection we used in
# Resume Analyzer and Roadmap, applied consistently here too.

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.skill_tracker import skill_tracker_bp
from app.skill_tracker.forms import SkillForm
from app.models.skill import Skill
from app.extensions import db


@skill_tracker_bp.route("/")
@login_required
def index():
    skills = Skill.query.filter_by(user_id=current_user.id).order_by(Skill.created_at.desc()).all()
    total_hours = sum(s.learning_hours for s in skills)
    return render_template("skill_tracker/index.html", skills=skills, total_hours=total_hours)


@skill_tracker_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_skill():
    form = SkillForm()

    if form.validate_on_submit():
        new_skill = Skill(
            user_id=current_user.id,
            name=form.name.data.strip(),
            level=form.level.data,
            progress_percent=form.progress_percent.data,
            learning_hours=form.learning_hours.data,
        )
        db.session.add(new_skill)
        db.session.commit()
        flash(f'Added "{new_skill.name}" to your skills.', "success")
        return redirect(url_for("skill_tracker.index"))

    return render_template("skill_tracker/form.html", form=form, mode="add")


@skill_tracker_bp.route("/edit/<int:skill_id>", methods=["GET", "POST"])
@login_required
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)

    if skill.user_id != current_user.id:
        flash("You do not have permission to edit that skill.", "error")
        return redirect(url_for("skill_tracker.index"))

    form = SkillForm(obj=skill)

    if form.validate_on_submit():
        skill.name = form.name.data.strip()
        skill.level = form.level.data
        skill.progress_percent = form.progress_percent.data
        skill.learning_hours = form.learning_hours.data
        db.session.commit()
        flash(f'Updated "{skill.name}".', "success")
        return redirect(url_for("skill_tracker.index"))

    return render_template("skill_tracker/form.html", form=form, mode="edit", skill=skill)


@skill_tracker_bp.route("/delete/<int:skill_id>", methods=["POST"])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)

    if skill.user_id != current_user.id:
        flash("You do not have permission to delete that skill.", "error")
        return redirect(url_for("skill_tracker.index"))

    skill_name = skill.name
    db.session.delete(skill)
    db.session.commit()
    flash(f'Deleted "{skill_name}".', "success")
    return redirect(url_for("skill_tracker.index"))
