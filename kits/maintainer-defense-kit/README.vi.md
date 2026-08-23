# Maintainer Defense Kit

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

Kit cài policy có thể rollback và workflow chỉ đọc. Mặc định chỉ preview; chế độ apply không ghi đè nội dung khác, ghi ownership/hash, chặn path hoặc symlink không an toàn và không xoá file đã bị sửa.

## Profile

| Profile | Tác động runtime |
| --- | --- |
| `observe` | Phân tích PR chỉ đọc và job summary; không có tác động nhìn thấy bởi contributor |
| `balanced` | Cùng signal contract và một status check có thể fail; không comment, label, close hay lock |
| `hardened` | `balanced` cộng dependency review và phân tích tĩnh GitHub Actions |

Mỗi profile cài bug form, PR template, policy, playbook, đặc tả nhãn thủ công tuỳ chọn và adoption record bằng English, Vietnamese hoặc Japanese.

## Preview, apply, verify

```bash
python3 scripts/install_kit.py --target /duong/dan/du-an --profile observe --language vi --repo OWNER/REPOSITORY
python3 scripts/install_kit.py --target /duong/dan/du-an --profile observe --language vi --repo OWNER/REPOSITORY --apply
python3 scripts/install_kit.py --target /duong/dan/du-an --verify
```

Installer chỉ ghi file cục bộ; không gọi GitHub, tạo label, đặt required check, commit hay push. Repository owner tự cấu hình setting trực tuyến.

## Rollback

```bash
python3 scripts/install_kit.py --target /duong/dan/du-an --uninstall
```

Uninstall chỉ xoá file nguyên vẹn do installer sở hữu và dừng nếu file đã bị sửa. Bắt đầu bằng `observe`; chỉ chuyển sang status gate sau khi lấy mẫu đại diện, owner phê duyệt, có appeal và rollback đã test. Đọc [giới hạn an toàn](../../docs/vi/SAFETY.md) và [playbook](../../docs/vi/PLAYBOOK.md).
