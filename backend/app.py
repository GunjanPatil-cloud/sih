import os
import sys

# Ensure backend directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from config import Config


def create_app():
    """Application factory."""
    frontend_dir = os.path.abspath(os.path.join(Config.BASE_DIR, '..', 'frontend'))
    app = Flask(
        __name__,
        template_folder=os.path.join(frontend_dir, 'templates'),
        static_folder=os.path.join(frontend_dir, 'static'),
    )
    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_UPLOAD_SIZE

    # Ensure upload directory exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    # Register blueprints
    from routes.main import main_bp
    from routes.scan import scan_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(scan_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    print(f"\n  ✦ SIH Compliance System running at http://localhost:{Config.PORT}\n")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
