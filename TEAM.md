# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng):
- Lớp: `L3A` / `L3B`
- Repo của bàn: `K5-<L3A|L3B>-DAY10-<TenNhom>-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Trần Quốc Đông |2A202603643| Kỹ sư cổng|Đông|
|   2 |Vương Xuân Dương|2A202603703| Sản phẩm và kinh doanh |             |
|   3 |Nguyễn Minh Thông|2A202603637| Vận hành và pháp lý|             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Phân công cho nhóm 3 thành viên

Cài đặt (README mục 2) đã hoàn thành theo thông tin của nhóm. Công việc tiếp theo bắt đầu từ Phiếu A.
TV1, TV2, TV3 tương ứng ba dòng trong bảng thành viên; điền tên và MSSV thật trước khi nộp.
Người phụ trách Python nhận TV1. Ba người cùng chốt mọi ngưỡng và quyết định v1/v2.

Đầu vào chung: [eval card Lab 9 do nhóm cung cấp](docs/eval_card.md), một PRD v1.1 từ Lab 9, `problem-set.md`, `data/world.json` và ba phiếu trong `templates/`.
PRD v1.1 chưa có trong repo hiện tại; TV2 phụ trách tiếp nhận và đối chiếu mục tiêu, bên liên quan, yêu cầu khi tài liệu được cung cấp.

### TV1 — Kỹ sư cổng

- **Phiếu A:** viết **A2 / câu 1.3** (offline metric cho một bước); soát định nghĩa, mẫu số, nguồn dữ liệu và khả năng kiểm tra các ngưỡng ở A4. Sau khi cả nhóm đồng ý, chạy ký tiêu chí, commit và push; ghi giờ, hash/commit vào **A5**.
- **Đo vòng 1:** chạy baseline, gate và trace `T-002@55`; điền **B0–B2 / câu 2.1–2.2**, gồm khuyến nghị tự chặn/người duyệt/kết hợp. Bàn giao mã chạy, ticket@seed, dòng trace, số liệu tổng và theo kho/hãng cho TV2, TV3.
- **Cổng vòng 1:** từ pre-mortem và HAZOP chung, viết **2–3 cổng** trong `lab10/guards.py` (`pre_guard`, `write_gate`); điền **B7.1–B7.2 / câu 2.6–2.7**. Cùng TV3 thiết kế tính chất và hai ticket hiểm; TV1 chạy `--adhoc`, dán kết quả vào **B7.3 / câu 2.8**. Chạy eval kiểm cổng và public tests.
- **Chốt vòng 1:** sau khi code và toàn bộ config đã thống nhất, chạy `lab10.checkpoint`, eval bộ nền ở mốc `prepared`, rồi gate. Cung cấp bằng chứng cho B8; thực hiện commit/push mốc vòng 1.
- **Sự cố:** sau khi Coach phát thẻ và nhóm bốc số, kéo upstream và chạy `lab10.grade --incident Sx` trước khi sửa vòng 2; ghi **C0**. Dò ít nhất hai ticket hỏng khác kiểu, viết **C2 / câu 3.1**: ít nhất hai lỗi khác nguồn, có ít nhất một lỗi chìm.
- **Sửa và theo dõi:** sửa `guards.py`, viết phần kỹ thuật của **C7 / câu 3.5**; thêm ít nhất một hàm mới trong `lab10/monitors.py`, đăng ký vào `MONITORS`, điền **C8 / câu 3.6**. Monitor chỉ dùng dữ liệu không có nhãn; `escalation_rate` có sẵn không tính là chỉ số mới. Chạy eval thẻ, eval lại bộ nền và grade.
- **Bàn giao cuối:** gửi report ba mốc, mã chạy, số liệu và nhánh rủi ro còn hở; góp bằng chứng kỹ thuật cho C6/C9 và C12. Chạy `python -m lab10.check_submission --collect`; phối hợp xử lý thiếu sót. Demo cổng, trace, monitor và ticket hiểm.
- **File chính:** `lab10/guards.py`, `lab10/monitors.py`; các mục phiếu kỹ thuật được giao ở trên. Không sửa bộ đo hoặc dữ liệu bị khoá.

### TV2 — Sản phẩm và kinh doanh

- **Phiếu A:** viết **A1 / câu 1.1** (mục tiêu hệ thống), chủ trì **A4 / câu 1.6** và điền `config/acceptance_criteria.json`: năm ngưỡng bắt buộc, một ngưỡng nên có, `business_ops`, điều kiện dừng, bốn dòng `decision_rule`. Cả nhóm duyệt ngưỡng và hai câu ranh giới đầu ra trước khi TV1 ký.
- **Dữ liệu và drift:** viết **B3 / câu 2.3**: trường then chốt, nguồn sự thật/bản sao, một drift cụ thể, thời điểm, chỉ số bị ảnh hưởng và cách phát hiện. Tra `policies`, `orders[].parcels`, `ops_limits`, `ops_facts` trong `data/world.json`.
- **Cổng kinh doanh:** điền phần **`business`** trong `config/operating_gates.json`; viết **B7.4 / câu 2.9**: trần tiền hoàn ngày, ngân sách tiền máy/ticket, phạm vi pilot, ROI. Mỗi con số phải có lý do từ dữ liệu, đồng thời kiểm tra tác động tới chi phí tổng/ticket và hàng chờ cùng TV3.
- **Quyết định v1:** chủ trì **B8**, dùng report `base` và `prepared` của TV1: ba bằng chứng có mã chạy, dòng `decision_rule`, kho/hãng xấu nhất, ngày xem xét lại. Cả nhóm quyết, TV2 ghi lại trước sự cố.
- **Sự cố:** viết specification kiểm được ở **C5 / câu 3.2**; hỗ trợ TV3 phần **C3** liên quan dữ liệu/kinh doanh đúng thẻ. Viết phần sửa `business` trong **C7**; với S5, cùng TV1 thiết kế chỉ số chi phí theo kho ở C8. Phân tích chi phí, ROI, phạm vi và khoản thiệt hại trong report.
- **Quyết định v2:** chủ trì **C12** và ba dòng bắt buộc, dùng số liệu mới nhất của TV1/TV3; ghi rõ đổi hay giữ so với v1, ngưỡng còn trượt, phân khúc xấu nhất, prepared đã đỡ được gì và điều cần đo trong pilot thật. Gửi nội dung đã thống nhất cho TV3 điền `submission.json`.
- **Demo:** giải thích mục tiêu, lý do chọn ngưỡng, chi phí/ROI, quyết định v1/v2 và giới hạn bằng chứng mock.
- **File chính:** `config/acceptance_criteria.json` trước khi ký, phần `business` của `config/operating_gates.json`; A4, B3, B7.4, B8, C5 phần specification, C12.

### TV3 — Vận hành và pháp lý

- **Phiếu A:** viết **A1 / câu 1.2** (mục tiêu của kế toán đối soát và trưởng ca), **A2 / câu 1.4** (telemetry production, khung thời gian, ngưỡng báo động); góp điều kiện dừng và ranh giới dữ liệu/thẩm quyền cho A4.
- **Rủi ro vòng 1:** chủ trì **B4–B5 / câu 2.4**. HAZOP có ít nhất ba dòng trên một tool ghi và thêm ít nhất hai dòng ngoài kỹ thuật; lấy ý kiến TV1 về tool, TV2 về tiền/phạm vi. Checklist đủ chín nhóm, mỗi dòng có trạng thái, bằng chứng và một PIC có tên.
- **Cổng vận hành/pháp lý:** điền phần **`operations` và `legal`** trong `config/operating_gates.json`; viết **B7.5–B7.6 / câu 2.10**: runbook 1–3 và giờ cao điểm. Nêu ai trực/duyệt/dừng, công suất, thời gian chờ, thời hạn dừng, kênh báo, dữ liệu cấm gửi bên thứ ba, điều kiện ghi lỗi hãng. Mã nhân viên trong tình huống lấy từ `data/world.json`, mục `staff`.
- **Behavioral test:** cùng TV1 đặt một tính chất, viết hai ticket mới để thử quy tắc tổng quát, giữ lại cho demo; cùng đọc kết quả B7.3.
- **Sự cố:** ghi số thẻ vào Phiếu C; chủ trì **C3** phần đúng thẻ, **C4** HAZOP sự cố riêng (ít nhất ba dòng, có một nhánh chưa thấy trên trace), **C5 / câu 3.3** giả định môi trường. Với S4, làm phần giờ cao điểm thay cho C3 theo hướng dẫn phiếu.
- **Quản lý rủi ro sau sửa:** tổng hợp **C9** fault tree sau sửa từ phân tích chung; viết **C10** risk register (ít nhất một dòng, có metric/ngưỡng dẫn đến hành động), **C11** checklist cập nhật và runbook 4–5. Viết phần sửa `operations`/`legal` trong C7, giải thích giảm hay ngăn tác hại.
- **Gom và nộp:** điền `submission/submission.json` theo quyết định và ba câu ở C12; soát `team`, `members` dạng `HoVaTen-MSSV`, thẻ, v1/v2. Kiểm đủ các mục phiếu, file và nhật ký khi TV1 chạy collect. Nhắc từng người hoàn thành mục cá nhân và tự nộp link repo trên LMS.
- **File chính:** phần `operations`/`legal` của `config/operating_gates.json`, `submission/submission.json`; B4–B5, B7.5–B7.6, C3–C4, C5 phần môi trường, C9–C11.

### Mốc cả nhóm phải cùng chốt

Các mốc phút là đồng hồ lab trong README, không phải thời lượng tính lại từ lúc chia việc.

| Mốc | Việc chung và điều kiện bàn giao |
|---|---|
| **15–60** | Đọc eval card, chọn chung PRD v1.1; mỗi người viết phần Phiếu A được giao; cùng làm **A3 / câu 1.5**, soát A4 và giải thích từng ngưỡng. |
| **60–65** | TV2 hoàn thiện tiêu chí sau thống nhất; TV1 ký, commit, push và ghi A5. Chỉ chạy đánh giá sau khi commit ký đã push. |
| **65–85** | TV1 đo/trace, TV2 lập bản đồ dữ liệu, TV3 làm HAZOP/checklist; cả nhóm viết **B6 / câu 2.5**, đủ bốn lăng kính, chọn 2–3 nguyên nhân thành cổng. |
| **85–105** | Làm code, `business`, `operations`/`legal` song song theo phần được giao; tích hợp config xong mới đo. TV1 bàn giao mã chạy và các ca còn hỏng. |
| **105–115** | Chốt snapshot vòng 1, đo `prepared`; TV2 ghi B8 theo quyết định chung, TV1 commit/push. Từ đây giữ nguyên snapshot và v1. |
| **125–155** | Nhận đúng thẻ, grade ngay trước sửa; cùng làm **C1 / câu 3.0** và **C6 / câu 3.4**. TV3 tổng hợp fault tree trước sửa, TV1/TV2 cung cấp nhánh kỹ thuật/kinh doanh; mỗi lá có bằng chứng, ít nhất hai nhánh ở hai tầng khác nhau. |
| **155–185** | Sửa đúng code/con số/người; C7 ghi rõ từng thay đổi, mã chạy và giảm hay ngăn. Cùng soát C9, rủi ro còn hở và runbook. TV1 cung cấp kết quả integrity, visible, regression, monitor và các ngưỡng còn trượt. |
| **185–200** | Cùng chốt v2; TV2 ghi C12, TV3 điền `submission.json`, TV1 chạy collect. Sửa các dòng thiếu tới `ĐỦ THÀNH PHẦN`. |
| **200–240** | Demo khoảng 5 phút: TV1 2 phút kỹ thuật, TV2 1,5 phút số liệu/quyết định, TV3 1,5 phút tác hại/runbook. Sau demo trả cấu hình thử về bản v2, chạy lại grade/collect nếu đã thay đổi; push bài cuối. Mỗi người tự viết đóng góp, bằng chứng, exit ticket, việc dùng AI và tự nộp LMS. |

### Dùng eval card Lab 9 trong phân công

Các số dưới đây là kết quả **do nhóm cung cấp trong eval card**, chưa chạy lại trong repo Day 10.

| Đầu vào Lab 9 | Người theo dõi | Việc cần làm ở Day 10 |
|---|---|---|
| Baseline `E-swarm-20261117-f5a5`, SHA `f5a537bbd9c9`; `fixed` đạt gate, `seeded_regression` bị chặn theo card | TV1 + TV2 | Giữ run ID/SHA làm nguồn dẫn cho phân tích trước đo. Bộ Lab 9 có **14 × 5 = 70 trials**; bộ nền Day 10 có **22 × 5 = 110 trials**. Kết quả và CI của hai bộ cần ghi riêng. |
| `C-002@11`: `model_override` tin độ trễ trong ticket thay vì DB; kiểm tiền hoàn và số tiền trả lời | TV1 | Đưa thành giả thuyết rủi ro cho pre-mortem; kiểm tra dữ kiện, quyền ghi và đối chiếu ledger bằng quy tắc tổng quát. Phân tích trace Day 10 `T-002@55` theo dữ liệu thực tế của nó, không coi hai mã ticket là cùng ca. |
| `pass_rate`, `pass_5`, `refund_amount_correct`, `reply_amount_correct` | TV1 + TV2 | Soát định nghĩa và mẫu số trước khi thiết kế metric. `pass_k` Day 10 là pass^k (đúng cả 5/5 seed). `wrongful_refund_vnd` là số tiền hoàn quá mức, không thay cho mọi khía cạnh của hai metric đúng số tiền ở Lab 9. Giữ schema tiêu chí Day 10. |
| `approval_bypass=0`, `secret_leak=0` trên baseline | TV1 + TV3 | Dùng làm yêu cầu an toàn đầu vào; xem riêng phê duyệt và dữ liệu cá nhân gửi bên thứ ba. `secret_leak` Lab 9 không thay thế `pii_leaks` Day 10. |
| `judge_tone` đạt calibration; `judge_helpful` không đạt, recall 0,300 | TV1 + TV3 | Chỉ coi judge tone là bằng chứng về tone trong phạm vi đã kiểm; loại helpful khỏi cổng chặn. Đánh giá số tiền, ledger, phê duyệt bằng dữ kiện và kiểm tra xác định. |
| `cost_per_success=49.5670 VND` trên baseline; chi phí tăng ở seeded regression | TV2 + TV3 | Không dùng trực tiếp làm ngưỡng `cost_per_ticket_vnd_max` hoặc ngân sách tiền máy/ticket: khác mẫu số/phạm vi chi phí. Chọn ngưỡng trước đo từ `ops_facts`, `ops_limits`; sau ký mới đo lại chi phí, ROI, hàng chờ và sức người duyệt. |
| MockLLM, bộ eval nhỏ, calibration replay chưa kiểm trên held-out/người thật | TV2 + TV3 | Đưa vào giả định môi trường, risk register, runbook và ba dòng bắt buộc ở C12; nêu dữ liệu cần đo trong pilot thật. Kết quả `fixed` của Lab 9 không tự quyết định được Gate 1 Day 10. |

### Phối hợp và ràng buộc

- Mỗi người tự viết các mục phiếu được giao; phiếu gốc ở `templates/`. TV3 soát tính đầy đủ, TV1 soát bằng chứng kỹ thuật, TV2 soát số liệu và quyết định. Bản trong `submission/docs/` do collect chép lại.
- TV2 phụ trách `business`, TV3 phụ trách `operations`/`legal` trong cùng file JSON; thống nhất lượt ghi file hoặc hợp nhất thay đổi trước khi TV1 đo. Mọi lần bàn giao nêu khoá, giá trị trước/sau, lý do, mã chạy và mục phiếu liên quan.
- Tiêu chí ký một lần rồi giữ nguyên; snapshot vòng 1 và v1 giữ nguyên sau khi chốt. Chỉ làm thẻ đã bốc, không sửa file bị khoá, không xử lý riêng theo mã ticket/câu chữ.
- Không chặn hết, thu hẹp pilot về 0 hoặc tăng người trực vô lý để làm đẹp report. **Tiếp tục** chỉ được chọn khi bằng chứng và mọi ngưỡng đã ký cho phép; ba quyết định còn lại cần lý do, số liệu và hành động cụ thể.
- Mỗi người phải giải thích được phần mình làm và những con số cả nhóm đã chốt. `ĐỦ THÀNH PHẦN` xác nhận đủ hồ sơ, không thay cho kết luận đạt Gate 1.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
