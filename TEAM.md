# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `nhom3n`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-nhom3n-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S7`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Trần Quốc Đông | 2A202603643 | Kỹ sư cổng | x |
|   2 | Vương Xuân Dương | 2A202603703 | Sản phẩm và kinh doanh | |
|   3 | Nguyễn Minh Thông | 2A202603637 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## TranQuocDong-2A202603643

### Phần việc phụ trách

Kỹ sư cổng. Phiếu B mục B7.1–B7.3 và Phiếu C mục C7–C8.

### Đóng góp cụ thể

- Dựng 3 cổng vòng 1 trong `lab10/guards.py`: `pre_guard` ghim chính sách theo ngày hiệu lực (`effective_policy`); `_gate_refund` tính lại quyền lợi từ tracking DB, chặn hoàn lần hai, kiểm hạn mức/approval và chặn nhánh `fail_open`; `_gate_fault` và `_gate_notify` chỉ cho ghi lỗi/gửi hãng khi tracking có căn cứ, đúng kiện–hãng, payload chỉ gồm `carrier_notice_fields`. Chốt bằng `checkpoint`, hash `e7699e44`; mô tả ở Phiếu B mục B7.1.
- Viết B7.2 (hai bước tránh rò rỉ): cổng chỉ so với nguồn sự thật, trong code không có mã ticket hay câu chữ của khách; tách bộ dùng để chỉnh khỏi bộ dùng để quyết định, chốt cổng trước khi bốc thẻ.
- Viết B7.3: tự đặt hai ticket `--adhoc` O-1002/C-02 (khách khai trễ 9 ngày) và O-1026/C-10 (quà tặng, chèn câu lệnh); ghi lại trước–sau ở sổ cái, lỗi hãng và dòng `GỬI HÃNG`. Ca O-1026 là bằng chứng `customer_note` và `recipient_contact` bị cắt.
- C7: từ trace `S7-01`, `S7-02`, `S7-04`, `S7-20`, `S7-21` và đối chứng `S7-05`, sửa `_gate_notify` để dựng lại payload từ DB, kiểm ticket thuộc đúng chủ đơn, bắt buộc có `fault_rows` đúng ticket–đơn–kiện–hãng, bỏ `district` nếu giá trị chứa liên hệ người nhận; thêm trần hoàn tự động 300.000đ/khách/ngày trong `_gate_refund`.
- C8: thêm monitor `recipient_contact_blocked_rate` vào `lab10/monitors.py`, đọc cờ `recipient_contact_blocked` của dòng guard `notify_trimmed`; kiểm trên bộ nền (0,0) và S7 (0,75, và 0,8333 khi đổi mẫu số).
- Các lần chạy chính: `R-S7-after-20261118-165007-f90e53` (ràng buộc đơn–kiện–hãng), `R-S7-after-20261118-165020-8a53fa` (trần 300.000đ), `R-S7-after-20261118-171622-b01b73` (chốt).
- Dùng AI: (1) nhờ AI đọc `lab10/agent.py`, `tools.py`, `helpers.py` và tóm tắt các nhánh `Verdict` trước khi viết cổng; (2) yêu cầu AI gợi ý ba cách chặn `notify_carrier` (lọc theo tên trường, dựng lại payload, kiểm chéo DB), AI chỉ ra lỗ hổng "trường được phép nhưng giá trị bẩn" và gợi ý hàm `_contact_in`; (3) nhờ AI sinh bộ ticket `--adhoc` biến thể (SĐT có dấu cách, chỉ có địa chỉ, mã vận đơn 10 chữ số) và soát cú pháp `Verdict.modify`/`Verdict.escalate`; (4) nhờ AI rà bảng C7 và diễn đạt phần "ngăn hay giảm". Phần chọn ngưỡng, logic cuối cùng và kết luận từng nhánh tôi tự chạy trace và đối chiếu DB trước khi chốt.

### Bằng chứng

Đối chiếu commit chốt cổng `a6e276d` và commit xử lý S7 `7877338` với phần việc của mình.

### Exit ticket

- **Học được:** Một cổng tốt là danh sách cho phép dựng từ nguồn sự thật, không phải bộ lọc theo mẫu chữ; vòng 1 đã chặn 30/30 lượt lộ trước khi bàn biết thẻ, nhưng chỉ khi vòng 2 dựng lại payload từ DB thì mới đóng được nhánh "dữ liệu bẩn nằm trong trường được phép".
- **Chưa chắc:** `carrier_notice_fields` trong mock có đúng điều khoản hợp đồng thật của từng hãng hay không; nếu hợp đồng đổi hoặc danh sách trong `policies` sai thì cổng sẽ trung thành với một spec sai, và tôi chưa biết ai sẽ ký xác nhận mỗi lần danh sách đó thay đổi.

