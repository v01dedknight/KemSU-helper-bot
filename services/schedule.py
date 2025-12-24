from typing import Dict, List

# Each category contains a specific file assigned to the groups
SCHEDULE_DATA: Dict[str, Dict[str, str]] = {
    "I курс": {
        "ФИТ-251, МОА-251": "https://kemsu.ru/upload/education/schedule/ic/och/IC_1c_fit-251,moa-251_3.pdf",
        "ПМИ-251, ПИ-251, КБ-251": "https://kemsu.ru/upload/education/schedule/ic/och/IC_1c_pmi-251,pi-251,kb-251_4.pdf",
        "ПИз-251": "https://kemsu.ru/upload/education/schedule/ic/zaoch/IC_zaoch_1c_piz-251.pdf",
        "ПМИм-251": "https://kemsu.ru/upload/education/schedule/ic/och/IC_mag_1c_pmim-251.pdf",
        "МОАм-251": "https://kemsu.ru/upload/education/schedule/ic/och/IC_mag_1c_moam-251_2.pdf",
        "ПИм-251": "https://kemsu.ru/upload/education/schedule/ic/och/IC_mag_1c_pim-251_3.pdf",
    },
    "II курс": {
        "ПМИ-241, ПИ-241, КБ-241": "https://kemsu.ru/upload/education/schedule/ic/och/IC_2c_pmi-241,pi-241,%20kb-241_4.pdf",
        "ФИТ-241, МОА-241": "https://kemsu.ru/upload/education/schedule/ic/och/IC_2c_fit-241,moa-241_2.pdf",
        "ПИз-241": "https://kemsu.ru/upload/education/schedule/ic/zaoch/IC_zaoch_2c_piz-241_2.pdf",
        "МОАм-241": "https://kemsu.ru/upload/education/schedule/ic/och/IC_mag_2c_moam-241_2.pdf",
        "ПИм-241": "https://kemsu.ru/upload/education/schedule/ic/och/IC_mag_2c_pim-241_2.pdf",
        "ПМИм-241": "https://kemsu.ru/upload/education/schedule/ic/och/IC_mag_2c_pmim-241_2.pdf",
    },
    "III курс": {
        "ПМИ-231, ПИ-231, КБ-231": "https://kemsu.ru/upload/education/schedule/ic/och/IC_3c_pmi-231,pi-231,kb-231_7.pdf",
        "ФИТ-231, МОА-231": "https://kemsu.ru/upload/education/schedule/ic/och/IC_3c_fit-231,moa-231_3.pdf",
        "ПИз-231": "https://kemsu.ru/upload/education/schedule/ic/zaoch/IC_zaoch_3c_piz-231.pdf",
    },
    "IV курс": {
        "ФИТ-221, МОА-221": "https://kemsu.ru/upload/education/schedule/ic/och/IC_4c_fit-221,moa-221_2.pdf",
        "ПМИ-221, ПИ-221, КБ-221": "https://kemsu.ru/upload/education/schedule/ic/och/IC_4c_pmi-221,pi-221_kb-221_3.pdf",
        "ПИз-221": "https://kemsu.ru/upload/education/schedule/ic/zaoch/IC_zaoch_4c_piz-221.pdf",
    },
    "V курс": {
        "ПИз-221": "https://kemsu.ru/upload/education/schedule/ic/zaoch/IC_zaoch_5c_piz-211_3.pdf",
    },
    "Экзамены": {
        "ПМИ-251, ПИ-251, ФИТ-251, МОА-251, КБ-251": "https://kemsu.ru/upload/education/schedule/ic/exam/IC_1c_25-26_exam_pmi,pi,fit,moa,kb-251.pdf",
        "ПМИ-241, ПИ-241, ФИТ-241, МОА-241, КБ-241": "https://kemsu.ru/upload/education/schedule/ic/exam/IC_2c_25-26_exam_pmi,pi,fit,moa,kb-241_2.pdf",
        "ПМИ-231, ПИ-231, ФИТ-231, МОА-231, КБ-231": "https://kemsu.ru/upload/education/schedule/ic/exam/IC_3c_25-26_exam_pmi,pi,fit,moa,kb-231.pdf",
        "ПМИ-221, ПИ-221, ФИТ-221, МОА-221, КБ-221": "https://kemsu.ru/upload/education/schedule/ic/exam/IC_4c_25-26_exam_pmi,pi,fit,moa,kb-221.pdf",
        "ПИм-251": "https://kemsu.ru/upload/education/schedule/ic/exam/IC_1c_mag_25-26_exam_pim-251.pdf",
        "МОАм-251": "https://kemsu.ru/upload/education/schedule/ic/exam/IC_1c_mag_25-26_exam_moam-251.pdf",
        "ПМИм-251": "https://kemsu.ru/upload/education/schedule/ic/exam/IC_1c_mag_25-26_exam_pmim-251.pdf",
        "ПИм-241": "https://kemsu.ru/upload/education/schedule/ic/exam/IC_2c_mag_25-26_exam_pim-241_2.pdf",
        "МОАм-241": "https://kemsu.ru/upload/education/schedule/ic/exam/IC_2c_mag_25-26_exam_moam-241.pdf",
        "ПМИм-241": "https://kemsu.ru/upload/education/schedule/ic/exam/IC_1c_mag_25-26_exam_pmim-241.pdf",
    },
    "Государственная итоговая аттестация": {
        "09.03.03 Прикладная информатика": "https://kemsu.ru/upload/education/schedule/ic/gia/IC_GIA_090303_z_5c_2025-2026.pdf",
    },
}

# UX part

# Select the schedule category (groups, exams, and state final exams)
def get_categories() -> List[str]:
    return list(SCHEDULE_DATA.keys())

# Group selection (encapsulated after category selection)
def get_groups(category: str) -> List[str]:
    return list(SCHEDULE_DATA.get(category, {}).keys())

# The schedule is transmitted (encapsulated after group selection)
def get_schedule_url(category: str, group: str) -> str | None:
    return SCHEDULE_DATA.get(category, {}).get(group)