"""
AusVisa Finance — Australia
Built for international students AND working holiday makers in Australia.
Japanese-first, fully bilingual EN/JA.

Pages:
  🏠 Home
  💰 Super Claim Calculator
  🧾 Tax Estimator
  💸 Money Transfer
  ⏱️ WHM Employer Tracker
  🏦 Bank Account Guide   (coming soon)
  📋 Work Rights          (coming soon)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AusVisa Finance",
    page_icon="🦘",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
body, [data-testid="stAppViewContainer"] { background: #0d1117; }
[data-testid="stSidebar"] { background: #161b22; border-right: 1px solid #30363d; }

.card {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 20px 24px; margin: 10px 0;
}
.card-green  { border-left: 4px solid #3fb950; }
.card-yellow { border-left: 4px solid #d29922; }
.card-red    { border-left: 4px solid #f85149; }
.card-blue   { border-left: 4px solid #58a6ff; }

.big-number {
    font-size: 42px; font-weight: 800; color: #3fb950; margin: 8px 0;
}
.big-number-yellow { color: #d29922; }
.label-sm { font-size: 12px; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; }
.step-box {
    background: #0f2027; border: 1px solid #1f6feb; border-radius: 8px;
    padding: 14px 18px; margin: 8px 0; font-size: 14px; color: #c9d1d9;
}
.warn-box {
    background: #2d1a00; border: 1px solid #d29922; border-radius: 8px;
    padding: 12px 16px; font-size: 13px; color: #d29922; margin: 10px 0;
}
.hero-title { font-size: 32px; font-weight: 800; color: #e6edf3; margin: 0; }
.hero-sub   { font-size: 16px; color: #8b949e; margin-top: 6px; }
a { color: #58a6ff !important; }

@media (max-width: 640px) {
    .big-number { font-size: 32px; }
    .hero-title { font-size: 24px; }
}
</style>
""", unsafe_allow_html=True)

# ── global visa + language (sidebar) ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🦘 AusVisa Finance")
    st.caption(
        "For international students & working holiday makers in Australia\n"
        "留学生・ワーキングホリデーのためのお金ガイド"
    )
    st.markdown("---")

    lang_choice = st.radio(
        "Language / 言語",
        ["🇬🇧 English", "🇯🇵 日本語"],
        horizontal=True,
    )
    lang = "ja" if "日本語" in lang_choice else "en"
    st.markdown("---")

    # ── global visa selector ──────────────────────────────────────────────────
    st.markdown(
        "<span style='font-size:12px;color:#8b949e;text-transform:uppercase;letter-spacing:0.5px'>"
        + ("Your visa type" if lang == "en" else "あなたのビザの種類")
        + "</span>",
        unsafe_allow_html=True,
    )
    _gv_opts_en = [
        "🎓 Student (500)",
        "🎒 Working Holiday (417)",
        "🎒 Work & Holiday (462)",
        "🏆 Graduate (485)",
        "🔧 Temporary work (482)",
        "🤷 Not sure / other",
    ]
    _gv_opts_ja = [
        "🎓 学生ビザ（500）",
        "🎒 ワーキングホリデー（417）",
        "🎒 ワーキング＆ホリデー（462）",
        "🏆 卒業生ビザ（485）",
        "🔧 一時就労ビザ（482）",
        "🤷 わからない／その他",
    ]
    _gv_opts = _gv_opts_ja if lang == "ja" else _gv_opts_en
    _gv_sel  = st.selectbox(
        "visa", _gv_opts, label_visibility="collapsed", key="global_visa_label"
    )
    # derive a simple key used by every page
    if   "417" in _gv_sel: gv = "whm_417"
    elif "462" in _gv_sel: gv = "whm_462"
    elif "485" in _gv_sel: gv = "grad_485"
    elif "482" in _gv_sel: gv = "work_482"
    elif "500" in _gv_sel: gv = "student_500"
    else:                   gv = "other"

    is_whm_global    = gv in ("whm_417", "whm_462")
    is_student_global = gv == "student_500"
    is_grad_global   = gv == "grad_485"

    st.markdown("---")

    pages_en = [
        "🏠 Home",
        "💰 Super Claim Calculator",
        "🧾 Tax Estimator",
        "💸 Money Transfer",
        "⏱️ WHM Employer Tracker",
        "🏦 Bank Account Guide",
        "📋 Work Rights",
    ]
    pages_ja = [
        "🏠 ホーム",
        "💰 スーパー請求計算機",
        "🧾 税金計算機",
        "💸 海外送金",
        "⏱️ WHM雇用主トラッカー",
        "🏦 銀行口座ガイド",
        "📋 就労権利",
    ]
    nav_opts  = pages_ja if lang == "ja" else pages_en
    nav_sel   = st.radio("nav", nav_opts, label_visibility="collapsed")
    page      = pages_en[nav_opts.index(nav_sel)]

    st.markdown("---")
    st.caption(
        "Made by a Japanese student at UQ.\nGeneral information only — not financial or legal advice."
        if lang == "en" else
        "UQの日本人留学生が制作。情報提供のみ。"
    )

