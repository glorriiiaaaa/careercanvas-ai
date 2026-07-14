# app/roadmap/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.roadmap import roadmap_bp
from app.roadmap.forms import RoadmapForm
from app.roadmap.services import generate_roadmap
from app.models.roadmap import Roadmap
from app.extensions import db


@roadmap_bp.route("/", methods=["GET", "POST"])
@login_required
def select_goal():
    form = RoadmapForm()

    if form.validate_on_submit():
        try:
            data = generate_roadmap(form.career_goal.data)

            new_roadmap = Roadmap(
                user_id=current_user.id,
                career_goal=form.career_goal.data,
                estimated_timeline=data["estimated_timeline"],
                weekly_plan=data["weekly_plan"],
                recommended_courses=data["recommended_courses"],
                suggested_projects=data["suggested_projects"],
            )
            db.session.add(new_roadmap)
            db.session.commit()

            return redirect(url_for("roadmap.view", roadmap_id=new_roadmap.id))

        except ValueError as e:
            flash(f"AI generation failed: {str(e)}", "error")
        except Exception as e:
            flash(f"Something went wrong generating your roadmap: {str(e)}", "error")

    return render_template("roadmap/select.html", form=form)


@roadmap_bp.route("/view/<int:roadmap_id>")
@login_required
def view(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)

    if roadmap.user_id != current_user.id:
        flash("You do not have permission to view that roadmap.", "error")
        return redirect(url_for("roadmap.history"))

    return render_template("roadmap/view.html", roadmap=roadmap)


@roadmap_bp.route("/history")
@login_required
def history():
    roadmaps = Roadmap.query.filter_by(user_id=current_user.id).order_by(Roadmap.created_at.desc()).all()
    return render_template("roadmap/history.html", roadmaps=roadmaps)
