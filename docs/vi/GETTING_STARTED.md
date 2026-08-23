# Bắt đầu

Yêu cầu Python 3.10 trở lên và một checkout mà bạn có quyền kiểm tra. Auditor không cần dependency runtime, GitHub token hay kết nối mạng.

## Chạy từ source

```bash
git clone https://github.com/thangldw/awesome-maintainer-defense.git
cd awesome-maintainer-defense
make standalone
python3 dist/maintainer-defense-kit.py audit .
```

Auditor chỉ đọc file policy, workflow và Git metadata cục bộ; không chạy mã và không ghi vào target.

## Cài bằng pipx

```bash
pipx install maintainer-defense-kit==1.1.1
maintainer-defense audit /path/to/repository
```

## Đọc kết quả

Mỗi finding có severity, rule ID ổn định, vị trí, bằng chứng, threat scenario và remediation đề xuất. Trước khi chấp nhận finding, kiểm tra file còn hoạt động hay không và control tương đương có nằm ngoài checkout hay không.

```bash
maintainer-defense audit . --format json --output maintainer-defense.json
maintainer-defense audit . --format sarif --output maintainer-defense.sarif
maintainer-defense audit . --fail-on high
```

`--fail-on` trả exit 2 nếu báo cáo hiệu lực có finding bằng hoặc cao hơn ngưỡng; input/config lỗi trả exit 1.

## Tạo patch để review

```bash
maintainer-defense fix . --output recommended.patch
git apply --check recommended.patch
```

Lệnh không áp dụng patch. Hãy review, test và xin phê duyệt theo quy trình của repo.

Đọc tiếp: [An toàn](SAFETY.md), [Playbook](PLAYBOOK.md) và [CLI canonical bằng English](../AUDITOR.md).
