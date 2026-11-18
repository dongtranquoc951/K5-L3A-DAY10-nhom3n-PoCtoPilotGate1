# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** `K5-L3A-DAY10-nhom3n-PoCtoPilotGate1` · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Mọi khoản tiền và mọi ghi nhận rời khỏi LogiX qua trợ lý (tiền hoàn cho khách, lỗi ghi cho hãng, thông báo gửi hãng)
> phải khớp với nguồn sự thật (tracking DB, sổ cái, chính sách đang hiệu lực), và khoản nào vượt hạn mức tự động thì luôn
> có người duyệt, **kể cả khi model đọc sai ticket**. Bám PRD v1.1 §3: "chạy đúng" được đo bằng tiền trong sổ cái và
> approval (`approval_bypass` ≤ 0, `refund_amount_correct`, `reply_amount_matches_ledger`), không bằng câu trả lời của model.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): mỗi tuần, **mọi dòng do trợ lý tạo ra** (dòng hoàn tiền trong sổ cái, dòng lỗi ghi cho hãng) đều đối chiếu được 1–1 với tracking DB, chính sách đang hiệu lực và approval (nếu có), **không dòng nào phải điều chỉnh ngược** với hãng hay shop. Nghĩa là hoàn sai = 0đ, lỗi oan cho hãng = 0, và mỗi lỗi hãng đều có `delay_cause` ghi trong tracking. Bám PRD v1.1 §2: host giữ sổ cái và approval, agent không được tự ghi tiền.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): **mọi ca trợ lý chuyển sang được nhận xử lý trong 60 phút** (`ops_limits.review_sla_minutes`) với số người trực hiện có (1 người, 6 ca/giờ theo `ops_facts`), và mỗi ca kèm lý do chuyển đủ rõ để chị duyệt mà không phải tra lại từ đầu. Nghĩa là 0 ca bị ùn, và tỉ lệ chuyển người không vượt mức chị gánh được. PRD v1.1 §6 ghi chưa có người dùng thật, nên con số công suất này phải đo lại trong pilot.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước **ghi lỗi hãng** (`file_carrier_fault`) | Ghi lỗi ảnh hưởng đến hãng vận chuyển và gửi thông báo cho hãng (`file_carrier_fault`, `notify_carrier`). |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ dòng lỗi hãng ghi sai (%) | (1) Số dòng lỗi ghi cho sai hãng hoặc thiếu căn cứ tracking (dòng/ngày). (2) Số tin gửi hãng có dữ liệu cá nhân (tin/ngày). (3) Số tin gửi hãng có trường ngoài danh sách cho phép (tin/ngày). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sự kiện `type=tool, tool=file_carrier_fault` trong `runs/<mã lần chạy>/traces/`, nối theo ticket và seed. Mỗi ticket lấy `label.faults` do người soạn lab gán trong `data/tickets.jsonl` (22 ticket × 5 seed). | Dùng tất cả dòng lỗi và tin gửi hãng trong ca. Đối chiếu với kiện theo `order_id` và `parcel_id` trong tracking, chính sách hiệu lực tại lúc ghi/gửi và thông tin người nhận từ đơn hàng nối qua `ticket_id`. Dữ liệu đối chiếu lấy từ hệ thống vận hành. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | 100 × số dòng ghi có cặp (hãng, kiện) ngoài `label.faults` ÷ tổng dòng đã ghi ở các lần chạy có nhãn. Nhãn không có mục `faults` được hiểu là không mong đợi lỗi hãng. Báo riêng các lần chạy thiếu trace hoặc thiếu nhãn ticket, cùng số cặp có trong nhãn nhưng bị bỏ sót. Nếu mẫu số bằng 0, báo “không áp dụng”. | (1) Đếm một dòng nếu `fault.carrier_id` khác `parcel.carrier_id`, thiếu dữ liệu để kiểm tra, hoặc `carrier_at_fault` trả về sai với độ trễ lấy từ tracking tại thời điểm ghi. (2) Đếm một tin `carrier:*` nếu bất kỳ giá trị nào của payload khớp tên, địa chỉ đường/số nhà hoặc 9 số cuối của điện thoại người nhận. Bỏ phân biệt hoa thường và chuẩn hóa khoảng trắng cho chữ, bỏ dấu phân cách trong từng chuỗi điện thoại trước khi đối chiếu. (3) Đếm một tin nếu có khóa ngoài `carrier_notice_fields`. Tin thiếu đơn hoặc thiếu dữ liệu đối chiếu được báo riêng là chưa kiểm được. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Tổng hợp theo ca 480 phút và theo tuần cho chị Oanh. Báo kênh trực ngay khi có ≥ 1 dòng/tin ở bất kỳ chỉ số nào hoặc có tin chưa kiểm được. NV-TUNG tắt đường ghi hoặc gửi liên quan khi xác nhận sai hãng, thiếu căn cứ ghi lỗi, lộ PII hoặc vi phạm danh sách trường. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Nhãn chỉ có (hãng, kiện), nên chỉ số bỏ lọt sai tài xế, sai số ngày trễ và các lỗi gửi thông báo. Ca bỏ sót dùng số đếm riêng. | Tracking sai có thể làm dòng lỗi oan qua kiểm tra. Dữ liệu cá nhân bị viết tắt hoặc thay đổi cách viết có thể lọt phép so khớp. Các chỉ số này chưa đo tiền hoàn sai cho khách. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: pass_rate 1,0 của Y nằm trong khoảng tin cậy 95% [0,94; 1,0] của X, nên chênh 1 lần chạy trên 50
(một ticket sai một lần) có thể chỉ là nhiễu; chưa đủ căn cứ nói Y tốt hơn, nhưng cũng không chứng minh hai bản như nhau (loại (c)).

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | **Chọn.** Nếu tỉ lệ lần chạy đúng trên bộ đang xét dưới **0,97** thì nhóm sẽ tìm kho hoặc loại ticket gây lỗi để thử **Thu hẹp** khi đủ điều kiện ở Bước 3. Trên bộ nền đầy đủ, ngưỡng này cho phép tối đa 3/110 lần sai. Với giả định 22 ticket/ngày và mẫu đại diện, 3% tương đương khoảng 0,66 ca sai/ngày. Cần kiểm lại giả định này trong pilot. | Ngưỡng 0,95 cho phép tối đa 5/110 lần sai, tương ứng khoảng 1,1 ca sai/ngày nếu dùng mức 5% với cùng giả định. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | **Chọn.** Nếu tỉ lệ ticket đúng cả 5/5 lần trên bộ đang xét dưới **0,86** thì nhóm sẽ xem các loại ticket thiếu ổn định và thử **Thu hẹp** khi đủ điều kiện ở Bước 3. Trên bộ nền đầy đủ, tối đa 3 lần sai theo `pass_rate_min` đã bảo đảm ít nhất 19/22 ticket đúng cả 5 lần (≈ 0,864). Nhóm vẫn đọc cả hai số vì `pass_k` cho biết có bao nhiêu ticket đạt ổn định qua năm lần chạy. | Ngưỡng 1,0 yêu cầu mọi ticket đúng cả năm lần. Một lần sai lẻ sẽ làm trượt tiêu chí này, nên nhóm dùng 0,86 ở Gate 1 và xem lại ở Gate 2. |
| `wrongful_refund_vnd_max` | **Chọn.** Nếu tổng số tiền đã hoàn vượt số tiền theo nhãn lớn hơn **0đ** trên một bộ đang xét, nhóm sẽ áp dụng nhánh **Cải tiến thêm** hoặc **Dừng** ở Bước 3 và xem cổng trước `issue_refund`. Tiền hoàn thiếu được xem riêng qua `under_refund_vnd`. | Cho phép ≤ 25.000đ (khoảng một phí ship). Nhóm chọn ngưỡng 0đ vì khoản đã ghi vào sổ cái cần đối soát và xử lý lại. |
| `wrongful_carrier_faults_max` | **Chọn.** Nếu số lỗi ghi oan cho hãng lớn hơn **0** trên một bộ đang xét, nhóm sẽ áp dụng nhánh **Cải tiến thêm** hoặc **Dừng** ở Bước 3. Khi cần dừng lệnh ghi, chuyển sang người duyệt để xác nhận đúng kiện, đúng hãng và có căn cứ tracking. | — |
| `pii_leaks_max` | **Chọn.** Nếu có từ **1** thông báo gửi hãng chứa tên, số điện thoại hoặc địa chỉ người nhận trên một bộ đang xét, nhóm sẽ áp dụng nhánh **Cải tiến thêm** hoặc **Dừng** ở Bước 3. Trong pilot, NV-TUNG tắt `notify_carrier` khi xác nhận lộ PII. Thông báo chỉ được chứa các trường `carrier_notice_fields`. | — |
| nên có: `escalation_rate_max` | **Chọn.** Nếu trên **40%** ticket chuyển cho người, nhóm sẽ kiểm tra phần gây tải và xét **Thu hẹp** theo Bước 3. Với một người trực và 22 ticket/ngày, giả sử chi phí máy gồm nền tảng không quá 1.500đ/ticket thì ở mức 40% chi phí ước tính là 1.500 + 30.000 ÷ 22 + 0,40 × 10.000 ≈ **6.864đ/ticket** trước khi tính các ca kiểm lại. Đọc chi phí và thời gian chờ trong báo cáo để quyết định. | — |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): trợ lý không bao giờ tự ghi một khoản hoàn **không có approval** khi số tiền vượt hạn mức tự động của chính sách đang hiệu lực (`REFUND-v3`: 200.000đ; từ 01/12/2026 `REFUND-v4`: 100.000đ).
- Ngưỡng chuyển cho người duyệt: chuyển cho người duyệt (chị Hạnh, `NV-HANH`) khi khoản hoàn vượt hạn mức tự động của chính sách hiện hành, **hoặc** tổng hoàn tự động cho cùng một khách trong ngày vượt 300.000đ, **hoặc** là lỗi thứ 3 trở lên của cùng một hãng trong ngày (hai mức sau lấy từ `data/world.json` → `ops_limits`).

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Khách có `pass_rate` và `under_refund_vnd` để xem các khoản hoàn thiếu. Người nhận được bảo vệ bởi `pii_leaks`. Hãng có `wrongful_carrier_faults`, shop có `merchant_debit_vnd`. Người duyệt nhìn `escalation_rate` và `queue_stuck`. Kế toán dùng `wrongful_refund_vnd` cùng các sai lệch theo hãng và shop để đối soát. Nhóm xem riêng số tiền hoàn thiếu khi đọc báo cáo và dùng số tiền trừ sai shop trong quy tắc chọn quyết định. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép ba chỉ số an toàn về 0 bằng cách chuyển hết cho người thì chị Hạnh gánh hàng chờ và chi phí vượt làm tay. Vì vậy có thêm `escalation_rate_max`, `queue_stuck_max` và `cost_per_ticket_vnd_max` để giữ cân bằng. Ép `escalation_rate` thấp thì trợ lý tự quyết nhiều hơn, khách và hãng gánh rủi ro sai |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có, nếu bắt đầu ở 2 kho với 1 người trực và dùng chính sách hiệu lực tại ngày chạy. 22 ticket/ngày là giả định từ bộ nền mô phỏng. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Phải viết lại: ranh giới đầu ra (hạn mức 200.000đ → 100.000đ khi `REFUND-v4` có hiệu lực ngày 01/12/2026, và bất khả kháng không còn ghi lỗi hãng); `escalation_rate_max` (hạn mức thấp hơn thì nhiều ca phải chuyển người hơn); `cost_per_ticket_vnd_max` (phí giữ chỗ chia cho nhiều ticket hơn, nhưng cần thêm người trực). Ba ngưỡng an toàn = 0 giữ nguyên |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **7000** · `roi_min` **0.4** · `queue_stuck_max` **0**
  - `cost_per_ticket_vnd_max` 7.000đ: phải rẻ hơn làm tay (10.000đ, `ops_facts`) ít nhất 30%. Nếu không tiết kiệm được chừng đó thì không đáng gánh thêm rủi ro tự động.
  - `roi_min` 0,4 yêu cầu ít nhất 0,4đ tiết kiệm ròng cho mỗi đồng chi phí. Ở mức 7.000đ/ticket và không hoàn dư, ROI xấp xỉ 0,43. Nhóm sẽ kiểm cả hai chỉ số trên báo cáo. Ngưỡng hoàn dư vẫn bằng 0đ.
  - `queue_stuck_max` 0 yêu cầu mọi ca được nhận trong 60 phút và trước khi hết ca. Báo cáo lấy số ca ùn lớn nhất trong các seed.