## VuongXuanDuong-2A202603703

### Phần việc phụ trách

Sản phẩm và kinh doanh. Phiếu A, Phiếu B mục B7.4 và B8, Phiếu C mục C12.

### Đóng góp cụ thể

- Phiếu A: viết A1 (mục tiêu hệ thống và hai góc nhìn chị Oanh/chị Hạnh), A2 (offline metric cho bước `file_carrier_fault` và telemetry production), A3 (chọn kết luận (b) vì khoảng tin cậy chồng lấn), A4 (câu tiêu chí cho 5 chỉ số bắt buộc và `escalation_rate`, bốn nhánh `decision_rule`, `stop_condition`), A5 ký `404d387`, hash tiêu chí `26ade5c8`.
- B7.4: đặt 4 số trong mục `business`: trần hoàn tự động/ngày 2.000.000đ (bằng ngân sách Finance, ngày tệ nhất của bộ nền là 155.000đ), ngân sách 1.500đ/ticket, `pilot_scope` 4 kho HN–HCM–DN–CT (bỏ `HCM-B2B`), `roi_min` 0,4; mỗi số ghi lý do lấy từ `ops_limits`/`ops_facts`.
- B8: chạy `checkpoint` (hash `e7699e44`) và `gate` trên `R-base-prepared-20261118-161921-5217ec`; kết luận không có dòng vượt trần, chọn **Tiếp tục** ở 4 kho và ký v1.
- C12: dựng bảng so v1–v2 từ grade `R-S7-grade-20261118-171622-b01b73` và hai bộ after; đã thử thu hẹp còn HN–HCM ở C0 dòng 9–10 nhưng loại vì độ phủ bộ nền còn 59%, ROI 1,24 → 0,80, chi phí S7 5.005đ → 6.434đ; chốt **Tiếp tục** 4 kho kèm điều kiện Pháp chế đối chiếu `carrier_notice_fields`, và viết ba dòng bắt buộc vào `submission/submission.json`.
- Dùng AI: (1) nhờ AI phác thảo A1–A5, đặc biệt chuyển yêu cầu thành câu tiêu chí đúng mẫu "Nếu … thì …" và đề xuất hai phiên bản ngưỡng (0,97/0,95; 0,86/1,0) để bàn chọn; (2) đưa report JSON cho AI trích số prepared/after, tính lại khoảng tin cậy, ROI và chi phí, lập bảng so v1–v2; (3) nhờ AI soát tính nhất quán giữa `acceptance_criteria.json`, `decision_rule` và `submission.json`, và nháp ba dòng bắt buộc; (4) nhờ AI đọc lại `form-a-criteria.md` để tìm câu tiêu chí nào chưa nói "nếu trượt thì làm gì". Ngưỡng cuối cùng, lý do chọn và quyết định Tiếp tục do tôi và bàn chốt sau khi tự đọc lại report.

### Bằng chứng

Đối chiếu bản tiêu chí ký ở `404d387`, Phiếu B mục B8 và Phiếu C mục C12 với phần việc của mình.

### Exit ticket

- **Học được:** "Tiếp tục" chỉ đáng tin khi nhìn đồng thời pass_rate, độ phủ, chi phí và ROI; thử thu hẹp còn 2 kho làm chi phí S7 đẹp hơn nhưng độ phủ bộ nền rơi còn 59% và ROI 1,24 → 0,80, nên số đẹp mà mất phạm vi không phải là quyết định tốt.
- **Chưa chắc:** Chi phí 1.500đ/ticket, ROI 1,0 và tỉ lệ chuyển người 0,2273 đang đo trên mock; khi chạy LLM thật, ticket dài và giờ cao điểm có thể đẩy chi phí hoặc thời gian chờ duyệt vượt ngưỡng đã ký, nên tôi chưa chắc ngưỡng 7.000đ và ROI 0,4 còn đúng sau vài tuần pilot.

## NguyenMinhThong-2A202603637

### Phần việc phụ trách

Vận hành và pháp lý. Phiếu B mục B4–B5 và B7.5–B7.6, Phiếu C mục C10–C11.

