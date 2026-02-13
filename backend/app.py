from sched import scheduler
from flask import Flask
from flask_cors import CORS

# import blueprints
from routes.user_routes import user_bp
from routes.subscription_routes import subscription_bp
from apscheduler.schedulers.background import BackgroundScheduler
from services.subscription_service import check_subscription_expiry_and_notify

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(subscription_bp)
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_subscription_expiry_and_notify, 'interval', minutes=1)
    scheduler.start()

    # Root route (just to test server)
    @app.route("/")
    def home():
        return {"message": "Smart Power V2 running"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
