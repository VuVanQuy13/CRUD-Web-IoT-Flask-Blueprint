from flask import Blueprint , render_template

farm_bp = Blueprint('farm', __name__ , url_prefix='/farm' , template_folder='farm_templates')

@farm_bp.route('/<int:farm_id>')
def index(farm_id):
    return render_template('farm.html' , farm_id=farm_id)
