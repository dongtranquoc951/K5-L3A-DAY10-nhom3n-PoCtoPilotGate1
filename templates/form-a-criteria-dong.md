# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

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

> …

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): …
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): …

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
| **Bước / hành vi được đo** | Chọn phiên bản chính sách hoàn tiền tại sự kiện `policy`, trước bước tính số tiền hoàn. Kiểm tra `policy_id` agent chọn có đúng phiên bản hiệu lực tại ngày xử lý của bộ dữ liệu hay không. | |
| **Thước đo** (một câu, có đơn vị) | `policy_effective_match_rate`: tỉ lệ (%) trial đã tới bước chọn chính sách mà agent chọn đúng duy nhất một `policy_id` đang hiệu lực tại `as_of`. Giá trị cao hơn nghĩa là bước chọn chính sách chính xác hơn trên các trial đo được. | |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Kế hoạch đo trên bộ nền `data/tickets.jsonl`: 22 ticket × 5 seed 11/22/33/44/55 = 110 trial. Sau khi ký tiêu chí, lấy các sự kiện có `type = policy` và trường `policy_id` từ `events` trong `runs/<mã lần chạy>/traces/<ticket_id>@<seed>.json`. Nguồn kỳ vọng là `data/world.json`: `as_of`, `policies[].policy_id`, `effective_from`, `effective_to`; dùng ngày của bộ dữ liệu, không dùng ngày máy. TV1 lập nhãn kỳ vọng theo khoảng hiệu lực, TV2 kiểm tra chéo quy tắc và các ngày biên. Hai đầu mút đều được tính; `effective_to = null` nghĩa là chưa có ngày kết thúc. Không lấy cờ `index_active` hoặc chính lựa chọn của agent làm nhãn đúng. | |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Mỗi cặp `ticket_id@seed` tính một lần. Gọi `N_policy` là số trial có ít nhất một sự kiện `policy`; `N_đúng` là số trial trong đó có đúng một sự kiện này, có đúng một chính sách thỏa `effective_from <= as_of <= effective_to` và `policy_id` được chọn khớp chính sách đó. Tính `100 × N_đúng / N_policy`; nếu `N_policy = 0` thì ghi `N/A`. Trial có nhiều sự kiện `policy`, thiếu/không nhận diện được `policy_id`, hoặc không xác định được duy nhất một chính sách hiệu lực không tính vào tử số; lỗi khoảng hiệu lực được ghi riêng là lỗi dữ liệu để phân biệt nguồn lỗi. Trial không có sự kiện `policy` được loại khỏi mẫu số và đếm riêng kèm lý do từ trace (ví dụ trả lời ngoài luồng hoàn tiền hoặc chuyển người trước bước này). Đối chiếu danh sách 110 trial dự kiến; trace thiếu/hỏng ghi riêng, không quy thành ca đúng. Luôn báo kèm `N_policy`, `N_đúng`, số ca sai, số ca không tới bước và số trace thiếu/hỏng để tránh kết luận từ phần nhỏ của bộ thử. | |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không chứng minh tracking đúng, tính tiền đúng, phê duyệt hợp lệ, ledger/tiền trả lời khớp nhau hay không lộ dữ liệu cá nhân. Không phát hiện một chính sách có khoảng hiệu lực hợp lệ nhưng nội dung DB sai hoặc đã lỗi thời so với thực tế. Chỉ đánh giá các trial tới bước chọn chính sách; chuyển quá nhiều ca cho người có thể làm mẫu số nhỏ nên phải đọc cùng số ca không tới bước, `pass_rate` và `escalation_rate`. Bộ nền ít ngày hiệu lực nên khả năng phát hiện lỗi chuyển phiên bản còn hạn chế. | |

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

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Giải thích một câu: …

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
| `pass_rate_min` | | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | | |
| `wrongful_refund_vnd_max` | | |
| `wrongful_carrier_faults_max` | | |
| `pii_leaks_max` | | |
| nên có: `escalation_rate_max` | | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): ____
- Ngưỡng chuyển cho người duyệt: ____

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | |

**Góp ý kỹ thuật của Kỹ sư cổng để nhóm soát trước khi chốt ngưỡng:**

- `pass_rate` tính theo trial; `pass_k` ở lab này là pass^k, ticket đúng cả 5/5 seed, khác pass@k (đúng ít nhất một lần). Với bộ nền đầy đủ có 110 trial và 22 ticket; soát đúng mẫu số khi viết câu tiêu chí.
- `wrongful_refund_vnd` là tổng phần tiền hoàn quá mức, không bao gồm mọi trường hợp hoàn thiếu hoặc số tiền trả lời không khớp ledger. Khi dựng cổng ở vòng sau, cần kiểm tra cả kết quả ghi và hành động trả lời; mức hoàn sai bằng 0 chưa chứng minh toàn bộ luồng đúng.
- `wrongful_carrier_faults` đếm bản ghi lỗi hãng không thuộc kỳ vọng; `pii_leaks` đếm thông báo gửi hãng chứa PII theo bộ đo. Giữ riêng hai tác hại và đối tượng bị ảnh hưởng khi nhóm chọn điều kiện dừng; không thay bằng `secret_leak` của Lab 9.
- Soát riêng ngân sách tiền máy/ticket trong cổng vận hành và chi phí tổng/ticket trong report; thống nhất với TV2/TV3 cách đọc ROI, số ca ùn và tác động của chuyển người duyệt trước khi chốt `business_ops`.
- `policy_effective_match_rate` ở câu 1.3 là metric chẩn đoán cho một bước; chưa phải chỉ số có sẵn trong `lab10.eval`. Không thêm trường vào schema `acceptance_criteria.json`; sau khi ký, tính metric từ trace theo định nghĩa ở A2. Ngưỡng và hành động của A4 vẫn cần cả nhóm thống nhất trước lần đánh giá đầu tiên.

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` ____ · `roi_min` ____ · `queue_stuck_max` ____
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

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
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | Chưa ký: `acceptance_criteria.json` còn trống ngưỡng và chưa có `acceptance_criteria.lock`. Chờ nhóm hoàn thiện, thống nhất A4 rồi ghi thời điểm ký thực tế. |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | Chưa có commit ký tiêu chí; điền 7 ký tự đầu sau khi ký và commit thành công. |
| Đã push lên `origin main` thành công? | Chưa; thực hiện sau khi ký và commit thành công, trước lần đánh giá đầu tiên. |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
