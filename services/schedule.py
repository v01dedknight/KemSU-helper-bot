from typing import Dict, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Base directory with local PDF schedules
SCHEDULES_DIR = Path("assets/schedules")

# Mapping: category -> group name -> relative pdf path
SCHEDULE_DATA: Dict[str, Dict[str, Path]] = {

    # I COURSE
    "I курс": {
        "ФИТ-251, МОА-251": SCHEDULES_DIR / "1/IC_1c_fit-251,moa-251_3.pdf",
        "ПМИ-251, ПИ-251, КБ-251": SCHEDULES_DIR / "1/IC_1c_pmi-251,pi-251,kb-251_4.pdf",
        "ПИз-251": SCHEDULES_DIR / "1/IC_zaoch_1c_piz-251_2.pdf",
        "ПМИм-251": SCHEDULES_DIR / "1/IC_mag_1c_pmim-251.pdf",
        "МОАм-251": SCHEDULES_DIR / "1/IC_mag_1c_moam-251_2.pdf",
        "ПИм-251": SCHEDULES_DIR / "1/IC_mag_1c_pim-251_3.pdf",
    },

    # II COURSE
    "II курс": {
        "ФИТ-241, МОА-241": SCHEDULES_DIR / "2/IC_2c_fit-241,moa-241_2.pdf",
        "ПМИ-241, ПИ-241, КБ-241": SCHEDULES_DIR / "2/IC_2c_pmi-241,pi-241, kb-241_4.pdf",
        "ПИз-241": SCHEDULES_DIR / "2/IC_zaoch_2c_piz-241_3.pdf",
        "МОАм-241": SCHEDULES_DIR / "2/IC_mag_2c_moam-241_2.pdf",
        "ПИм-241": SCHEDULES_DIR / "2/IC_mag_2c_pim-241_2.pdf",
        "ПМИм-241": SCHEDULES_DIR / "2/IC_mag_2c_pmim-241_2.pdf",
    },

    # III COURSE
    "III курс": {
        "ФИТ-231, МОА-231": SCHEDULES_DIR / "3/IC_3c_fit-231,moa-231_3.pdf",
        "ПМИ-231, ПИ-231, КБ-231": SCHEDULES_DIR / "3/IC_3c_pmi-231,pi-231,kb-231_7.pdf",
        "ПИз-231": SCHEDULES_DIR / "3/IC_zaoch_3c_piz-231_2.pdf",
    },

    # IV COURSE
    "IV курс": {
        "ФИТ-221, МОА-221": SCHEDULES_DIR / "4/IC_4c_fit-221,moa-221_2.pdf",
        "ПМИ-221, ПИ-221, КБ-221": SCHEDULES_DIR / "4/IC_4c_pmi-221,pi-221_kb-221_3.pdf",
        "ПИз-221": SCHEDULES_DIR / "4/IC_zaoch_4c_piz-221_2.pdf",
    },

    # V COURSE
    "V курс": {
        "ПИз-221": SCHEDULES_DIR / "5/IC_zaoch_5c_piz-211_4.pdf",
    },

    # EXAMS 
    "Экзамены": {
        "ПМИ-251, ПИ-251, ФИТ-251, МОА-251, КБ-251":
            SCHEDULES_DIR / "exams/IC_1c_25-26_exam_pmi,pi,fit,moa,kb-251.pdf",

        "ПМИ-241, ПИ-241, ФИТ-241, МОА-241, КБ-241":
            SCHEDULES_DIR / "exams/IC_2c_25-26_exam_pmi,pi,fit,moa,kb-241_2.pdf",

        "ПМИ-231, ПИ-231, ФИТ-231, МОА-231, КБ-231":
            SCHEDULES_DIR / "exams/IC_3c_25-26_exam_pmi,pi,fit,moa,kb-231.pdf",

        "ПМИ-221, ПИ-221, ФИТ-221, МОА-221, КБ-221":
            SCHEDULES_DIR / "exams/IC_4c_25-26_exam_pmi,pi,fit,moa,kb-221.pdf",

        "ПИм-251":
            SCHEDULES_DIR / "exams/IC_1c_mag_25-26_exam_pim-251.pdf",

        "МОАм-251":
            SCHEDULES_DIR / "exams/IC_1c_mag_25-26_exam_moam-251.pdf",

        "ПМИм-251":
            SCHEDULES_DIR / "exams/IC_1c_mag_25-26_exam_pmim-251.pdf",

        "ПИм-241":
            SCHEDULES_DIR / "exams/IC_2c_mag_25-26_exam_pim-241_2.pdf",

        "МОАм-241":
            SCHEDULES_DIR / "exams/IC_2c_mag_25-26_exam_moam-241.pdf",

        "ПМИм-241":
            SCHEDULES_DIR / "exams/IC_1c_mag_25-26_exam_pmim-241.pdf",
    },

    # STATE FINAL CERTIFICATION
    "Государственная итоговая аттестация": {
        "09.03.03 Прикладная информатика":
            SCHEDULES_DIR / "statefinalcertification/IC_GIA_090303_z_5c_2025-2026.pdf",
    },
}


# PUBLIC API 

def get_categories() -> List[str]:
    logger.debug("Fetching schedule categories")
    return list(SCHEDULE_DATA.keys())


def get_groups(category: str) -> List[str]:
    logger.debug(f"Fetching groups for category: {category}")
    return list(SCHEDULE_DATA.get(category, {}).keys())


def get_schedule_path(category: str, group: str) -> Path | None:
    logger.warning(f"Schedule not found for category={category}, group={group}")
    path = SCHEDULE_DATA.get(category, {}).get(group)
    return path if path and path.exists() else None