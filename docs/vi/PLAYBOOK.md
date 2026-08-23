# Playbook bảo vệ maintainer

## 1. Triage

Lưu URL, revision, workflow run, timestamp và bằng chứng đã loại dữ liệu nhạy cảm. Tách security report khỏi public intake. Phân loại rủi ro trước mắt: flood, unsafe workflow, lộ credential, destructive automation hoặc governance gap. Không suy diễn tác giả hay ý định từ danh tính và phong cách.

## 2. Review

Đối chiếu finding với file đang hoạt động và context của repo. Kiểm tra ruleset, policy tổ chức hoặc setting bên ngoài có thay đổi applicability không. Với workflow, lần theo untrusted input đến nơi thực thi hoặc authority.

## 3. Phê duyệt

Chỉ định owner; ghi control, permission, nơi nhận dữ liệu, tác động với contributor, exception, appeal, review date và rollback chính xác. Control tác động cao cần repo owner phê duyệt; đề xuất từ auditor không phải authorization.

## 4. Rollout

Bắt đầu bằng local audit và profile `observe`. Chạy test đại diện, lấy mẫu cả item bị flag và không bị flag. Ưu tiên routing trung tính và status check. Chỉ bật close, lock, block, delete hoặc interaction limit khi có nhu cầu đo được, human review và thời hạn.

## 5. Incident và recovery

Chỉ định incident owner, dừng automation chưa chắc chắn, bảo toàn bằng chứng nhưng không đưa secret vào log public. Cô lập untrusted execution, revoke credential, vô hiệu artifact và dùng control có thời hạn. Sau đó rollback, mở lại item hợp lệ, bỏ restriction đúng lịch và ghi retrospective không đổ lỗi.

Mỗi control cần adoption record gồm owner, ngày, profile, signal window, findings, false positives, appeals, quyết định threshold, rollback trigger và review date. Thiếu owner, review date hoặc rollback đã test thì quay về observe.
