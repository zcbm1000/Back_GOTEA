from flask import Flask, render_template, request
from blueprints.member.routes import member_bp
from blueprints.dashboard.routes import dashboard_bp

app = Flask(__name__)

app.register_blueprint(member_bp)
# app.register_blueprint(dashboard_bp)
app.secret_key = 'your_very_secret_and_unique_string_here'

# 메인
@app.route('/')
def main_home():
    result = request.args.get('result')
    return render_template('main_home.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')