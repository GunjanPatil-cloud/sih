import os
import sys

# Ensure backend directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from config import Config


def create_app():
    """Application factory."""
    base_dir = os.path.abspath(os.path.dirname(__file__))

    possible_template_dirs = [
        os.path.join(base_dir, 'templates'),
        os.path.abspath(os.path.join(base_dir, '..', 'frontend', 'templates')),
        os.path.abspath(os.path.join(os.getcwd(), 'frontend', 'templates')),
        os.path.abspath(os.path.join(os.getcwd(), 'backend', 'templates')),
    ]
    template_dir = next((d for d in possible_template_dirs if os.path.isdir(d)), os.path.join(base_dir, 'templates'))

    possible_static_dirs = [
        os.path.join(base_dir, 'static'),
        os.path.abspath(os.path.join(base_dir, '..', 'frontend', 'static')),
        os.path.abspath(os.path.join(os.getcwd(), 'frontend', 'static')),
        os.path.abspath(os.path.join(os.getcwd(), 'backend', 'static')),
    ]
    static_dir = next((d for d in possible_static_dirs if os.path.isdir(d)), os.path.join(base_dir, 'static'))

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
    )
    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_UPLOAD_SIZE

    # Ensure upload directory exists (safe for serverless read-only filesystem)
    try:
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    except OSError:
        pass

    # Register blueprints
    from routes.main import main_bp
    from routes.scan import scan_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(scan_bp)

    return app


# WSGI application instance
app = create_app()

if __name__ == '__main__':
    print(f"\n  ✦ SIH Compliance System running at http://localhost:{Config.PORT}\n")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
