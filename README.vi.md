# Awesome Maintainer Defense — Tiếng Việt

[Tài liệu ba ngôn ngữ](README.md) · [日本語](README.ja.md)

Maintainer Defense Kit là CLI Python chạy offline để kiểm tra policy và ranh giới tin cậy của GitHub Actions. Công cụ không cần network hoặc GitHub token. `fix` chỉ tạo unified diff để người dùng xem xét, không tự sửa file, đổi setting, commit hoặc push.

```bash
python3 scripts/build_standalone.py
python3 dist/maintainer-defense-kit.py audit .
python3 dist/maintainer-defense-kit.py fix . --output recommended.patch
```

Finding là bằng chứng cần con người review, không phải kết luận về tác giả, ý định hoặc độ an toàn. Các workflow nằm bên trong `kits/**/.github/` là asset mẫu của sản phẩm và không chạy trong repo này.

## Catalog đã review

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

Phát hành chuẩn: `v1.1.0`. Giấy phép [MIT](LICENSE).
