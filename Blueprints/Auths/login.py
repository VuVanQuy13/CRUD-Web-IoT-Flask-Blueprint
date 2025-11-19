from flask import Blueprint , render_template , request , session , url_for , redirect
import sqlite3
import os

login_bp = Blueprint('login' , __name__ , template_folder='auth_templates' , static_folder='static' , url_prefix='/login')
    
BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # Lấy địa chỉ file này
DB_PATH = os.path.join(BASE_DIR, '..', '..', 'database.db')            # Lấy thư mục chứa file login.py nghĩa là .../Blueprints


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@login_bp.route('/' , methods=["GET" , "POST"])
def login():
    if session.get('account'):
        return redirect(url_for('board.board'))


    if request.method == "GET":
        return render_template('login.html')    
    elif request.method == "POST":
        taikhoan = request.form.get('username')
        matkhau = request.form.get('password')
        conn = get_db_connection()
        user_sql = """
            SELECT * FROM login_user 
            WHERE username=:taikhoan AND password=:matkhau
        """
        user = conn.execute(user_sql , {
            "taikhoan": taikhoan,
            "matkhau": matkhau
        }).fetchone()

        conn.close()

        if user:
            session['account'] = 'thanhcong'
            return redirect(url_for('board.board'))
        else:
            error = "Tên đăng nhập hoặc mật khẩu không đúng"
    
    return render_template('login.html' , error = error)
        


@login_bp.route('/log_out')
def log_out():
    session.pop('account')
    return redirect(url_for('login.login'))



