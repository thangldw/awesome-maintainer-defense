# Playbook bảo vệ maintainer

## Cấp 0 — Nền tảng

- Công bố policy contribution, AI hỗ trợ, unsolicited PR, code of conduct và báo cáo bảo mật.
- Yêu cầu bug report có phiên bản, môi trường, reproduction tối thiểu, kết quả thực tế và kỳ vọng.
- Bảo vệ `.github/`, release workflow, package manifest và file ownership bằng CODEOWNERS và review bắt buộc.
- Dùng ruleset cho review, status check, chống xóa và force-push.
- Đặt quyền `GITHUB_TOKEN` rõ ràng theo từng job và ghim Action bên thứ ba vào commit SHA đã review.
- Bật private vulnerability reporting và xác định ai được kích hoạt chế độ sự cố.

## Cấp 1 — Quan sát

- Đo số submission, thời gian phản hồi, lý do đóng, item được mở lại và giờ review.
- Chạy công cụ mới ở dry-run/report-only ít nhất hai chu kỳ review đại diện.
- Lấy mẫu cả item bị gắn cờ và không bị gắn cờ để thấy false negative.
- Ghi false positive theo loại contributor, ngôn ngữ, khu vực code và lý do.
- Không kết luận một người độc hại hoặc dùng AI chỉ dựa trên điểm số.

Chỉ chuyển cấp khi team mô tả được vấn đề, chi phí mỗi tuần, tín hiệu hữu ích và ngưỡng false positive chấp nhận được.

## Cấp 2 — Review-first

- Dùng nhãn trung lập như `needs-human-review`.
- Tắt auto-close, lock, block và cáo buộc công khai.
- Chỉ miễn trừ maintainer, bot được duyệt, contributor quen thuộc và automation phát hành khi có lý do.
- Mọi hành động tác động cao cần quyết định của con người.
- Công bố đường khiếu nại ngắn dựa trên bằng chứng mới.

[Balanced starter kit](../../kits/balanced) triển khai mức này cho PR triage.

## Cấp 3 — Chế độ sự cố

1. Chỉ định incident owner và mở decision log có timestamp.
2. Lưu URL, screenshot, webhook delivery ID, workflow run ID và audit log; không chép secret vào log.
3. Tạm dừng automation rủi ro và release nếu tính toàn vẹn chưa chắc chắn.
4. Giới hạn tương tác tạm thời cho existing users, contributors hoặc collaborators.
5. Chỉ close/lock đúng nhóm submission bị ảnh hưởng; mọi kiểm soát rộng phải có hạn dùng.
6. Block hoặc báo cáo abuse khi hành vi vi phạm quy tắc nền tảng, không chỉ vì bất đồng kỹ thuật.
7. Rotate credential bị lộ, vô hiệu artifact và kiểm tra lịch sử workflow khi có khả năng compromise.
8. Thông báo trạng thái ngắn gọn, không khuếch đại quấy rối hoặc công khai bằng chứng nhạy cảm.

## Cấp 4 — Phục hồi

- Gỡ interaction limit và lockdown đúng lịch.
- Mở lại item hợp lệ bị ảnh hưởng bởi kiểm soát rộng.
- Thông báo cho contributor khi false positive tạo hành động công khai.
- So sánh tải review, báo cáo hợp lệ bị bỏ sót, false positive và thời gian phục hồi với baseline.
- Chỉ chuyển kiểm soát đã chứng minh hiệu quả thành policy dài hạn.
- Viết retrospective không đổ lỗi, tách hành vi tấn công, giới hạn nền tảng, lỗi cấu hình và năng lực maintainer.

Mỗi automation phải có owner, mục tiêu đo được, quyền, data boundary, hành động tác động cao, ngày review và cách rollback. Không nên giữ enforcement nếu thiếu một trong các mục này.
