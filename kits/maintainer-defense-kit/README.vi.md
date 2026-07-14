# Maintainer Defense Kit

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

Baseline có thể cài và rollback để giảm tải review nhưng không tuyên bố phát hiện nội dung do AI tạo. Installer mặc định dry-run, không ghi đè file khác nội dung, ghi hash của từng file và có thể xác minh hoặc gỡ chính xác phần do nó tạo.

## Profile

| Profile | Quyền token | Tác động |
| --- | --- | --- |
| `observe` (mặc định) | chỉ đọc | Chỉ ghi job summary; dùng để đo tín hiệu và false positive |
| `balanced` | ghi PR | Chỉ thêm `needs-human-review`; không comment, close hay lock |
| `hardened` | theo từng job | `balanced` cộng dependency review và phân tích tĩnh workflow |

Mọi profile đều cài issue form, PR template, policy, playbook, đặc tả nhãn và hồ sơ triển khai bằng `en`, `vi` hoặc `ja`.

## Cài đặt an toàn

Chạy từ repository này. Lệnh đầu chỉ xem trước:

```bash
python3 scripts/install_kit.py --target /duong/dan/du-an --profile observe --language vi --repo OWNER/REPOSITORY
python3 scripts/install_kit.py --target /duong/dan/du-an --profile observe --language vi --repo OWNER/REPOSITORY --apply
python3 scripts/install_kit.py --target /duong/dan/du-an --verify
```

Trước khi dùng `balanced` hoặc `hardened`, tạo nhãn trung lập mà workflow yêu cầu:

```bash
gh label create needs-human-review --repo OWNER/REPOSITORY --color D4C5F9 --description "Hàng đợi trung lập để maintainer review"
```

## Rollback

```bash
python3 scripts/install_kit.py --target /duong/dan/du-an --uninstall
```

Uninstall chỉ xóa file installer đã tạo và từ chối nếu file đó đã bị sửa. Installer không gọi GitHub API, tạo nhãn, đổi setting hay commit code. Action được ghim bằng commit SHA và theo dõi trong [`pins.json`](../../pins.json).

Đây là baseline đã được test kỹ thuật, không phải chứng nhận bảo mật. [Hồ sơ đảm bảo](../../docs/vi/KIT_ASSURANCE.md) nêu rõ phần đã đảm bảo và phần chưa có bằng chứng thực địa.
