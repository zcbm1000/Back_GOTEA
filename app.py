from flask import Flask, render_template, request
from blueprints.member.routes import member_bp
from blueprints.dashboard.routes import dashboard_bp

app = Flask(__name__)


app.register_blueprint(member_bp)
app.register_blueprint(dashboard_bp)

# 메인
@app.route('/')
def home():
    return render_template('/athta_home')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')