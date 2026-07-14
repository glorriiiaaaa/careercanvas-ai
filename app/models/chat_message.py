# app/models/chat_message.py
#
# WHY THIS FILE EXISTS:
# Stores every message (both user and AI) in a user's AI Coach
# conversation. Storing role separately (user vs assistant) lets us
# reconstruct the full conversation in order and replay it as context
# for the AI on each new message - the same pattern real chat apps use.

from datetime import datetime
from app.extensions import db


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    role = db.Column(db.String(10), nullable=False)   # "user" or "assistant"
    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    user = db.relationship("User", backref=db.backref("chat_messages", lazy=True))

    def __repr__(self):
        return f"<ChatMessage {self.role} - user {self.user_id}>"
