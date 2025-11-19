from flask import Blueprint , render_template , url_for , request , redirect
import sqlite3
import os

register_bp = Blueprint('register' , __name__ , template_folder='auth_templates' , url_prefix='/register')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR , '..' , '..' , 'database.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn



@register_bp.route('/', methods=["GET"])
def register():
    return render_template('register.html')

@register_bp.route('/accept_register' , methods=["POST"])
def accept_register():
    taikhoan = request.form.get('username')
    matkhau = request.form.get('password')
    confirm_matkhau = request.form.get('confirm_password')
    if matkhau != confirm_matkhau:
        return "<h1> Mật khẩu không trùng nhau </h1>"
    
    conn = get_db_connection()
    try:
        add_register_sql = """
            INSERT INTO login_user(username , password) 
            VALUES(:username , :password)
        """
        conn.execute(add_register_sql , {
            "username": taikhoan,
            "password": matkhau
        })
        conn.commit()
        return redirect(url_for('login.login'))

    except sqlite3.IntegrityError:
        return "<h1> Tài khoản đã tồn tại </h1>"
    finally:
        conn.close()
    