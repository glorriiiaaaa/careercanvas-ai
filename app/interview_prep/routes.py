# app/interview_prep/routes.py
from flask import render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app.interview_prep import interview_prep_bp
from app.interview_prep.forms import CategoryForm, AnswerForm
from app.interview_prep.services import generate_questions, evaluate_answer
from app.models.interview import InterviewSession
from app.models.resume import ResumeAnalysis
from app.extensions import db


@interview_prep_bp.route("/", methods=["GET", "POST"])
@login_required
def select_category():
    form = CategoryForm()

    if form.validate_on_submit():
        category = form.category.data
        resume_text = None

        if category == "Resume-Based":
            latest_resume = (
                ResumeAnalysis.query.filter_by(user_id=current_user.id)
                .order_by(ResumeAnalysis.created_at.desc())
                .first()
            )
            if latest_resume is None:
                flash("Upload a resume in Resume Analyzer first to use Resume-Based questions.", "error")
                return redirect(url_for("interview_prep.select_category"))
            resume_text = latest_resume.extracted_text

        try:
            questions = generate_questions(category, resume_text)
        except Exception as e:
            flash(f"Could not generate questions: {str(e)}", "error")
            return redirect(url_for("interview_prep.select_category"))

        # Store the in-progress session in the browser session (not DB yet) -
        # we only save to the database once the user finishes all questions.
        session["interview_category"] = category
        session["interview_questions"] = questions
        session["interview_answers"] = []
        session["interview_current_index"] = 0

        return redirect(url_for("interview_prep.answer_question"))

    return render_template("interview_prep/select.html", form=form)


@interview_prep_bp.route("/answer", methods=["GET", "POST"])
@login_required
def answer_question():
    questions = session.get("interview_questions")
    if not questions:
        flash("Please start a new practice session.", "error")
        return redirect(url_for("interview_prep.select_category"))

    current_index = session.get("interview_current_index", 0)

    if current_index >= len(questions):
        return redirect(url_for("interview_prep.finish_session"))

    form = AnswerForm()
    current_question = questions[current_index]

    if form.validate_on_submit():
        try:
            feedback_data = evaluate_answer(current_question, form.answer.data)
        except Exception as e:
            flash(f"Could not evaluate answer: {str(e)}", "error")
            return render_template(
                "interview_prep/answer.html", form=form, question=current_question,
                question_number=current_index + 1, total_questions=len(questions)
            )

        answers = session.get("interview_answers", [])
        answers.append({
            "question": current_question,
            "answer": form.answer.data,
            "feedback": feedback_data["feedback"],
            "answer_rating": feedback_data["answer_rating"],
            "confidence_score": feedback_data["confidence_score"],
            "grammar_score": feedback_data["grammar_score"],
        })
        session["interview_answers"] = answers
        session["interview_current_index"] = current_index + 1

        return redirect(url_for("interview_prep.answer_question"))

    return render_template(
        "interview_prep/answer.html", form=form, question=current_question,
        question_number=current_index + 1, total_questions=len(questions)
    )


@interview_prep_bp.route("/finish")
@login_required
def finish_session():
    answers = session.get("interview_answers", [])
    category = session.get("interview_category", "HR")

    if not answers:
        flash("No completed session to save.", "error")
        return redirect(url_for("interview_prep.select_category"))

    overall_score = round(
        sum(a["confidence_score"] for a in answers) / len(answers)
    )

    new_session = InterviewSession(
        user_id=current_user.id,
        category=category,
        questions_and_answers=answers,
        overall_score=overall_score,
    )
    db.session.add(new_session)
    db.session.commit()

    # Clear the temporary in-progress session data
    session.pop("interview_category", None)
    session.pop("interview_questions", None)
    session.pop("interview_answers", None)
    session.pop("interview_current_index", None)

    return redirect(url_for("interview_prep.results", session_id=new_session.id))


@interview_prep_bp.route("/results/<int:session_id>")
@login_required
def results(session_id):
    interview_session = InterviewSession.query.get_or_404(session_id)

    if interview_session.user_id != current_user.id:
        flash("You do not have permission to view that session.", "error")
        return redirect(url_for("interview_prep.history"))

    return render_template("interview_prep/results.html", interview_session=interview_session)


@interview_prep_bp.route("/history")
@login_required
def history():
    sessions = (
        InterviewSession.query.filter_by(user_id=current_user.id)
        .order_by(InterviewSession.created_at.desc())
        .all()
    )
    return render_template("interview_prep/history.html", sessions=sessions)
