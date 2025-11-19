from flask import Blueprint , render_template , url_for , redirect , request , jsonify
import sqlite3
import os 

board_bp = Blueprint('board' , __name__ , static_folder='static' , template_folder='board_templates' , url_prefix='/board')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR , '..' , '..' , 'database.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH , timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

# render farm
@board_bp.route('/')
def board():
    conn = get_db_connection()
    sql_list_farm = """
        SELECT * FROM farm 
        ORDER BY id ASC
    """
    farms = conn.execute(sql_list_farm).fetchall()
    conn.close()
    return render_template("list_farm.html" , all_farms=farms)


# Add farm
@board_bp.route('/api/add' , methods=["POST"])
def add_farm():
    data = request.get_json()
    desc = data.get('description', '')         
    name = data.get('namefarm')      

    if not name: 
        return jsonify({
            "error": "Tên farm phải bắt buộc"
        }) , 400
    
    with sqlite3.connect(DB_PATH , timeout=10) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql_addFarm = """
            INSERT INTO farm(namefarm , description)
            VALUES (:namefarm , :description)
        """
        cur.execute(sql_addFarm , {
            "namefarm": name,
            "description": desc
        })
        farm_id = cur.lastrowid

    return jsonify({
        "id": farm_id,
        "namefarm": name,
        "description": desc
    })


# Delete Farm
@board_bp.route('/api/delete/<int:id>' , methods=["DELETE"])
def delete_farm(id):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.row_factory = sqlite3.Row
        sql_deleteFarm = """
            DELETE FROM farm
            WHERE id=:id
        """
        conn.execute(sql_deleteFarm , {
            "id": id
        })

    return  jsonify({
        "success": True
    })


# Update Farm
@board_bp.route('/api/update/<int:id>', methods=["POST"])
def update_farm(id):
    data = request.get_json()
    newname = data.get('namefarm')
    newdesc = data.get('description' ,'')

    if not newname:
        return jsonify({"error": "Tên farm không được để trống!"}), 400
    
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.row_factory = sqlite3.Row
        sql_updateFarm = """
            UPDATE farm 
            SET namefarm=:newname, description=:newdescription
            WHERE id=:id
        """
        conn.execute(sql_updateFarm, {
            "newname": newname,
            "newdescription": newdesc,
            "id": id
        })

    return jsonify({
        'success': True
    })


# Select Farm
@board_bp.route('/api/farm/<int:id>')
def select_farm(id):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.row_factory = sqlite3.Row
        sql_selectFarm = """
            SELECT * FROM farm
            WHERE id=:id
        """
        farm = conn.execute(sql_selectFarm , {
            "id":id
        }).fetchone()

    if not farm:
        return jsonify({
            "error": "farm không tồn tại"
        }) , 404
    
    return jsonify(dict(farm))



    












