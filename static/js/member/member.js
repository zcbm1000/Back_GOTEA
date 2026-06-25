// 회원가입 js
function signupForm() {
    console.log('signupForm() CALLED!');

    let form = document.signup_form;

    let mId = form.mId.value.trim();
    let mName = form.mName.value.trim();
    let mPw = form.mPw.value.trim();
    let mMail = form.mMail.value.trim();
    let mPhone = form.mPhone.value.trim();
    
    if (mId === '') {
        alert('아이디를 입력 하세요.');
        form.mId.focus();

    } if (mName === '') {
        alert('비밀번호를 입력 하세요.');
        form.mPw.focus();

    } else if (mPw === '') {
        alert('비밀번호를 입력 하세요.');
        form.mPw.focus();

    } else if (mMail === '') {
        alert('이메일을 입력 하세요.');
        form.mMail.focus();

    } else if (mPhone === '') {
        alert('전화번호를 입력 하세요.');
        form.mPhone.focus();
    } else {
        form.submit();
    } 
    
}

// 로그인
function signinForm() {
    console.log('signinForm() CALLED!');

    let form = document.signin_form;

    let mId = form.mId.value.trim();
    let mPw = form.mPw.value.trim();

    if (mId === '') {
        alert('아이디를 입력 하세요.');
        form.mId.focus();

    } else if (mPw === '') {
        alert('비밀번호를 입력 하세요.');
        form.mPw.focus();
    } else {
        form.submit();
    }
}

// 회원정보찾기(ai)
function sendOtp() {
    const emailInput = document.querySelector('input[name="mMail"]').value;

    if (!emailInput) {
        alert("이메일을 먼저 입력해주세요!");
        return;
    }

    const formData = new FormData();
    formData.append('mMail', emailInput);

    fetch('/member/send_verification', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
            
            let timeLeft = 180;

            const 
            timerBox = document.querySelector('#timer');

            setInterval(() => {
            timerBox.innerText = timeLeft;
            timeLeft = timeLeft - 1;
            
            
        }, 1000);
            
        } else {
            alert("발송 실패: " + data.message); 
        }
    })
    .catch(error => {
        console.error("에러 발생:", error);
        alert("서버 통신 중 오류가 발생했습니다.");
    });
}