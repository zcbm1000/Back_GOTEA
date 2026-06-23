from flask import Blueprint, render_template ,request, redirect, session
from utils.json_manager import load_members, save_members

member_bp = Blueprint(
    'member',
    __name__,
    url_prefix='/member'
)

# 회원가입 STAER
@member_bp.route('/signup_form')
def signup_form():
    return render_template('member/signup_form.html')

@member_bp.route('/signin_form')
def signin_form():

    result = request.args.get('result')

    return render_template('signin_form.html', result = result)


@member_bp.route('/signup_confirm', methods=['POST'])
def signup_confirm():
    mId = request.form['mId']
    mName = request.form['mName']
    mPw = request.form['mPw']  
    mMail = request.form['mMail'] 
    mPhone = request.form['mPhone']

    role = 'user'
    isApproved = 'pending'

    members = load_members()

    if mId in members:
        return render_template('member/signup_confirm', result='NG')

    members[mId] = {
        'mId':mId,
        'mName':mName,
        'mPw':mPw,
        'mMail':mMail,
        'mPhone':mPhone,
        'role':role,
        'isApproved':isApproved
    }

    save_members(members)

    return render_template('/', result='ok')

# 회원가입 END

# 로그인 STAER
@member_bp.route('/signin_confirm', methods=['POST'])
def signin_confirm():
    mId = request.form['mId']
    mPw = request.form['mPw']

    members = load_members()

    if mId in members and members[mId]['mPw'] == mPw:
        session['signinedMembrId'] = mId
        return redirect ('/')
    
    return redirect('/member/signin_form?result=fail')

# 로그인 END

# 관리자 권한
@member_bp.route('/transaction_history_form')
def transaction_history_form():

    mData = load_members()

    mId = mData[userId]['mId']
    userId = session.get('signInedMemberId')

    mName = mData[userId]['mName']
    mMail = mData[userId]['mMail']
    role = mData[userId]['role']
    isApproved = mData[userId]['isApproved']

    if userId is None:
        return redirect ('/')
    elif role == 'admin':
        return render_template(
            'member/admin_home.html', 
            mId=mId, 
            mName=mName,
            mMail = mMail,
            isApproved = isApproved)