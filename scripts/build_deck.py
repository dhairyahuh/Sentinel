import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_pitch_deck():
    prs = Presentation()
    # 16:9 Widescreen standard dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Color Palette - Modern Fintech / Executive Dark Theme
    COLOR_BG = RGBColor(11, 16, 21)          # #0B1015 Deep slate dark
    COLOR_CARD = RGBColor(19, 26, 36)        # #131A24 Card background
    COLOR_CARD_BORDER = RGBColor(30, 41, 59) # #1E293B Card border
    COLOR_ACCENT = RGBColor(14, 165, 233)     # #0EA5E9 Cyber Cyan
    COLOR_ACCENT_ALT = RGBColor(99, 102, 241)# #6366F1 Indigo / Purple
    COLOR_WHITE = RGBColor(248, 250, 252)    # #F8FAFC Heading White
    COLOR_TEXT = RGBColor(226, 232, 240)     # #E2E8F0 Body Text
    COLOR_MUTED = RGBColor(148, 163, 184)    # #94A3B8 Secondary Text
    COLOR_BADGE_BG = RGBColor(15, 23, 42)    # #0F172A Badge BG
    COLOR_ALERT = RGBColor(239, 68, 68)      # #EF4444 Danger Red
    COLOR_SUCCESS = RGBColor(16, 185, 129)   # #10B981 Emerald Green

    def set_slide_background(slide):
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = COLOR_BG
        bg_shape.line.fill.background() # No line
        return bg_shape

    def add_header(slide, tag_text, title_text, subtitle_text=None):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_ACCENT
        p_tag.font.name = "Arial"

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.55))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE
        p_title.font.name = "Arial"

        if subtitle_text:
            p_title.space_after = Pt(2)
            p_sub = tf_title.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = COLOR_MUTED
            p_sub.font.name = "Arial"

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # ==========================================
    # SLIDE 0: TITLE SLIDE
    # ==========================================
    s0 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s0)

    # Accent decorative glow bar
    glow = s0.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.12), Inches(3.8))
    glow.fill.solid()
    glow.fill.fore_color.rgb = COLOR_ACCENT
    glow.line.fill.background()

    # Track / Competition Badge
    badge_bg = add_card(s0, Inches(1.2), Inches(1.8), Inches(5.8), Inches(0.42), bg_color=COLOR_BADGE_BG, border_color=COLOR_ACCENT)
    tb_badge = s0.shapes.add_textbox(Inches(1.35), Inches(1.88), Inches(5.5), Inches(0.3))
    tf_b = tb_badge.text_frame
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = "YEL BUILD $ BANK 2026  •  TRACK 2  •  PROBLEM 5"
    p_b.font.size = Pt(10)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_ACCENT
    p_b.font.name = "Arial"

    # Main Product Name
    tb_name = s0.shapes.add_textbox(Inches(1.2), Inches(2.4), Inches(10.5), Inches(1.1))
    tf_name = tb_name.text_frame
    tf_name.margin_left = tf_name.margin_top = tf_name.margin_right = tf_name.margin_bottom = 0
    p_name = tf_name.paragraphs[0]
    p_name.text = "SENTINEL"
    p_name.font.size = Pt(48)
    p_name.font.bold = True
    p_name.font.color.rgb = COLOR_WHITE
    p_name.font.name = "Arial"

    # Tagline
    tb_tag = s0.shapes.add_textbox(Inches(1.2), Inches(3.55), Inches(10.5), Inches(0.6))
    tf_tag = tb_tag.text_frame
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "Financial crime doesn't hide in transactions. It hides in patterns."
    p_tag.font.size = Pt(18)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_ACCENT
    p_tag.font.name = "Arial"

    # One-liner description
    tb_desc = s0.shapes.add_textbox(Inches(1.2), Inches(4.25), Inches(10.5), Inches(0.8))
    tf_desc = tb_desc.text_frame
    tf_desc.word_wrap = True
    tf_desc.margin_left = tf_desc.margin_top = tf_desc.margin_right = tf_desc.margin_bottom = 0
    p_desc = tf_desc.paragraphs[0]
    p_desc.text = "Sentinel connects transactions, accounts, beneficiaries, and time-based behaviour to expose coordinated financial crime that isolated transaction-level detection misses."
    p_desc.font.size = Pt(13)
    p_desc.font.color.rgb = COLOR_TEXT
    p_desc.font.name = "Arial"

    # Bottom Metadata Card
    add_card(s0, Inches(1.2), Inches(5.35), Inches(10.9), Inches(1.2))
    tb_meta = s0.shapes.add_textbox(Inches(1.45), Inches(5.5), Inches(10.4), Inches(0.9))
    tf_meta = tb_meta.text_frame
    tf_meta.word_wrap = True
    tf_meta.margin_left = tf_meta.margin_top = tf_meta.margin_right = tf_meta.margin_bottom = 0
    
    p_m1 = tf_meta.paragraphs[0]
    p_m1.text = "PROBLEM STATEMENT:"
    p_m1.font.size = Pt(10)
    p_m1.font.bold = True
    p_m1.font.color.rgb = COLOR_MUTED
    p_m1.font.name = "Arial"
    
    p_m2 = tf_meta.add_paragraph()
    p_m2.text = "“Find a way to catch financial crime that only becomes visible across many transactions or accounts over time.”"
    p_m2.font.size = Pt(12)
    p_m2.font.color.rgb = COLOR_WHITE
    p_m2.font.name = "Arial"
    p_m2.space_before = Pt(3)

    # ==========================================
    # SLIDE 1: PROBLEM STATEMENT
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s1)
    add_header(s1, "01 / The Core Challenge", "Financial crime is bigger than a single transaction.", 
               "Why isolated, point-in-time fraud detection fails against modern distributed financial crime networks.")

    # Left Column: The Flaw of Isolated Inspection
    add_card(s1, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tb_p1 = s1.shapes.add_textbox(Inches(1.1), Inches(1.75), Inches(5.0), Inches(4.9))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True
    tf_p1.margin_left = tf_p1.margin_top = tf_p1.margin_right = tf_p1.margin_bottom = 0

    p = tf_p1.paragraphs[0]
    p.text = "TRADITIONAL TRANSACTION INSPECTION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ALERT
    p.font.name = "Arial"

    points_p1 = [
        ("Evaluates in isolation", "Analyses individual payments at time of authorization. Looks only at immediate amount, velocity, and device footprint."),
        ("Blind to coordinated distribution", "Criminal operations deliberately break illicit activity across multiple disparate accounts, micro-amounts, and staggered time intervals."),
        ("High False Positive tax", "Tightening single-transaction rules flags legitimate customers while letting structured, slow-moving coordinated rings slip past undetected."),
        ("Misses network evolution", "Attackers iteratively mutate account hops and timing patterns faster than static rule engines can be updated.")
    ]

    for title, desc in points_p1:
        p_t = tf_p1.add_paragraph()
        p_t.text = f"•  {title}"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_WHITE
        p_t.font.name = "Arial"
        p_t.space_before = Pt(8)

        p_d = tf_p1.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = COLOR_MUTED
        p_d.font.name = "Arial"
        p_d.space_before = Pt(2)

    # Right Column: Visual Diagram - The Pattern Network
    add_card(s1, Inches(6.7), Inches(1.5), Inches(5.8), Inches(5.4))
    tb_p2 = s1.shapes.add_textbox(Inches(7.0), Inches(1.75), Inches(5.2), Inches(4.9))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True
    tf_p2.margin_left = tf_p2.margin_top = tf_p2.margin_right = tf_p2.margin_bottom = 0

    p = tf_p2.paragraphs[0]
    p.text = "THE PATTERN REALITY: HOW CRIME ACTUALLY MOVES"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.font.name = "Arial"

    # Add 4 transaction mini-cards inside the right box
    txns = [
        ("Txn A", "Account #1042 → Beneficiary X", "₹4,950", "Looks normal (Below KYC check)"),
        ("Txn B", "Account #2891 → Beneficiary X", "₹4,800", "Looks normal (New device)"),
        ("Txn C", "Account #8410 → Beneficiary Y", "₹4,900", "Looks normal (Regular UPI flow)"),
        ("Txn D", "Account #9123 → Beneficiary X", "₹4,990", "Looks normal (Low velocity)")
    ]

    for i, (name, path, amt, status) in enumerate(txns):
        card_top = Inches(2.25 + i * 0.72)
        add_card(s1, Inches(7.0), card_top, Inches(5.2), Inches(0.62), bg_color=COLOR_BADGE_BG, border_color=COLOR_CARD_BORDER)
        tb_tx = s1.shapes.add_textbox(Inches(7.15), card_top + Inches(0.08), Inches(4.9), Inches(0.45))
        tf_tx = tb_tx.text_frame
        tf_tx.word_wrap = True
        tf_tx.margin_left = tf_tx.margin_top = tf_tx.margin_right = tf_tx.margin_bottom = 0
        
        p_tx = tf_tx.paragraphs[0]
        p_tx.text = f"{name}  |  {path}  •  {amt}"
        p_tx.font.size = Pt(10)
        p_tx.font.bold = True
        p_tx.font.color.rgb = COLOR_WHITE
        p_tx.font.name = "Arial"

        p_st = tf_tx.add_paragraph()
        p_st.text = f"Status: {status}"
        p_st.font.size = Pt(8.5)
        p_st.font.color.rgb = COLOR_MUTED
        p_st.font.name = "Arial"

    # Outcome banner at bottom of card
    add_card(s1, Inches(7.0), Inches(5.25), Inches(5.2), Inches(1.35), bg_color=RGBColor(24, 15, 20), border_color=COLOR_ALERT)
    tb_out = s1.shapes.add_textbox(Inches(7.2), Inches(5.35), Inches(4.8), Inches(1.15))
    tf_out = tb_out.text_frame
    tf_out.word_wrap = True
    tf_out.margin_left = tf_out.margin_top = tf_out.margin_right = tf_out.margin_bottom = 0

    p_o1 = tf_out.paragraphs[0]
    p_o1.text = "⚡ CONNECTED THROUGH COMMON DESTINATION & TIMING:"
    p_o1.font.size = Pt(9.5)
    p_o1.font.bold = True
    p_o1.font.color.rgb = COLOR_ALERT
    p_o1.font.name = "Arial"

    p_o2 = tf_out.add_paragraph()
    p_o2.text = "Coordinated Mule Smurfing Ring Funneling ₹19,640 into shared off-ramp entity within a 45-minute window. Single-txn engines approve all 4."
    p_o2.font.size = Pt(9.5)
    p_o2.font.color.rgb = COLOR_TEXT
    p_o2.font.name = "Arial"
    p_o2.space_before = Pt(3)

    # ==========================================
    # SLIDE 2: PROPOSED SOLUTION & ARCHITECTURE
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s2)
    add_header(s2, "02 / Proposed Solution", "Sentinel: Pattern Intelligence for Financial Crime",
               "A multi-scale intelligence engine that connects entities, tracks temporal behaviour, and explains coordinated risks.")

    # Left Column: Solution Capabilities & Architecture Flow
    add_card(s2, Inches(0.8), Inches(1.5), Inches(5.4), Inches(5.4))
    tb_s2 = s2.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(4.9), Inches(5.0))
    tf_s2 = tb_s2.text_frame
    tf_s2.word_wrap = True
    tf_s2.margin_left = tf_s2.margin_top = tf_s2.margin_right = tf_s2.margin_bottom = 0

    p = tf_s2.paragraphs[0]
    p.text = "END-TO-END PATTERN INTELLIGENCE PIPELINE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.font.name = "Arial"

    arch_steps = [
        ("1. Streaming Transaction Ingestion", "Captures raw payments with strict temporal causality."),
        ("2. Multi-Window Spatio-Temporal Extraction", "Calculates 67 rolling features across 1h, 24h, 7d intervals."),
        ("3. Entity & Relationship Graph Linking", "Connects accounts, beneficiaries, devices, and shared IP hops."),
        ("4. ML Ensemble & Threat Pattern Classification", "Scores risk probability & assigns specific crime taxonomy."),
        ("5. Explainable Inspector & Reason Codes", "Provides SHAP-style local feature contributions & counterfactuals."),
        ("6. Adaptive Mutation & Feedback Loop", "Stress-tests defense against synthetic pattern evasions.")
    ]

    for title, desc in arch_steps:
        p_t = tf_s2.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_WHITE
        p_t.font.name = "Arial"
        p_t.space_before = Pt(6)

        p_d = tf_s2.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = COLOR_MUTED
        p_d.font.name = "Arial"
        p_d.space_before = Pt(1)

    # Right Column: Actual Live UI Screenshot (Console View)
    add_card(s2, Inches(6.5), Inches(1.5), Inches(6.0), Inches(5.4))
    
    screenshot_console = "/Users/dhairyajain/Desktop/razorpay_win copy/razor/docs/media/screen_console.png"
    if os.path.exists(screenshot_console):
        s2.shapes.add_picture(screenshot_console, Inches(6.65), Inches(1.65), Inches(5.7), Inches(4.3))
    
    tb_cap = s2.shapes.add_textbox(Inches(6.65), Inches(6.05), Inches(5.7), Inches(0.7))
    tf_cap = tb_cap.text_frame
    tf_cap.word_wrap = True
    tf_cap.margin_left = tf_cap.margin_top = tf_cap.margin_right = tf_cap.margin_bottom = 0
    p_cap = tf_cap.paragraphs[0]
    p_cap.text = "REAL APPLICATION INTERFACE: Live streaming transaction monitor with instant risk stratification (Actionable Flag vs Low Risk), real-time pattern taxonomy tagging, and batch inspector routing."
    p_cap.font.size = Pt(8.5)
    p_cap.font.color.rgb = COLOR_MUTED
    p_cap.font.name = "Arial"

    # ==========================================
    # SLIDE 3: HOW IT WORKS (MAP -> SIMULATE -> DETECT -> EVOLVE)
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s3)
    add_header(s3, "03 / Technical Workflow", "From isolated payments to connected patterns",
               "The four-stage operational framework powering Sentinel's pattern intelligence engine.")

    # 4 Horizontal Workflow Cards
    stages = [
        ("01 / MAP", "Pattern Taxonomy", COLOR_ACCENT, [
            "Formalizes 9 distinct financial crime families across 67 mathematical features.",
            "Captures temporal bursts, structuring, mule fan-ins, and cycling.",
            "Eliminates reliance on arbitrary single-rule heuristics."
        ]),
        ("02 / SIMULATE", "Scenario Stress-Testing", COLOR_ACCENT_ALT, [
            "Generates realistic multi-account attack vectors at varying scales.",
            "Tests detector boundaries against coordinated smurfing & velocity jumps.",
            "Evaluates detector without risking live payment operations."
        ]),
        ("03 / DETECT", "Stacked ML Ensemble", COLOR_SUCCESS, [
            "Combines gradient boosted trees & temporal network feature aggregations.",
            "Calculates Wilson 95% confidence intervals on pattern recalls.",
            "Delivers calibrated risk probabilities and immediate reason codes."
        ]),
        ("04 / EVOLVE", "Adaptive Arms Race", RGBColor(245, 158, 11), [
            "Applies programmatic mutations (staggered timing, amount jitter).",
            "Monitors detection degradation under adversary evasion tactics.",
            "Quantifies defensive robustness across mutation iterations."
        ])
    ]

    card_w = Inches(2.78)
    card_gap = Inches(0.2)
    start_x = Inches(0.8)
    card_y = Inches(1.5)
    card_h = Inches(5.4)

    for i, (stage_num, stage_name, color, bullets) in enumerate(stages):
        pos_x = start_x + i * (card_w + card_gap)
        add_card(s3, pos_x, card_y, card_w, card_h)

        tb = s3.shapes.add_textbox(pos_x + Inches(0.18), card_y + Inches(0.2), card_w - Inches(0.36), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = stage_num
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = color
        p1.font.name = "Arial"

        p2 = tf.add_paragraph()
        p2.text = stage_name
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_WHITE
        p2.font.name = "Arial"
        p2.space_before = Pt(3)

        # Divider line representation
        p_div = tf.add_paragraph()
        p_div.text = "—" * 16
        p_div.font.size = Pt(8)
        p_div.font.color.rgb = COLOR_CARD_BORDER
        p_div.space_before = Pt(4)

        for bullet in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"• {bullet}"
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = COLOR_TEXT
            p_b.font.name = "Arial"
            p_b.space_before = Pt(8)

    # ==========================================
    # SLIDE 4: KEY FEATURES & TECHNOLOGY STACK
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s4)
    add_header(s4, "04 / Product & Engineering", "Built for investigation, not just scoring",
               "Deep operational toolset paired with a production-ready, strictly verifiable technology stack.")

    # Left: 6 Core Features (2 columns of 3)
    add_card(s4, Inches(0.8), Inches(1.5), Inches(7.5), Inches(5.4))
    tb_feat = s4.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(7.0), Inches(5.0))
    tf_feat = tb_feat.text_frame
    tf_feat.word_wrap = True
    tf_feat.margin_left = tf_feat.margin_top = tf_feat.margin_right = tf_feat.margin_bottom = 0

    p = tf_feat.paragraphs[0]
    p.text = "OPERATIONAL INVESTIGATION CAPABILITIES"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.font.name = "Arial"

    features = [
        ("1. Transaction Inspector", "Deep forensic view explaining exactly why an event was flagged with risk factor attribution."),
        ("2. Related Transaction Analysis", "Instant discovery of connected transfers across shared origin accounts and common targets."),
        ("3. Mule-Ring Detection", "Identifies fan-in convergence patterns where multiple feeder accounts channel funds to common off-ramps."),
        ("4. Campaign Clustering", "Detects coordinated multi-account bursts operating synchronously across narrow time windows."),
        ("5. Threat Pattern Catalog", "Comprehensive taxonomy indexing 9 verified financial crime patterns with baseline metrics."),
        ("6. Adaptive Mutation Lab", "Stress-tests detection models against iterative attack permutations and evasive timing shifts.")
    ]

    for title, desc in features:
        p_t = tf_feat.add_paragraph()
        p_t.text = f"•  {title}"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_WHITE
        p_t.font.name = "Arial"
        p_t.space_before = Pt(6)

        p_d = tf_feat.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = COLOR_MUTED
        p_d.font.name = "Arial"
        p_d.space_before = Pt(1)

    # Right: Verified Technology Stack
    add_card(s4, Inches(8.6), Inches(1.5), Inches(3.9), Inches(5.4))
    tb_stk = s4.shapes.add_textbox(Inches(8.85), Inches(1.7), Inches(3.4), Inches(5.0))
    tf_stk = tb_stk.text_frame
    tf_stk.word_wrap = True
    tf_stk.margin_left = tf_stk.margin_top = tf_stk.margin_right = tf_stk.margin_bottom = 0

    p_st = tf_stk.paragraphs[0]
    p_st.text = "VERIFIED REPOSITORY STACK"
    p_st.font.size = Pt(12)
    p_st.font.bold = True
    p_st.font.color.rgb = COLOR_SUCCESS
    p_st.font.name = "Arial"

    stack_items = [
        ("Frontend Architecture", "React 18 + TypeScript + Vite"),
        ("UI & Component Styling", "Tailwind CSS + Lucide Icons"),
        ("Data Visualization", "Recharts (ROC, PR, Metric Trends)"),
        ("Backend Services", "Python 3.11 + FastAPI (REST)"),
        ("Machine Learning", "scikit-learn ensemble + NumPy"),
        ("Data Persistence", "SQLite (Causal timeline storage)"),
        ("Cloud Deployment", "Vercel Edge Infrastructure")
    ]

    for layer, tech in stack_items:
        p_l = tf_stk.add_paragraph()
        p_l.text = layer.upper()
        p_l.font.size = Pt(8.5)
        p_l.font.bold = True
        p_l.font.color.rgb = COLOR_ACCENT
        p_l.font.name = "Arial"
        p_l.space_before = Pt(6)

        p_tc = tf_stk.add_paragraph()
        p_tc.text = tech
        p_tc.font.size = Pt(10)
        p_tc.font.color.rgb = COLOR_WHITE
        p_tc.font.name = "Arial"
        p_tc.space_before = Pt(1)

    # ==========================================
    # SLIDE 5: TECHNICAL DEPTH & EXPLAINABILITY
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s5)
    add_header(s5, "05 / Technical Depth & Forensics", "Explainable, adaptive, and measurable",
               "Moving beyond black-box classification: answering the 5 critical investigative questions.")

    # Left: The 5 Questions
    add_card(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tb_q = s5.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(5.1), Inches(5.0))
    tf_q = tb_q.text_frame
    tf_q.word_wrap = True
    tf_q.margin_left = tf_q.margin_top = tf_q.margin_right = tf_q.margin_bottom = 0

    p_qh = tf_q.paragraphs[0]
    p_qh.text = "NOT JUST 'FRAUD: YES' — ACTIONABLE ANSWERS"
    p_qh.font.size = Pt(11)
    p_qh.font.bold = True
    p_qh.font.color.rgb = COLOR_ACCENT
    p_qh.font.name = "Arial"

    questions = [
        ("WHY WAS IT FLAGGED?", "Reason codes ranking top contributing spatio-temporal features and threshold boundaries."),
        ("WHAT IS IT CONNECTED TO?", "Entity resolution linking past counterparties, shared beneficiary IDs, and IP clusters."),
        ("WHAT PATTERN DOES IT REPRESENT?", "Classification into 9 financial crime taxonomies (Mule smurfing, Layering, Velocity jump)."),
        ("HOW WELL DOES THE MODEL PERFORM?", "Per-pattern recall evaluation with rigorous 95% Wilson confidence intervals."),
        ("HOW DOES IT HANDLE EVASION?", "Adversarial mutation testing measuring detector degradation across synthetic evasion rounds.")
    ]

    for q_title, q_desc in questions:
        p_qt = tf_q.add_paragraph()
        p_qt.text = q_title
        p_qt.font.size = Pt(9.5)
        p_qt.font.bold = True
        p_qt.font.color.rgb = COLOR_WHITE
        p_qt.font.name = "Arial"
        p_qt.space_before = Pt(6)

        p_qd = tf_q.add_paragraph()
        p_qd.text = q_desc
        p_qd.font.size = Pt(8.5)
        p_qd.font.color.rgb = COLOR_MUTED
        p_qd.font.name = "Arial"
        p_qd.space_before = Pt(1)

    # Right: Screenshots (Inspector & Model Performance)
    add_card(s5, Inches(6.7), Inches(1.5), Inches(5.8), Inches(5.4))
    
    screenshot_insp = "/Users/dhairyajain/Desktop/razorpay_win copy/razor/docs/media/screen_inspector.png"
    screenshot_def = "/Users/dhairyajain/Desktop/razorpay_win copy/razor/docs/media/screen_defend.png"

    if os.path.exists(screenshot_insp):
        s5.shapes.add_picture(screenshot_insp, Inches(6.85), Inches(1.65), Inches(5.5), Inches(2.45))
    if os.path.exists(screenshot_def):
        s5.shapes.add_picture(screenshot_def, Inches(6.85), Inches(4.25), Inches(5.5), Inches(2.45))

    # ==========================================
    # SLIDE 6: CHALLENGES & FUTURE SCOPE
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s6)
    add_header(s6, "06 / Roadmap & Realistic Scope", "From prototype to financial-crime infrastructure",
               "Honest evaluation of current engineering boundaries and the roadmap to enterprise deployment.")

    # Left: Real Engineering Challenges
    add_card(s6, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tb_ch = s6.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(5.1), Inches(5.0))
    tf_ch = tb_ch.text_frame
    tf_ch.word_wrap = True
    tf_ch.margin_left = tf_ch.margin_top = tf_ch.margin_right = tf_ch.margin_bottom = 0

    p_ch = tf_ch.paragraphs[0]
    p_ch.text = "CURRENT TECHNICAL CHALLENGES"
    p_ch.font.size = Pt(11)
    p_ch.font.bold = True
    p_ch.font.color.rgb = COLOR_ALERT
    p_ch.font.name = "Arial"

    challenges = [
        ("Distributed Entity Resolution", "Mapping mule rings when fraudsters use synthetic or compromised accounts across disjoint banking rails."),
        ("Temporal Concept Drift", "Criminal syndicates continually alter transaction cadences, velocity bursts, and threshold-avoidance amounts."),
        ("Investigation Queue Fatigue", "Balancing high pattern recall with strict false-positive budgets to prevent analyst operational overload."),
        ("Synthetic vs Production Gap", "Calibrating models on synthetic pattern datasets before exposing to massive production transaction noise."),
        ("Label Latency in Crime Data", "Real financial crime confirmations often arrive weeks after execution via chargeback/SAR filings.")
    ]

    for c_title, c_desc in challenges:
        p_ct = tf_ch.add_paragraph()
        p_ct.text = f"•  {c_title}"
        p_ct.font.size = Pt(10)
        p_ct.font.bold = True
        p_ct.font.color.rgb = COLOR_WHITE
        p_ct.font.name = "Arial"
        p_ct.space_before = Pt(5)

        p_cd = tf_ch.add_paragraph()
        p_cd.text = f"   {c_desc}"
        p_cd.font.size = Pt(8.5)
        p_cd.font.color.rgb = COLOR_MUTED
        p_cd.font.name = "Arial"
        p_cd.space_before = Pt(1)

    # Right: Future Enterprise Roadmap
    add_card(s6, Inches(6.7), Inches(1.5), Inches(5.8), Inches(5.4))
    tb_fut = s6.shapes.add_textbox(Inches(6.95), Inches(1.7), Inches(5.3), Inches(5.0))
    tf_fut = tb_fut.text_frame
    tf_fut.word_wrap = True
    tf_fut.margin_left = tf_fut.margin_top = tf_fut.margin_right = tf_fut.margin_bottom = 0

    p_ft = tf_fut.paragraphs[0]
    p_ft.text = "FUTURE PRODUCTION ROADMAP (LABELED SCOPE)"
    p_ft.font.size = Pt(11)
    p_ft.font.bold = True
    p_ft.font.color.rgb = COLOR_SUCCESS
    p_ft.font.name = "Arial"

    future_items = [
        ("Graph-Native Detection Engines", "Integrating Graph Neural Networks (GNNs) for sub-millisecond dynamic subgraph clustering."),
        ("Streaming Kafka / Flink Pipeline", "Real-time stateful stream processing capable of handling 50,000+ UPI TPS."),
        ("Analyst Active Learning Loop", "Incorporating human investigator resolution outcomes directly into incremental model updates."),
        ("Privacy-Preserving Federated Intelligence", "Cross-institutional fraud signal sharing via secure multi-party computation without sharing PII."),
        ("Enterprise Feature Store Integration", "Low-latency point-in-time feature computation via Redis / Feast infrastructure.")
    ]

    for f_title, f_desc in future_items:
        p_ftt = tf_fut.add_paragraph()
        p_ftt.text = f"•  {f_title}"
        p_ftt.font.size = Pt(10)
        p_ftt.font.bold = True
        p_ftt.font.color.rgb = COLOR_WHITE
        p_ftt.font.name = "Arial"
        p_ftt.space_before = Pt(5)

        p_ftd = tf_fut.add_paragraph()
        p_ftd.text = f"   {f_desc}"
        p_ftd.font.size = Pt(8.5)
        p_ftd.font.color.rgb = COLOR_MUTED
        p_ftd.font.name = "Arial"
        p_ftd.space_before = Pt(1)

    # ==========================================
    # SLIDE 7: THANK YOU SLIDE
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s7)

    # Center card
    add_card(s7, Inches(2.2), Inches(1.4), Inches(8.933), Inches(4.7))

    tb_ty = s7.shapes.add_textbox(Inches(2.6), Inches(1.8), Inches(8.133), Inches(3.9))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_left = tf_ty.margin_top = tf_ty.margin_right = tf_ty.margin_bottom = 0

    p_t1 = tf_ty.paragraphs[0]
    p_t1.alignment = PP_ALIGN.CENTER
    p_t1.text = "SENTINEL"
    p_t1.font.size = Pt(40)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_WHITE
    p_t1.font.name = "Arial"

    p_t2 = tf_ty.add_paragraph()
    p_t2.alignment = PP_ALIGN.CENTER
    p_t2.text = "Financial crime doesn't hide in transactions. It hides in patterns."
    p_t2.font.size = Pt(15)
    p_t2.font.bold = True
    p_t2.font.color.rgb = COLOR_ACCENT
    p_t2.font.name = "Arial"
    p_t2.space_before = Pt(8)

    p_t3 = tf_ty.add_paragraph()
    p_t3.alignment = PP_ALIGN.CENTER
    p_t3.text = "YEL Build $ Bank 2026  •  Track 2 — Fraud Detection & Financial Crime Prevention  •  Problem 5"
    p_t3.font.size = Pt(11)
    p_t3.font.color.rgb = COLOR_MUTED
    p_t3.font.name = "Arial"
    p_t3.space_before = Pt(16)

    p_t4 = tf_ty.add_paragraph()
    p_t4.alignment = PP_ALIGN.CENTER
    p_t4.text = "Live Web Application: https://sentinel-sand-two.vercel.app\nGitHub Repository: https://github.com/dhairyahuh/Sentinel"
    p_t4.font.size = Pt(11)
    p_t4.font.bold = True
    p_t4.font.color.rgb = COLOR_TEXT
    p_t4.font.name = "Arial"
    p_t4.space_before = Pt(20)

    p_t5 = tf_ty.add_paragraph()
    p_t5.alignment = PP_ALIGN.CENTER
    p_t5.text = "Thank you to the Youth Economy Lab & IGDTUW Review Committee."
    p_t5.font.size = Pt(10)
    p_t5.font.color.rgb = COLOR_MUTED
    p_t5.font.name = "Arial"
    p_t5.space_before = Pt(16)

    # Save output
    output_path = "/Users/dhairyajain/Desktop/razorpay_win copy/razor/Sentinel_Pitch_Deck_YEL2026.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    create_pitch_deck()
