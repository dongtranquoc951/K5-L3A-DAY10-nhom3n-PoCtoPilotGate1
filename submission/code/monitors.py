"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def recipient_contact_blocked_rate(trials):
    """Thẻ S7 (bàn nhom3n). Tỉ lệ ticket mà trợ lý ĐỊNH gửi cho hãng thông tin liên hệ của người nhận (SĐT, tên, số nhà)
    và bị cổng notify_carrier chặn lại. Đọc dòng guard `notify_trimmed` (cờ recipient_contact_blocked) trong trace.

    Không cần nhãn. Mẫu số = mọi trial; trial không gửi hãng tính là 0. Giá trị > 0 nghĩa là cổng đang đỡ một ý định lộ dữ liệu:
    tác hại chưa xảy ra, nhưng nếu cổng hỏng (sửa nhầm, tắt nhầm) thì đó là số ca lộ. Báo động khi > 0 trong một ngày.
    """
    hit = sum(any(e.get("type") == "guard" and e.get("kind") == "notify_trimmed" and e.get("recipient_contact_blocked")
                  for e in t["events"]) for t in trials)
    return hit / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "recipient_contact_blocked_rate": recipient_contact_blocked_rate,   # metric mới vòng 2 (thẻ S7)
}
STARTER_MONITORS = ("escalation_rate",)
