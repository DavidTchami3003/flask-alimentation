from .auth import auth_bp
from .buffet import buffet_bp
from .consommation import conso_bp
from .planning import planning_bp
from .plats import plat_bp

def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(buffet_bp)
    app.register_blueprint(conso_bp)
    app.register_blueprint(planning_bp)
    app.register_blueprint(plat_bp)