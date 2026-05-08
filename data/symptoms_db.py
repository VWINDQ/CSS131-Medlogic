from kanren import Relation, facts

# Relations Opject ซึ่งในเชิง Logic Programming ถือเป็นการกำหนด Predicate เพื่อใช้เป็นโครงสร้างหลักในการเก็บ facts
# ── Relations (think: database tables) ─────────────────────────────────────
has_symptom      = Relation()   # (disease, symptom) <- ใช้ประกาศข้อเท็จจริงว่า โรค X มีอาการ Y
risk_factor      = Relation()   # (disease, risk_factor) <- ใช้ประกาศข้อเท็จจริงว่า โรค X มีปัจจัยเสี่ยง Y
disease_category = Relation()   # (disease, category) <- ใช้ประกาศข้อเท็จจริงว่า โรค X อยู่ในหมวดหมู่ Y

# ──  has_symptom - โรค x อาการ y ─────
_SYMPTOM_FACTS = [
    # ── ระบบทางเดินหายใจ ───
    # -- ไข้หวัดใหญ่ --
    ("influenza",           "fever"), # ไข้
    ("influenza",           "cough"), # ไอ
    ("influenza",           "body_aches"), # ปวดเมื่อยตามตัว
    ("influenza",           "fatigue"), # อ่อนเพลีย
    ("influenza",           "headache"), # ปวดหัว
    # -- ไข้ --
    ("common_cold",         "runny_nose"), # น้ำมูกไหล
    ("common_cold",         "sore_throat"), # เจ็บคอ
    ("common_cold",         "sneezing"), # จาม
    ("common_cold",         "mild_cough"), # ไอเล็กน้อย
    ("common_cold",         "congestion"), # คัดจมูก
    # -- covid19 --
    ("covid19",             "fever"), # ไข้
    ("covid19",             "cough"), # ไอ
    ("covid19",             "loss_of_taste"), # สูญเสียการรับรส
    ("covid19",             "loss_of_smell"), # สูญเสียการดม
    ("covid19",             "fatigue"), # อ่อนเพลีย
    ("covid19",             "shortness_of_breath"), # หายใจลำบาก
    # -- ปอดบวม --
    ("pneumonia",           "high_fever"), # ไข้สูง
    ("pneumonia",           "chest_pain"), # เจ็บหน้าอก
    ("pneumonia",           "productive_cough"), # ไอมีเสมหะ
    ("pneumonia",           "shortness_of_breath"), # หายใจลำบาก
    ("pneumonia",           "fatigue"), # อ่อนเพลีย

    # ── ระบบทางเดินอาหาร ──
    # -- อาหารเป็นพิษ --
    ("gastroenteritis",     "nausea"), # คลืืนไส้
    ("gastroenteritis",     "vomiting"), # อาเจียน
    ("gastroenteritis",     "diarrhea"), # ท้องเสีย
    ("gastroenteritis",     "stomach_cramps"), # ปวดท้องเกร็ง
    ("gastroenteritis",     "fatigue"), # เหนื่อยล้า
    # -- ไส้ติ่งอักเสบ --
    ("appendicitis",        "severe_abdominal_pain"), # ปวดท้องรุนแรง
    ("appendicitis",        "nausea"), # คลื่นไส้
    ("appendicitis",        "fever"), # ไข้
    ("appendicitis",        "loss_of_appetite"), # เบื่ออาหาร

    # -- ระบบทั่วไป --
    # -- ภาวะขาดน้ำ --
    ("dehydration",         "dizziness"), # เวียนศีรษะ
    ("dehydration",         "dry_mouth"), # ปากแห้ง
    ("dehydration",         "fatigue"), # อ่อนเพลีย
    ("dehydration",         "headache"), # ปวดหัว
    # -- โลหิตจาง --
    ("anemia",              "fatigue"), # อ่อนเพลีย
    ("anemia",              "pallor"), # ซีด
    ("anemia",              "shortness_of_breath"), # หายใจลำบาก
    ("anemia",              "dizziness"), # เวียนศีรษะ
    #-- ADHD --
    ("adhd",                "inattention"), # ขาดสมาธิ
    ("adhd",                "hyperactivity"), # อยู่ไม่นิ่ง/ซนผิดปกติ
    ("adhd",                "impulsivity"),  # หุนหันพลันแล่น
    ("adhd",                "restlessness"), # กระสับกระส่าย
    ("adhd",                "difficulty_focusing"), # จดจ่อกับสิ่งใดสิ่งหนึ่งได้ยาก
]

