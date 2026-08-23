# Awesome Maintainer Defense

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

Awesome Maintainer Defense là auditor chạy offline, chỉ đọc và bộ kiểm soát có thể hoàn tác dành cho maintainer. Công cụ kiểm tra policy cục bộ và ranh giới tin cậy của GitHub Actions mà không cần token hay kết nối mạng. Công cụ không chạy mã nguồn của repo, không đọc setting GitHub trực tuyến và không xác định ai đã viết contribution.

## Quickstart

Yêu cầu Python 3.10 trở lên.

```bash
make standalone
python3 dist/maintainer-defense-kit.py audit .
```

Mỗi finding là đầu mối để con người xem xét, không phải bằng chứng repo đã bị xâm nhập hoặc contributor có ý đồ xấu.

## Auditor kiểm tra gì

- Bằng chứng còn thiếu về security policy, ownership, structured intake, cập nhật dependency và kỳ vọng branch protection.
- Token authority quá rộng, Action dùng ref thay đổi được, đường chạy PR input trong privileged workflow, shell interpolation và artifact không an toàn giữa các workflow.
- Moderation có tính phá huỷ, proxy dựa trên danh tính/lịch sử và thiếu đường appeal.

## Từ finding đến patch được review

`fix` chỉ tạo unified diff, không sửa repo:

```bash
python3 dist/maintainer-defense-kit.py fix . --output recommended.patch
git apply --check recommended.patch
```

Chỉ áp dụng patch sau khi maintainer kiểm tra bằng chứng, tác động và CI.

## Giới hạn bằng chứng

Test hiện tại xác minh detection có tính xác định, JSON/SARIF, remediation dạng patch, installer xử lý conflict và các invariant của workflow đi kèm. Dự án không tuyên bố độ chính xác thực địa trên tập repo đại diện, không quan sát setting GitHub trực tuyến và không chứng minh tác giả hay ý định.

## Cài đặt

```bash
pipx install maintainer-defense-kit==1.1.1
maintainer-defense audit .
```

Thông tin checksum và các kênh phát hành nằm trong [tài liệu phân phối bằng tiếng Anh](docs/DISTRIBUTION.md).

## Tài liệu

- [Bắt đầu](docs/vi/GETTING_STARTED.md)
- [An toàn và giới hạn](docs/vi/SAFETY.md)
- [Playbook vận hành](docs/vi/PLAYBOOK.md)
- [Pilot và consent](docs/vi/PILOTS.md)
- [Trung tâm tài liệu](docs/vi/README.md)

## Catalog

[Catalog được tạo từ dữ liệu đã review](docs/CATALOG.md) là tài liệu phụ, không phải chứng nhận hay endorsement. Hãy tự kiểm tra permission, data boundary, tác động tối đa, trạng thái bảo trì và license.

## Điều khoản

Các tài liệu [Security](SECURITY.md), [Support](SUPPORT.md), [Privacy](PRIVACY.md), [Terms](TERMS.md) và [License](LICENSE) bằng tiếng Anh là bản canonical. Nội dung tiếng Việt chỉ hỗ trợ sử dụng sản phẩm, không tạo điều khoản riêng.
