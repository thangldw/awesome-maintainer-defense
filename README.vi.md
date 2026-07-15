# Awesome Maintainer Defense

> Audit repository trước. Chỉ cài điều bạn hiểu. Mọi biện pháp thực thi phải đảo ngược được.

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Quality](https://github.com/thangldw/awesome-maintainer-defense/actions/workflows/quality.yml/badge.svg)](https://github.com/thangldw/awesome-maintainer-defense/actions/workflows/quality.yml)
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Dự án cung cấp một hệ thống phòng vệ thống nhất: auditor offline, kit có thể rollback, catalog có bằng chứng và policy/template triển khai được. Dự án **chống lạm dụng, không chống AI**; finding là đầu vào để review, không phải bằng chứng về tác giả hay ý định.

## Audit trước

Tải CLI v1.0 không có dependency và kiểm tra checksum. Audit không dùng mạng hay GitHub token.

```bash
curl -fLO https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.0/maintainer-defense-kit.py
curl -fLO https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.0/maintainer-defense-kit.py.sha256

sha256sum -c maintainer-defense-kit.py.sha256
# macOS: shasum -a 256 -c maintainer-defense-kit.py.sha256

python3 maintainer-defense-kit.py audit .
python3 maintainer-defense-kit.py audit . --format sarif > maintainer-defense.sarif
python3 maintainer-defense-kit.py fix . --output recommended.patch
```

`fix` chỉ sinh unified diff; không sửa file, GitHub setting, commit hay push. Xem [auditor reference](docs/AUDITOR.md) và [pilot trên repository công khai](docs/AUDITOR_PILOT.md).

## Cài profile phòng vệ

Preview là mặc định. Chỉ thêm `--apply` sau khi review toàn bộ file đích.

```bash
python3 maintainer-defense-kit.py --target . --profile observe --language vi --repo OWNER/REPOSITORY
python3 maintainer-defense-kit.py --target . --profile observe --language vi --repo OWNER/REPOSITORY --apply
python3 maintainer-defense-kit.py --target . --verify
```

![Demo terminal 35 giây: dry-run, cài observe, verify rồi uninstall](assets/demo.gif)

## Chọn bước tiếp theo

| Trạng thái | Hành động |
| --- | --- |
| Chưa có baseline | Review [native controls](docs/NATIVE_CONTROLS.md), rồi chạy audit |
| Tải contribution bình thường | Cài `observe`; chưa tạo tác động nhìn thấy với contributor |
| Review overload đã đo được | Cân nhắc `balanced`; giữ human review và đường khiếu nại |
| Có rủi ro supply chain | Dùng `hardened`; review pin, token và dependency policy |
| Đang có incident | Theo [playbook tiếng Việt](docs/vi/PLAYBOOK.md); mọi giới hạn phải có thời hạn |

Xem [documentation hub](docs/README.md) để đi tới product reference, operations, evidence và deployable assets.

## Tài nguyên

Catalog được sinh từ [`catalog.json`](catalog.json); bản dịch nằm trong [`i18n/vi.json`](i18n/vi.json). ⭐ là điểm bắt đầu thực dụng, không phải xếp hạng hay vị trí trả phí.

<!-- catalog:start -->

### Phát hiện lạm dụng & kiểm duyệt

Phát hiện, gắn nhãn, cách ly hoặc xử lý spam, quấy rối và contribution tự động chất lượng thấp.

| Tài nguyên | Loại | Giấy phép | Giá trị chính |
| --- | --- | --- | --- |
| [Niubi Guard](https://github.com/Albert-Weasker/niubi_guard) ⭐ | công cụ | Apache-2.0 | Hệ thống phát hiện và xử lý lạm dụng repository, bao gồm spam, quấy rối và tấn công phối hợp. |
| [Anti Slop](https://github.com/peakoss/anti-slop) ⭐ | GitHub Action | AGPL-3.0 | GitHub Action có thể cấu hình để phát hiện và đóng pull request chất lượng thấp hoặc AI-slop. |
| [GitHub AI Moderator](https://github.com/github/ai-moderator) | GitHub Action | MIT | Action dùng model để gắn nhãn spam, link spam và nội dung mà model suy đoán do AI tạo. |
| [AI Community Moderator](https://github.com/benbalter/ai-community-moderator) | GitHub Action | MIT | Kiểm duyệt tương tác cộng đồng dựa trên hướng dẫn contribution và code of conduct của dự án. |
| [AI Assessment Comment Labeler](https://github.com/github/ai-assessment-comment-labeler) | GitHub Action | MIT | Action tiếp nhận issue, lấy đánh giá từ AI và áp dụng các nhãn có thể cấu hình. |

### Niềm tin contributor & kiểm soát gia nhập

Dùng vouch công khai hoặc lịch sử contribution để kiểm soát quyền tham gia mà không đóng cửa dự án với tất cả mọi người.

| Tài nguyên | Loại | Giấy phép | Giá trị chính |
| --- | --- | --- | --- |
| [Fossier](https://github.com/PThorpe92/fossier) | công cụ | MIT | Workflow và CLI tương thích với Vouch để giảm spam pull request không được yêu cầu. |
| [Vouch](https://github.com/mitchellh/vouch) ⭐ | công cụ | MIT | Quản lý niềm tin cộng đồng bằng vouch công khai trước khi một người được phép tham gia. |
| [Good Egg](https://github.com/2ndSetAI/good-egg) | GitHub Action | MIT | Chấm điểm tác giả pull request dựa trên lịch sử contribution của họ trên GitHub. |

### Tiếp nhận & phân loại

Giảm tải review bằng biểu mẫu có cấu trúc, nhãn, tự động hóa vòng đời và cơ chế lockdown khẩn cấp.

| Tài nguyên | Loại | Giấy phép | Giá trị chính |
| --- | --- | --- | --- |
| [Labeler](https://github.com/actions/labeler) | GitHub Action | MIT | Action chính thức để gắn nhãn pull request theo file thay đổi và mẫu tên branch. |
| [Stale](https://github.com/actions/stale) | GitHub Action | MIT | Action chính thức để đánh dấu và tùy chọn đóng issue hoặc pull request không còn hoạt động. |
| [Lock Threads](https://github.com/dessant/lock-threads) | GitHub Action | MIT | Khóa issue, pull request và discussion đã đóng sau một khoảng thời gian có thể cấu hình. |
| [Repo Lockdown](https://github.com/dessant/repo-lockdown) ⭐ | GitHub Action | MIT | Action khẩn cấp đóng và khóa ngay issue hoặc pull request mới. |
| [Issue Metrics](https://github.com/github-community-projects/issue-metrics) | GitHub Action | MIT | Đo thời gian phản hồi của issue, pull request và discussion rồi tạo báo cáo Markdown. |

### Quản trị repository & quyền truy cập

Giữ chính sách bảo mật, branch protection và thiết lập repository nhất quán giữa nhiều dự án.

| Tài nguyên | Loại | Giấy phép | Giá trị chính |
| --- | --- | --- | --- |
| [OpenSSF Allstar](https://github.com/ossf/allstar) ⭐ | GitHub App | Apache-2.0 | Liên tục kiểm tra và thực thi chính sách bảo mật trên các GitHub organization. |
| [Safe Settings](https://github.com/github-community-projects/safe-settings) ⭐ | GitHub App | ISC | Quản lý tập trung thiết lập repository, branch protection và team, có dry-run cho pull request. |
| [Repository Settings App](https://github.com/repository-settings/app) | GitHub App | ISC | Đồng bộ thiết lập repository từ file `.github/settings.yml` được quản lý bằng version control. |

### Bảo vệ workflow & chuỗi cung ứng

Bảo vệ CI, dependency, secret và đường merge khỏi contribution độc hại hoặc bị xâm nhập.

| Tài nguyên | Loại | Giấy phép | Giá trị chính |
| --- | --- | --- | --- |
| [Harden-Runner](https://github.com/step-security/harden-runner) ⭐ | GitHub Action | Apache-2.0 | Theo dõi network egress, tính toàn vẹn file và tiến trình trên GitHub-hosted runner. |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) ⭐ | công cụ | Apache-2.0 | Kiểm tra tự động tình trạng bảo mật của dự án mã nguồn mở và dependency. |
| [zizmor](https://github.com/zizmorcore/zizmor) ⭐ | công cụ | MIT | Phân tích tĩnh các vấn đề bảo mật và tính đúng đắn trong GitHub Actions workflow. |
| [pinact](https://github.com/suzuki-shunsuke/pinact) | công cụ | MIT | Ghim GitHub Action và reusable workflow vào commit hash bất biến. |
| [Dependency Review Action](https://github.com/actions/dependency-review-action) ⭐ | GitHub Action | MIT | Chặn pull request đưa vào dependency có lỗ hổng hoặc giấy phép không được phép. |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | công cụ | AGPL-3.0 | Tìm và xác minh credential bị lộ trước khi trở thành sự cố cho maintainer. |
| [PRevent](https://github.com/apiiro/PRevent) | GitHub App | MIT | Phát hiện thay đổi pull request đáng ngờ có thể cho thấy mã độc. |
| [OSV-Scanner](https://github.com/google/osv-scanner) ⭐ | công cụ | Apache-2.0 | Quét lockfile, SBOM và source artifact bằng cơ sở dữ liệu lỗ hổng OSV. |
| [Gitleaks](https://github.com/gitleaks/gitleaks) ⭐ | công cụ | MIT | Phát hiện secret trong lịch sử Git, thư mục, file và standard input. |

### Chính sách & playbook

Đặt kỳ vọng trước khi có sự cố và phản ứng nhất quán khi sự cố xảy ra.

| Tài nguyên | Loại | Giấy phép | Giá trị chính |
| --- | --- | --- | --- |
| [Open Source AI Contribution Policies](https://github.com/melissawm/open-source-ai-contribution-policies) ⭐ | danh sách | CC0-1.0 | Catalog so sánh cách các dự án mã nguồn mở quản lý contribution do AI tạo. |
| [OpenSSF AI-Slop Best-Practices Work Item](https://github.com/ossf/wg-vulnerability-disclosures/issues/178) | nhóm làm việc | N/A | Work item đang mở để xây dựng thực hành cho báo cáo bảo mật và contribution AI chất lượng thấp; chưa phải tiêu chuẩn hoàn chỉnh. |

<!-- catalog:end -->

## Hợp đồng an toàn

- Đánh giá chất lượng và rủi ro repository, không đoán tác giả.
- Không chạy code không tin cậy với secret hoặc write token.
- Bắt đầu bằng quan sát; chỉ thực thi khi có bằng chứng.
- Công bố rule, owner, review date, rollback và đường khiếu nại.
- Không xem scanner result hay catalog listing là chứng nhận bảo mật.

Đọc [hồ sơ đảm bảo tiếng Việt](docs/vi/KIT_ASSURANCE.md) trước khi dùng production. Template là điểm khởi đầu, không phải tư vấn pháp lý. Dự án dùng [MIT License](LICENSE).
