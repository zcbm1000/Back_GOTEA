from flask import Blueprint, render_template ,request, redirect, session, url_for
from utils.json_manager import load_members, save_members
from email.message import EmailMessage
import random
import smtplib


member_bp = Blueprint(
    'member',
    __name__,
    url_prefix='/member'
)

# 회원가입 STAER
@member_bp.route('/signup_form')
def signup_form():
    return render_template('member/signup_form.html')

@member_bp.route('/signup_confirm', methods=['POST'])
def signup_confirm():
    mId = request.form['mId']
    mName = request.form['mName']
    mPw = request.form['mPw']  
    mMail = request.form['mMail'] 
    mPhone = request.form['mPhone']

    role = 'user'
    isApproved = False

    members = load_members()

    if mId in members:
        return render_template('member/signup_form.html', result='NG')

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
    
    return redirect('/?result=ok')

# 회원가입 END

# 로그인 STAER
@member_bp.route('/signin_form')
def signin_form():
    result = request.args.get('result')
    return render_template('member/signin_form.html', result = result)

@member_bp.route('/signin_confirm', methods=['POST'])
def signin_confirm():
    mId = request.form['mId']
    mPw = request.form['mPw']

    members = load_members()

    if mId not in members:
        return redirect('/member/signin_form?result=LOGIN_FAILED')
    
    elif members[mId]['mPw'] != mPw:
        return redirect('/member/signin_form?result=LOGIN_FAILED')

    elif members[mId]['isApproved'] == False:
        return redirect ('/member/signin_form?result=PENDING')
        
    else:
        session['signinedMembrId'] = mId
        return render_template('main_home.html')
    
# 로그인 END

# 회원정보 찾기 STAER
@member_bp.route('/find_account_form')
def find_account_form():
    return render_template('find_account_form.html')

@member_bp.route('/send_verification')
def send_verification():

    otpMail = EmailMessage()
    otpMail['Subject'] = "email verification code"
    otpMail['To'] = request.form['mMail']

    session['otp'] =''.join(str(random.randint(0, 9)) for _ in range(6))
    otpMail.set_content(f"당신의 인증번호는 [{session['otp']}] 입니다.") 
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('igoeun126@gmail.com', 'wbyl yhub iatk frsr')
        server.send_message(otpMail)

    return {"status": "success", "message": "인증번호가 발송되었습니다."}

@member_bp.route('/verify_otp')
def verify_otp():
    otpotpsession = session.get('otp')
    otp = request.form['otp']

    if otpotpsession == otp:
        return {"status": "success", "message": "인증 성공!"}
    else:
        {"status": "fail", "message": "인증번호가 맞지 않습니다."}


# 회원정보 찾기 END

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
            'admin_home.html', 
            mId=mId, 
            mName=mName,
            mMail = mMail,
            isApproved = isApproved)
    