# import sentry_sdk
from flask import Flask, render_template
# from sentry_sdk.integrations.flask import FlaskIntegration
from flask_sqlalchemy import SQLAlchemy
# To configure the SDK, initialize it with the integration before or after your app has been initialized:
# sentry_sdk.init(
#     dsn="https://0d00b25a81934bbfb047905ded8997d2@sentry.io/5170498",
#     integrations=[FlaskIntegration()],
#     sample_rate=0.4,
#     max_breadcrumbs=25
# )
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '47LWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)
    
    from altocumulus.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from altocumulus.about import about as about_blueprint
    app.register_blueprint(about_blueprint)
    
    from altocumulus.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from altocumulus.graphs import graphs as graphs_blueprint
    app.register_blueprint(graphs_blueprint)
    
    from altocumulus.feeds import feeds as feeds_blueprint
    app.register_blueprint(feeds_blueprint)
    
    # from altocumulus.upload import upload as upload_blueprint
    # app.register_blueprint(upload_blueprint)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html'), 404

    return app