# ══════════════════════════════════════════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown(
        "<div class='hero-title'>🦘 AusVisa Finance</div>"
        "<div class='hero-sub'>"
        + ("Free money tools for international students & working holiday makers in Australia — built by one of you."
           if lang == "en" else
           "留学生・ワーキングホリデーのための無料お金ガイド — 同じ立場の人間が作りました。")
        + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("")

    # ── the problem ───────────────────────────────────────────────────────────
    if lang == "en":
        st.markdown("""
Most international students and working holiday makers leave Australia without knowing:

- 💰 They're owed **superannuation** from every job — often $2,000–$8,000 sitting unclaimed
- 🧾 They paid **too much tax** and are owed a refund — but never lodged a return
- 💸 They lost **3–5% on every money transfer** home when Wise costs 0.5%
- ⏱️ WHM holders hit the **6-month employer limit** without realising, risking their visa
- 📋 They have **full workplace rights** — many employers underpay people who don't know this

The language barrier makes all of this worse. This site exists to fix that.
Free, bilingual EN/JA, no sign-up needed.
""")
    else:
        st.markdown("""
多くの留学生・ワーキングホリデー参加者がオーストラリアを離れる際に以下を知らないことが多いです：

- 💰 すべての職場から**スーパーアニュエーション（退職金）**が積み立てられており、多くの場合2,000〜8,000ドルが未請求のまま
- 🧾 **税金を払いすぎており還付を受けられる**のに、確定申告をしたことがない
- 💸 Wiseなら0.5%なのに、銀行送金で**毎回3〜5%の手数料**を払っている
- ⏱️ WHM保持者が知らないうちに**6ヶ月の雇用主制限**を超え、ビザリスクを抱えている
- 📋 **完全な労働権**があるにもかかわらず、知らないために低賃金で働かされている

言語の壁がこれらをさらに難しくしています。このサイトはその問題を解決するために作られました。
無料・日英バイリンガル・登録不要。
""")

    st.markdown("---")

    # ── personalised "start here" card based on global visa ───────────────────
    _visa_advice = {
        "student_500": (
            "🎓 You're on a **Student visa (500)**",
            "🎓 **学生ビザ（500）**をお持ちですね",
            "Your priority tools: **Super Claim Calculator** (don't leave without claiming it) → **Tax Estimator** → **Money Transfer**. Work rights: 48h/fortnight during semester.",
            "優先ツール：**スーパー請求計算機**（帰国前に必ず請求）→ **税金計算機** → **海外送金**。就労：学期中48時間/2週間。",
        ),
        "whm_417": (
            "🎒 You're on a **Working Holiday visa (417)**",
            "🎒 **ワーキングホリデービザ（417）**をお持ちですね",
            "Your priority tools: **WHM Employer Tracker** (don't breach the 6-month limit) → **Super Claim Calculator** → **Tax Estimator** (you get the 15% flat rate). Second-year visa? Track your regional work days in the tracker.",
            "優先ツール：**WHM雇用主トラッカー**（6ヶ月制限に注意）→ **スーパー請求計算機** → **税金計算機**（15%の特別税率）。2年目ビザ希望の場合は地方就労日数もトラッカーで管理。",
        ),
        "whm_462": (
            "🎒 You're on a **Work and Holiday visa (462)**",
            "🎒 **ワーキング＆ホリデービザ（462）**をお持ちですね",
            "Your priority tools: **WHM Employer Tracker** (6-month employer limit applies) → **Super Claim Calculator** → **Tax Estimator** (15% flat rate on first $45k). Second-year visa requires 88 days regional work.",
            "優先ツール：**WHM雇用主トラッカー**（6ヶ月制限あり）→ **スーパー請求計算機** → **税金計算機**（最初の$45kは15%）。2年目ビザには88日の地方就労が必要。",
        ),
        "grad_485": (
            "🏆 You're on a **Graduate visa (485)**",
            "🏆 **卒業生ビザ（485）**をお持ちですね",
            "You have full work rights with no hour limits. Priority tools: **Tax Estimator** (you're likely a tax resident — make sure to lodge a return) → **Super Claim Calculator** → **Money Transfer**.",
            "就労権は無制限です。優先ツール：**税金計算機**（税務居住者の可能性が高い — 確定申告を忘れずに）→ **スーパー請求計算機** → **海外送金**。",
        ),
        "work_482": (
            "🔧 You're on a **Temporary Skill Shortage visa (482)**",
            "🔧 **一時技能不足ビザ（482）**をお持ちですね",
            "You can only work for your sponsoring employer. Priority tools: **Tax Estimator** → **Super Claim Calculator** → **Money Transfer**.",
            "就労はスポンサー雇用主のみ可能です。優先ツール：**税金計算機** → **スーパー請求計算機** → **海外送金**。",
        ),
        "other": (
            "👋 Welcome to AusVisa Finance",
            "👋 AusVisa Financeへようこそ",
            "Select your visa type in the sidebar and the site will show you exactly which tools matter most for your situation.",
            "サイドバーでビザの種類を選択すると、あなたの状況に合った優先ツールが表示されます。",
        ),
    }
    _va = _visa_advice.get(gv, _visa_advice["other"])
    _va_title = _va[1] if lang == "ja" else _va[0]
    _va_desc  = _va[3] if lang == "ja" else _va[2]
    st.markdown(
        f"<div class='card card-blue' style='padding:16px 20px'>"
        f"<b style='color:#e6edf3'>{_va_title}</b><br>"
        f"<span style='color:#8b949e;font-size:13px'>{_va_desc}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("")

    # ── tools grid ────────────────────────────────────────────────────────────
    st.markdown("### " + ("All tools" if lang == "en" else "全ツール"))
    c1, c2 = st.columns(2)
    tools = [
        ("💰", "Super Claim Calculator",
         "スーパー請求計算機",
         "How much super are you owed? Calculate it and get the step-by-step claim guide.",
         "退職金がいくら受け取れるか計算し、帰国前に請求する方法を確認。",
         True, c1),
        ("🧾", "Tax Estimator",
         "税金計算機",
         "Enter your visa, dates, and income — we calculate your tax and estimate your refund.",
         "ビザ・滞在期間・収入を入力 — 税額と還付額を自動計算。",
         True, c2),
        ("💸", "Money Transfer Comparison",
         "海外送金比較",
         "7 providers compared side by side. See exactly how much more you get with Wise.",
         "7社を横並び比較。Wiseでいくら多く受け取れるか一目でわかる。",
         True, c1),
        ("⏱️", "WHM Employer Tracker",
         "WHM雇用主トラッカー",
         "Track your 6-month employer limit and second-year visa regional work progress.",
         "6ヶ月の雇用主制限と2年目ビザのための地方就労進捗を追跡。",
         True, c2),
        ("🏦", "Bank Account Guide",
         "銀行口座ガイド",
         "Which Australian bank account is best when you first arrive?",
         "到着直後に最適なオーストラリアの銀行口座は？",
         False, c1),
        ("📋", "Work Rights",
         "就労権利",
         "Know your rights — hours, pay rates, entitlements by visa type.",
         "就労権を知る — ビザ別の時間・賃金・権利。",
         False, c2),
    ]
    for icon, title_en, title_ja, desc_en, desc_ja, live, col in tools:
        title = title_ja if lang == "ja" else title_en
        desc  = desc_ja  if lang == "ja" else desc_en
        badge = ("✅ Live" if lang == "en" else "✅ 公開中") if live else ("🔜 Coming soon" if lang == "en" else "🔜 近日公開")
        col.markdown(
            f"<div class='card {'card-green' if live else 'card-yellow'}'>"
            f"<span style='font-size:24px'>{icon}</span> "
            f"<span style='font-size:11px;color:#8b949e'>{badge}</span><br>"
            f"<b style='color:#e6edf3'>{title}</b><br>"
            f"<span style='font-size:13px;color:#8b949e'>{desc}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        "<div class='warn-box'>"
        + ("⚠️ This site provides general information only. It is not financial, tax, or legal advice. "
           "For complex situations, consult a registered tax agent or migration lawyer."
           if lang == "en" else
           "⚠️ このサイトは一般的な情報提供のみを目的としています。税務・法律的なアドバイスではありません。"
           "複雑な状況については、登録税務代理人または移民弁護士にご相談ください。")
        + "</div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
#  SUPER CLAIM CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💰 Super Claim Calculator":

    st.markdown(
        "## 💰 " + ("Super Claim Calculator" if lang == "en" else "スーパーアニュエーション請求計算機")
    )

    if lang == "en":
        st.markdown("""
**Every international student who works in Australia is entitled to superannuation.**
Most don't know it exists — or how to claim it when they leave.

When you leave Australia permanently, you can claim your super back through the
**DASP (Departing Australia Superannuation Payment)** system. Tax is deducted (35%),
but it's still thousands of dollars most people walk away from.
""")
    else:
        st.markdown("""
**オーストラリアで働いたすべての留学生はスーパーアニュエーションを受け取る権利があります。**
ほとんどの人はその存在を知らず、帰国時に請求しないまま去ってしまいます。

オーストラリアを永久に離れる際、**DASP（オーストラリア離国時スーパーアニュエーション支払い）**
制度を通じてスーパーを請求できます。35%の税金が差し引かれますが、
それでも多くの人が見捨てている数千ドルです。
""")

    st.markdown("---")

    # ── SGC rates by year ─────────────────────────────────────────────────────
    SGC_RATES = {
        2017: 0.095, 2018: 0.095, 2019: 0.095, 2020: 0.095,
        2021: 0.100, 2022: 0.105, 2023: 0.110, 2024: 0.115,
        2025: 0.120, 2026: 0.120,
    }

    # ── inputs ────────────────────────────────────────────────────────────────
    st.markdown("### " + ("Step 1 — Enter your work history" if lang == "en" else "ステップ1 — 就労歴を入力"))

    col1, col2 = st.columns(2)
    with col1:
        start_year = st.selectbox(
            "Year you started working in Australia" if lang == "en" else "オーストラリアで働き始めた年",
            options=list(range(2017, 2027)),
            index=6,
        )
    with col2:
        end_year = st.selectbox(
            "Year you stopped / last worked" if lang == "en" else "最後に働いた年（または現在）",
            options=list(range(2017, 2027)),
            index=9,
        )

    if end_year < start_year:
        st.error("End year must be after start year." if lang == "en" else "終了年は開始年より後にしてください。")
        st.stop()

    total_income = st.number_input(
        "Total income earned in Australia (AUD) — approximate is fine" if lang == "en"
        else "オーストラリアでの総収入（AUD）— 概算で大丈夫です",
        min_value=0, max_value=500000, value=35000, step=1000,
        help="Add up all your Australian wages. Check your payslips, myTax, or bank statements."
        if lang == "en" else
        "全てのオーストラリアでの賃金を合計してください。給与明細・myTax・銀行明細を確認。",
    )

    # distribute income evenly across years for a weighted SGC estimate
    years_worked = end_year - start_year + 1
    income_per_year = total_income / years_worked if years_worked > 0 else total_income
    weighted_sgc = sum(
        SGC_RATES.get(y, 0.12) * income_per_year
        for y in range(start_year, end_year + 1)
    ) / total_income if total_income > 0 else SGC_RATES.get(start_year, 0.12)

    super_gross   = total_income * weighted_sgc
    dasp_tax      = super_gross * 0.35
    super_net     = super_gross - dasp_tax

    already_found = st.slider(
        "How much super have you already found / confirmed? (AUD)" if lang == "en"
        else "すでに確認済みのスーパー残高は？（AUD）",
        min_value=0, max_value=int(super_gross * 1.5) + 1000,
        value=0, step=100,
        help="If you've already logged into your super fund and seen a balance, enter it here."
        if lang == "en" else
        "すでにスーパーファンドにログインして残高を確認している場合はここに入力。",
    )

    st.markdown("---")

    # ── results ───────────────────────────────────────────────────────────────
    st.markdown("### " + ("Your Result" if lang == "en" else "計算結果"))

    display_gross = already_found if already_found > 0 else super_gross
    display_tax   = display_gross * 0.35
    display_net   = display_gross - display_tax

    r1, r2, r3 = st.columns(3)
    r1.markdown(
        f"<div class='card card-blue'>"
        f"<div class='label-sm'>{'Est. super owed' if lang == 'en' else '推定スーパー残高'}</div>"
        f"<div class='big-number' style='color:#58a6ff'>${display_gross:,.0f}</div>"
        f"<div style='color:#8b949e;font-size:12px'>{'gross, before tax' if lang == 'en' else '税引き前'}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    r2.markdown(
        f"<div class='card card-red'>"
        f"<div class='label-sm'>{'DASP tax (35%)' if lang == 'en' else 'DASP税（35%）'}</div>"
        f"<div class='big-number' style='color:#f85149'>−${display_tax:,.0f}</div>"
        f"<div style='color:#8b949e;font-size:12px'>{'withheld by ATO' if lang == 'en' else 'ATOが源泉徴収'}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    r3.markdown(
        f"<div class='card card-green'>"
        f"<div class='label-sm'>{'You receive' if lang == 'en' else 'あなたが受け取る金額'}</div>"
        f"<div class='big-number'>${display_net:,.0f}</div>"
        f"<div style='color:#8b949e;font-size:12px'>{'after 35% DASP tax' if lang == 'en' else '35% DASP税引き後'}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── in JPY ────────────────────────────────────────────────────────────────
    st.markdown("")
    aud_jpy = st.number_input(
        "AUD/JPY rate (adjust if needed)" if lang == "en" else "AUD/JPY レート（必要に応じて変更）",
        min_value=50.0, max_value=200.0, value=97.0, step=0.5,
    )
    jpy_amount = display_net * aud_jpy
    st.markdown(
        f"<div class='card card-green'>"
        f"<span class='label-sm'>{'In Japanese Yen' if lang == 'en' else '日本円換算'}</span><br>"
        f"<span style='font-size:28px;font-weight:800;color:#3fb950'>¥{jpy_amount:,.0f}</span>"
        f"<span style='color:#8b949e;font-size:13px;margin-left:12px'>"
        f"{'at current AUD/JPY rate' if lang == 'en' else '現在のAUD/JPYレートで'}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── sgc rate note ─────────────────────────────────────────────────────────
    with st.expander("📊 " + ("How is this calculated?" if lang == "en" else "どうやって計算しているの？")):
        rate_data = [(y, f"{r*100:.1f}%") for y, r in SGC_RATES.items()
                     if start_year <= y <= end_year]
        st.dataframe(
            pd.DataFrame(rate_data, columns=["Year", "Super Guarantee Rate"]),
            hide_index=True, use_container_width=True,
        )
        if lang == "en":
            st.markdown("""
The Super Guarantee rate is set by the Australian government and has been increasing
toward 12% by 2025. Your employer is required to pay this percentage of your gross wages
into a super fund on your behalf, on top of your regular pay.

The 35% DASP tax applies to the taxable component when international students claim their
super after permanently departing Australia. It is higher than the tax paid by Australian
residents (15%), but it is still far better than leaving the money behind.
""")
        else:
            st.markdown("""
スーパーギャランティー率はオーストラリア政府が設定しており、2025年に向けて12%まで段階的に引き上げられています。
雇用主は通常の給与に加えて、この割合をスーパーファンドに積み立てる義務があります。

35%のDASP税は、留学生がオーストラリアを永久に離れた後にスーパーを請求する際の課税成分に適用されます。
オーストラリア居住者（15%）より高い税率ですが、お金を置いていくよりはるかに得です。
""")

    # ── how to claim ──────────────────────────────────────────────────────────
    st.markdown("### " + ("Step 2 — How to claim" if lang == "en" else "ステップ2 — 請求方法"))

    steps_en = [
        ("1️⃣", "Find your super fund",
         "Log in to myGov (my.gov.au) → link your ATO account → go to Super. "
         "This shows all super funds linked to your Tax File Number, including lost super."),
        ("2️⃣", "Get your Tax File Number (TFN)",
         "You need your TFN to claim. If you've forgotten it, log in to myGov "
         "or check your old tax return or payslip."),
        ("3️⃣", "Leave Australia first",
         "DASP can only be claimed after you have departed Australia permanently "
         "and your visa has expired or been cancelled."),
        ("4️⃣", "Apply via the ATO DASP portal",
         "Go to: ato.gov.au/dasp — Apply online. You'll need your TFN, passport, "
         "visa details, and super fund details. Processing takes 2–4 weeks."),
        ("5️⃣", "Receive payment",
         "ATO pays directly to your nominated bank account (can be a Japanese bank). "
         "Convert using Wise to get the best AUD/JPY rate."),
    ]
    steps_ja = [
        ("1️⃣", "スーパーファンドを探す",
         "myGov（my.gov.au）にログイン → ATOアカウントを連携 → 「Super」を確認。"
         "税務番号（TFN）に紐づく全てのスーパーファンド（未請求含む）が表示されます。"),
        ("2️⃣", "税務番号（TFN）を確認する",
         "請求にはTFNが必要です。忘れた場合はmyGovにログインするか、"
         "過去の確定申告書または給与明細で確認してください。"),
        ("3️⃣", "まずオーストラリアを離国する",
         "DASPはオーストラリアを永久に離れ、ビザが失効またはキャンセルされた後にのみ申請できます。"),
        ("4️⃣", "ATO DASPポータルで申請する",
         "ato.gov.au/dasp にアクセス → オンラインで申請。"
         "TFN・パスポート・ビザ情報・スーパーファンド情報が必要です。処理に2〜4週間かかります。"),
        ("5️⃣", "受け取り",
         "ATOが指定の銀行口座（日本の銀行口座も可）に直接振り込みます。"
         "Wiseを使って最良のAUD/JPYレートで日本円に換えましょう。"),
    ]

    steps = steps_ja if lang == "ja" else steps_en
    for icon, title, desc in steps:
        st.markdown(
            f"<div class='step-box'>"
            f"<b>{icon} {title}</b><br>"
            f"<span style='color:#8b949e;font-size:13px'>{desc}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown(
        "<div class='card card-blue'>"
        + ("🔗 <b>Official ATO DASP portal:</b> "
           "<a href='https://www.ato.gov.au/individuals-and-families/super-for-individuals-and-families/super/growing-and-keeping-track-of-your-super/keeping-track-of-your-super/departing-australia-superannuation-payment' target='_blank'>"
           "ato.gov.au — Departing Australia Superannuation Payment</a>"
           if lang == "en" else
           "🔗 <b>ATO DASPポータル（公式）：</b> "
           "<a href='https://www.ato.gov.au/individuals-and-families/super-for-individuals-and-families/super/growing-and-keeping-track-of-your-super/keeping-track-of-your-super/departing-australia-superannuation-payment' target='_blank'>"
           "ato.gov.au — 離国時スーパーアニュエーション支払い</a>")
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown(
        "<div class='warn-box'>"
        + ("⚠️ This calculator gives an estimate only. Your actual super balance depends on your "
           "specific employers, whether they paid on time, and any investment returns or fees. "
           "Always verify your actual balance through myGov before claiming."
           if lang == "en" else
           "⚠️ この計算機はあくまで概算です。実際のスーパー残高は雇用主、支払いタイミング、"
           "運用益・手数料によって異なります。請求前に必ずmyGovで実際の残高を確認してください。")
        + "</div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
#  TAX ESTIMATOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧾 Tax Estimator":

    st.markdown("## 🧾 " + ("Tax Estimator" if lang == "en" else "税金計算機"))

    # ── big concept explainer ─────────────────────────────────────────────────
    with st.expander(
        "📖 " + ("Read this first — Australian tax is confusing for international students"
                  if lang == "en" else
                  "まず読んでください — 留学生にとってオーストラリアの税金はわかりにくい"),
        expanded=True,
    ):
        if lang == "en":
            st.markdown("""
**The #1 thing that trips up international students: residency for tax purposes.**

Your *visa type* does NOT determine how you're taxed. Your *time spent in Australia* does.

| Your situation | Tax status | Key difference |
|---|---|---|
| In Australia 183+ days in the tax year | **Australian tax resident** | $18,200 tax-free threshold. You pay 0% on the first $18,200. |
| In Australia less than 183 days | **Foreign resident for tax** | No tax-free threshold. Taxed at 32.5% from dollar 1. |
| Working Holiday visa (417 or 462) | **Working Holiday Maker** | Special flat rate: 15% on first $45,000. |

**Most student visa (500) holders who study a full year are Australian tax residents.**
This is good — it means you likely have tax withheld at the higher foreign-resident rate
by employers who don't know your status, which means you're probably owed a refund.

**Tax year in Australia:** 1 July → 30 June (not a calendar year).
""")
        else:
            st.markdown("""
**留学生が最も混乱するポイント：税務上の居住者ステータス**

課税方法はビザの種類ではなく、**オーストラリアで過ごした日数**で決まります。

| あなたの状況 | 税務ステータス | 主な違い |
|---|---|---|
| 税年度内に183日以上滞在 | **オーストラリア税務居住者** | $18,200まで非課税。最初の$18,200は0%。 |
| 183日未満の滞在 | **非居住者（外国居住者）** | 非課税枠なし。1ドルから32.5%課税。 |
| ワーキングホリデービザ（417/462） | **ワーキングホリデーメーカー** | 特別レート：最初の$45,000は15%。 |

**1年間フルに学ぶ学生ビザ（500）保持者の多くはオーストラリア税務居住者です。**
これは有利です — 雇用主があなたのステータスを知らずに高い外国居住者税率で源泉徴収している
場合が多いため、還付を受けられる可能性が高いです。

**オーストラリアの税年度：** 7月1日 → 翌年6月30日（暦年ではない）
""")

    st.markdown("---")

    # ── tax calculation helpers ───────────────────────────────────────────────
    def calc_resident_tax(income: float) -> float:
        if income <= 18200:
            return 0.0
        elif income <= 45000:
            return (income - 18200) * 0.19
        elif income <= 120000:
            return 5092 + (income - 45000) * 0.325
        elif income <= 180000:
            return 29467 + (income - 120000) * 0.37
        else:
            return 51667 + (income - 180000) * 0.45

    def calc_foreign_tax(income: float) -> float:
        if income <= 135000:
            return income * 0.325
        elif income <= 190000:
            return 43875 + (income - 135000) * 0.37
        else:
            return 64225 + (income - 190000) * 0.45

    def calc_whm_tax(income: float) -> float:
        if income <= 45000:
            return income * 0.15
        elif income <= 120000:
            return 6750 + (income - 45000) * 0.325
        elif income <= 180000:
            return 31125 + (income - 120000) * 0.37
        else:
            return 53325 + (income - 180000) * 0.45

    def calc_lito(income: float) -> float:
        if income <= 37500:
            return 700.0
        elif income <= 45000:
            return 700 - (income - 37500) * 0.05
        elif income <= 66667:
            return 325 - (income - 45000) * 0.015
        else:
            return 0.0

    # ── inputs ────────────────────────────────────────────────────────────────
    st.markdown("### " + ("Step 1 — Your situation" if lang == "en" else "ステップ1 — あなたの状況"))

    # financial year bounds
    FY_RANGES = {
        "FY2025-26": (date(2025, 7, 1), date(2026, 6, 30)),
        "FY2024-25": (date(2024, 7, 1), date(2025, 6, 30)),
        "FY2023-24": (date(2023, 7, 1), date(2024, 6, 30)),
        "FY2022-23": (date(2022, 7, 1), date(2023, 6, 30)),
    }
    MONTHS_EN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    MONTHS_JA = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]
    MONTH_LABELS = MONTHS_JA if lang == "ja" else MONTHS_EN
    YEARS = list(range(2020, 2027))

    col_a, col_b = st.columns(2)
    with col_a:
        fy = st.selectbox(
            "Financial year" if lang == "en" else "会計年度",
            list(FY_RANGES.keys()),
            index=0,
            help="Australian tax year runs 1 Jul to 30 Jun."
                 if lang == "en" else
                 "オーストラリアの税年度は7月1日〜翌年6月30日。",
        )
    with col_b:
        visa_opts_en = [
            "🎓 Student visa (subclass 500)",
            "🏆 Graduate visa (subclass 485)",
            "🎒 Working Holiday (subclass 417)",
            "🎒 Work and Holiday (subclass 462)",
            "🔧 Temporary Skill Shortage (subclass 482)",
            "🌏 Other temporary visa",
        ]
        visa_opts_ja = [
            "🎓 学生ビザ（サブクラス500）",
            "🏆 卒業生ビザ（サブクラス485）",
            "🎒 ワーキングホリデー（サブクラス417）",
            "🎒 ワーキングホリデー（サブクラス462）",
            "🔧 一時技能不足ビザ（サブクラス482）",
            "🌏 その他の一時ビザ",
        ]
        visa_opts  = visa_opts_ja if lang == "ja" else visa_opts_en
        # pre-select index based on global visa chosen in sidebar
        _gv_to_tax_idx = {
            "student_500": 0, "grad_485": 1, "whm_417": 2,
            "whm_462": 3, "work_482": 4, "other": 5,
        }
        _tax_default_idx = _gv_to_tax_idx.get(gv, 0)
        visa_sel   = st.selectbox(
            "Your visa type" if lang == "en" else "ビザの種類",
            visa_opts,
            index=_tax_default_idx,
        )
        is_whm = "417" in visa_sel or "462" in visa_sel

    # work rights mini-card per visa ──────────────────────────────────────────
    WORK_RIGHTS = {
        "500": (
            "🎓 Student visa (500)",
            "学生ビザ（500）",
            "48 hrs/fortnight during semester · Unlimited during official holiday periods · Super entitlements apply from day 1",
            "学期中48時間/2週間 · 公式休暇期間は無制限 · スーパーは初日から権利あり",
            "card-blue",
        ),
        "485": (
            "🏆 Graduate visa (485)",
            "卒業生ビザ（485）",
            "Full work rights · No hour limits · Super entitlements apply · Valid 2–5 years post-graduation",
            "フルの就労権 · 時間制限なし · スーパー権利あり · 卒業後2〜5年有効",
            "card-green",
        ),
        "417": (
            "🎒 Working Holiday (417)",
            "ワーキングホリデー（417）",
            "Unlimited hours · Max 6 months with one employer · Special 15% tax rate · Super entitlements apply",
            "時間無制限 · 1雇用主最大6ヶ月 · 特別15%税率 · スーパー権利あり",
            "card-yellow",
        ),
        "462": (
            "🎒 Work and Holiday (462)",
            "ワーキングホリデー（462）",
            "Unlimited hours · Max 6 months with one employer · Special 15% tax rate · Super entitlements apply",
            "時間無制限 · 1雇用主最大6ヶ月 · 特別15%税率 · スーパー権利あり",
            "card-yellow",
        ),
        "482": (
            "🔧 TSS visa (482)",
            "一時技能不足ビザ（482）",
            "Work only for sponsoring employer · Hours set by contract · Super entitlements apply · Taxed as resident if 183+ days",
            "スポンサー雇用主のみ就労可 · 契約による時間 · スーパー権利あり · 183日以上で居住者課税",
            "card-blue",
        ),
        "other": (
            "🌏 Other temporary visa",
            "その他の一時ビザ",
            "Work rights depend on your specific visa conditions — check immi.homeaffairs.gov.au",
            "就労権はビザの条件によります — immi.homeaffairs.gov.auで確認",
            "card-yellow",
        ),
    }
    vkey = (
        "417" if "417" in visa_sel else
        "462" if "462" in visa_sel else
        "485" if "485" in visa_sel else
        "482" if "482" in visa_sel else
        "500" if "500" in visa_sel else
        "other"
    )
    vt = WORK_RIGHTS[vkey]
    v_title = vt[1] if lang == "ja" else vt[0]
    v_desc  = vt[3] if lang == "ja" else vt[2]
    st.markdown(
        f"<div class='card {vt[4]}' style='padding:10px 16px;margin:8px 0'>"
        f"<b style='color:#e6edf3'>{v_title}</b><br>"
        f"<span style='color:#8b949e;font-size:12px'>{v_desc}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    fy_start, fy_end = FY_RANGES[fy]

    if is_whm:
        tax_status = "whm"
        st.markdown(
            "<div class='step-box'>🎒 "
            + ("Working Holiday Maker rate applies: <b>15% flat on first $45,000</b>, "
               "then standard brackets above that. No tax-free threshold."
               if lang == "en" else
               "ワーキングホリデーレート適用：<b>最初の$45,000は一律15%</b>、以降は通常の税率。非課税枠なし。")
            + "</div>",
            unsafe_allow_html=True,
        )
    else:
        # ── arrival / departure month selectors ───────────────────────────────
        st.markdown(
            "<span style='color:#8b949e;font-size:13px'>"
            + ("Enter when you arrived and left Australia — we'll calculate your days automatically."
               if lang == "en" else
               "オーストラリアへの入国・出国月を入力 — 滞在日数を自動計算します。")
            + "</span>",
            unsafe_allow_html=True,
        )
        ca1, ca2, ca3, ca4 = st.columns(4)
        with ca1:
            arr_m = st.selectbox(
                "Arrived (month)" if lang == "en" else "入国（月）",
                MONTH_LABELS, index=8,
            )
        with ca2:
            arr_y = st.selectbox(
                "Arrived (year)" if lang == "en" else "入国（年）",
                YEARS, index=4,
            )
        with ca3:
            still_here = st.checkbox(
                "Still in AU" if lang == "en" else "まだ滞在中",
                value=False,
            )
        with ca4:
            if not still_here:
                dep_m = st.selectbox(
                    "Left (month)" if lang == "en" else "出国（月）",
                    MONTH_LABELS, index=5,
                )
                dep_y = st.selectbox(
                    "Left (year)" if lang == "en" else "出国（年）",
                    YEARS, index=5,
                )

        # build dates — use 1st of arrival month, last day of departure month
        arr_month_idx = MONTH_LABELS.index(arr_m) + 1
        arr_date = date(arr_y, arr_month_idx, 1)

        if still_here:
            dep_date = date.today()
        else:
            dep_month_idx = MONTH_LABELS.index(dep_m) + 1
            # last day of departure month
            if dep_month_idx == 12:
                dep_date = date(dep_y, 12, 31)
            else:
                dep_date = date(dep_y, dep_month_idx + 1, 1) - __import__("datetime").timedelta(days=1)

        # clamp to the selected FY
        eff_start  = max(arr_date, fy_start)
        eff_end    = min(dep_date, fy_end)
        days_in_fy = max(0, (eff_end - eff_start).days)

        if days_in_fy >= 183:
            tax_status = "resident"
            st.markdown(
                "<div class='card card-green' style='padding:12px 16px;margin:8px 0'>"
                f"<b style='color:#3fb950'>✅ ~{days_in_fy} days in Australia during {fy}</b><br>"
                "<span style='color:#8b949e;font-size:13px'>"
                + ("183+ days → you are likely an <b>Australian tax resident</b>. "
                   "You get the $18,200 tax-free threshold."
                   if lang == "en" else
                   "183日以上 → <b>オーストラリア税務居住者</b>の可能性が高いです。"
                   "$18,200まで非課税枠があります。")
                + "</span></div>",
                unsafe_allow_html=True,
            )
        elif days_in_fy > 0:
            tax_status = "foreign"
            st.markdown(
                "<div class='card card-yellow' style='padding:12px 16px;margin:8px 0'>"
                f"<b style='color:#d29922'>⚠️ ~{days_in_fy} days in Australia during {fy}</b><br>"
                "<span style='color:#8b949e;font-size:13px'>"
                + ("Under 183 days → you are likely a <b>foreign resident for tax</b>. "
                   "No tax-free threshold — taxed at 32.5% from dollar 1."
                   if lang == "en" else
                   "183日未満 → <b>外国居住者（税務上）</b>の可能性が高いです。"
                   "非課税枠なし — 1ドルから32.5%課税。")
                + "</span></div>",
                unsafe_allow_html=True,
            )
        else:
            tax_status = "foreign"
            st.warning(
                "No days in Australia fall within this financial year. Check your dates."
                if lang == "en" else
                "この会計年度内にオーストラリア滞在日数がありません。日付を確認してください。"
            )

    # ── Step 2: income breakdown ──────────────────────────────────────────────
    st.markdown("### " + ("Step 2 — Income" if lang == "en" else "ステップ2 — 収入"))

    ic1, ic2 = st.columns(2)
    with ic1:
        payg_income = st.number_input(
            "💼 PAYG wages (jobs with tax withheld)" if lang == "en"
            else "💼 PAYG賃金（源泉徴収あり）",
            min_value=0, max_value=300000, value=28000, step=500,
            help="Regular employment where your employer deducts tax from each pay."
                 if lang == "en" else "雇用主が毎回の給与から税金を差し引く通常の雇用。",
        )
        tax_withheld = st.number_input(
            "Tax withheld from above (AUD) — from payslips or myGov"
            if lang == "en" else
            "上記から源泉徴収された税額（AUD）— 給与明細またはmyGovで確認",
            min_value=0, max_value=150000, value=6000, step=100,
            help="Total PAYG tax deducted across all your payslips this financial year."
                 if lang == "en" else "この会計年度の全給与明細から差し引かれたPAYG税の合計。",
        )
    with ic2:
        abn_income = st.number_input(
            "🛵 ABN / gig income (Uber Eats, DoorDash, Airtasker, freelance)"
            if lang == "en" else
            "🛵 ABN・ギグ収入（Uber Eats・DoorDash・Airtasker・フリーランス）",
            min_value=0, max_value=300000, value=0, step=500,
            help="Income earned with an ABN where NO tax is withheld. You pay this yourself at tax time."
                 if lang == "en" else
                 "ABNで得た収入で税金が源泉徴収されていないもの。確定申告時に自分で納税します。",
        )
        if abn_income > 0:
            st.markdown(
                "<div class='warn-box' style='font-size:12px;padding:8px 12px'>"
                + ("⚠️ No tax withheld on ABN income — expect a tax bill on this portion."
                   if lang == "en" else
                   "⚠️ ABN収入には源泉徴収なし — この部分の税金は自分で支払います。")
                + "</div>",
                unsafe_allow_html=True,
            )

    total_gross_income = payg_income + abn_income

    # ── Step 3: deductions ────────────────────────────────────────────────────
    st.markdown("### " + ("Step 3 — Deductions (reduces your tax)" if lang == "en" else "ステップ3 — 控除（税金を下げる）"))

    if lang == "en":
        st.caption("These are work-related expenses you can claim to reduce your taxable income. Only include what you genuinely spent for work — the ATO can audit deductions.")
    else:
        st.caption("仕事に関連した経費で課税所得を下げることができます。実際に仕事のために使った費用のみ申告してください。")

    # ATO cents-per-km rates by FY
    CPK_RATES = {"FY2025-26": 0.91, "FY2024-25": 0.88, "FY2023-24": 0.85, "FY2022-23": 0.78}
    cpk_rate = CPK_RATES.get(fy, 0.88)

    with st.expander("🚗 " + ("Vehicle / delivery km" if lang == "en" else "車・配達の走行距離"), expanded=(abn_income > 0)):
        if lang == "en":
            st.caption(f"ATO rate for {fy}: **{cpk_rate} cents per km** (up to 5,000 km max). For Uber Eats, DoorDash, or any work driving.")
        else:
            st.caption(f"{fy}のATOレート：**1kmあたり{cpk_rate}セント**（最大5,000km）。Uber Eats・DoorDash・業務運転すべて対象。")
        work_km = st.number_input(
            "Work-related km driven this year" if lang == "en" else "今年の業務走行距離（km）",
            min_value=0, max_value=5000, value=0, step=50,
        )
        vehicle_deduction = min(work_km, 5000) * cpk_rate
        if work_km > 0:
            st.success(f"{'Vehicle deduction' if lang == 'en' else '車両控除'}: A${vehicle_deduction:,.2f}")

    with st.expander("📱 " + ("Phone & internet" if lang == "en" else "スマホ・インターネット")):
        if lang == "en":
            st.caption("Claim the work-use % of your total annual phone/internet bill. For Uber Eats: delivery app use, maps, customer calls = often 60–80%.")
        else:
            st.caption("年間のスマホ・インターネット料金の業務使用割合を申請。Uber Eats：アプリ・地図・顧客対応 = 通常60〜80%。")
        ph1, ph2 = st.columns(2)
        with ph1:
            phone_total = st.number_input(
                "Annual phone + internet bill (AUD)" if lang == "en" else "年間スマホ・通信費合計（AUD）",
                min_value=0, max_value=5000, value=0, step=50,
            )
        with ph2:
            phone_work_pct = st.slider(
                "Work use %" if lang == "en" else "業務使用割合 %",
                min_value=0, max_value=100, value=50, step=5,
            )
        phone_deduction = phone_total * phone_work_pct / 100
        if phone_total > 0:
            st.success(f"{'Phone deduction' if lang == 'en' else '通信費控除'}: A${phone_deduction:,.2f}")

    with st.expander("🏠 " + ("Home office" if lang == "en" else "在宅勤務")):
        if lang == "en":
            st.caption(f"ATO fixed rate method: **67 cents per hour** worked from home. Covers electricity, internet, stationery. Applies from FY2022-23 onwards.")
        else:
            st.caption(f"ATO固定レート方式：在宅勤務**1時間あたり67セント**。電気・インターネット・文具代をカバー。FY2022-23以降適用。")
        home_hours = st.number_input(
            "Hours worked from home this year" if lang == "en" else "今年の在宅勤務時間数",
            min_value=0, max_value=3000, value=0, step=10,
        )
        home_deduction = home_hours * 0.67
        if home_hours > 0:
            st.success(f"{'Home office deduction' if lang == 'en' else '在宅勤務控除'}: A${home_deduction:,.2f}")

    with st.expander("🛍️ " + ("Equipment, uniform & other" if lang == "en" else "機器・制服・その他")):
        if lang == "en":
            st.caption("Work equipment under $300 can be claimed in full immediately. Over $300 is depreciated. Insulated delivery bags, safety shoes, uniforms all count.")
        else:
            st.caption("$300未満の業務機器はすぐに全額申請可能。$300以上は減価償却。保温バッグ・安全靴・制服もすべて対象。")
        eq1, eq2 = st.columns(2)
        with eq1:
            equipment_deduction = st.number_input(
                "Work equipment & tools (AUD)" if lang == "en" else "業務機器・道具（AUD）",
                min_value=0, max_value=10000, value=0, step=50,
                help="Laptop, tools, safety gear, insulated delivery bag, helmet, etc."
                     if lang == "en" else "PC・道具・安全用品・保温バッグ・ヘルメットなど。",
            )
        with eq2:
            uniform_deduction = st.number_input(
                "Uniform / laundry (AUD)" if lang == "en" else "制服・洗濯費（AUD）",
                min_value=0, max_value=2000, value=0, step=10,
                help="Compulsory uniforms or protective clothing. Laundry costs at $1/load."
                     if lang == "en" else "義務付けられた制服または保護服。洗濯費は1回$1。",
            )
        other_deduction = st.number_input(
            "Other work-related deductions (AUD)" if lang == "en" else "その他の業務関連控除（AUD）",
            min_value=0, max_value=10000, value=0, step=50,
            help="Union fees, professional memberships, self-education directly related to current job."
                 if lang == "en" else "組合費・専門職会費・現在の仕事に直接関連する自己啓発費。",
        )

    total_deductions = vehicle_deduction + phone_deduction + home_deduction + equipment_deduction + uniform_deduction + other_deduction
    taxable_income   = max(0.0, total_gross_income - total_deductions)

    if total_deductions > 0:
        st.markdown(
            f"<div class='card card-green' style='padding:10px 16px'>"
            f"<span style='color:#8b949e;font-size:12px'>{'Total deductions' if lang == 'en' else '控除合計'}</span> "
            f"<b style='color:#3fb950;font-size:18px'>−A${total_deductions:,.0f}</b>"
            f"<span style='color:#8b949e;font-size:12px;margin-left:16px'>"
            f"{'Taxable income' if lang == 'en' else '課税所得'}: A${taxable_income:,.0f}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── Step 4: other settings ────────────────────────────────────────────────
    st.markdown("### " + ("Step 4 — Final settings" if lang == "en" else "ステップ4 — その他の設定"))

    col_c, col_d = st.columns(2)
    with col_c:
        # WHMs are NOT Medicare exempt; students/grads usually are
        _medicare_default = not is_whm_global
        medicare_exempt = st.checkbox(
            "Medicare Levy exempt (most international students qualify)"
            if lang == "en" else
            "メディケアレビー免除（ほとんどの留学生が対象）",
            value=_medicare_default,
            help="International students on student visas can apply for a Medicare Levy Exemption "
                 "Certificate from Medicare Australia. Working Holiday Makers are NOT exempt."
                 if lang == "en" else
                 "学生ビザの留学生はメディケアオーストラリアから免除証明書を取得できます。"
                 "ワーキングホリデーは対象外です。",
        )
    with col_d:
        has_tfn = st.checkbox(
            "You provided your TFN to all employers"
            if lang == "en" else "全雇用主にTFN（税務番号）を提供した",
            value=True,
            help="Without a TFN, employers must withhold at 47% (top rate). "
                 "No-TFN withholding often creates a large refund."
                 if lang == "en" else
                 "TFNなしの場合、雇用主は47%（最高税率）で源泉徴収。大きな還付が発生することがあります。",
        )
    if not has_tfn and tax_withheld < payg_income * 0.40:
        st.markdown(
            "<div class='warn-box' style='font-size:12px;padding:8px 12px'>"
            + ("⚠️ Without a TFN, your employer should have withheld ~47%. "
               "Your entered withheld amount looks low — double-check your payslips."
               if lang == "en" else
               "⚠️ TFNなしの場合、雇用主は約47%を源泉徴収するはずです。"
               "入力した源泉徴収額が少ないようです — 給与明細を再確認してください。")
            + "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── calculations ──────────────────────────────────────────────────────────
    if tax_status == "resident":
        gross_tax = calc_resident_tax(taxable_income)
        lito      = calc_lito(taxable_income)
    elif tax_status == "foreign":
        gross_tax = calc_foreign_tax(taxable_income)
        lito      = 0.0
    else:
        gross_tax = calc_whm_tax(taxable_income)
        lito      = 0.0

    medicare  = 0.0 if medicare_exempt else taxable_income * 0.02
    tax_owed  = max(0.0, gross_tax - lito + medicare)
    balance   = tax_withheld - tax_owed   # positive = refund, negative = bill

    st.markdown("### " + ("Your Result" if lang == "en" else "計算結果"))

    r1, r2, r3, r4 = st.columns(4)
    r1.markdown(
        f"<div class='card card-blue'>"
        f"<div class='label-sm'>{'Gross income' if lang == 'en' else '総収入'}</div>"
        f"<div style='font-size:22px;font-weight:800;color:#58a6ff'>${total_gross_income:,.0f}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    r2.markdown(
        f"<div class='card card-green'>"
        f"<div class='label-sm'>{'Deductions' if lang == 'en' else '控除'}</div>"
        f"<div style='font-size:22px;font-weight:800;color:#3fb950'>−${total_deductions:,.0f}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    r3.markdown(
        f"<div class='card card-yellow'>"
        f"<div class='label-sm'>{'LITO offset' if lang == 'en' else 'LITOオフセット'}</div>"
        f"<div style='font-size:22px;font-weight:800;color:#d29922'>−${lito:,.0f}</div>"
        f"<div style='color:#8b949e;font-size:10px'>{'residents only' if lang == 'en' else '居住者のみ'}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    r4.markdown(
        f"<div class='card card-blue'>"
        f"<div class='label-sm'>{'Tax owed' if lang == 'en' else '税額'}</div>"
        f"<div style='font-size:22px;font-weight:800;color:#58a6ff'>${tax_owed:,.0f}</div>"
        f"<div style='color:#8b949e;font-size:10px'>{'after offsets' if lang == 'en' else 'オフセット後'}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("")

    # ── refund vs bill ────────────────────────────────────────────────────────
    if balance >= 0:
        st.markdown(
            f"<div class='card card-green' style='text-align:center;padding:24px'>"
            f"<div class='label-sm'>{'🎉 Estimated tax refund' if lang == 'en' else '🎉 推定税金還付額'}</div>"
            f"<div style='font-size:52px;font-weight:900;color:#3fb950'>${balance:,.0f}</div>"
            f"<div style='color:#8b949e;font-size:13px'>"
            + (f"You withheld ${tax_withheld:,.0f} · Tax owed ${tax_owed:,.0f} · Deductions saved you ${total_deductions:,.0f} in taxable income"
               if lang == "en" else
               f"源泉徴収額${tax_withheld:,.0f} · 税額${tax_owed:,.0f} · 控除で課税所得${total_deductions:,.0f}を削減")
            + f"</div></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='card card-red' style='text-align:center;padding:24px'>"
            f"<div class='label-sm'>{'⚠️ Estimated amount owing' if lang == 'en' else '⚠️ 追加納税額'}</div>"
            f"<div style='font-size:52px;font-weight:900;color:#f85149'>${abs(balance):,.0f}</div>"
            f"<div style='color:#8b949e;font-size:13px'>"
            + (f"Tax owed ${tax_owed:,.0f} · Only ${tax_withheld:,.0f} withheld"
               + (f" · Your ABN income of ${abn_income:,.0f} had no tax withheld" if abn_income > 0 else "")
               if lang == "en" else
               f"税額${tax_owed:,.0f} · 源泉徴収額${tax_withheld:,.0f}"
               + (f" · ABN収入${abn_income:,.0f}は源泉徴収なし" if abn_income > 0 else ""))
            + f"</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("")

    # ── full breakdown table ──────────────────────────────────────────────────
    with st.expander("📊 " + ("Full breakdown" if lang == "en" else "詳細内訳")):
        rows_en = [
            ("PAYG wages (employer withholds tax)", f"${payg_income:,.0f}"),
            ("ABN / gig income (no tax withheld)", f"${abn_income:,.0f}"),
            ("Total gross income", f"${total_gross_income:,.0f}"),
            ("Vehicle deduction", f"−${vehicle_deduction:,.2f}"),
            ("Phone & internet deduction", f"−${phone_deduction:,.2f}"),
            ("Home office deduction", f"−${home_deduction:,.2f}"),
            ("Equipment & uniform deduction", f"−${equipment_deduction + uniform_deduction:,.2f}"),
            ("Other deductions", f"−${other_deduction:,.2f}"),
            ("Taxable income", f"${taxable_income:,.0f}"),
            ("Tax status", {"resident": "Australian resident", "foreign": "Foreign resident", "whm": "Working Holiday Maker"}[tax_status]),
            ("Gross income tax", f"${gross_tax:,.0f}"),
            ("Low Income Tax Offset (LITO)", f"−${lito:,.0f}"),
            ("Medicare Levy (2%)", "Exempt" if medicare_exempt else f"${medicare:,.0f}"),
            ("Total tax owed", f"${tax_owed:,.0f}"),
            ("Tax already withheld", f"${tax_withheld:,.0f}"),
            ("Result", f"{'REFUND' if balance >= 0 else 'OWING'}: ${abs(balance):,.0f}"),
        ]
        rows_ja = [
            ("PAYG賃金（源泉徴収あり）", f"${payg_income:,.0f}"),
            ("ABN・ギグ収入（源泉徴収なし）", f"${abn_income:,.0f}"),
            ("総収入", f"${total_gross_income:,.0f}"),
            ("車両控除", f"−${vehicle_deduction:,.2f}"),
            ("スマホ・通信費控除", f"−${phone_deduction:,.2f}"),
            ("在宅勤務控除", f"−${home_deduction:,.2f}"),
            ("機器・制服控除", f"−${equipment_deduction + uniform_deduction:,.2f}"),
            ("その他控除", f"−${other_deduction:,.2f}"),
            ("課税所得", f"${taxable_income:,.0f}"),
            ("税務ステータス", {"resident": "オーストラリア居住者", "foreign": "外国居住者", "whm": "ワーキングホリデー"}[tax_status]),
            ("総所得税", f"${gross_tax:,.0f}"),
            ("低所得税オフセット（LITO）", f"−${lito:,.0f}"),
            ("メディケアレビー（2%）", "免除" if medicare_exempt else f"${medicare:,.0f}"),
            ("納税額合計", f"${tax_owed:,.0f}"),
            ("源泉徴収済み税額", f"${tax_withheld:,.0f}"),
            ("結果", f"{'還付' if balance >= 0 else '追加納税'}: ${abs(balance):,.0f}"),
        ]
        rows = rows_ja if lang == "ja" else rows_en
        st.dataframe(
            pd.DataFrame(rows, columns=["Item" if lang == "en" else "項目", "Amount" if lang == "en" else "金額"]),
            hide_index=True, use_container_width=True,
        )

        if not has_tfn:
            st.warning(
                "⚠️ Without a TFN, your employer should have withheld at 47%. "
                "This means your withheld amount may be much higher than shown — "
                "update the 'tax withheld' field with your actual payslip numbers."
                if lang == "en" else
                "⚠️ TFNなしの場合、雇用主は47%で源泉徴収しているはずです。"
                "実際の給与明細の数字を「源泉徴収額」欄に入力してください。"
            )

        if lang == "en":
            st.markdown("""
**How Australian tax brackets work (progressive system):**
You don't pay the top rate on all income — only on the portion above each threshold.
Example for a resident earning $40,000:
- First $18,200 → $0 tax
- Next $21,800 ($18,201–$40,000) → × 19% = $4,142
- Total gross tax: **$4,142**
- Minus LITO ($700 - ($40,000-$37,500)×0.05 = $575): **$3,567 final tax**
""")
        else:
            st.markdown("""
**オーストラリアの累進課税の仕組み：**
収入全体に最高税率が適用されるのではなく、各しきい値を超えた部分にのみ適用されます。
例：居住者で$40,000の収入の場合：
- 最初の$18,200 → 税金$0
- 次の$21,800（$18,201〜$40,000）→ × 19% = $4,142
- 総所得税：**$4,142**
- LITOを差し引く（$700 - ($40,000-$37,500)×0.05 = $575）：**最終税額 $3,567**
""")

    st.markdown("---")

    # ── how to lodge ──────────────────────────────────────────────────────────
    st.markdown("### " + ("Step 2 — How to lodge your tax return" if lang == "en" else "ステップ2 — 確定申告の方法"))

    lodge_steps_en = [
        ("1️⃣", "Wait until after 31 July",
         "Most employers upload your income statement to myGov by 31 July. "
         "If you lodge too early, income data may be missing and you'll need to amend."),
        ("2️⃣", "Log in to myGov → link ATO",
         "Go to my.gov.au. Link your ATO account if you haven't already. "
         "Your TFN is needed. If you've forgotten your TFN, it's in myGov under ATO."),
        ("3️⃣", "Lodge via myTax (free)",
         "ATO online tax return is called myTax. It pre-fills most data from your employer. "
         "Takes about 20 minutes. You can do it yourself — it's straightforward."),
        ("4️⃣", "Claim your deductions",
         "Work-related expenses: uniform, equipment, professional memberships, study materials "
         "directly related to your current job (not your degree). Keep receipts."),
        ("5️⃣", "Receive your refund",
         "ATO processes most refunds within 2 weeks. Paid directly to your Australian bank account. "
         "If you've already closed your account, update your bank details in myGov first."),
    ]
    lodge_steps_ja = [
        ("1️⃣", "7月31日以降に申告する",
         "ほとんどの雇用主は7月31日までに所得明細をmyGovにアップロードします。"
         "早く申告しすぎると収入データが欠落し、修正が必要になる場合があります。"),
        ("2️⃣", "myGovにログイン → ATOを連携",
         "my.gov.auにアクセス。まだATOアカウントを連携していない場合は連携してください。"
         "TFNが必要です。TFNを忘れた場合は、myGovのATO下で確認できます。"),
        ("3️⃣", "myTaxで申告（無料）",
         "ATOのオンライン確定申告はmyTaxと呼ばれます。雇用主からのデータが自動入力されます。"
         "約20分で完了。難しくないので自分でできます。"),
        ("4️⃣", "経費控除を申請する",
         "業務関連費用：制服、機器、職業団体会費、現在の仕事に直接関連する学習教材"
         "（学位コース自体は対象外）。領収書を保管してください。"),
        ("5️⃣", "還付金を受け取る",
         "ATOはほとんどの還付を2週間以内に処理します。オーストラリアの銀行口座に直接振り込まれます。"
         "すでに口座を閉鎖している場合は、先にmyGovで銀行情報を更新してください。"),
    ]
    lodge_steps = lodge_steps_ja if lang == "ja" else lodge_steps_en
    for icon, title, desc in lodge_steps:
        st.markdown(
            f"<div class='step-box'>"
            f"<b>{icon} {title}</b><br>"
            f"<span style='color:#8b949e;font-size:13px'>{desc}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown(
        "<div class='card card-blue'>"
        + ("🔗 <b>Lodge your tax return free:</b> "
           "<a href='https://www.ato.gov.au/individuals-and-families/lodging-your-tax-return/lodge-your-tax-return-online-with-mytax' target='_blank'>"
           "ato.gov.au — myTax online lodgment</a>"
           if lang == "en" else
           "🔗 <b>無料で確定申告：</b> "
           "<a href='https://www.ato.gov.au/individuals-and-families/lodging-your-tax-return/lodge-your-tax-return-online-with-mytax' target='_blank'>"
           "ato.gov.au — myTaxオンライン申告</a>")
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown(
        "<div class='warn-box'>"
        + ("⚠️ This is an estimate. Your actual tax depends on deductions, other income sources, "
           "and your exact residency determination. If your situation is complex (multiple jobs, "
           "overseas income, visa changes mid-year), consider using a registered tax agent (~$80–150 AUD)."
           if lang == "en" else
           "⚠️ これは概算です。実際の税額は控除額、その他の収入源、正確な居住者判定によって異なります。"
           "状況が複雑な場合（複数の仕事、海外収入、年度途中のビザ変更など）は"
           "登録税務代理人（約$80〜150 AUD）の利用をご検討ください。")
        + "</div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
#  MONEY TRANSFER COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💸 Money Transfer":

    st.markdown("## 💸 " + ("Money Transfer Comparison" if lang == "en" else "海外送金比較"))

    # ── the problem ───────────────────────────────────────────────────────────
    st.markdown(
        "<div class='card card-red'>"
        + ("<b style='color:#f85149'>Australian banks charge 3–5% on international transfers.</b>"
           " On a $5,000 AUD transfer that's $150–$250 lost to fees — before you even notice."
           "<br><span style='color:#8b949e;font-size:13px'>Wise charges around 0.5%. "
           "The difference on a $5,000 transfer: you keep an extra ~$175 AUD.</span>"
           if lang == "en" else
           "<b style='color:#f85149'>オーストラリアの銀行は海外送金に3〜5%を請求します。</b>"
           " $5,000 AUDの送金なら$150〜$250が手数料として消えます。"
           "<br><span style='color:#8b949e;font-size:13px'>Wiseの手数料は約0.5%。"
           "$5,000の送金での差額：約$175 AUD多く受け取れます。</span>")
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── provider data ─────────────────────────────────────────────────────────
    # (name, rate_markup, flat_fee_aud, colour, category)
    # rate_markup = % added on top of mid-market rate (their profit on the exchange)
    # flat_fee_aud = fixed transfer fee in AUD equivalent
    PROVIDERS = [
        ("Wise",          0.005,  0.00, "#3fb950", "best"),
        ("Remitly",       0.015,  3.99, "#58a6ff", "good"),
        ("Western Union", 0.020,  5.00, "#8b949e", "ok"),
        ("NAB",           0.035,  8.00, "#d29922", "bank"),
        ("CommBank",      0.035,  6.00, "#d29922", "bank"),
        ("ANZ",           0.040,  9.00, "#f85149", "bank"),
        ("Westpac",       0.040,  9.00, "#f85149", "bank"),
    ]

    CURRENCIES = {
        "🇯🇵 JPY (Japanese Yen)":     ("JPY", 97.0),
        "🇨🇳 CNY (Chinese Yuan)":     ("CNY", 4.65),
        "🇰🇷 KRW (Korean Won)":       ("KRW", 920.0),
        "🇮🇳 INR (Indian Rupee)":     ("INR", 54.0),
        "🇬🇧 GBP (British Pound)":    ("GBP", 0.51),
        "🇺🇸 USD (US Dollar)":        ("USD", 0.64),
    }

    # ── inputs ────────────────────────────────────────────────────────────────
    st.markdown("### " + ("Step 1 — Your transfer" if lang == "en" else "ステップ1 — 送金情報"))

    col1, col2 = st.columns(2)
    with col1:
        send_aud = st.number_input(
            "Amount to send (AUD)" if lang == "en" else "送金額（AUD）",
            min_value=100, max_value=100000, value=5000, step=100,
        )
    with col2:
        currency_label = st.selectbox(
            "Destination currency" if lang == "en" else "受取通貨",
            list(CURRENCIES.keys()),
        )
    currency_code, default_rate = CURRENCIES[currency_label]

    rate = st.number_input(
        f"Current mid-market AUD/{currency_code} rate (adjust if needed)"
        if lang == "en" else
        f"現在のAUD/{currency_code} レート（必要に応じて変更）",
        min_value=0.01, max_value=100000.0, value=float(default_rate), step=0.1,
        format="%.2f",
    )

    st.markdown("---")

    # ── calculations ──────────────────────────────────────────────────────────
    results = []
    for name, markup, flat_fee, colour, cat in PROVIDERS:
        aud_after_fee  = max(0.0, send_aud - flat_fee)
        effective_rate = rate * (1 - markup)
        recipient_gets = aud_after_fee * effective_rate
        # total cost in AUD = what you sent minus what arrived back-converted at mid rate
        total_fee_aud  = send_aud - (recipient_gets / rate)
        results.append({
            "name": name,
            "recipient_gets": recipient_gets,
            "total_fee_aud": total_fee_aud,
            "markup_pct": markup * 100,
            "flat_fee": flat_fee,
            "colour": colour,
            "cat": cat,
        })

    wise_gets = results[0]["recipient_gets"]

    # ── results ───────────────────────────────────────────────────────────────
    st.markdown("### " + ("What your recipient gets" if lang == "en" else "受取人が受け取る金額"))

    # bar chart
    fig = go.Figure()
    names   = [r["name"] for r in results]
    amounts = [r["recipient_gets"] for r in results]
    colours = [r["colour"] for r in results]

    fig.add_trace(go.Bar(
        x=amounts,
        y=names,
        orientation="h",
        marker_color=colours,
        text=[
            f"{currency_code} {a:,.0f}  (fee: A${r['total_fee_aud']:.0f})"
            for a, r in zip(amounts, results)
        ],
        textposition="outside",
        textfont=dict(color="#e6edf3", size=12),
        hovertemplate="<b>%{y}</b><br>Recipient gets: "
                      + currency_code + " %{x:,.0f}<extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#e6edf3"),
        xaxis=dict(
            showgrid=True, gridcolor="#21262d",
            title=f"Amount received ({currency_code})",
            tickformat=",",
            color="#8b949e",
        ),
        yaxis=dict(autorange="reversed", color="#e6edf3"),
        margin=dict(l=0, r=120, t=20, b=40),
        height=320,
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── highlight card: wise saving ───────────────────────────────────────────
    worst_bank  = max(r["total_fee_aud"] for r in results if r["cat"] == "bank")
    wise_fee    = results[0]["total_fee_aud"]
    saving_aud  = worst_bank - wise_fee
    saving_ccy  = saving_aud * rate

    st.markdown(
        f"<div class='card card-green' style='text-align:center;padding:20px'>"
        f"<div class='label-sm'>{'💡 Wise vs worst bank — you save' if lang == 'en' else '💡 Wise vs 最悪の銀行 — 節約額'}</div>"
        f"<div style='font-size:40px;font-weight:900;color:#3fb950'>"
        f"A${saving_aud:,.0f}"
        f"<span style='font-size:18px;color:#8b949e;font-weight:400;margin-left:12px'>"
        f"= {currency_code} {saving_ccy:,.0f}"
        f"</span></div>"
        f"<div style='color:#8b949e;font-size:13px'>"
        + (f"On a A${send_aud:,} transfer, Wise saves you A${saving_aud:,.0f} compared to the most expensive bank."
           if lang == "en" else
           f"A${send_aud:,}の送金で、最も手数料の高い銀行と比べてWiseはA${saving_aud:,.0f}節約できます。")
        + f"</div></div>",
        unsafe_allow_html=True,
    )

    st.markdown("")

    # ── detailed table ────────────────────────────────────────────────────────
    with st.expander("📊 " + ("Full fee breakdown" if lang == "en" else "詳細手数料内訳")):
        table_rows = []
        for r in results:
            table_rows.append({
                "Provider":              r["name"],
                f"Recipient gets ({currency_code})": f"{r['recipient_gets']:,.0f}",
                "Total cost (AUD)":      f"A${r['total_fee_aud']:.2f}",
                "Rate markup":           f"{r['markup_pct']:.1f}%",
                "Flat fee":              f"A${r['flat_fee']:.2f}",
            })
        st.dataframe(
            pd.DataFrame(table_rows),
            hide_index=True, use_container_width=True,
        )

        if lang == "en":
            st.markdown("""
**How banks hide their fees:**
Banks rarely charge an obvious transfer fee. Instead they give you a
worse exchange rate than the mid-market rate (the "real" rate you see on Google).
That margin — typically 3–5% — is their profit. You only notice if you compare.

**How Wise works:**
Wise uses the mid-market rate and charges a small transparent fee (~0.5%).
They convert your AUD into local currency in their own accounts and pay out locally
in the destination country — so no international wire fees.
""")
        else:
            st.markdown("""
**銀行が手数料を隠す方法：**
銀行は明示的な送金手数料をあまり請求しません。その代わり、
中間市場レート（Googleで見られる「本当の」レート）より悪いレートを提示します。
そのマージン（通常3〜5%）が銀行の利益です。比較しないと気づきません。

**Wiseの仕組み：**
Wiseは中間市場レートを使用し、小さな透明な手数料（約0.5%）を請求します。
自社の口座でAUDを現地通貨に換えて現地で支払うため、
国際電信送金手数料がかかりません。
""")

    st.markdown("---")

    # ── wise CTA ──────────────────────────────────────────────────────────────
    st.markdown("### " + ("Use Wise for your next transfer" if lang == "en" else "次の送金にWiseを使う"))

    wise_url = st.secrets.get("WISE_REFERRAL_URL", "https://wise.com") if hasattr(st, "secrets") else "https://wise.com"

    st.markdown(
        f"<div class='card card-green' style='padding:24px'>"
        f"<div style='font-size:20px;font-weight:700;color:#e6edf3;margin-bottom:8px'>"
        f"{'🌿 Wise — Send money the smart way' if lang == 'en' else '🌿 Wise — かしこく送金する'}"
        f"</div>"
        f"<div style='color:#8b949e;font-size:14px;margin-bottom:16px'>"
        + ("✅ Mid-market exchange rate (same as Google)<br>"
           "✅ Transparent fee shown upfront before you send<br>"
           "✅ Usually 0.4–0.6% for AUD → JPY<br>"
           "✅ Money arrives same day or next day<br>"
           "✅ Send from your Australian bank account"
           if lang == "en" else
           "✅ 中間市場レート（Googleと同じ）を使用<br>"
           "✅ 送金前に手数料を透明に表示<br>"
           "✅ AUD→JPYは通常0.4〜0.6%<br>"
           "✅ 当日または翌日着金<br>"
           "✅ オーストラリアの銀行口座から送金可能")
        + f"</div>"
        f"<a href='{wise_url}' target='_blank' style='"
        f"background:#3fb950;color:#0d1117;padding:12px 28px;border-radius:8px;"
        f"font-weight:700;font-size:15px;text-decoration:none;display:inline-block'>"
        + ("Open a free Wise account →" if lang == "en" else "無料でWiseアカウントを開設 →")
        + f"</a>"
        f"<span style='color:#8b949e;font-size:11px;margin-left:16px'>"
        + ("Referral link — we may earn a small fee if you sign up, at no cost to you."
           if lang == "en" else
           "紹介リンク — ご登録いただいた場合、あなたの負担なしで少額の報酬を受け取る場合があります。")
        + f"</span></div>",
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown(
        "<div class='warn-box'>"
        + ("⚠️ Exchange rates shown are estimates using user-provided mid-market rates. "
           "Actual rates and fees vary by amount, currency, payment method, and date. "
           "Always check the provider's website for the exact rate before sending."
           if lang == "en" else
           "⚠️ 表示されているレートはユーザーが入力した中間市場レートを使用した概算です。"
           "実際のレートと手数料は金額・通貨・支払い方法・日付によって異なります。"
           "送金前に必ずプロバイダーのウェブサイトで正確なレートを確認してください。")
        + "</div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
#  WHM EMPLOYER TRACKER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⏱️ WHM Employer Tracker":

    import calendar as _calendar

    def _add_months(d: date, months: int) -> date:
        month = d.month - 1 + months
        year  = d.year + month // 12
        month = month % 12 + 1
        day   = min(d.day, _calendar.monthrange(year, month)[1])
        return date(year, month, day)

    st.markdown("## ⏱️ " + ("WHM Employer Tracker" if lang == "en" else "WHM雇用主トラッカー"))

    if lang == "en":
        st.markdown("""
**Working Holiday Makers (visa 417 and 462) can only work for the same employer for 6 months.**
After 6 months, you must move to a different employer or risk breaching your visa conditions.

Many people lose track of this — especially when shifts are casual and start dates are vague.
This tracker tells you exactly where you stand.
""")
    else:
        st.markdown("""
**ワーキングホリデービザ（417・462）保持者は同じ雇用主のもとで最大6ヶ月しか働けません。**
6ヶ月を超えると、ビザ条件違反になる可能性があります。

カジュアルシフトが多く開始日が曖昧なため、多くの人がこれを見落とします。
このトラッカーで正確な状況を確認しましょう。
""")

    st.markdown("---")

    # ── visa sub-type ─────────────────────────────────────────────────────────
    st.markdown("### " + ("Your visa" if lang == "en" else "あなたのビザ"))
    whm_visa = st.radio(
        "Visa subclass" if lang == "en" else "ビザサブクラス",
        ["417 — Working Holiday", "462 — Work and Holiday"],
        horizontal=True,
    )

    # ── employer 6-month tracker ──────────────────────────────────────────────
    st.markdown("### " + ("Step 1 — 6-month employer limit" if lang == "en" else "ステップ1 — 6ヶ月雇用主制限"))

    WM = MONTHS_JA if lang == "ja" else MONTHS_EN  # reuse month labels from Tax page scope — define locally
    WM = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    WM_JA = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"]
    WM_LABELS = WM_JA if lang == "ja" else WM
    WY = list(range(2022, 2028))

    ec1, ec2, ec3, ec4 = st.columns(4)
    with ec1:
        emp_start_m = st.selectbox(
            "Started (month)" if lang == "en" else "開始（月）", WM_LABELS, index=0
        )
    with ec2:
        emp_start_y = st.selectbox(
            "Started (year)" if lang == "en" else "開始（年）", WY, index=2
        )
    with ec3:
        still_working = st.checkbox(
            "Still working there" if lang == "en" else "まだ働いている", value=True
        )
    with ec4:
        if not still_working:
            emp_end_m = st.selectbox(
                "Left (month)" if lang == "en" else "退職（月）", WM_LABELS, index=5
            )
            emp_end_y = st.selectbox(
                "Left (year)" if lang == "en" else "退職（年）", WY, index=2
            )

    start_month_idx  = WM_LABELS.index(emp_start_m) + 1
    emp_start_date   = date(emp_start_y, start_month_idx, 1)
    emp_deadline     = _add_months(emp_start_date, 6)

    if still_working:
        as_of = date.today()
    else:
        end_month_idx = WM_LABELS.index(emp_end_m) + 1
        as_of = date(emp_end_y, end_month_idx, 28)

    days_worked    = max(0, (as_of - emp_start_date).days)
    days_limit     = max(1, (emp_deadline - emp_start_date).days)
    days_remaining = (emp_deadline - as_of).days
    pct            = min(100, int(days_worked / days_limit * 100))

    # colour
    if days_remaining < 0:
        bar_colour, card_class, status_icon = "#f85149", "card-red", "🚨"
    elif days_remaining <= 30:
        bar_colour, card_class, status_icon = "#d29922", "card-yellow", "⚠️"
    else:
        bar_colour, card_class, status_icon = "#3fb950", "card-green", "✅"

    # progress bar HTML
    st.markdown(
        f"<div style='background:#21262d;border-radius:6px;height:18px;margin:12px 0'>"
        f"<div style='background:{bar_colour};width:{pct}%;height:100%;border-radius:6px;"
        f"transition:width 0.4s'></div></div>",
        unsafe_allow_html=True,
    )

    if days_remaining >= 0:
        st.markdown(
            f"<div class='card {card_class}' style='padding:16px 20px'>"
            f"<b style='font-size:18px'>{status_icon} "
            + (f"{days_worked} days worked · {days_remaining} days remaining"
               if lang == "en" else
               f"{days_worked}日就労済み · 残り{days_remaining}日")
            + f"</b><br><span style='color:#8b949e;font-size:13px'>"
            + (f"6-month limit reached: {emp_deadline.strftime('%d %B %Y')} — "
               f"{'move on before this date' if days_remaining > 0 else 'you must already have left'}"
               if lang == "en" else
               f"6ヶ月期限：{emp_deadline.strftime('%Y年%m月%d日')} — "
               f"{'この日までに退職してください' if days_remaining > 0 else 'すでに退職が必要な日を過ぎています'}")
            + f"</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='card card-red' style='padding:16px 20px'>"
            f"<b style='font-size:18px'>🚨 "
            + (f"Over the 6-month limit by {abs(days_remaining)} days"
               if lang == "en" else
               f"6ヶ月制限を{abs(days_remaining)}日超過しています")
            + f"</b><br><span style='color:#8b949e;font-size:13px'>"
            + ("Your 6-month limit was "
               f"{emp_deadline.strftime('%d %B %Y')}. "
               "If you are still with this employer, you may be in breach of your visa conditions. "
               "Contact a migration agent for advice."
               if lang == "en" else
               f"6ヶ月の期限は{emp_deadline.strftime('%Y年%m月%d日')}でした。"
               "まだ同じ雇用主のもとで働いている場合、ビザ条件違反の可能性があります。"
               "移民エージェントにご相談ください。")
            + f"</span></div>",
            unsafe_allow_html=True,
        )

    with st.expander("ℹ️ " + ("About the 6-month rule" if lang == "en" else "6ヶ月ルールについて")):
        if lang == "en":
            st.markdown("""
The 6-month limit applies per employer, not per job. If you work at two different McDonald's
franchises owned by different companies, that resets the clock. If they're the same owner, it doesn't.

**Exceptions:** Some industries and employers are approved for longer stays. Regional agricultural
employers and some healthcare/tourism employers may be on the approved list — check your visa
grant notice or immi.homeaffairs.gov.au for details.

**The clock starts** from the first day you work for that employer — not from when you signed a contract.
""")
        else:
            st.markdown("""
6ヶ月制限は雇用主単位で適用されます。異なる会社が経営する2つのマクドナルドなら時計はリセットされます。
同じオーナーなら引き継ぎとみなされます。

**例外：** 一部の業種・雇用主は長期就労が認められています。地方の農業雇用主や
医療・観光業の一部が対象になることがあります — ビザ許可通知またはimmi.homeaffairs.gov.auで確認してください。

**カウント開始日**は契約日ではなく、実際に初日に働いた日からです。
""")

    st.markdown("---")

    # ── second year visa tracker ───────────────────────────────────────────────
    st.markdown("### " + ("Step 2 — Second year visa (88 days regional work)" if lang == "en" else "ステップ2 — 2年目ビザ（地方就労88日）"))

    if lang == "en":
        st.markdown("""
To qualify for a **second-year Working Holiday visa**, you need to complete **88 days**
of specified work in a regional area of Australia during your first visa.

Qualifying work includes: farm work, fruit picking, fishing, mining, construction in regional areas.
""")
    else:
        st.markdown("""
**2年目のワーキングホリデービザ**を取得するには、最初のビザ期間中に
オーストラリアの地方エリアで**88日間**の指定就労を完了する必要があります。

対象となる就労：農業・果物収穫・漁業・鉱業・地方エリアでの建設業など。
""")

    num_periods = st.number_input(
        "How many regional work periods do you want to add?" if lang == "en" else "地方就労期間をいくつ追加しますか？",
        min_value=1, max_value=5, value=1, step=1,
    )

    total_regional_days = 0
    for i in range(int(num_periods)):
        st.markdown(f"**{'Period' if lang == 'en' else '期間'} {i+1}**")
        rp1, rp2, rp3, rp4 = st.columns(4)
        with rp1:
            rs_m = st.selectbox(f"{'Start month' if lang == 'en' else '開始月'} {i+1}", WM_LABELS, index=0, key=f"rs_m_{i}")
        with rp2:
            rs_y = st.selectbox(f"{'Start year' if lang == 'en' else '開始年'} {i+1}", WY, index=2, key=f"rs_y_{i}")
        with rp3:
            re_m = st.selectbox(f"{'End month' if lang == 'en' else '終了月'} {i+1}", WM_LABELS, index=2, key=f"re_m_{i}")
        with rp4:
            re_y = st.selectbox(f"{'End year' if lang == 'en' else '終了年'} {i+1}", WY, index=2, key=f"re_y_{i}")

        rs_idx   = WM_LABELS.index(rs_m) + 1
        re_idx   = WM_LABELS.index(re_m) + 1
        rs_date  = date(rs_y, rs_idx, 1)
        re_month = re_idx + 1 if re_idx < 12 else 1
        re_year  = re_y if re_idx < 12 else re_y + 1
        re_date  = date(re_year, re_month, 1) - __import__("datetime").timedelta(days=1)
        period_days = max(0, (re_date - rs_date).days)
        total_regional_days += period_days
        st.caption(f"{'~' if lang == 'en' else '約'}{period_days} {'days' if lang == 'en' else '日'}")

    reg_pct = min(100, int(total_regional_days / 88 * 100))
    reg_colour = "#3fb950" if total_regional_days >= 88 else "#d29922" if total_regional_days >= 60 else "#58a6ff"

    st.markdown(
        f"<div style='background:#21262d;border-radius:6px;height:18px;margin:12px 0'>"
        f"<div style='background:{reg_colour};width:{reg_pct}%;height:100%;border-radius:6px'></div></div>",
        unsafe_allow_html=True,
    )

    if total_regional_days >= 88:
        st.markdown(
            f"<div class='card card-green' style='padding:14px 18px'>"
            f"<b style='color:#3fb950'>✅ "
            + (f"{total_regional_days} days — you qualify for the second-year visa!"
               if lang == "en" else
               f"{total_regional_days}日 — 2年目ビザの条件を満たしています！")
            + f"</b></div>",
            unsafe_allow_html=True,
        )
    else:
        needed = 88 - total_regional_days
        st.markdown(
            f"<div class='card card-blue' style='padding:14px 18px'>"
            f"<b>"
            + (f"{total_regional_days} / 88 days — {needed} more days needed"
               if lang == "en" else
               f"{total_regional_days} / 88日 — あと{needed}日必要")
            + f"</b></div>",
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown(
        "<div class='card card-blue'>"
        + ("🔗 <b>Official WHM visa info:</b> "
           "<a href='https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/work-holiday-417' target='_blank'>"
           "immi.homeaffairs.gov.au — Working Holiday visa (417)</a>"
           if lang == "en" else
           "🔗 <b>ワーキングホリデービザ公式情報：</b> "
           "<a href='https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/work-holiday-417' target='_blank'>"
           "immi.homeaffairs.gov.au — ワーキングホリデービザ（417）</a>")
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown(
        "<div class='warn-box'>"
        + ("⚠️ This tracker is an estimate based on the dates you enter. "
           "Day counts are approximate (month-level precision). "
           "For visa compliance decisions, always verify with the Department of Home Affairs or a registered migration agent."
           if lang == "en" else
           "⚠️ このトラッカーは入力された日付に基づく概算です。"
           "日数計算は月単位の精度です。"
           "ビザコンプライアンスの判断には、必ず内務省または登録移民エージェントに確認してください。")
        + "</div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
#  COMING SOON PAGES
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown(f"## {page}")
    st.info(
        "This page is coming soon. The Super Claim Calculator is live now — start there."
        if lang == "en" else
        "このページは近日公開予定です。スーパー請求計算機は今すぐ使えます。"
    )
    if st.button("← " + ("Go to Super Calculator" if lang == "en" else "スーパー計算機へ")):
        st.rerun()
