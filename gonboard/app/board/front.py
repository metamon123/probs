from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db_session

board_bp = Blueprint("board", __name__, template_folder='templates')

@board_bp.route("/")
def index():
    return render_template("main.html")


@board_bp.route("/board/<board_name>", methods=["GET"])
@board_bp.route("/board/<board_name>/<int:post_id>", methods=["GET"])
def board(board_name, post_id=None):
    pass


@board_bp.route("/upload/", methods=["GET", "POST"])
def upload():
    pass
