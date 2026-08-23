# Pilot và consent

Pilot chỉ bắt đầu khi maintainer hoặc người đại diện được uỷ quyền cung cấp repo public, full commit SHA, vai trò reviewer và mức công bố qua [pilot issue form](https://github.com/thangldw/awesome-maintainer-defense/issues/new?template=auditor-pilot.yml). Repo public hoặc sự im lặng không phải consent công bố.

Auditor chạy offline trên revision đã pin, không chạy code và không sửa target. Reviewer phân loại từng finding là true positive, false positive, not applicable hoặc unresolved; raw report và report sau suppression được giữ riêng.

Chỉ công bố trường dữ liệu đúng với lựa chọn disclosure. Loại bỏ secret, personal data và nội dung private. Pilot do chủ dự án tự chạy phải ghi rõ không độc lập và không đại diện; nó chỉ chứng minh khả năng tái tạo workflow, không chứng minh field accuracy.

Không tạo score, ranking hoặc hồ sơ contributor. Hợp đồng đầy đủ nằm trong [pilot program bằng English](../AUDITOR_PILOT_PROGRAM.md); bundle đã công bố nằm tại [pilot evidence](../../pilots/README.md).
