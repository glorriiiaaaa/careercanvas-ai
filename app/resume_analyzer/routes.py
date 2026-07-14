# app/resume_analyzer/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.resume_analyzer import resume_analyzer_bp
from app.resume_analyzer.forms import ResumeUploadForm
from app.resume_analyzer.services import extract_text_from_pdf, analyze_resume_text
from app.models.resume import ResumeAnalysis
from app.extensions import db


@resume_analyzer_bp.route("/", methods=["GET", "POST"])
@login_required
def upload():
    form = ResumeUploadForm()

    if form.validate_on_submit():
        uploaded_file = form.resume_file.data

        try:
            resume_text = extract_text_from_pdf(uploaded_file.stream)

            if not resume_text or len(resume_text) < 50:
                flash("Could not extract enough text from that PDF. Make sure it is not a scanned image.", "error")
                return render_template("resume_analyzer/upload.html", form=form)

            analysis_data = analyze_resume_text(resume_text)

            new_analysis = ResumeAnalysis(
                user_id=current_user.id,
                original_filename=uploaded_file.filename,
                extracted_text=resume_text,
                ats_score=analysis_data["ats_score"],
                strengths=analysis_data["strengths"],
                weaknesses=analysis_data["weaknesses"],
                missing_skills=analysis_data["missing_skills"],
                keyword_suggestions=analysis_data["keyword_suggestions"],
                improved_bullets=analysis_data["improved_bullets"],
            )
            db.session.add(new_analysis)
            db.session.commit()

            return redirect(url_for("resume_analyzer.results", analysis_id=new_analysis.id))

        except ValueError as e:
            flash(f"AI analysis failed: {str(e)}", "error")
        except Exception as e:
            flash(f"Something went wrong processing your resume: {str(e)}", "error")

    return render_template("resume_analyzer/upload.html", form=form)


@resume_analyzer_bp.route("/results/<int:analysis_id>")
@login_required
def results(analysis_id):
    analysis = ResumeAnalysis.query.get_or_404(analysis_id)

    # Security check: users can only view their OWN analyses.
    # Without this, any logged-in user could view anyone's resume data
    # just by changing the ID in the URL (an "insecure direct object reference").
    if analysis.user_id != current_user.id:
        flash("You do not have permission to view that analysis.", "error")
        return redirect(url_for("resume_analyzer.history"))

    return render_template("resume_analyzer/results.html", analysis=analysis)


@resume_analyzer_bp.route("/history")
@login_required
def history():
    analyses = ResumeAnalysis.query.filter_by(user_id=current_user.id).order_by(ResumeAnalysis.created_at.desc()).all()
    return render_template("resume_analyzer/history.html", analyses=analyses)
