"""
International Student Finance — Australia
Built for international students (Japanese-first) navigating Australian money.

Pages:
  🏠 Home
  💰 Super Claim Calculator
  🧾 Tax Estimator        (coming soon)
  💸 Money Transfer        (coming soon)
  🏦 Bank Account Guide   (coming soon)
  📋 Work Rights          (coming soon)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AusStudent Finance",
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

# ── language ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🦘 AusStudent Finance")
    st.caption("For international students in Australia\nオーストラリアの留学生のために")
    st.markdown("---")

    lang_choice = st.radio(
        "Language / 言語",
        ["🇬🇧 English", "🇯🇵 日本語"],
        horizontal=True,
    )
    lang = "ja" if "日本語" in lang_choice else "en"
    st.markdown("---")

    pages_en = [
        "🏠 Home",
        "💰 Super Claim Calculator",
        "🧾 Tax Estimator",
        "💸 Money Transfer",
        "🏦 Bank Account Guide",
        "📋 Work Rights",
    ]
    pages_ja = [
        "🏠 ホーム",
        "💰 スーパー請求計算機",
        "🧾 税金計算機",
        "💸 海外送金",
        "🏦 銀行口座ガイド",
        "📋 就労権利",
    ]
    nav_opts  = pages_ja if lang == "ja" else pages_en
    nav_sel   = st.radio("nav", nav_opts, label_visibility="collapsed")
    page      = pages_en[nav_opts.index(nav_sel)]

    st.markdown("---")
    st.caption(
        "Made by a Japanese finance student at UQ.\nData is for guidance only — not financial or legal advice."
        if lang == "en" else
        "UQの日本人留学生が制作。情報提供のみを目的としています。"
    )

# ══════════════════════════════════════════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown(
        "<div class='hero-title'>🦘 AusStudent Finance</div>"
        "<div class='hero-sub'>"
        + ("The money guide built for international students in Australia — by one of us."
           if lang == "en" else
           "オーストラリアの留学生のためのお金ガイド — 同じ留学生が作りました。")
        + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("")

    # ── the problem ───────────────────────────────────────────────────────────
    if lang == "en":
        st.markdown("""
Most international students leave Australia without knowing:

- 💰 They're owed **superannuation** from every Australian employer — often $2,000–$8,000
- 🧾 They're probably owed a **tax refund** and don't know how to claim it
- 💸 They're paying **3–5% in bank fees** to send money home when Wise charges 0.5%
- 📋 They have **full workplace rights** — many employers underpay international students who don't know this

This site exists to fix that. Free, bilingual, built specifically for you.
""")
    else:
        st.markdown("""
多くの留学生はオーストラリアを離れる際に以下を知らないことが多いです：

- 💰 すべてのオーストラリア雇用主から**スーパーアニュエーション（退職金）**が支払われており、多くの場合2,000〜8,000ドル相当
- 🧾 おそらく**税金の還付**を受ける権利があるが、請求方法を知らない
- 💸 Wiseを使えば0.5%の手数料で送金できるのに、銀行で**3〜5%の手数料**を払っている
- 📋 **完全な労働権**があるにもかかわらず、知らないために多くの留学生が低賃金で働かされている