# ── Risk - โรค x ปัจจัยเสี่ยง y ──
_RISK_FACTS = [
    # -- ไข้หวัดใหญ่ --
    ("influenza",           "elderly"), # เป็น ผู้สูงอายุ
    ("influenza",           "immunocompromised"), # มีภูมิคุ้มกันบกพร่อง
    # -- ปอดบวม --
    ("pneumonia",           "elderly"), # เป็นผู้สูงอายุ
    ("pneumonia",           "smoker"), # สูบบบุหรี่
    # -- covid19 --
    ("covid19",             "elderly"), # เป็นผู้สูงอายุ
    ("covid19",             "obesity"), # ภาวะอ้วน
    # -- โลหิตจาง --
    ("anemia",              "vegetarian"), # มังสวิรัติ
    ("anemia",              "female"), # เพศหญิง 
    # -- ภาวะขาดน้ำ --
    ("dehydration",         "athlete"), # นักกีฬา
    # -- อาหารเป็นพิษ --
    ("gastroenteritis",     "traveler"), # นักท่องเที่ยว (เสี่ยงจากการกินอาหารที่ไม่สะอาด)
    # -- ADHD --
    ("adhd",                "family_history"), # มีคนในครอบครัวเป็น
]

# ── Disease-Category - โรค x หมวดหมู่ y ──
_CATEGORY_FACTS = [
    # -- ไข้หวัดใหญ่ --
    ("influenza",           "respiratory"), # โรคระบบทางเดินหายใจ
    # -- ไข้ --
    ("common_cold",         "respiratory"), # โรคระบบทางเดินหายใจ
    # -- covid19 --
    ("covid19",             "respiratory"), # โรคระบบทางเดินหายใจ
    # -- ปอดบวม --
    ("pneumonia",           "respiratory"), # โรคระบบทางเดินหายใจ
    # -- อาหารเป็นพิษ --
    ("gastroenteritis",     "gastrointestinal"), # ระบบทางเดินอาหาร
    # -- ไส้ติ่งอักเสบ --
    ("appendicitis",        "gastrointestinal"), # ระบบทางเดินอาหาร
    # -- ภาวะขาดน้ำ --
    ("dehydration",         "general"), # ระบบทั่วไป
    # -- โลหิตจาง --
    ("anemia",              "general"), # ระบบทั่วไป
    # --ADHD --
    ("adhd",                "neurodevelopmental"), # กลุ่มโรคพัฒนาการทางระบบประสาท
]

# ── Human-Readable Descriptions ─────────────────────────────────────────────
DISEASE_DESCRIPTIONS: dict[str, str] = {
    # -- ไข้หวัดใหญ่ --
    "influenza":        "A contagious viral infection affecting the respiratory tract.",
    # -- ไข้ --
    "common_cold":      "A mild upper-respiratory infection caused by various viruses.",
    # -- covid19 --
    "covid19":          "An infectious disease caused by the SARS-CoV-2 coronavirus.",
    # -- ปอดบวม --
    "pneumonia":        "Infection inflaming air sacs in one or both lungs.",
    # -- อาหารเป็นพิษ --
    "gastroenteritis":  "Inflammation of the stomach and intestines (stomach flu).",
    # -- ไส้ติ่งอักเสบ --   
    "appendicitis":     "Inflammation of the appendix — requires urgent medical care.",
    # -- ภาวะขาดน้ำ --
    "dehydration":      "Occurs when fluid loss exceeds fluid intake.",
    # -- โลหิตจาง --
    "anemia":           "Insufficient healthy red blood cells to carry adequate oxygen.",
    # -- ADHD --
    "adhd":             "A neurodevelopmental disorder characterized by inattention, hyperactivity, and impulsivity.",
}

VALID_SYMPTOMS: list[str] = sorted({s for _, s in _SYMPTOM_FACTS})
VALID_RISK_FACTORS: list[str] = sorted({r for _, r in _RISK_FACTS})


def load_facts() -> None:
    """
    Assert all facts into their Kanren Relations.
    Must be called once before any query is run.
    """
    facts(has_symptom,      *_SYMPTOM_FACTS)
    facts(risk_factor,      *_RISK_FACTS)
    facts(disease_category, *_CATEGORY_FACTS)
    print("[MedLogic] Knowledge base loaded: "
          f"{len(_SYMPTOM_FACTS)} symptom facts, "
          f"{len(_RISK_FACTS)} risk facts.")
