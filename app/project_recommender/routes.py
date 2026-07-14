# app/project_recommender/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.project_recommender import project_recommender_bp
from app.project_recommender.forms import InterestsForm
from app.project_recommender.services import generate_project_ideas
from app.models.project_recommendation import ProjectRecommendation
from app.extensions import db


@project_recommender_bp.route("/", methods=["GET", "POST"])
@login_required
def select_interests():
    form = InterestsForm()

    if form.validate_on_submit():
        try:
            projects = generate_project_ideas(form.interests.data)

            new_rec = ProjectRecommendation(
                user_id=current_user.id,
                interests=form.interests.data.strip(),
                projects=projects,
            )
            db.session.add(new_rec)
            db.session.commit()

            return redirect(url_for("project_recommender.view", rec_id=new_rec.id))

        except Exception as e:
            flash(f"Could not generate project ideas: {str(e)}", "error")

    return render_template("project_recommender/select.html", form=form)


@project_recommender_bp.route("/view/<int:rec_id>")
@login_required
def view(rec_id):
    rec = ProjectRecommendation.query.get_or_404(rec_id)

    if rec.user_id != current_user.id:
        flash("You do not have permission to view that recommendation.", "error")
        return redirect(url_for("project_recommender.history"))

    return render_template("project_recommender/view.html", rec=rec)


@project_recommender_bp.route("/history")
@login_required
def history():
    recs = (
        ProjectRecommendation.query.filter_by(user_id=current_user.id)
        .order_by(ProjectRecommendation.created_at.desc())
        .all()
    )
    return render_template("project_recommender/history.html", recs=recs)