### Đóng góp cụ thể

- B4: chủ trì HAZOP vòng 1 trên `file_carrier_fault` với 5 dòng: `delay_days` WRONG (`T-002@55`, DB 2 ngày, ticket 5 ngày), `parcel_id`/`carrier_id` INVALID (code luôn ghi `parcels[0]`), `delay_cause` INCOMPLETE (nhiều đơn không có nguyên nhân vẫn bị gán `CARRIER`), số lỗi/hãng PERTURBED, `fail_open` INCAPABLE; thêm 4 dòng ngoài code (người duyệt, ngân sách, phạm vi pilot, dữ liệu gửi bên thứ ba).
- B5: lập checklist 9 nhóm việc, gắn PIC từng dòng (Đông: 1, 3, 4; Dương: 2, 6, 9; Thông: 5, 7, 8), ghi trạng thái và bằng chứng; trước vòng 2 phần lớn còn "Chưa".
- B7.5: điền mục `operations`/`legal` trong `config/operating_gates.json`: PIC `NV-TUNG`, người duyệt `NV-HANH`, 1 người trực, 6 ca/giờ, chờ tối đa 60 phút, 4 điều kiện dừng, kênh `#logix-refund-pilot`; cấm `customer_note`/`recipient_contact` ra bên thứ ba và bắt buộc `carrier_fault_requires_recorded_cause`. Viết Runbook 1–3 (ai chịu trách nhiệm, ngưỡng vàng/đỏ, cách dừng trong 15 phút).
- B7.6: tính giờ cao điểm: 22 ticket/ngày dồn gấp ba thành 66 ticket/giờ, khoảng 18 ca/giờ cần người so với 6 ca/người/giờ; đặt ngưỡng gọi thêm người (≥ 6 ca chờ hoặc ≥ 30 phút), ngưỡng thu hẹp/tắt; ước thêm 1 người thành 5.820đ/ticket, ROI 0,72, thêm 2 người vượt 7.000đ và ROI 0,39.
- C10: thêm 2 dòng risk register: (1) đổi agent/prompt làm lộ kiểu mới hoặc cổng bị gỡ — dấu hiệu là monitor C8, xử lý tắt `notify_carrier`, nhóm MANAGE; (2) `carrier_notice_fields` khác hợp đồng — chưa có metric, chặn mở pilot tới khi Pháp chế đối chiếu, nhóm GOVERN.
- C11: cập nhật checklist (1, 3, 7 Xong; 8 còn phần pilot thật; 9 có v2) và viết Runbook 4–5: tín hiệu lẽ ra phải báo trước, đổi ngưỡng monitor, giữ 1 người trực/4 kho, báo hãng trong 24 giờ, nói rõ dữ liệu đã đi và không thu hồi được; ba kịch bản "nếu… thì…".
- Dùng AI: (1) nhờ AI dựng khung bảng HAZOP theo 5 guideword và gợi ý 4 thành phần ngoài code; (2) đưa `data/world.json` cho AI tra `staff`, `ops_limits`, `ops_facts` và tính lại giờ cao điểm, chi phí thêm người; (3) nhờ AI nháp runbook 1–5, checklist 9 nhóm và 2 dòng risk register, rồi kiểm từng con số với `config/operating_gates.json`; (4) nhờ AI rà lại email Pháp chế để không bỏ sót yêu cầu "báo cáo nguyên nhân và biện pháp trong ngày". Kết luận pháp lý, điều kiện dừng và thông điệp cho bên thứ ba tôi tự viết.

### Bằng chứng

Đối chiếu checklist và runbook trong Phiếu B và Phiếu C với phần việc của mình.

### Exit ticket

- **Học được:** Spec của kênh gửi hãng phải do pháp lý sở hữu và kiểm được bằng danh sách trường, không để agent tự soạn; và một điều kiện dừng chỉ có giá trị khi có người bấm, thời hạn 15 phút và kênh báo cụ thể.
- **Chưa chắc:** Liệu Pháp chế có kịp đối chiếu `carrier_notice_fields` với hợp đồng từng hãng trước ngày mở pilot hay không; nếu chậm, điều kiện "chưa có biên bản thì không bật `notify_carrier`" vẫn giữ được, nhưng tôi chưa rõ ai chịu trách nhiệm nếu hợp đồng và danh sách trong `policies` khác nhau ngay trong tuần chạy thử.
