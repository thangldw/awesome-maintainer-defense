# An toàn và giới hạn

Auditor kiểm tra tĩnh checkout cục bộ. Công cụ không gọi GitHub, không chạy mã repo, không đọc secret và không thay đổi file, Git state, setting, branch hay pull request. `fix` luôn chỉ xuất unified diff để con người review.

Finding không chứng minh exploitability, compromise, authorship, ý định hoặc chất lượng của contributor. Severity phản ánh authority hoặc tác động hợp lý của pattern; reviewer phải xác minh context và control bên ngoài.

Không chạy mã PR không tin cậy trong job có secret, OIDC hoặc write token. Đặt permission mặc định rỗng, pin Action bằng full commit SHA và coi artifact từ PR là dữ liệu không tin cậy. Không dùng danh tính, account age hay lịch sử đóng góp làm bằng chứng rủi ro.

Auditor không thấy live ruleset, branch protection, organization policy, GitHub App, role eligibility, label, private reporting setting hoặc hành vi dịch vụ bên ngoài. Bản audit sạch không có nghĩa toàn bộ repo an toàn.

Security, privacy, support, terms và license bằng [English](../../SECURITY.md) là canonical.
