"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict

# Cổng vòng 1 của bàn nhom3n (Phiếu B mục B6 / B7.1). Không có nhánh nào theo mã ticket hay câu chữ của khách:
# mọi quyết định so với nguồn sự thật (đơn, tracking, chính sách theo ngày hiệu lực, phê duyệt, sổ cái, trần Ops).


def _policy(ctx):
    """Chính sách có hiệu lực theo NGÀY (không theo cờ index_active bật tay)."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _facts(ctx, order_id):
    """(đơn, kiện mà ticket nói tới, số ngày trễ theo tracking, chính sách) hoặc None nếu không tra được."""
    order = ctx.tools.lookup_order(order_id)
    pol = _policy(ctx)
    if order is None or pol is None:
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, parcel, H.db_delay_days(parcel, ctx.as_of), pol


def _approval_ok(ctx, approval_id, amount):
    """Phê duyệt chỉ hợp lệ khi đúng ticket, còn hiệu lực, chưa dùng và đủ hạn mức."""
    a = next(iter(ctx.tools.lookup_approvals(approval_id=approval_id)), None)
    return (a is not None and a["ticket_id"] == ctx.ticket["ticket_id"] and a["status"] == "valid"
            and a["expires_at"] >= ctx.as_of and a["max_vnd"] >= amount)


def _strikes_full(ctx, carrier_id):
    """Đã đủ số lỗi tự động cho hãng này trong ngày (ops_limits)? Lỗi tiếp theo phải có người duyệt."""
    limit = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    return limit is not None and len(ctx.tools.fault_rows(carrier_id=carrier_id)) >= limit


def _auto_refunded_today_for(ctx, customer_id, today_total):
    """Tính tiền hoàn tự động hôm nay cho một khách, bỏ qua sổ cái từ ngày trước."""
    # Sổ cái trả về theo thứ tự ghi. Tổng hoàn tự động hôm nay giúp xác định
    # phần cuối của sổ cái thuộc ngày hiện tại, kể cả khi có dòng đã được duyệt.
    remaining = today_total
    total = 0
    for row in reversed(ctx.tools.ledger_rows()):
        if remaining == 0:
            break
        if row.get("approval_id"):
            continue
        amount = row["amount_vnd"]
        remaining -= amount
        if row["customer_id"] == customer_id:
            total += amount
    return total


def pre_guard(ctx):
    # Cổng 1 (phần chính sách): ghim phiên bản chính sách theo ngày hiệu lực.
    pol = _policy(ctx)
    if pol is None:
        return Verdict.escalate("không có chính sách hoàn tiền nào hiệu lực vào ngày " + ctx.as_of)
    return Verdict.allow(policy_id=pol["policy_id"])


def write_gate(ctx, action):
    tool = action["tool"]
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify(ctx, action)
    return Verdict.allow()


def _gate_refund(ctx, a):
    """Cổng 1: tiền hoàn không vượt quyền lợi tính từ tracking DB theo chính sách đúng ngày."""
    if a.get("basis") == "fail_open":
        return Verdict.escalate("model kiểm chính sách lỗi (429): không tự hoàn khi chưa kiểm được, chuyển người")
    if ctx.tools.ledger_rows(order_id=a["order_id"]):
        return Verdict.deny("đơn đã có khoản hoàn trong sổ cái: không hoàn lần hai")
    f = _facts(ctx, a["order_id"])
    if f is None:
        return Verdict.escalate("không tra được đơn hoặc chính sách để đối chiếu số tiền")
    order, parcel, delay, pol = f
    ent = H.entitlement_vnd(pol, order, delay, parcel.get("delay_cause"))
    amount, aid = int(a["amount_vnd"]), a.get("approval_id")
    if aid and not _approval_ok(ctx, aid, min(amount, ent)):
        return Verdict.escalate(f"phê duyệt {aid} không hợp lệ cho ticket này (sai ticket, hết hạn, đã dùng hoặc thiếu hạn mức)")
    if ent <= 0:
        ctx.log("refund_vs_db", asked=amount, entitled=0, db_delay_days=delay)
        return Verdict.deny(f"theo tracking trễ {delay} ngày, chính sách {pol['policy_id']} không cho hoàn")
    if H.carrier_at_fault(pol, parcel, delay) and _strikes_full(ctx, parcel["carrier_id"]):
        return Verdict.escalate(f"hãng {parcel['carrier_id']} đã đủ số lỗi tự động trong ngày: ca này cần người duyệt")
    changes = {}
    if amount > ent:
        changes["amount_vnd"] = ent
    if a.get("payer", "LOGIX") != "LOGIX" and not aid:
        changes["payer"] = "LOGIX"
    final = changes.get("amount_vnd", amount)
    if not aid:
        if final > pol["auto_limit_vnd"]:
            return Verdict.escalate(f"số tiền {final} vượt hạn mức tự động {pol['auto_limit_vnd']}: cần phê duyệt")
        cap = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
        if cap is not None:
            today_total = ctx.tools.auto_refund_today_vnd()
            if today_total + final > cap:
                spent = _auto_refunded_today_for(ctx, order["customer_id"], today_total)
                if spent + final > cap:
                    ctx.log("customer_daily_auto_refund_cap", spent_vnd=spent, requested_vnd=final, cap_vnd=cap)
                    return Verdict.escalate(f"vượt trần hoàn tự động {cap}đ mỗi khách trong ngày: cần phê duyệt")
    if changes:
        ctx.log("refund_vs_db", asked=amount, entitled=ent, db_delay_days=delay, changes=changes)
        return Verdict.modify(f"chỉnh theo tracking DB (trễ {delay} ngày, quyền lợi {ent})", **changes)
    return Verdict.allow()


def _gate_fault(ctx, a):
    """Cổng 1 + 2: chỉ ghi lỗi hãng khi tracking có nguyên nhân thuộc lỗi hãng, đúng kiện, đúng hãng, đúng số ngày."""
    f = _facts(ctx, a["order_id"])
    if f is None:
        return Verdict.deny("không tra được đơn hoặc chính sách: không ghi lỗi hãng")
    order, parcel, delay, pol = f
    if not H.carrier_at_fault(pol, parcel, delay):
        ctx.log("fault_blocked", recorded_cause=parcel.get("delay_cause"), db_delay_days=delay)
        return Verdict.deny(f"tracking không cho thấy lỗi hãng (nguyên nhân {parcel.get('delay_cause')}, trễ {delay} ngày)")
    if _strikes_full(ctx, parcel["carrier_id"]):
        return Verdict.escalate(f"hãng {parcel['carrier_id']} đã đủ số lỗi tự động trong ngày: cần người duyệt")
    want = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
            "driver_id": parcel.get("driver_id"), "delay_days": delay}
    changes = {k: v for k, v in want.items() if a.get(k) != v}
    if changes:
        ctx.log("fault_fixed", changes=changes)
        return Verdict.modify("ghi lỗi theo kiện trễ và số ngày trễ trong tracking", **changes)
    return Verdict.allow()


def _contact_in(obj, recipient):
    """Gói tin có chứa SĐT (9 số cuối), tên hoặc số nhà/đường của người nhận trong DB không? So với dữ liệu thật, không đoán bằng mẫu."""
    blob = str(obj)
    phone = H.digits(recipient.get("phone", ""))[-9:]
    return bool(phone and phone in H.digits(blob)) or any(
        v and v.lower() in blob.lower() for v in (recipient.get("name"), recipient.get("street")))


def _gate_notify(ctx, a):
    """Dựng tin từ DB cho đúng đơn, kiện và hãng đã ghi lỗi trên ticket."""
    order_id = ctx.ticket.get("order_id")
    facts = _facts(ctx, order_id)
    if facts is None:
        return Verdict.deny("không tra được đơn hoặc chính sách: không gửi gì cho hãng")
    order, parcel, delay, pol = facts
    if order["customer_id"] != ctx.ticket.get("customer_id"):
        return Verdict.deny("ticket không thuộc chủ đơn: không gửi gì cho hãng")
    ticket_id = ctx.ticket["ticket_id"]
    carrier_id = parcel["carrier_id"]
    if a.get("ticket_id") != ticket_id or a.get("carrier_id") != carrier_id:
        return Verdict.deny("ticket hoặc hãng nhận tin không khớp")
    if not ctx.tools.fault_rows(ticket_id=ticket_id, order_id=order_id,
                                 parcel_id=parcel["parcel_id"], carrier_id=carrier_id):
        return Verdict.deny("chưa ghi lỗi cho đúng kiện và hãng: không gửi thông báo")

    recipient = order.get("recipient") or {}
    district = recipient.get("district")
    if not isinstance(district, str) or _contact_in(district, recipient):
        district = None
    truth = {"order_id": order_id, "parcel_id": parcel["parcel_id"],
             "district": district, "delay_days": delay}
    allowed = pol.get("carrier_notice_fields") or ()
    kept = {k: truth[k] for k in allowed if truth.get(k) is not None}
    if not kept:
        return Verdict.deny("chính sách không cho gửi trường nào trong thông báo")
    payload = a.get("payload") or {}
    if kept != payload:
        contact = _contact_in({k: v for k, v in payload.items() if kept.get(k) != v}, recipient)
        ctx.log("notify_trimmed", dropped=sorted(k for k in payload if kept.get(k) != payload[k]),
                recipient_contact_blocked=contact)
        return Verdict.modify("tin gửi hãng dựng lại từ DB, chỉ gồm trường được phép", payload=kept)
    return Verdict.allow()