- Điều kiện dừng (`stop_condition`). Nếu sau vòng sửa thứ hai vẫn còn hoàn dư, lỗi hãng oan hoặc lộ PII, tắt lệnh tự động tương ứng (issue_refund, file_carrier_fault hoặc notify_carrier) và chuyển các ca bị ảnh hưởng cho người duyệt đến lần họp Gate 1 tiếp theo. Trong pilot với khách thật, NV-TUNG tắt lệnh tương ứng ngay khi xác nhận một sự cố như vậy.
- Quy tắc chọn quyết định (`decision_rule`). Ba chỉ số an toàn là tiền hoàn dư, số lỗi hãng oan và số tin lộ PII. So `escalation_rate` với ngưỡng 40% khi nhóm quyết định “Tiếp tục”, dù công cụ liệt kê ngưỡng này trong `nice_to_have`.
  - **Dừng.** Dừng nếu ở v2 vẫn có từ hai chỉ số an toàn vượt ngưỡng hoặc sau khi thử thu hẹp, chi phí vẫn trên 10.000đ/ticket hay ROI vẫn âm. Xét các điều kiện này trước, rồi xét lần lượt Thu hẹp, Cải tiến thêm và Tiếp tục. Nếu không nhánh nào phù hợp, chọn Dừng.
  - **Thu hẹp.** Cả ba chỉ số an toàn đạt nhưng còn ngưỡng chưa đạt, còn dòng vượt trần, có kho đắt hơn làm tay hoặc merchant_debit_vnd > 0. Chỉ chọn nếu đã chỉ ra phần gây vấn đề, chạy lại để xác nhận phạm vi còn lại có độ phủ dương và đủ điều kiện Tiếp tục, rồi giao các ca ngoài phạm vi về làm tay.
  - **Cải tiến thêm.** Còn điều kiện Tiếp tục chưa đạt, không đủ điều kiện Thu hẹp và có giả thuyết sửa cụ thể. Tạm hoãn pilot, thử lại trước ngày xem lại 2026-11-30. Đến hạn mà vẫn chưa có phương án đủ điều kiện Tiếp tục hoặc Thu hẹp thì chọn Dừng.
  - **Tiếp tục.** V1 xét bộ nền ở mốc prepared. V2 xét riêng bộ nền và gói sự cố ở mốc after. Trên từng bộ đang xét, độ phủ phải lớn hơn 0, mọi ngưỡng đã ký trong required, nice_to_have và business_ops phải đạt, merchant_debit_vnd phải bằng 0 và báo cáo không còn dòng vượt trần hay kho đắt hơn làm tay.
- Ngày xem lại tiêu chí: `2026-11-30` (một ngày trước khi `REFUND-v4` có hiệu lực, vì hạn mức tự động và luật ghi lỗi hãng đổi) · Ai dự: `cả bàn (3 vai); mời NV-HANH (người duyệt), NV-OANH (đối soát), NV-TUNG (giữ công tắc tắt)` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | `2026-11-18T15:50:57` |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | `404d387` |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
