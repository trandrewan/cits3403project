from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Chat, User
from . import db


chat = Blueprint('chat', __name__)


@chat.route('/save_chat', methods=['POST'])
def save_chat():
    chat_content = request.json.get('chatContent')
    
    new_chat = Chat(data='\n'.join(chat_content), user_id=current_user.id)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify(status='success')


@chat.route('/get_chats', methods=['GET'])
@login_required
def get_chats():
    chats = Chat.query.filter_by(user_id=current_user.id).all()
    chats_list = [{"id": chat.id, "data": chat.data, "date": chat.date} for chat in chats]
    return jsonify(chats=chats_list)

@chat.route('/chat')
@login_required
def chat_page():
    chat_id = request.args.get('id')
    chat = Chat.query.filter_by(id=chat_id, user_id=current_user.id).first()
    if chat:
        return render_template('home.html', chat=chat.data, user=current_user)
    else:
        return "Chat not found", 404

@chat.route('/history')
@login_required
def history_page():
    return render_template('history.html', user=current_user)

@chat.route('/get_chat', methods=['GET'])
@login_required
def get_chat():
    chat_id = request.args.get('id')
    
    chat = Chat.query.get(chat_id)
    if chat and chat.user_id == current_user.id:
        return jsonify(chat=chat.data)
    else:
        return jsonify(error='Chat not found or unauthorized'), 404