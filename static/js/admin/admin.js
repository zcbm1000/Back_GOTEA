//  회원삭제 로직
function deleteMember(mId) {
    let isDelete = confirm("정말로 삭제하시겠습니까?");

if (isDelete) {
        fetch('/member/delete_member', {
            method: 'POST',
            body: new URLSearchParams({ 'mId': mId })
        })
        .then(response => {
            alert(mId + " 회원 삭제가 완료되었습니다.");
            location.reload(); 
        });
        
    } else {
        alert("삭제가 취소되었습니다.");
    }
}
