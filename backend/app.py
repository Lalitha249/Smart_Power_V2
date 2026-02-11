from flask import Flask
from flask_cors import CORS

# import blueprints
from routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(user_bp)

    # Root route (just to test server)
    @app.route("/")
    def home():
        return {"message": "Smart Power V2 running"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
