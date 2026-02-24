import os
from flask import Flask
from flask_cors import CORS

# import blueprints
from routes.user_routes import user_bp
from routes.subscription_routes import subscription_bp
from routes.usage_routes import usage_bp
from apscheduler.schedulers.background import BackgroundScheduler
from services.subscription_service import check_subscription_expiry_and_notify


def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates")
    )

    CORS(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(subscription_bp)
    app.register_blueprint(usage_bp)

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_subscription_expiry_and_notify, 'interval', minutes=1)
    scheduler.start()

    @app.route("/")
    def home():
        return {"message": "Smart Power V2 running"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
