from flask import Blueprint, render_template ,request, redirect, session, url_for, jsonify
from utils.json_manager import load_members, save_members
from email.message import EmailMessage
import random
import smtplib
import datetime


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

    isCurrent = is_current_user_approved()
    members = load_members()

    if mId not in members:
        return redirect('/member/signin_form?result=LOGIN_FAILED')
    
    elif members[mId]['mPw'] != mPw:
        return redirect('/member/signin_form?result=LOGIN_FAILED')

    elif members[mId]['isApproved'] == False:
        return redirect ('/member/signin_form?result=PENDING')
        
    else:
        session['signInedMemberId'] = mId
        return render_template('main_home.html', members=members,isCurrent=isCurrent)
    
def is_current_user_approved():
    member_id = session.get('signInedMemberId')

    if not member_id:
        return False
    
    members = load_members()

    if member_id in members:
        return members[member_id].get('isApproved', False)
    return False

    
# 로그인 END

# 회원정보 수정 STAER
@member_bp.route('/modify_form')
def modify_form():
    members = load_members()
    member = members[session.get('signInedMemberId')]
    return render_template('modify_form.html', member = member)

@member_bp.route('/modify_confirm', methods=['POST'])
def modify_confirm():

    members = load_members()
    mId = session.get('signInedMemberId')

    if mId in members:
        
        mId = request.form['mId']
        mPw = request.form['mPw']
        mMail = request.form['mMail']
        mPhone = request.form['mPhone']

        members = load_members()
        member = members[mId]

        member['mPw'] = mPw
        member['mMail'] = mMail
        member['mPhone'] = mPhone

        save_members(members)
        return render_template('modify_form.html', result = 'ok')
    
# 회원정보 수정 END

# 회원정보 찾기 STAER
@member_bp.route('/id_find_form')
def id_find_form():
    session.pop('is_email_verified', None)
    session.pop('verified_email', None)
    session.pop('otp', None)
    session.pop('otp_email', None)
    session.pop('otp_time', None)
    
    return render_template('member/id_find_form.html')


@member_bp.route('/pw_find_form')
def pw_find_form():
    session.pop('is_email_verified', None)
    session.pop('verified_email', None)
    session.pop('otp', None)
    session.pop('otp_email', None)
    session.pop('otp_time', None)
    
    return render_template('member/pw_find_form.html')


@member_bp.route('/send_verification', methods=['POST'])
def send_verification():
    email_to = request.form.get('mMail')

    if not email_to:
        return jsonify({"status": "error", "message": "이메일 주소가 없습니다."})

    session.pop('otp', None)
    session.pop('otp_email', None)
    session.pop('otp_time', None)
    session.pop('is_email_verified', None)
    session.pop('verified_email', None)

    otp = ''.join(str(random.randint(0, 9)) for _ in range(6))

    session['otp'] = otp
    session['otp_email'] = email_to
    session['otp_time'] = datetime.now().timestamp()

    otpMail = EmailMessage()
    otpMail['Subject'] = "이메일 인증 번호 안내"
    otpMail['To'] = email_to
    otpMail.set_content(f"당신의 인증번호는 [{otp}] 입니다.")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('igoeun126@gmail.com', 'wbyl yhub iatk frsr')
            server.send_message(otpMail)
        return jsonify({"status": "success", "message": "인증번호가 발송되었습니다."})
    except Exception as e:
        print("메일 발송 에러 :", e)
        return jsonify({"status": "error", "message": "메일 발송에 실패했습니다."})


@member_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    user_email = request.form.get('mMail')
    user_otp = request.form.get('otp')

    if not user_email or not user_otp:
        return jsonify({"status": "error", "message": "데이터가 누락되었습니다."})

    saved_otp = session.get('otp')
    saved_email = session.get('otp_email')
    saved_time = session.get('otp_time')

    if not saved_time or datetime.now().timestamp() - saved_time > 180:
        return jsonify({"status": "error", "message": "인증번호가 만료되었습니다."})

    if saved_otp and saved_email == user_email and str(saved_otp) == str(user_otp).strip():
        session['is_email_verified'] = True
        session['verified_email'] = user_email
        session.pop('otp', None)
        session.pop('otp_email', None)
        session.pop('otp_time', None)
        return jsonify({"status": "success", "message": "인증에 성공했습니다."})

    return jsonify({"status": "error", "message": "인증번호가 일치하지 않습니다."})


@member_bp.route('/id_find_confirm', methods=['POST'])
def id_find_confirm():
    if not session.get('is_email_verified'):
        return "<script>alert('이메일 인증이 필요합니다.'); history.back();</script>"

    user_name = request.form.get('mName')
    user_email = request.form.get('mMail')

    if session.get('verified_email') != user_email:
        return "<script>alert('인증한 이메일과 입력한 이메일이 다릅니다.'); history.back();</script>"

    found_id = "test_user_id" 

    if found_id:
        return render_template('id_find_result.html', found_id=found_id)

    return "<script>alert('일치하는 회원 정보가 없습니다.'); history.back();</script>"


@member_bp.route('/pw_find_confirm', methods=['POST'])
def pw_find_confirm():
    if not session.get('is_email_verified'):
        return "<script>alert('이메일 인증이 필요합니다.'); history.back();</script>"

    user_id = request.form.get('mId')
    user_name = request.form.get('mName')
    user_email = request.form.get('mMail')

    if session.get('verified_email') != user_email:
        return "<script>alert('인증한 이메일과 입력한 이메일이 다릅니다.'); history.back();</script>"

    user_exists = True

    if user_exists:
        return render_template('pw_reset_form.html', mId=user_id)

    return "<script>alert('일치하는 회원 정보가 없습니다.'); history.back();</script>"
# 회원정보 찾기 END

# 관리자 권한 화면
@member_bp.route('/transaction_history_form')
def transaction_history_form():

    userId = session.get('signInedMemberId')

    if userId is None:
        return redirect ('/')

    members = load_members()

    if userId not in members:
        return redirect ('/')

    mId = members[userId]['mId']
    mName = members[userId]['mName']
    mMail = members[userId]['mMail']
    role = members[userId]['role']
    isApproved = members[userId]['isApproved']

    if role  != 'admin':
        return redirect ('/')
    
    return render_template(
        'admin_home.html', 
        members=members,
        role=role,
        mId=mId, 
        mName=mName,
        mMail = mMail,
        isApproved = isApproved)

@member_bp.route('/delete_member', methods=['POST'])
def delete_member():
    members = load_members()
    user_id = request.form.get('mId')

    if user_id in members:
        del members[user_id]
        save_members(members)
        session.clear()
        return jsonify({"result": "success"})