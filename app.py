import os
from flask import Flask, render_template
from models import db, User, Resume, CoverLetter, Job
from profile_bp import profile_bp
from resume_bp import resume_bp
from cover_bp import cover_bp
from jobs_bp import jobs_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True, static_folder="static", template_folder="templates")
    os.makedirs(app.instance_path, exist_ok=True)

    # Secret key for session
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Auto-create DB tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(resume_bp, url_prefix="/resumes")
    app.register_blueprint(cover_bp, url_prefix="/cover-letters")
    app.register_blueprint(jobs_bp, url_prefix="/jobs")

    # Root page → Dashboard
    @app.route("/", endpoint="dashboard")
    def homepage():
        # Pass resumes, covers, jobs for dashboard
        from models import Resume, CoverLetter, Job
        resumes = Resume.query.all()
        covers = CoverLetter.query.all()
        jobs = Job.query.all()
        return render_template('dashboard.html', resumes=resumes, covers=covers, jobs=jobs)

    # Catch-all route to avoid old login URLs
    @app.route("/<path:path>")
    def catch_all(path):
        resumes = Resume.query.all()
        covers = CoverLetter.query.all()
        jobs = Job.query.all()
        return render_template('dashboard.html', resumes=resumes, covers=covers, jobs=jobs)

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render's port
    app.run(host="0.0.0.0", port=port, debug=True)
