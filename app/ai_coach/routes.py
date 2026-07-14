# app/ai_coach/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.ai_coach import ai_coach_bp
from app.ai_coach.forms import ChatForm
from app.ai_coach.services import get_coach_reply
from app.models.chat_message import ChatMessage
from app.extensions import db

MAX_HISTORY_MESSAGES = 20   # how many past messages we feed back to the AI as context


@ai_coach_bp.route("/", methods=["GET", "POST"])
@login_required
def chat():
    form = ChatForm()

    if form.validate_on_submit():
        user_message = ChatMessage(user_id=current_user.id, role="user", content=form.message.data.strip())
        db.session.add(user_message)
        db.session.commit()

        recent_messages = (
            ChatMessage.query.filter_by(user_id=current_user.id)
            .order_by(ChatMessage.created_at.desc())
            .limit(MAX_HISTORY_MESSAGES)
            .all()
        )
        recent_messages.reverse()  # oldest to newest, for correct conversational order

        history = [{"role": m.role, "content": m.content} for m in recent_messages]

        try:
            reply_text = get_coach_reply(history)
        except Exception as e:
            reply_text = f"Sorry, I ran into an error responding: {str(e)}"

        ai_message = ChatMessage(user_id=current_user.id, role="assistant", content=reply_text)
        db.session.add(ai_message)
        db.session.commit()

        return redirect(url_for("ai_coach.chat"))

    all_messages = (
        ChatMessage.query.filter_by(user_id=current_user.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    return render_template("ai_coach/chat.html", form=form, messages=all_messages)


@ai_coach_bp.route("/clear", methods=["POST"])
@login_required
def clear_chat():
    ChatMessage.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("Conversation cleared.", "success")
    return redirect(url_for("ai_coach.chat"))
