# Maintainer Defense Kit — hồ sơ đảm bảo

**Trạng thái:** baseline đã được xác minh kỹ thuật; chưa phải chứng nhận bảo mật và chưa được kiểm chứng trên tập repository công khai đại diện.

“Defense” ở đây là giảm chi phí review và đường tự động hóa không an toàn, không phải xác định contribution do người hay AI tạo.

## Đã được đảm bảo bằng test

- `observe` dùng sự kiện `pull_request`, token chỉ đọc, không checkout code PR và không comment, gắn nhãn, close hay lock.
- Installer mặc định dry-run, kiểm tra conflict trước khi ghi, không overwrite, lưu SHA-256 và ownership trong manifest.
- Uninstall chỉ xóa file installer tạo và dừng nếu file đã sửa; đường dẫn vượt repository, manifest độc hại và symlink đều bị từ chối.
- `balanced` và `hardened` chỉ có thể làm fail một status check có tên; không comment, gắn nhãn, close, lock, merge hay chạy code PR.
- Baseline tắt rõ ràng các proxy về username, tuổi tài khoản, số lần fork, profile công khai/đầy đủ, lịch sử merge toàn cục, emoji và danh tính commit author.
- Mọi Action dùng commit SHA đầy đủ, có record trong `pins.json`; tag upstream và trạng thái commit verified được kiểm tra định kỳ.
- Ma trận end-to-end kiểm tra 3 profile × 3 ngôn ngữ, cùng conflict, rollback, file đã sửa, file có sẵn, manifest độc hại và symlink.

## Sửa lỗi từ audit lần hai

Workflow cũ có thể comment lặp lại, việc gắn nhãn có thể thất bại âm thầm và default upstream chứa nhiều proxy danh tính/lịch sử không phù hợp quality-first. Bản sửa label-only đầu tiên vẫn dùng `pull_request_target`; zizmor đã từ chối đúng vì trust boundary đặc quyền. Thiết kế cuối dùng `pull_request` chỉ đọc, không comment/gắn nhãn, tắt các proxy và biến output được kiểm soát thành status gate. Issue form cũng không còn phụ thuộc nhãn chưa khai báo.

## Chưa được đảm bảo

- Không detector nào trong repo chứng minh chắc chắn tác giả AI, ý định hay chất lượng contributor.
- Chưa có dataset thực địa đã review quyền riêng tư để đo precision, recall, false positive, thời gian maintainer tiết kiệm hay tỷ lệ contributor bỏ cuộc.
- Commit upstream được xác minh không đồng nghĩa mã Action bên thứ ba đã được audit toàn diện.
- GitHub setting, ruleset, sự tồn tại của nhãn và private vulnerability reporting nằm ngoài quyền của installer.
- Bản dịch Việt/Nhật có test cấu trúc nhưng chưa được chuyên gia bảo mật/pháp lý bản ngữ review độc lập.
- Đây không phải control tuân thủ, tư vấn pháp lý, SLA hay bảo hành.

## Cổng chấp nhận production

Chỉ chuyển khỏi `observe` khi đã: rà soát native control; chỉ định owner, review SLA, kênh khiếu nại và người tắt khẩn cấp; ghi baseline; test status gate cả trường hợp fail và hồi phục; review false positive bằng người thật; và tất cả verification/CI đều pass.

Kết luận trung thực: **cài đặt, quyền, rollback, pinning và localization đã được test; hiệu quả kiểm duyệt ngoài thực tế chưa được đảm bảo**.
