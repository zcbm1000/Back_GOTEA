from flask import Blueprint, render_template ,request, redirect, session
from utils.json_manager import load_members, save_members

member_bp = Blueprint(
    'member',
    __name__,
    url_prefix='/member'
)

@member_bp.route('/signup_form')
def signup_form():
    return render_template('signup_form.html')

@member_bp.route('', methods=['POST'])
def signup_confirm():
    mId = request.form['mId']                # 회원ID
    mPw = request.form['mPw']                # 회원PW
    mMail = request.form['mMail']            # mMail
    mPhone = request.form['mPhone']          # mPhone
    isApproved = request.form['pending']     # 승인여부

    members = load_members()

    if mId in members:
        return render_template('# 가입되어잇는 아이디입니다.  빨간색 또는 팝업창', result='NG')

    members[mId] = {
        'mId':mId,
        'mPw':mPw,
        'mMail':mMail,
        'mPhone':mPhone,
        'isApproved':isApproved
    }

    save_members(members)

    return render_template('/', result='ok')