このサイトはその問題を解決するために作られました。無料・バイリンガル・あなたのために。
""")

    st.markdown("---")

    # ── tools grid ────────────────────────────────────────────────────────────
    st.markdown(
        "### " + ("Tools" if lang == "en" else "ツール"),
    )
    c1, c2 = st.columns(2)
    tools = [
        ("💰", "Super Claim Calculator",
         "スーパー請求計算機",
         "Find out how much super you're owed and how to claim it before you leave.",
         "退職金がいくら受け取れるか計算し、帰国前に請求する方法を確認。",
         True, c1),
        ("🧾", "Tax Estimator",
         "税金計算機",
         "Estimate your tax refund from Australian casual work.",
         "アルバイト収入からの税金還付額を計算。",
         False, c2),
        ("💸", "Money Transfer Comparison",
         "海外送金比較",
         "Compare Wise vs banks to stop overpaying on transfers to Japan.",
         "WiseとBank手数料を比較して送金コストを節約。",
         False, c1),
        ("🏦", "Bank Account Guide",
         "銀行口座ガイド",
         "Which Australian bank account is best for a new international student?",
         "新着留学生に最適なオーストラリアの銀行口座は？",
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

    col_a, col_b = st.columns(2)
    with col_a:
        fy = st.selectbox(
            "Financial year" if lang == "en" else "会計年度",
            ["FY2025-26", "FY2024-25", "FY2023-24", "FY2022-23"],
            index=0,
            help="Australian tax year runs 1 Jul to 30 Jun."
                 if lang == "en" else
                 "オーストラリアの税年度は7月1日〜翌年6月30日。",
        )
    with col_b:
        status_opts_en = [
            "🇦🇺 Australian tax resident (183+ days)",
            "🌏 Foreign resident for tax (<183 days)",
            "🎒 Working Holiday Maker (417/462 visa)",
        ]
        status_opts_ja = [
            "🇦🇺 オーストラリア税務居住者（183日以上）",
            "🌏 外国居住者（183日未満）",
            "🎒 ワーキングホリデー（417/462ビザ）",
        ]
        status_opts = status_opts_ja if lang == "ja" else status_opts_en
        status_sel = st.selectbox(
            "Your tax residency status" if lang == "en" else "税務上の居住者ステータス",
            status_opts,
        )
        if "resident" in status_sel or "居住者" in status_sel and "外国" not in status_sel:
            tax_status = "resident"
        elif "Foreign" in status_sel or "外国" in status_sel:
            tax_status = "foreign"
        else:
            tax_status = "whm"

    income = st.number_input(
        "Total Australian income this financial year (AUD)"
        if lang == "en" else "この会計年度のオーストラリアでの総収入（AUD）",
        min_value=0, max_value=300000, value=28000, step=500,
        help="Include wages, tips, cash jobs — everything you earned in Australia."
             if lang == "en" else
             "賃金、チップ、現金バイトなど、オーストラリアで得たすべての収入を含めてください。",
    )

    tax_withheld = st.number_input(
        "Tax already withheld by your employer (AUD) — check your payslips or myGov income statement"
        if lang == "en" else
        "雇用主がすでに源泉徴収した税額（AUD）— 給与明細またはmyGovの所得明細を確認",
        min_value=0, max_value=150000, value=6000, step=100,
        help="This is the PAYG tax deducted from your wages each pay period."
             if lang == "en" else
             "これは毎回の給与から差し引かれたPAYG税です。",
    )

    col_c, col_d = st.columns(2)
    with col_c:
        medicare_exempt = st.checkbox(
            "Medicare Levy exempt (most international students qualify)"
            if lang == "en" else
            "メディケアレビー免除（ほとんどの留学生が対象）",
            value=(tax_status != "whm"),
            help="International students on student visas can apply for a Medicare Levy Exemption "
                 "Certificate from Medicare Australia. Working Holiday Makers are NOT exempt."
                 if lang == "en" else
                 "学生ビザの留学生はメディケアオーストラリアから免除証明書を取得できます。"
                 "ワーキングホリデーは対象外です。",
        )
    with col_d:
        has_tfn = st.checkbox(
            "You gave your employer your Tax File Number (TFN)"
            if lang == "en" else "雇用主にTFN（税務番号）を提供した",
            value=True,
            help="Without a TFN, employers must withhold tax at the top rate (47%). "
                 "If you didn't provide it, your withholding may be very high."
                 if lang == "en" else
                 "TFNがない場合、雇用主は最高税率（47%）で源泉徴収しなければなりません。",
        )

    st.markdown("---")

    # ── calculations ──────────────────────────────────────────────────────────
    if tax_status == "resident":
        gross_tax = calc_resident_tax(income)
        lito      = calc_lito(income)
    elif tax_status == "foreign":
        gross_tax = calc_foreign_tax(income)
        lito      = 0.0
    else:
        gross_tax = calc_whm_tax(income)
        lito      = 0.0

    medicare  = 0.0 if medicare_exempt else income * 0.02
    tax_owed  = max(0.0, gross_tax - lito + medicare)
    balance   = tax_withheld - tax_owed   # positive = refund, negative = bill

    st.markdown("### " + ("Your Result" if lang == "en" else "計算結果"))

    r1, r2, r3 = st.columns(3)
    r1.markdown(
        f"<div class='card card-blue'>"
        f"<div class='label-sm'>{'Gross tax on income' if lang == 'en' else '収入への総税額'}</div>"
        f"<div class='big-number' style='color:#58a6ff'>${gross_tax:,.0f}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    r2.markdown(
        f"<div class='card card-yellow'>"
        f"<div class='label-sm'>{'LITO offset applied' if lang == 'en' else '低所得税オフセット'}</div>"
        f"<div class='big-number' style='color:#d29922'>−${lito:,.0f}</div>"
        f"<div style='color:#8b949e;font-size:11px'>{'residents only' if lang == 'en' else '居住者のみ'}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    r3.markdown(
        f"<div class='card {'card-green' if balance >= 0 else 'card-red'}'>"
        f"<div class='label-sm'>{'Tax owed this year' if lang == 'en' else '今年の税額'}</div>"
        f"<div class='big-number' style='color:{'#3fb950' if balance >= 0 else '#f85149'}'>${tax_owed:,.0f}</div>"
        f"<div style='color:#8b949e;font-size:11px'>{'after offsets' if lang == 'en' else 'オフセット後'}</div>"
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
            + ("You paid ${:,.0f} but only owed ${:,.0f}. The ATO owes you the difference."
               .format(tax_withheld, tax_owed)
               if lang == "en" else
               "源泉徴収額${:,.0f} − 税額${:,.0f} = 還付額".format(tax_withheld, tax_owed))
            + f"</div></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='card card-red' style='text-align:center;padding:24px'>"
            f"<div class='label-sm'>{'⚠️ Estimated amount owing' if lang == 'en' else '⚠️ 追加納税額'}</div>"
            f"<div style='font-size:52px;font-weight:900;color:#f85149'>${abs(balance):,.0f}</div>"
            f"<div style='color:#8b949e;font-size:13px'>"
            + ("You owed ${:,.0f} but only had ${:,.0f} withheld. You'll need to pay the difference."
               .format(tax_owed, tax_withheld)
               if lang == "en" else
               "税額${:,.0f} − 源泉徴収額${:,.0f} = 追加納税額".format(tax_owed, tax_withheld))
            + f"</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("")

    # ── full breakdown table ──────────────────────────────────────────────────
    with st.expander("📊 " + ("Full breakdown" if lang == "en" else "詳細内訳")):
        rows_en = [
            ("Gross income", f"${income:,.0f}"),
            ("Tax status", {"resident": "Australian resident", "foreign": "Foreign resident", "whm": "Working Holiday Maker"}[tax_status]),
            ("Gross income tax", f"${gross_tax:,.0f}"),
            ("Low Income Tax Offset (LITO)", f"−${lito:,.0f}"),
            ("Medicare Levy (2%)", "Exempt" if medicare_exempt else f"${medicare:,.0f}"),
            ("Total tax owed", f"${tax_owed:,.0f}"),
            ("Tax already withheld", f"${tax_withheld:,.0f}"),
            ("Result", f"{'REFUND' if balance >= 0 else 'OWING'}: ${abs(balance):,.0f}"),
        ]
        rows_ja = [
            ("総収入", f"${income:,.0f}"),
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
