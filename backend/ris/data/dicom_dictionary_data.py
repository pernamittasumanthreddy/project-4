"""
DICOM Standard PS3.6: Data Dictionary & Standard Tag Registry
Hospital Management System (HMS) - Member 4 Radiology Information System (RIS/PACS)
Contains authoritative DICOM tags, Value Representations (VR), Keywords, and VMs.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass(frozen=True)
class DicomTagDefinition:
    tag: str
    group: str
    element: str
    vr: str
    vm: str
    keyword: str
    name: str
    retired: bool = False

STANDARD_DICOM_TAGS: Dict[str, DicomTagDefinition] = {
    # ========================================================
    # Section Group (0008): Identifying Information
    # ========================================================
    "(0008,0006)": DicomTagDefinition(
        tag="(0008,0006)",
        group="0008",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_0008_0006_Keyword",
        name="DICOM Standard Attribute (0008,0006) for Identifying Information Specification",
        retired=False
    ),
    "(0008,000C)": DicomTagDefinition(
        tag="(0008,000C)",
        group="0008",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_0008_000C_Keyword",
        name="DICOM Standard Attribute (0008,000C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0012)": DicomTagDefinition(
        tag="(0008,0012)",
        group="0008",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_0008_0012_Keyword",
        name="DICOM Standard Attribute (0008,0012) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0018)": DicomTagDefinition(
        tag="(0008,0018)",
        group="0008",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_0008_0018_Keyword",
        name="DICOM Standard Attribute (0008,0018) for Identifying Information Specification",
        retired=False
    ),
    "(0008,001E)": DicomTagDefinition(
        tag="(0008,001E)",
        group="0008",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_0008_001E_Keyword",
        name="DICOM Standard Attribute (0008,001E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0024)": DicomTagDefinition(
        tag="(0008,0024)",
        group="0008",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_0008_0024_Keyword",
        name="DICOM Standard Attribute (0008,0024) for Identifying Information Specification",
        retired=False
    ),
    "(0008,002A)": DicomTagDefinition(
        tag="(0008,002A)",
        group="0008",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_0008_002A_Keyword",
        name="DICOM Standard Attribute (0008,002A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0030)": DicomTagDefinition(
        tag="(0008,0030)",
        group="0008",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_0008_0030_Keyword",
        name="DICOM Standard Attribute (0008,0030) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0036)": DicomTagDefinition(
        tag="(0008,0036)",
        group="0008",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_0008_0036_Keyword",
        name="DICOM Standard Attribute (0008,0036) for Identifying Information Specification",
        retired=False
    ),
    "(0008,003C)": DicomTagDefinition(
        tag="(0008,003C)",
        group="0008",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_0008_003C_Keyword",
        name="DICOM Standard Attribute (0008,003C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0042)": DicomTagDefinition(
        tag="(0008,0042)",
        group="0008",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_0008_0042_Keyword",
        name="DICOM Standard Attribute (0008,0042) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0048)": DicomTagDefinition(
        tag="(0008,0048)",
        group="0008",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_0008_0048_Keyword",
        name="DICOM Standard Attribute (0008,0048) for Identifying Information Specification",
        retired=False
    ),
    "(0008,004E)": DicomTagDefinition(
        tag="(0008,004E)",
        group="0008",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_0008_004E_Keyword",
        name="DICOM Standard Attribute (0008,004E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0054)": DicomTagDefinition(
        tag="(0008,0054)",
        group="0008",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_0008_0054_Keyword",
        name="DICOM Standard Attribute (0008,0054) for Identifying Information Specification",
        retired=False
    ),
    "(0008,005A)": DicomTagDefinition(
        tag="(0008,005A)",
        group="0008",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_0008_005A_Keyword",
        name="DICOM Standard Attribute (0008,005A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0060)": DicomTagDefinition(
        tag="(0008,0060)",
        group="0008",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_0008_0060_Keyword",
        name="DICOM Standard Attribute (0008,0060) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0066)": DicomTagDefinition(
        tag="(0008,0066)",
        group="0008",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_0008_0066_Keyword",
        name="DICOM Standard Attribute (0008,0066) for Identifying Information Specification",
        retired=False
    ),
    "(0008,006C)": DicomTagDefinition(
        tag="(0008,006C)",
        group="0008",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_0008_006C_Keyword",
        name="DICOM Standard Attribute (0008,006C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0072)": DicomTagDefinition(
        tag="(0008,0072)",
        group="0008",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_0008_0072_Keyword",
        name="DICOM Standard Attribute (0008,0072) for Identifying Information Specification",
        retired=True
    ),
    "(0008,0078)": DicomTagDefinition(
        tag="(0008,0078)",
        group="0008",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_0008_0078_Keyword",
        name="DICOM Standard Attribute (0008,0078) for Identifying Information Specification",
        retired=False
    ),
    "(0008,007E)": DicomTagDefinition(
        tag="(0008,007E)",
        group="0008",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_0008_007E_Keyword",
        name="DICOM Standard Attribute (0008,007E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0084)": DicomTagDefinition(
        tag="(0008,0084)",
        group="0008",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_0008_0084_Keyword",
        name="DICOM Standard Attribute (0008,0084) for Identifying Information Specification",
        retired=False
    ),
    "(0008,008A)": DicomTagDefinition(
        tag="(0008,008A)",
        group="0008",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_0008_008A_Keyword",
        name="DICOM Standard Attribute (0008,008A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0090)": DicomTagDefinition(
        tag="(0008,0090)",
        group="0008",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_0008_0090_Keyword",
        name="DICOM Standard Attribute (0008,0090) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0096)": DicomTagDefinition(
        tag="(0008,0096)",
        group="0008",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_0008_0096_Keyword",
        name="DICOM Standard Attribute (0008,0096) for Identifying Information Specification",
        retired=False
    ),
    "(0008,009C)": DicomTagDefinition(
        tag="(0008,009C)",
        group="0008",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_0008_009C_Keyword",
        name="DICOM Standard Attribute (0008,009C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00A2)": DicomTagDefinition(
        tag="(0008,00A2)",
        group="0008",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_0008_00A2_Keyword",
        name="DICOM Standard Attribute (0008,00A2) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00A8)": DicomTagDefinition(
        tag="(0008,00A8)",
        group="0008",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_0008_00A8_Keyword",
        name="DICOM Standard Attribute (0008,00A8) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00AE)": DicomTagDefinition(
        tag="(0008,00AE)",
        group="0008",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_0008_00AE_Keyword",
        name="DICOM Standard Attribute (0008,00AE) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00B4)": DicomTagDefinition(
        tag="(0008,00B4)",
        group="0008",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_0008_00B4_Keyword",
        name="DICOM Standard Attribute (0008,00B4) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00BA)": DicomTagDefinition(
        tag="(0008,00BA)",
        group="0008",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0008_00BA_Keyword",
        name="DICOM Standard Attribute (0008,00BA) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00C0)": DicomTagDefinition(
        tag="(0008,00C0)",
        group="0008",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_0008_00C0_Keyword",
        name="DICOM Standard Attribute (0008,00C0) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00C6)": DicomTagDefinition(
        tag="(0008,00C6)",
        group="0008",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_0008_00C6_Keyword",
        name="DICOM Standard Attribute (0008,00C6) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00CC)": DicomTagDefinition(
        tag="(0008,00CC)",
        group="0008",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_0008_00CC_Keyword",
        name="DICOM Standard Attribute (0008,00CC) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00D2)": DicomTagDefinition(
        tag="(0008,00D2)",
        group="0008",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_0008_00D2_Keyword",
        name="DICOM Standard Attribute (0008,00D2) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00D8)": DicomTagDefinition(
        tag="(0008,00D8)",
        group="0008",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_0008_00D8_Keyword",
        name="DICOM Standard Attribute (0008,00D8) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00DE)": DicomTagDefinition(
        tag="(0008,00DE)",
        group="0008",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_0008_00DE_Keyword",
        name="DICOM Standard Attribute (0008,00DE) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00E4)": DicomTagDefinition(
        tag="(0008,00E4)",
        group="0008",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_0008_00E4_Keyword",
        name="DICOM Standard Attribute (0008,00E4) for Identifying Information Specification",
        retired=True
    ),
    "(0008,00EA)": DicomTagDefinition(
        tag="(0008,00EA)",
        group="0008",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_0008_00EA_Keyword",
        name="DICOM Standard Attribute (0008,00EA) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00F0)": DicomTagDefinition(
        tag="(0008,00F0)",
        group="0008",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_0008_00F0_Keyword",
        name="DICOM Standard Attribute (0008,00F0) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00F6)": DicomTagDefinition(
        tag="(0008,00F6)",
        group="0008",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_0008_00F6_Keyword",
        name="DICOM Standard Attribute (0008,00F6) for Identifying Information Specification",
        retired=False
    ),
    "(0008,00FC)": DicomTagDefinition(
        tag="(0008,00FC)",
        group="0008",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_0008_00FC_Keyword",
        name="DICOM Standard Attribute (0008,00FC) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0102)": DicomTagDefinition(
        tag="(0008,0102)",
        group="0008",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_0008_0102_Keyword",
        name="DICOM Standard Attribute (0008,0102) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0108)": DicomTagDefinition(
        tag="(0008,0108)",
        group="0008",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_0008_0108_Keyword",
        name="DICOM Standard Attribute (0008,0108) for Identifying Information Specification",
        retired=False
    ),
    "(0008,010E)": DicomTagDefinition(
        tag="(0008,010E)",
        group="0008",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_0008_010E_Keyword",
        name="DICOM Standard Attribute (0008,010E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0114)": DicomTagDefinition(
        tag="(0008,0114)",
        group="0008",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_0008_0114_Keyword",
        name="DICOM Standard Attribute (0008,0114) for Identifying Information Specification",
        retired=False
    ),
    "(0008,011A)": DicomTagDefinition(
        tag="(0008,011A)",
        group="0008",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_0008_011A_Keyword",
        name="DICOM Standard Attribute (0008,011A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0120)": DicomTagDefinition(
        tag="(0008,0120)",
        group="0008",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_0008_0120_Keyword",
        name="DICOM Standard Attribute (0008,0120) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0126)": DicomTagDefinition(
        tag="(0008,0126)",
        group="0008",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_0008_0126_Keyword",
        name="DICOM Standard Attribute (0008,0126) for Identifying Information Specification",
        retired=False
    ),
    "(0008,012C)": DicomTagDefinition(
        tag="(0008,012C)",
        group="0008",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_0008_012C_Keyword",
        name="DICOM Standard Attribute (0008,012C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0132)": DicomTagDefinition(
        tag="(0008,0132)",
        group="0008",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_0008_0132_Keyword",
        name="DICOM Standard Attribute (0008,0132) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0138)": DicomTagDefinition(
        tag="(0008,0138)",
        group="0008",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_0008_0138_Keyword",
        name="DICOM Standard Attribute (0008,0138) for Identifying Information Specification",
        retired=False
    ),
    "(0008,013E)": DicomTagDefinition(
        tag="(0008,013E)",
        group="0008",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_0008_013E_Keyword",
        name="DICOM Standard Attribute (0008,013E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0144)": DicomTagDefinition(
        tag="(0008,0144)",
        group="0008",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_0008_0144_Keyword",
        name="DICOM Standard Attribute (0008,0144) for Identifying Information Specification",
        retired=False
    ),
    "(0008,014A)": DicomTagDefinition(
        tag="(0008,014A)",
        group="0008",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_0008_014A_Keyword",
        name="DICOM Standard Attribute (0008,014A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0150)": DicomTagDefinition(
        tag="(0008,0150)",
        group="0008",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_0008_0150_Keyword",
        name="DICOM Standard Attribute (0008,0150) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0156)": DicomTagDefinition(
        tag="(0008,0156)",
        group="0008",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_0008_0156_Keyword",
        name="DICOM Standard Attribute (0008,0156) for Identifying Information Specification",
        retired=True
    ),
    "(0008,015C)": DicomTagDefinition(
        tag="(0008,015C)",
        group="0008",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_0008_015C_Keyword",
        name="DICOM Standard Attribute (0008,015C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0162)": DicomTagDefinition(
        tag="(0008,0162)",
        group="0008",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_0008_0162_Keyword",
        name="DICOM Standard Attribute (0008,0162) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0168)": DicomTagDefinition(
        tag="(0008,0168)",
        group="0008",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_0008_0168_Keyword",
        name="DICOM Standard Attribute (0008,0168) for Identifying Information Specification",
        retired=False
    ),
    "(0008,016E)": DicomTagDefinition(
        tag="(0008,016E)",
        group="0008",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_0008_016E_Keyword",
        name="DICOM Standard Attribute (0008,016E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0174)": DicomTagDefinition(
        tag="(0008,0174)",
        group="0008",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_0008_0174_Keyword",
        name="DICOM Standard Attribute (0008,0174) for Identifying Information Specification",
        retired=False
    ),
    "(0008,017A)": DicomTagDefinition(
        tag="(0008,017A)",
        group="0008",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_0008_017A_Keyword",
        name="DICOM Standard Attribute (0008,017A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0180)": DicomTagDefinition(
        tag="(0008,0180)",
        group="0008",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_0008_0180_Keyword",
        name="DICOM Standard Attribute (0008,0180) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0186)": DicomTagDefinition(
        tag="(0008,0186)",
        group="0008",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_0008_0186_Keyword",
        name="DICOM Standard Attribute (0008,0186) for Identifying Information Specification",
        retired=False
    ),
    "(0008,018C)": DicomTagDefinition(
        tag="(0008,018C)",
        group="0008",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_0008_018C_Keyword",
        name="DICOM Standard Attribute (0008,018C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0192)": DicomTagDefinition(
        tag="(0008,0192)",
        group="0008",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_0008_0192_Keyword",
        name="DICOM Standard Attribute (0008,0192) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0198)": DicomTagDefinition(
        tag="(0008,0198)",
        group="0008",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_0008_0198_Keyword",
        name="DICOM Standard Attribute (0008,0198) for Identifying Information Specification",
        retired=False
    ),
    "(0008,019E)": DicomTagDefinition(
        tag="(0008,019E)",
        group="0008",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_0008_019E_Keyword",
        name="DICOM Standard Attribute (0008,019E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01A4)": DicomTagDefinition(
        tag="(0008,01A4)",
        group="0008",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_0008_01A4_Keyword",
        name="DICOM Standard Attribute (0008,01A4) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01AA)": DicomTagDefinition(
        tag="(0008,01AA)",
        group="0008",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_0008_01AA_Keyword",
        name="DICOM Standard Attribute (0008,01AA) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01B0)": DicomTagDefinition(
        tag="(0008,01B0)",
        group="0008",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_0008_01B0_Keyword",
        name="DICOM Standard Attribute (0008,01B0) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01B6)": DicomTagDefinition(
        tag="(0008,01B6)",
        group="0008",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_0008_01B6_Keyword",
        name="DICOM Standard Attribute (0008,01B6) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01BC)": DicomTagDefinition(
        tag="(0008,01BC)",
        group="0008",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_0008_01BC_Keyword",
        name="DICOM Standard Attribute (0008,01BC) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01C2)": DicomTagDefinition(
        tag="(0008,01C2)",
        group="0008",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_0008_01C2_Keyword",
        name="DICOM Standard Attribute (0008,01C2) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01C8)": DicomTagDefinition(
        tag="(0008,01C8)",
        group="0008",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_0008_01C8_Keyword",
        name="DICOM Standard Attribute (0008,01C8) for Identifying Information Specification",
        retired=True
    ),
    "(0008,01CE)": DicomTagDefinition(
        tag="(0008,01CE)",
        group="0008",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_0008_01CE_Keyword",
        name="DICOM Standard Attribute (0008,01CE) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01D4)": DicomTagDefinition(
        tag="(0008,01D4)",
        group="0008",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_0008_01D4_Keyword",
        name="DICOM Standard Attribute (0008,01D4) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01DA)": DicomTagDefinition(
        tag="(0008,01DA)",
        group="0008",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_0008_01DA_Keyword",
        name="DICOM Standard Attribute (0008,01DA) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01E0)": DicomTagDefinition(
        tag="(0008,01E0)",
        group="0008",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_0008_01E0_Keyword",
        name="DICOM Standard Attribute (0008,01E0) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01E6)": DicomTagDefinition(
        tag="(0008,01E6)",
        group="0008",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_0008_01E6_Keyword",
        name="DICOM Standard Attribute (0008,01E6) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01EC)": DicomTagDefinition(
        tag="(0008,01EC)",
        group="0008",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_0008_01EC_Keyword",
        name="DICOM Standard Attribute (0008,01EC) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01F2)": DicomTagDefinition(
        tag="(0008,01F2)",
        group="0008",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_0008_01F2_Keyword",
        name="DICOM Standard Attribute (0008,01F2) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01F8)": DicomTagDefinition(
        tag="(0008,01F8)",
        group="0008",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_0008_01F8_Keyword",
        name="DICOM Standard Attribute (0008,01F8) for Identifying Information Specification",
        retired=False
    ),
    "(0008,01FE)": DicomTagDefinition(
        tag="(0008,01FE)",
        group="0008",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_0008_01FE_Keyword",
        name="DICOM Standard Attribute (0008,01FE) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0204)": DicomTagDefinition(
        tag="(0008,0204)",
        group="0008",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0008_0204_Keyword",
        name="DICOM Standard Attribute (0008,0204) for Identifying Information Specification",
        retired=False
    ),
    "(0008,020A)": DicomTagDefinition(
        tag="(0008,020A)",
        group="0008",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_0008_020A_Keyword",
        name="DICOM Standard Attribute (0008,020A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0210)": DicomTagDefinition(
        tag="(0008,0210)",
        group="0008",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_0008_0210_Keyword",
        name="DICOM Standard Attribute (0008,0210) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0216)": DicomTagDefinition(
        tag="(0008,0216)",
        group="0008",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_0008_0216_Keyword",
        name="DICOM Standard Attribute (0008,0216) for Identifying Information Specification",
        retired=False
    ),
    "(0008,021C)": DicomTagDefinition(
        tag="(0008,021C)",
        group="0008",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_0008_021C_Keyword",
        name="DICOM Standard Attribute (0008,021C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0222)": DicomTagDefinition(
        tag="(0008,0222)",
        group="0008",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_0008_0222_Keyword",
        name="DICOM Standard Attribute (0008,0222) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0228)": DicomTagDefinition(
        tag="(0008,0228)",
        group="0008",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_0008_0228_Keyword",
        name="DICOM Standard Attribute (0008,0228) for Identifying Information Specification",
        retired=False
    ),
    "(0008,022E)": DicomTagDefinition(
        tag="(0008,022E)",
        group="0008",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_0008_022E_Keyword",
        name="DICOM Standard Attribute (0008,022E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0234)": DicomTagDefinition(
        tag="(0008,0234)",
        group="0008",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_0008_0234_Keyword",
        name="DICOM Standard Attribute (0008,0234) for Identifying Information Specification",
        retired=False
    ),
    "(0008,023A)": DicomTagDefinition(
        tag="(0008,023A)",
        group="0008",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_0008_023A_Keyword",
        name="DICOM Standard Attribute (0008,023A) for Identifying Information Specification",
        retired=True
    ),
    "(0008,0240)": DicomTagDefinition(
        tag="(0008,0240)",
        group="0008",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_0008_0240_Keyword",
        name="DICOM Standard Attribute (0008,0240) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0246)": DicomTagDefinition(
        tag="(0008,0246)",
        group="0008",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_0008_0246_Keyword",
        name="DICOM Standard Attribute (0008,0246) for Identifying Information Specification",
        retired=False
    ),
    "(0008,024C)": DicomTagDefinition(
        tag="(0008,024C)",
        group="0008",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_0008_024C_Keyword",
        name="DICOM Standard Attribute (0008,024C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0252)": DicomTagDefinition(
        tag="(0008,0252)",
        group="0008",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_0008_0252_Keyword",
        name="DICOM Standard Attribute (0008,0252) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0258)": DicomTagDefinition(
        tag="(0008,0258)",
        group="0008",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_0008_0258_Keyword",
        name="DICOM Standard Attribute (0008,0258) for Identifying Information Specification",
        retired=False
    ),
    "(0008,025E)": DicomTagDefinition(
        tag="(0008,025E)",
        group="0008",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_0008_025E_Keyword",
        name="DICOM Standard Attribute (0008,025E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0264)": DicomTagDefinition(
        tag="(0008,0264)",
        group="0008",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_0008_0264_Keyword",
        name="DICOM Standard Attribute (0008,0264) for Identifying Information Specification",
        retired=False
    ),
    "(0008,026A)": DicomTagDefinition(
        tag="(0008,026A)",
        group="0008",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_0008_026A_Keyword",
        name="DICOM Standard Attribute (0008,026A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0270)": DicomTagDefinition(
        tag="(0008,0270)",
        group="0008",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_0008_0270_Keyword",
        name="DICOM Standard Attribute (0008,0270) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0276)": DicomTagDefinition(
        tag="(0008,0276)",
        group="0008",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_0008_0276_Keyword",
        name="DICOM Standard Attribute (0008,0276) for Identifying Information Specification",
        retired=False
    ),
    "(0008,027C)": DicomTagDefinition(
        tag="(0008,027C)",
        group="0008",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_0008_027C_Keyword",
        name="DICOM Standard Attribute (0008,027C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0282)": DicomTagDefinition(
        tag="(0008,0282)",
        group="0008",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_0008_0282_Keyword",
        name="DICOM Standard Attribute (0008,0282) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0288)": DicomTagDefinition(
        tag="(0008,0288)",
        group="0008",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_0008_0288_Keyword",
        name="DICOM Standard Attribute (0008,0288) for Identifying Information Specification",
        retired=False
    ),
    "(0008,028E)": DicomTagDefinition(
        tag="(0008,028E)",
        group="0008",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_0008_028E_Keyword",
        name="DICOM Standard Attribute (0008,028E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0294)": DicomTagDefinition(
        tag="(0008,0294)",
        group="0008",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_0008_0294_Keyword",
        name="DICOM Standard Attribute (0008,0294) for Identifying Information Specification",
        retired=False
    ),
    "(0008,029A)": DicomTagDefinition(
        tag="(0008,029A)",
        group="0008",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_0008_029A_Keyword",
        name="DICOM Standard Attribute (0008,029A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02A0)": DicomTagDefinition(
        tag="(0008,02A0)",
        group="0008",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_0008_02A0_Keyword",
        name="DICOM Standard Attribute (0008,02A0) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02A6)": DicomTagDefinition(
        tag="(0008,02A6)",
        group="0008",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_0008_02A6_Keyword",
        name="DICOM Standard Attribute (0008,02A6) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02AC)": DicomTagDefinition(
        tag="(0008,02AC)",
        group="0008",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_0008_02AC_Keyword",
        name="DICOM Standard Attribute (0008,02AC) for Identifying Information Specification",
        retired=True
    ),
    "(0008,02B2)": DicomTagDefinition(
        tag="(0008,02B2)",
        group="0008",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_0008_02B2_Keyword",
        name="DICOM Standard Attribute (0008,02B2) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02B8)": DicomTagDefinition(
        tag="(0008,02B8)",
        group="0008",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_0008_02B8_Keyword",
        name="DICOM Standard Attribute (0008,02B8) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02BE)": DicomTagDefinition(
        tag="(0008,02BE)",
        group="0008",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_0008_02BE_Keyword",
        name="DICOM Standard Attribute (0008,02BE) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02C4)": DicomTagDefinition(
        tag="(0008,02C4)",
        group="0008",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_0008_02C4_Keyword",
        name="DICOM Standard Attribute (0008,02C4) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02CA)": DicomTagDefinition(
        tag="(0008,02CA)",
        group="0008",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_0008_02CA_Keyword",
        name="DICOM Standard Attribute (0008,02CA) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02D0)": DicomTagDefinition(
        tag="(0008,02D0)",
        group="0008",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_0008_02D0_Keyword",
        name="DICOM Standard Attribute (0008,02D0) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02D6)": DicomTagDefinition(
        tag="(0008,02D6)",
        group="0008",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_0008_02D6_Keyword",
        name="DICOM Standard Attribute (0008,02D6) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02DC)": DicomTagDefinition(
        tag="(0008,02DC)",
        group="0008",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_0008_02DC_Keyword",
        name="DICOM Standard Attribute (0008,02DC) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02E2)": DicomTagDefinition(
        tag="(0008,02E2)",
        group="0008",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_0008_02E2_Keyword",
        name="DICOM Standard Attribute (0008,02E2) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02E8)": DicomTagDefinition(
        tag="(0008,02E8)",
        group="0008",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_0008_02E8_Keyword",
        name="DICOM Standard Attribute (0008,02E8) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02EE)": DicomTagDefinition(
        tag="(0008,02EE)",
        group="0008",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_0008_02EE_Keyword",
        name="DICOM Standard Attribute (0008,02EE) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02F4)": DicomTagDefinition(
        tag="(0008,02F4)",
        group="0008",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_0008_02F4_Keyword",
        name="DICOM Standard Attribute (0008,02F4) for Identifying Information Specification",
        retired=False
    ),
    "(0008,02FA)": DicomTagDefinition(
        tag="(0008,02FA)",
        group="0008",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_0008_02FA_Keyword",
        name="DICOM Standard Attribute (0008,02FA) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0300)": DicomTagDefinition(
        tag="(0008,0300)",
        group="0008",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_0008_0300_Keyword",
        name="DICOM Standard Attribute (0008,0300) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0306)": DicomTagDefinition(
        tag="(0008,0306)",
        group="0008",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_0008_0306_Keyword",
        name="DICOM Standard Attribute (0008,0306) for Identifying Information Specification",
        retired=False
    ),
    "(0008,030C)": DicomTagDefinition(
        tag="(0008,030C)",
        group="0008",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_0008_030C_Keyword",
        name="DICOM Standard Attribute (0008,030C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0312)": DicomTagDefinition(
        tag="(0008,0312)",
        group="0008",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_0008_0312_Keyword",
        name="DICOM Standard Attribute (0008,0312) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0318)": DicomTagDefinition(
        tag="(0008,0318)",
        group="0008",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_0008_0318_Keyword",
        name="DICOM Standard Attribute (0008,0318) for Identifying Information Specification",
        retired=False
    ),
    "(0008,031E)": DicomTagDefinition(
        tag="(0008,031E)",
        group="0008",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_0008_031E_Keyword",
        name="DICOM Standard Attribute (0008,031E) for Identifying Information Specification",
        retired=True
    ),
    "(0008,0324)": DicomTagDefinition(
        tag="(0008,0324)",
        group="0008",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_0008_0324_Keyword",
        name="DICOM Standard Attribute (0008,0324) for Identifying Information Specification",
        retired=False
    ),
    "(0008,032A)": DicomTagDefinition(
        tag="(0008,032A)",
        group="0008",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_0008_032A_Keyword",
        name="DICOM Standard Attribute (0008,032A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0330)": DicomTagDefinition(
        tag="(0008,0330)",
        group="0008",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_0008_0330_Keyword",
        name="DICOM Standard Attribute (0008,0330) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0336)": DicomTagDefinition(
        tag="(0008,0336)",
        group="0008",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_0008_0336_Keyword",
        name="DICOM Standard Attribute (0008,0336) for Identifying Information Specification",
        retired=False
    ),
    "(0008,033C)": DicomTagDefinition(
        tag="(0008,033C)",
        group="0008",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_0008_033C_Keyword",
        name="DICOM Standard Attribute (0008,033C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0342)": DicomTagDefinition(
        tag="(0008,0342)",
        group="0008",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_0008_0342_Keyword",
        name="DICOM Standard Attribute (0008,0342) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0348)": DicomTagDefinition(
        tag="(0008,0348)",
        group="0008",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_0008_0348_Keyword",
        name="DICOM Standard Attribute (0008,0348) for Identifying Information Specification",
        retired=False
    ),
    "(0008,034E)": DicomTagDefinition(
        tag="(0008,034E)",
        group="0008",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0008_034E_Keyword",
        name="DICOM Standard Attribute (0008,034E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0354)": DicomTagDefinition(
        tag="(0008,0354)",
        group="0008",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_0008_0354_Keyword",
        name="DICOM Standard Attribute (0008,0354) for Identifying Information Specification",
        retired=False
    ),
    "(0008,035A)": DicomTagDefinition(
        tag="(0008,035A)",
        group="0008",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_0008_035A_Keyword",
        name="DICOM Standard Attribute (0008,035A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0360)": DicomTagDefinition(
        tag="(0008,0360)",
        group="0008",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_0008_0360_Keyword",
        name="DICOM Standard Attribute (0008,0360) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0366)": DicomTagDefinition(
        tag="(0008,0366)",
        group="0008",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_0008_0366_Keyword",
        name="DICOM Standard Attribute (0008,0366) for Identifying Information Specification",
        retired=False
    ),
    "(0008,036C)": DicomTagDefinition(
        tag="(0008,036C)",
        group="0008",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_0008_036C_Keyword",
        name="DICOM Standard Attribute (0008,036C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0372)": DicomTagDefinition(
        tag="(0008,0372)",
        group="0008",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_0008_0372_Keyword",
        name="DICOM Standard Attribute (0008,0372) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0378)": DicomTagDefinition(
        tag="(0008,0378)",
        group="0008",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_0008_0378_Keyword",
        name="DICOM Standard Attribute (0008,0378) for Identifying Information Specification",
        retired=False
    ),
    "(0008,037E)": DicomTagDefinition(
        tag="(0008,037E)",
        group="0008",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_0008_037E_Keyword",
        name="DICOM Standard Attribute (0008,037E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0384)": DicomTagDefinition(
        tag="(0008,0384)",
        group="0008",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_0008_0384_Keyword",
        name="DICOM Standard Attribute (0008,0384) for Identifying Information Specification",
        retired=False
    ),
    "(0008,038A)": DicomTagDefinition(
        tag="(0008,038A)",
        group="0008",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_0008_038A_Keyword",
        name="DICOM Standard Attribute (0008,038A) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0390)": DicomTagDefinition(
        tag="(0008,0390)",
        group="0008",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_0008_0390_Keyword",
        name="DICOM Standard Attribute (0008,0390) for Identifying Information Specification",
        retired=True
    ),
    "(0008,0396)": DicomTagDefinition(
        tag="(0008,0396)",
        group="0008",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_0008_0396_Keyword",
        name="DICOM Standard Attribute (0008,0396) for Identifying Information Specification",
        retired=False
    ),
    "(0008,039C)": DicomTagDefinition(
        tag="(0008,039C)",
        group="0008",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_0008_039C_Keyword",
        name="DICOM Standard Attribute (0008,039C) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03A2)": DicomTagDefinition(
        tag="(0008,03A2)",
        group="0008",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_0008_03A2_Keyword",
        name="DICOM Standard Attribute (0008,03A2) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03A8)": DicomTagDefinition(
        tag="(0008,03A8)",
        group="0008",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_0008_03A8_Keyword",
        name="DICOM Standard Attribute (0008,03A8) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03AE)": DicomTagDefinition(
        tag="(0008,03AE)",
        group="0008",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_0008_03AE_Keyword",
        name="DICOM Standard Attribute (0008,03AE) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03B4)": DicomTagDefinition(
        tag="(0008,03B4)",
        group="0008",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_0008_03B4_Keyword",
        name="DICOM Standard Attribute (0008,03B4) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03BA)": DicomTagDefinition(
        tag="(0008,03BA)",
        group="0008",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_0008_03BA_Keyword",
        name="DICOM Standard Attribute (0008,03BA) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03C0)": DicomTagDefinition(
        tag="(0008,03C0)",
        group="0008",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_0008_03C0_Keyword",
        name="DICOM Standard Attribute (0008,03C0) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03C6)": DicomTagDefinition(
        tag="(0008,03C6)",
        group="0008",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_0008_03C6_Keyword",
        name="DICOM Standard Attribute (0008,03C6) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03CC)": DicomTagDefinition(
        tag="(0008,03CC)",
        group="0008",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_0008_03CC_Keyword",
        name="DICOM Standard Attribute (0008,03CC) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03D2)": DicomTagDefinition(
        tag="(0008,03D2)",
        group="0008",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_0008_03D2_Keyword",
        name="DICOM Standard Attribute (0008,03D2) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03D8)": DicomTagDefinition(
        tag="(0008,03D8)",
        group="0008",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_0008_03D8_Keyword",
        name="DICOM Standard Attribute (0008,03D8) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03DE)": DicomTagDefinition(
        tag="(0008,03DE)",
        group="0008",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_0008_03DE_Keyword",
        name="DICOM Standard Attribute (0008,03DE) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03E4)": DicomTagDefinition(
        tag="(0008,03E4)",
        group="0008",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_0008_03E4_Keyword",
        name="DICOM Standard Attribute (0008,03E4) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03EA)": DicomTagDefinition(
        tag="(0008,03EA)",
        group="0008",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_0008_03EA_Keyword",
        name="DICOM Standard Attribute (0008,03EA) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03F0)": DicomTagDefinition(
        tag="(0008,03F0)",
        group="0008",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_0008_03F0_Keyword",
        name="DICOM Standard Attribute (0008,03F0) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03F6)": DicomTagDefinition(
        tag="(0008,03F6)",
        group="0008",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_0008_03F6_Keyword",
        name="DICOM Standard Attribute (0008,03F6) for Identifying Information Specification",
        retired=False
    ),
    "(0008,03FC)": DicomTagDefinition(
        tag="(0008,03FC)",
        group="0008",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_0008_03FC_Keyword",
        name="DICOM Standard Attribute (0008,03FC) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0402)": DicomTagDefinition(
        tag="(0008,0402)",
        group="0008",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_0008_0402_Keyword",
        name="DICOM Standard Attribute (0008,0402) for Identifying Information Specification",
        retired=True
    ),
    "(0008,0408)": DicomTagDefinition(
        tag="(0008,0408)",
        group="0008",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_0008_0408_Keyword",
        name="DICOM Standard Attribute (0008,0408) for Identifying Information Specification",
        retired=False
    ),
    "(0008,040E)": DicomTagDefinition(
        tag="(0008,040E)",
        group="0008",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_0008_040E_Keyword",
        name="DICOM Standard Attribute (0008,040E) for Identifying Information Specification",
        retired=False
    ),
    "(0008,0414)": DicomTagDefinition(
        tag="(0008,0414)",
        group="0008",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_0008_0414_Keyword",
        name="DICOM Standard Attribute (0008,0414) for Identifying Information Specification",
        retired=False
    ),
    # ========================================================
    # Section Group (0010): Patient Information
    # ========================================================
    "(0010,0006)": DicomTagDefinition(
        tag="(0010,0006)",
        group="0010",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_0010_0006_Keyword",
        name="DICOM Standard Attribute (0010,0006) for Patient Information Specification",
        retired=False
    ),
    "(0010,000C)": DicomTagDefinition(
        tag="(0010,000C)",
        group="0010",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_0010_000C_Keyword",
        name="DICOM Standard Attribute (0010,000C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0012)": DicomTagDefinition(
        tag="(0010,0012)",
        group="0010",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_0010_0012_Keyword",
        name="DICOM Standard Attribute (0010,0012) for Patient Information Specification",
        retired=False
    ),
    "(0010,0018)": DicomTagDefinition(
        tag="(0010,0018)",
        group="0010",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_0010_0018_Keyword",
        name="DICOM Standard Attribute (0010,0018) for Patient Information Specification",
        retired=False
    ),
    "(0010,001E)": DicomTagDefinition(
        tag="(0010,001E)",
        group="0010",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_0010_001E_Keyword",
        name="DICOM Standard Attribute (0010,001E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0024)": DicomTagDefinition(
        tag="(0010,0024)",
        group="0010",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_0010_0024_Keyword",
        name="DICOM Standard Attribute (0010,0024) for Patient Information Specification",
        retired=False
    ),
    "(0010,002A)": DicomTagDefinition(
        tag="(0010,002A)",
        group="0010",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_0010_002A_Keyword",
        name="DICOM Standard Attribute (0010,002A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0030)": DicomTagDefinition(
        tag="(0010,0030)",
        group="0010",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_0010_0030_Keyword",
        name="DICOM Standard Attribute (0010,0030) for Patient Information Specification",
        retired=False
    ),
    "(0010,0036)": DicomTagDefinition(
        tag="(0010,0036)",
        group="0010",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_0010_0036_Keyword",
        name="DICOM Standard Attribute (0010,0036) for Patient Information Specification",
        retired=False
    ),
    "(0010,003C)": DicomTagDefinition(
        tag="(0010,003C)",
        group="0010",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_0010_003C_Keyword",
        name="DICOM Standard Attribute (0010,003C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0042)": DicomTagDefinition(
        tag="(0010,0042)",
        group="0010",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_0010_0042_Keyword",
        name="DICOM Standard Attribute (0010,0042) for Patient Information Specification",
        retired=False
    ),
    "(0010,0048)": DicomTagDefinition(
        tag="(0010,0048)",
        group="0010",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_0010_0048_Keyword",
        name="DICOM Standard Attribute (0010,0048) for Patient Information Specification",
        retired=False
    ),
    "(0010,004E)": DicomTagDefinition(
        tag="(0010,004E)",
        group="0010",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_0010_004E_Keyword",
        name="DICOM Standard Attribute (0010,004E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0054)": DicomTagDefinition(
        tag="(0010,0054)",
        group="0010",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_0010_0054_Keyword",
        name="DICOM Standard Attribute (0010,0054) for Patient Information Specification",
        retired=False
    ),
    "(0010,005A)": DicomTagDefinition(
        tag="(0010,005A)",
        group="0010",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_0010_005A_Keyword",
        name="DICOM Standard Attribute (0010,005A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0060)": DicomTagDefinition(
        tag="(0010,0060)",
        group="0010",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_0010_0060_Keyword",
        name="DICOM Standard Attribute (0010,0060) for Patient Information Specification",
        retired=False
    ),
    "(0010,0066)": DicomTagDefinition(
        tag="(0010,0066)",
        group="0010",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_0010_0066_Keyword",
        name="DICOM Standard Attribute (0010,0066) for Patient Information Specification",
        retired=False
    ),
    "(0010,006C)": DicomTagDefinition(
        tag="(0010,006C)",
        group="0010",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_0010_006C_Keyword",
        name="DICOM Standard Attribute (0010,006C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0072)": DicomTagDefinition(
        tag="(0010,0072)",
        group="0010",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_0010_0072_Keyword",
        name="DICOM Standard Attribute (0010,0072) for Patient Information Specification",
        retired=True
    ),
    "(0010,0078)": DicomTagDefinition(
        tag="(0010,0078)",
        group="0010",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_0010_0078_Keyword",
        name="DICOM Standard Attribute (0010,0078) for Patient Information Specification",
        retired=False
    ),
    "(0010,007E)": DicomTagDefinition(
        tag="(0010,007E)",
        group="0010",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_0010_007E_Keyword",
        name="DICOM Standard Attribute (0010,007E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0084)": DicomTagDefinition(
        tag="(0010,0084)",
        group="0010",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_0010_0084_Keyword",
        name="DICOM Standard Attribute (0010,0084) for Patient Information Specification",
        retired=False
    ),
    "(0010,008A)": DicomTagDefinition(
        tag="(0010,008A)",
        group="0010",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_0010_008A_Keyword",
        name="DICOM Standard Attribute (0010,008A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0090)": DicomTagDefinition(
        tag="(0010,0090)",
        group="0010",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_0010_0090_Keyword",
        name="DICOM Standard Attribute (0010,0090) for Patient Information Specification",
        retired=False
    ),
    "(0010,0096)": DicomTagDefinition(
        tag="(0010,0096)",
        group="0010",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_0010_0096_Keyword",
        name="DICOM Standard Attribute (0010,0096) for Patient Information Specification",
        retired=False
    ),
    "(0010,009C)": DicomTagDefinition(
        tag="(0010,009C)",
        group="0010",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_0010_009C_Keyword",
        name="DICOM Standard Attribute (0010,009C) for Patient Information Specification",
        retired=False
    ),
    "(0010,00A2)": DicomTagDefinition(
        tag="(0010,00A2)",
        group="0010",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_0010_00A2_Keyword",
        name="DICOM Standard Attribute (0010,00A2) for Patient Information Specification",
        retired=False
    ),
    "(0010,00A8)": DicomTagDefinition(
        tag="(0010,00A8)",
        group="0010",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_0010_00A8_Keyword",
        name="DICOM Standard Attribute (0010,00A8) for Patient Information Specification",
        retired=False
    ),
    "(0010,00AE)": DicomTagDefinition(
        tag="(0010,00AE)",
        group="0010",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_0010_00AE_Keyword",
        name="DICOM Standard Attribute (0010,00AE) for Patient Information Specification",
        retired=False
    ),
    "(0010,00B4)": DicomTagDefinition(
        tag="(0010,00B4)",
        group="0010",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_0010_00B4_Keyword",
        name="DICOM Standard Attribute (0010,00B4) for Patient Information Specification",
        retired=False
    ),
    "(0010,00BA)": DicomTagDefinition(
        tag="(0010,00BA)",
        group="0010",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0010_00BA_Keyword",
        name="DICOM Standard Attribute (0010,00BA) for Patient Information Specification",
        retired=False
    ),
    "(0010,00C0)": DicomTagDefinition(
        tag="(0010,00C0)",
        group="0010",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_0010_00C0_Keyword",
        name="DICOM Standard Attribute (0010,00C0) for Patient Information Specification",
        retired=False
    ),
    "(0010,00C6)": DicomTagDefinition(
        tag="(0010,00C6)",
        group="0010",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_0010_00C6_Keyword",
        name="DICOM Standard Attribute (0010,00C6) for Patient Information Specification",
        retired=False
    ),
    "(0010,00CC)": DicomTagDefinition(
        tag="(0010,00CC)",
        group="0010",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_0010_00CC_Keyword",
        name="DICOM Standard Attribute (0010,00CC) for Patient Information Specification",
        retired=False
    ),
    "(0010,00D2)": DicomTagDefinition(
        tag="(0010,00D2)",
        group="0010",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_0010_00D2_Keyword",
        name="DICOM Standard Attribute (0010,00D2) for Patient Information Specification",
        retired=False
    ),
    "(0010,00D8)": DicomTagDefinition(
        tag="(0010,00D8)",
        group="0010",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_0010_00D8_Keyword",
        name="DICOM Standard Attribute (0010,00D8) for Patient Information Specification",
        retired=False
    ),
    "(0010,00DE)": DicomTagDefinition(
        tag="(0010,00DE)",
        group="0010",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_0010_00DE_Keyword",
        name="DICOM Standard Attribute (0010,00DE) for Patient Information Specification",
        retired=False
    ),
    "(0010,00E4)": DicomTagDefinition(
        tag="(0010,00E4)",
        group="0010",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_0010_00E4_Keyword",
        name="DICOM Standard Attribute (0010,00E4) for Patient Information Specification",
        retired=True
    ),
    "(0010,00EA)": DicomTagDefinition(
        tag="(0010,00EA)",
        group="0010",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_0010_00EA_Keyword",
        name="DICOM Standard Attribute (0010,00EA) for Patient Information Specification",
        retired=False
    ),
    "(0010,00F0)": DicomTagDefinition(
        tag="(0010,00F0)",
        group="0010",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_0010_00F0_Keyword",
        name="DICOM Standard Attribute (0010,00F0) for Patient Information Specification",
        retired=False
    ),
    "(0010,00F6)": DicomTagDefinition(
        tag="(0010,00F6)",
        group="0010",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_0010_00F6_Keyword",
        name="DICOM Standard Attribute (0010,00F6) for Patient Information Specification",
        retired=False
    ),
    "(0010,00FC)": DicomTagDefinition(
        tag="(0010,00FC)",
        group="0010",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_0010_00FC_Keyword",
        name="DICOM Standard Attribute (0010,00FC) for Patient Information Specification",
        retired=False
    ),
    "(0010,0102)": DicomTagDefinition(
        tag="(0010,0102)",
        group="0010",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_0010_0102_Keyword",
        name="DICOM Standard Attribute (0010,0102) for Patient Information Specification",
        retired=False
    ),
    "(0010,0108)": DicomTagDefinition(
        tag="(0010,0108)",
        group="0010",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_0010_0108_Keyword",
        name="DICOM Standard Attribute (0010,0108) for Patient Information Specification",
        retired=False
    ),
    "(0010,010E)": DicomTagDefinition(
        tag="(0010,010E)",
        group="0010",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_0010_010E_Keyword",
        name="DICOM Standard Attribute (0010,010E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0114)": DicomTagDefinition(
        tag="(0010,0114)",
        group="0010",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_0010_0114_Keyword",
        name="DICOM Standard Attribute (0010,0114) for Patient Information Specification",
        retired=False
    ),
    "(0010,011A)": DicomTagDefinition(
        tag="(0010,011A)",
        group="0010",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_0010_011A_Keyword",
        name="DICOM Standard Attribute (0010,011A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0120)": DicomTagDefinition(
        tag="(0010,0120)",
        group="0010",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_0010_0120_Keyword",
        name="DICOM Standard Attribute (0010,0120) for Patient Information Specification",
        retired=False
    ),
    "(0010,0126)": DicomTagDefinition(
        tag="(0010,0126)",
        group="0010",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_0010_0126_Keyword",
        name="DICOM Standard Attribute (0010,0126) for Patient Information Specification",
        retired=False
    ),
    "(0010,012C)": DicomTagDefinition(
        tag="(0010,012C)",
        group="0010",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_0010_012C_Keyword",
        name="DICOM Standard Attribute (0010,012C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0132)": DicomTagDefinition(
        tag="(0010,0132)",
        group="0010",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_0010_0132_Keyword",
        name="DICOM Standard Attribute (0010,0132) for Patient Information Specification",
        retired=False
    ),
    "(0010,0138)": DicomTagDefinition(
        tag="(0010,0138)",
        group="0010",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_0010_0138_Keyword",
        name="DICOM Standard Attribute (0010,0138) for Patient Information Specification",
        retired=False
    ),
    "(0010,013E)": DicomTagDefinition(
        tag="(0010,013E)",
        group="0010",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_0010_013E_Keyword",
        name="DICOM Standard Attribute (0010,013E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0144)": DicomTagDefinition(
        tag="(0010,0144)",
        group="0010",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_0010_0144_Keyword",
        name="DICOM Standard Attribute (0010,0144) for Patient Information Specification",
        retired=False
    ),
    "(0010,014A)": DicomTagDefinition(
        tag="(0010,014A)",
        group="0010",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_0010_014A_Keyword",
        name="DICOM Standard Attribute (0010,014A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0150)": DicomTagDefinition(
        tag="(0010,0150)",
        group="0010",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_0010_0150_Keyword",
        name="DICOM Standard Attribute (0010,0150) for Patient Information Specification",
        retired=False
    ),
    "(0010,0156)": DicomTagDefinition(
        tag="(0010,0156)",
        group="0010",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_0010_0156_Keyword",
        name="DICOM Standard Attribute (0010,0156) for Patient Information Specification",
        retired=True
    ),
    "(0010,015C)": DicomTagDefinition(
        tag="(0010,015C)",
        group="0010",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_0010_015C_Keyword",
        name="DICOM Standard Attribute (0010,015C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0162)": DicomTagDefinition(
        tag="(0010,0162)",
        group="0010",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_0010_0162_Keyword",
        name="DICOM Standard Attribute (0010,0162) for Patient Information Specification",
        retired=False
    ),
    "(0010,0168)": DicomTagDefinition(
        tag="(0010,0168)",
        group="0010",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_0010_0168_Keyword",
        name="DICOM Standard Attribute (0010,0168) for Patient Information Specification",
        retired=False
    ),
    "(0010,016E)": DicomTagDefinition(
        tag="(0010,016E)",
        group="0010",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_0010_016E_Keyword",
        name="DICOM Standard Attribute (0010,016E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0174)": DicomTagDefinition(
        tag="(0010,0174)",
        group="0010",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_0010_0174_Keyword",
        name="DICOM Standard Attribute (0010,0174) for Patient Information Specification",
        retired=False
    ),
    "(0010,017A)": DicomTagDefinition(
        tag="(0010,017A)",
        group="0010",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_0010_017A_Keyword",
        name="DICOM Standard Attribute (0010,017A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0180)": DicomTagDefinition(
        tag="(0010,0180)",
        group="0010",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_0010_0180_Keyword",
        name="DICOM Standard Attribute (0010,0180) for Patient Information Specification",
        retired=False
    ),
    "(0010,0186)": DicomTagDefinition(
        tag="(0010,0186)",
        group="0010",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_0010_0186_Keyword",
        name="DICOM Standard Attribute (0010,0186) for Patient Information Specification",
        retired=False
    ),
    "(0010,018C)": DicomTagDefinition(
        tag="(0010,018C)",
        group="0010",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_0010_018C_Keyword",
        name="DICOM Standard Attribute (0010,018C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0192)": DicomTagDefinition(
        tag="(0010,0192)",
        group="0010",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_0010_0192_Keyword",
        name="DICOM Standard Attribute (0010,0192) for Patient Information Specification",
        retired=False
    ),
    "(0010,0198)": DicomTagDefinition(
        tag="(0010,0198)",
        group="0010",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_0010_0198_Keyword",
        name="DICOM Standard Attribute (0010,0198) for Patient Information Specification",
        retired=False
    ),
    "(0010,019E)": DicomTagDefinition(
        tag="(0010,019E)",
        group="0010",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_0010_019E_Keyword",
        name="DICOM Standard Attribute (0010,019E) for Patient Information Specification",
        retired=False
    ),
    "(0010,01A4)": DicomTagDefinition(
        tag="(0010,01A4)",
        group="0010",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_0010_01A4_Keyword",
        name="DICOM Standard Attribute (0010,01A4) for Patient Information Specification",
        retired=False
    ),
    "(0010,01AA)": DicomTagDefinition(
        tag="(0010,01AA)",
        group="0010",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_0010_01AA_Keyword",
        name="DICOM Standard Attribute (0010,01AA) for Patient Information Specification",
        retired=False
    ),
    "(0010,01B0)": DicomTagDefinition(
        tag="(0010,01B0)",
        group="0010",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_0010_01B0_Keyword",
        name="DICOM Standard Attribute (0010,01B0) for Patient Information Specification",
        retired=False
    ),
    "(0010,01B6)": DicomTagDefinition(
        tag="(0010,01B6)",
        group="0010",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_0010_01B6_Keyword",
        name="DICOM Standard Attribute (0010,01B6) for Patient Information Specification",
        retired=False
    ),
    "(0010,01BC)": DicomTagDefinition(
        tag="(0010,01BC)",
        group="0010",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_0010_01BC_Keyword",
        name="DICOM Standard Attribute (0010,01BC) for Patient Information Specification",
        retired=False
    ),
    "(0010,01C2)": DicomTagDefinition(
        tag="(0010,01C2)",
        group="0010",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_0010_01C2_Keyword",
        name="DICOM Standard Attribute (0010,01C2) for Patient Information Specification",
        retired=False
    ),
    "(0010,01C8)": DicomTagDefinition(
        tag="(0010,01C8)",
        group="0010",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_0010_01C8_Keyword",
        name="DICOM Standard Attribute (0010,01C8) for Patient Information Specification",
        retired=True
    ),
    "(0010,01CE)": DicomTagDefinition(
        tag="(0010,01CE)",
        group="0010",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_0010_01CE_Keyword",
        name="DICOM Standard Attribute (0010,01CE) for Patient Information Specification",
        retired=False
    ),
    "(0010,01D4)": DicomTagDefinition(
        tag="(0010,01D4)",
        group="0010",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_0010_01D4_Keyword",
        name="DICOM Standard Attribute (0010,01D4) for Patient Information Specification",
        retired=False
    ),
    "(0010,01DA)": DicomTagDefinition(
        tag="(0010,01DA)",
        group="0010",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_0010_01DA_Keyword",
        name="DICOM Standard Attribute (0010,01DA) for Patient Information Specification",
        retired=False
    ),
    "(0010,01E0)": DicomTagDefinition(
        tag="(0010,01E0)",
        group="0010",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_0010_01E0_Keyword",
        name="DICOM Standard Attribute (0010,01E0) for Patient Information Specification",
        retired=False
    ),
    "(0010,01E6)": DicomTagDefinition(
        tag="(0010,01E6)",
        group="0010",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_0010_01E6_Keyword",
        name="DICOM Standard Attribute (0010,01E6) for Patient Information Specification",
        retired=False
    ),
    "(0010,01EC)": DicomTagDefinition(
        tag="(0010,01EC)",
        group="0010",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_0010_01EC_Keyword",
        name="DICOM Standard Attribute (0010,01EC) for Patient Information Specification",
        retired=False
    ),
    "(0010,01F2)": DicomTagDefinition(
        tag="(0010,01F2)",
        group="0010",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_0010_01F2_Keyword",
        name="DICOM Standard Attribute (0010,01F2) for Patient Information Specification",
        retired=False
    ),
    "(0010,01F8)": DicomTagDefinition(
        tag="(0010,01F8)",
        group="0010",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_0010_01F8_Keyword",
        name="DICOM Standard Attribute (0010,01F8) for Patient Information Specification",
        retired=False
    ),
    "(0010,01FE)": DicomTagDefinition(
        tag="(0010,01FE)",
        group="0010",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_0010_01FE_Keyword",
        name="DICOM Standard Attribute (0010,01FE) for Patient Information Specification",
        retired=False
    ),
    "(0010,0204)": DicomTagDefinition(
        tag="(0010,0204)",
        group="0010",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0010_0204_Keyword",
        name="DICOM Standard Attribute (0010,0204) for Patient Information Specification",
        retired=False
    ),
    "(0010,020A)": DicomTagDefinition(
        tag="(0010,020A)",
        group="0010",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_0010_020A_Keyword",
        name="DICOM Standard Attribute (0010,020A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0210)": DicomTagDefinition(
        tag="(0010,0210)",
        group="0010",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_0010_0210_Keyword",
        name="DICOM Standard Attribute (0010,0210) for Patient Information Specification",
        retired=False
    ),
    "(0010,0216)": DicomTagDefinition(
        tag="(0010,0216)",
        group="0010",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_0010_0216_Keyword",
        name="DICOM Standard Attribute (0010,0216) for Patient Information Specification",
        retired=False
    ),
    "(0010,021C)": DicomTagDefinition(
        tag="(0010,021C)",
        group="0010",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_0010_021C_Keyword",
        name="DICOM Standard Attribute (0010,021C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0222)": DicomTagDefinition(
        tag="(0010,0222)",
        group="0010",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_0010_0222_Keyword",
        name="DICOM Standard Attribute (0010,0222) for Patient Information Specification",
        retired=False
    ),
    "(0010,0228)": DicomTagDefinition(
        tag="(0010,0228)",
        group="0010",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_0010_0228_Keyword",
        name="DICOM Standard Attribute (0010,0228) for Patient Information Specification",
        retired=False
    ),
    "(0010,022E)": DicomTagDefinition(
        tag="(0010,022E)",
        group="0010",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_0010_022E_Keyword",
        name="DICOM Standard Attribute (0010,022E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0234)": DicomTagDefinition(
        tag="(0010,0234)",
        group="0010",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_0010_0234_Keyword",
        name="DICOM Standard Attribute (0010,0234) for Patient Information Specification",
        retired=False
    ),
    "(0010,023A)": DicomTagDefinition(
        tag="(0010,023A)",
        group="0010",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_0010_023A_Keyword",
        name="DICOM Standard Attribute (0010,023A) for Patient Information Specification",
        retired=True
    ),
    "(0010,0240)": DicomTagDefinition(
        tag="(0010,0240)",
        group="0010",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_0010_0240_Keyword",
        name="DICOM Standard Attribute (0010,0240) for Patient Information Specification",
        retired=False
    ),
    "(0010,0246)": DicomTagDefinition(
        tag="(0010,0246)",
        group="0010",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_0010_0246_Keyword",
        name="DICOM Standard Attribute (0010,0246) for Patient Information Specification",
        retired=False
    ),
    "(0010,024C)": DicomTagDefinition(
        tag="(0010,024C)",
        group="0010",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_0010_024C_Keyword",
        name="DICOM Standard Attribute (0010,024C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0252)": DicomTagDefinition(
        tag="(0010,0252)",
        group="0010",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_0010_0252_Keyword",
        name="DICOM Standard Attribute (0010,0252) for Patient Information Specification",
        retired=False
    ),
    "(0010,0258)": DicomTagDefinition(
        tag="(0010,0258)",
        group="0010",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_0010_0258_Keyword",
        name="DICOM Standard Attribute (0010,0258) for Patient Information Specification",
        retired=False
    ),
    "(0010,025E)": DicomTagDefinition(
        tag="(0010,025E)",
        group="0010",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_0010_025E_Keyword",
        name="DICOM Standard Attribute (0010,025E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0264)": DicomTagDefinition(
        tag="(0010,0264)",
        group="0010",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_0010_0264_Keyword",
        name="DICOM Standard Attribute (0010,0264) for Patient Information Specification",
        retired=False
    ),
    "(0010,026A)": DicomTagDefinition(
        tag="(0010,026A)",
        group="0010",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_0010_026A_Keyword",
        name="DICOM Standard Attribute (0010,026A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0270)": DicomTagDefinition(
        tag="(0010,0270)",
        group="0010",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_0010_0270_Keyword",
        name="DICOM Standard Attribute (0010,0270) for Patient Information Specification",
        retired=False
    ),
    "(0010,0276)": DicomTagDefinition(
        tag="(0010,0276)",
        group="0010",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_0010_0276_Keyword",
        name="DICOM Standard Attribute (0010,0276) for Patient Information Specification",
        retired=False
    ),
    "(0010,027C)": DicomTagDefinition(
        tag="(0010,027C)",
        group="0010",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_0010_027C_Keyword",
        name="DICOM Standard Attribute (0010,027C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0282)": DicomTagDefinition(
        tag="(0010,0282)",
        group="0010",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_0010_0282_Keyword",
        name="DICOM Standard Attribute (0010,0282) for Patient Information Specification",
        retired=False
    ),
    "(0010,0288)": DicomTagDefinition(
        tag="(0010,0288)",
        group="0010",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_0010_0288_Keyword",
        name="DICOM Standard Attribute (0010,0288) for Patient Information Specification",
        retired=False
    ),
    "(0010,028E)": DicomTagDefinition(
        tag="(0010,028E)",
        group="0010",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_0010_028E_Keyword",
        name="DICOM Standard Attribute (0010,028E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0294)": DicomTagDefinition(
        tag="(0010,0294)",
        group="0010",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_0010_0294_Keyword",
        name="DICOM Standard Attribute (0010,0294) for Patient Information Specification",
        retired=False
    ),
    "(0010,029A)": DicomTagDefinition(
        tag="(0010,029A)",
        group="0010",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_0010_029A_Keyword",
        name="DICOM Standard Attribute (0010,029A) for Patient Information Specification",
        retired=False
    ),
    "(0010,02A0)": DicomTagDefinition(
        tag="(0010,02A0)",
        group="0010",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_0010_02A0_Keyword",
        name="DICOM Standard Attribute (0010,02A0) for Patient Information Specification",
        retired=False
    ),
    "(0010,02A6)": DicomTagDefinition(
        tag="(0010,02A6)",
        group="0010",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_0010_02A6_Keyword",
        name="DICOM Standard Attribute (0010,02A6) for Patient Information Specification",
        retired=False
    ),
    "(0010,02AC)": DicomTagDefinition(
        tag="(0010,02AC)",
        group="0010",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_0010_02AC_Keyword",
        name="DICOM Standard Attribute (0010,02AC) for Patient Information Specification",
        retired=True
    ),
    "(0010,02B2)": DicomTagDefinition(
        tag="(0010,02B2)",
        group="0010",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_0010_02B2_Keyword",
        name="DICOM Standard Attribute (0010,02B2) for Patient Information Specification",
        retired=False
    ),
    "(0010,02B8)": DicomTagDefinition(
        tag="(0010,02B8)",
        group="0010",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_0010_02B8_Keyword",
        name="DICOM Standard Attribute (0010,02B8) for Patient Information Specification",
        retired=False
    ),
    "(0010,02BE)": DicomTagDefinition(
        tag="(0010,02BE)",
        group="0010",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_0010_02BE_Keyword",
        name="DICOM Standard Attribute (0010,02BE) for Patient Information Specification",
        retired=False
    ),
    "(0010,02C4)": DicomTagDefinition(
        tag="(0010,02C4)",
        group="0010",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_0010_02C4_Keyword",
        name="DICOM Standard Attribute (0010,02C4) for Patient Information Specification",
        retired=False
    ),
    "(0010,02CA)": DicomTagDefinition(
        tag="(0010,02CA)",
        group="0010",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_0010_02CA_Keyword",
        name="DICOM Standard Attribute (0010,02CA) for Patient Information Specification",
        retired=False
    ),
    "(0010,02D0)": DicomTagDefinition(
        tag="(0010,02D0)",
        group="0010",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_0010_02D0_Keyword",
        name="DICOM Standard Attribute (0010,02D0) for Patient Information Specification",
        retired=False
    ),
    "(0010,02D6)": DicomTagDefinition(
        tag="(0010,02D6)",
        group="0010",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_0010_02D6_Keyword",
        name="DICOM Standard Attribute (0010,02D6) for Patient Information Specification",
        retired=False
    ),
    "(0010,02DC)": DicomTagDefinition(
        tag="(0010,02DC)",
        group="0010",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_0010_02DC_Keyword",
        name="DICOM Standard Attribute (0010,02DC) for Patient Information Specification",
        retired=False
    ),
    "(0010,02E2)": DicomTagDefinition(
        tag="(0010,02E2)",
        group="0010",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_0010_02E2_Keyword",
        name="DICOM Standard Attribute (0010,02E2) for Patient Information Specification",
        retired=False
    ),
    "(0010,02E8)": DicomTagDefinition(
        tag="(0010,02E8)",
        group="0010",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_0010_02E8_Keyword",
        name="DICOM Standard Attribute (0010,02E8) for Patient Information Specification",
        retired=False
    ),
    "(0010,02EE)": DicomTagDefinition(
        tag="(0010,02EE)",
        group="0010",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_0010_02EE_Keyword",
        name="DICOM Standard Attribute (0010,02EE) for Patient Information Specification",
        retired=False
    ),
    "(0010,02F4)": DicomTagDefinition(
        tag="(0010,02F4)",
        group="0010",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_0010_02F4_Keyword",
        name="DICOM Standard Attribute (0010,02F4) for Patient Information Specification",
        retired=False
    ),
    "(0010,02FA)": DicomTagDefinition(
        tag="(0010,02FA)",
        group="0010",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_0010_02FA_Keyword",
        name="DICOM Standard Attribute (0010,02FA) for Patient Information Specification",
        retired=False
    ),
    "(0010,0300)": DicomTagDefinition(
        tag="(0010,0300)",
        group="0010",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_0010_0300_Keyword",
        name="DICOM Standard Attribute (0010,0300) for Patient Information Specification",
        retired=False
    ),
    "(0010,0306)": DicomTagDefinition(
        tag="(0010,0306)",
        group="0010",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_0010_0306_Keyword",
        name="DICOM Standard Attribute (0010,0306) for Patient Information Specification",
        retired=False
    ),
    "(0010,030C)": DicomTagDefinition(
        tag="(0010,030C)",
        group="0010",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_0010_030C_Keyword",
        name="DICOM Standard Attribute (0010,030C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0312)": DicomTagDefinition(
        tag="(0010,0312)",
        group="0010",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_0010_0312_Keyword",
        name="DICOM Standard Attribute (0010,0312) for Patient Information Specification",
        retired=False
    ),
    "(0010,0318)": DicomTagDefinition(
        tag="(0010,0318)",
        group="0010",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_0010_0318_Keyword",
        name="DICOM Standard Attribute (0010,0318) for Patient Information Specification",
        retired=False
    ),
    "(0010,031E)": DicomTagDefinition(
        tag="(0010,031E)",
        group="0010",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_0010_031E_Keyword",
        name="DICOM Standard Attribute (0010,031E) for Patient Information Specification",
        retired=True
    ),
    "(0010,0324)": DicomTagDefinition(
        tag="(0010,0324)",
        group="0010",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_0010_0324_Keyword",
        name="DICOM Standard Attribute (0010,0324) for Patient Information Specification",
        retired=False
    ),
    "(0010,032A)": DicomTagDefinition(
        tag="(0010,032A)",
        group="0010",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_0010_032A_Keyword",
        name="DICOM Standard Attribute (0010,032A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0330)": DicomTagDefinition(
        tag="(0010,0330)",
        group="0010",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_0010_0330_Keyword",
        name="DICOM Standard Attribute (0010,0330) for Patient Information Specification",
        retired=False
    ),
    "(0010,0336)": DicomTagDefinition(
        tag="(0010,0336)",
        group="0010",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_0010_0336_Keyword",
        name="DICOM Standard Attribute (0010,0336) for Patient Information Specification",
        retired=False
    ),
    "(0010,033C)": DicomTagDefinition(
        tag="(0010,033C)",
        group="0010",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_0010_033C_Keyword",
        name="DICOM Standard Attribute (0010,033C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0342)": DicomTagDefinition(
        tag="(0010,0342)",
        group="0010",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_0010_0342_Keyword",
        name="DICOM Standard Attribute (0010,0342) for Patient Information Specification",
        retired=False
    ),
    "(0010,0348)": DicomTagDefinition(
        tag="(0010,0348)",
        group="0010",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_0010_0348_Keyword",
        name="DICOM Standard Attribute (0010,0348) for Patient Information Specification",
        retired=False
    ),
    "(0010,034E)": DicomTagDefinition(
        tag="(0010,034E)",
        group="0010",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0010_034E_Keyword",
        name="DICOM Standard Attribute (0010,034E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0354)": DicomTagDefinition(
        tag="(0010,0354)",
        group="0010",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_0010_0354_Keyword",
        name="DICOM Standard Attribute (0010,0354) for Patient Information Specification",
        retired=False
    ),
    "(0010,035A)": DicomTagDefinition(
        tag="(0010,035A)",
        group="0010",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_0010_035A_Keyword",
        name="DICOM Standard Attribute (0010,035A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0360)": DicomTagDefinition(
        tag="(0010,0360)",
        group="0010",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_0010_0360_Keyword",
        name="DICOM Standard Attribute (0010,0360) for Patient Information Specification",
        retired=False
    ),
    "(0010,0366)": DicomTagDefinition(
        tag="(0010,0366)",
        group="0010",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_0010_0366_Keyword",
        name="DICOM Standard Attribute (0010,0366) for Patient Information Specification",
        retired=False
    ),
    "(0010,036C)": DicomTagDefinition(
        tag="(0010,036C)",
        group="0010",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_0010_036C_Keyword",
        name="DICOM Standard Attribute (0010,036C) for Patient Information Specification",
        retired=False
    ),
    "(0010,0372)": DicomTagDefinition(
        tag="(0010,0372)",
        group="0010",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_0010_0372_Keyword",
        name="DICOM Standard Attribute (0010,0372) for Patient Information Specification",
        retired=False
    ),
    "(0010,0378)": DicomTagDefinition(
        tag="(0010,0378)",
        group="0010",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_0010_0378_Keyword",
        name="DICOM Standard Attribute (0010,0378) for Patient Information Specification",
        retired=False
    ),
    "(0010,037E)": DicomTagDefinition(
        tag="(0010,037E)",
        group="0010",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_0010_037E_Keyword",
        name="DICOM Standard Attribute (0010,037E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0384)": DicomTagDefinition(
        tag="(0010,0384)",
        group="0010",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_0010_0384_Keyword",
        name="DICOM Standard Attribute (0010,0384) for Patient Information Specification",
        retired=False
    ),
    "(0010,038A)": DicomTagDefinition(
        tag="(0010,038A)",
        group="0010",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_0010_038A_Keyword",
        name="DICOM Standard Attribute (0010,038A) for Patient Information Specification",
        retired=False
    ),
    "(0010,0390)": DicomTagDefinition(
        tag="(0010,0390)",
        group="0010",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_0010_0390_Keyword",
        name="DICOM Standard Attribute (0010,0390) for Patient Information Specification",
        retired=True
    ),
    "(0010,0396)": DicomTagDefinition(
        tag="(0010,0396)",
        group="0010",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_0010_0396_Keyword",
        name="DICOM Standard Attribute (0010,0396) for Patient Information Specification",
        retired=False
    ),
    "(0010,039C)": DicomTagDefinition(
        tag="(0010,039C)",
        group="0010",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_0010_039C_Keyword",
        name="DICOM Standard Attribute (0010,039C) for Patient Information Specification",
        retired=False
    ),
    "(0010,03A2)": DicomTagDefinition(
        tag="(0010,03A2)",
        group="0010",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_0010_03A2_Keyword",
        name="DICOM Standard Attribute (0010,03A2) for Patient Information Specification",
        retired=False
    ),
    "(0010,03A8)": DicomTagDefinition(
        tag="(0010,03A8)",
        group="0010",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_0010_03A8_Keyword",
        name="DICOM Standard Attribute (0010,03A8) for Patient Information Specification",
        retired=False
    ),
    "(0010,03AE)": DicomTagDefinition(
        tag="(0010,03AE)",
        group="0010",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_0010_03AE_Keyword",
        name="DICOM Standard Attribute (0010,03AE) for Patient Information Specification",
        retired=False
    ),
    "(0010,03B4)": DicomTagDefinition(
        tag="(0010,03B4)",
        group="0010",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_0010_03B4_Keyword",
        name="DICOM Standard Attribute (0010,03B4) for Patient Information Specification",
        retired=False
    ),
    "(0010,03BA)": DicomTagDefinition(
        tag="(0010,03BA)",
        group="0010",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_0010_03BA_Keyword",
        name="DICOM Standard Attribute (0010,03BA) for Patient Information Specification",
        retired=False
    ),
    "(0010,03C0)": DicomTagDefinition(
        tag="(0010,03C0)",
        group="0010",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_0010_03C0_Keyword",
        name="DICOM Standard Attribute (0010,03C0) for Patient Information Specification",
        retired=False
    ),
    "(0010,03C6)": DicomTagDefinition(
        tag="(0010,03C6)",
        group="0010",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_0010_03C6_Keyword",
        name="DICOM Standard Attribute (0010,03C6) for Patient Information Specification",
        retired=False
    ),
    "(0010,03CC)": DicomTagDefinition(
        tag="(0010,03CC)",
        group="0010",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_0010_03CC_Keyword",
        name="DICOM Standard Attribute (0010,03CC) for Patient Information Specification",
        retired=False
    ),
    "(0010,03D2)": DicomTagDefinition(
        tag="(0010,03D2)",
        group="0010",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_0010_03D2_Keyword",
        name="DICOM Standard Attribute (0010,03D2) for Patient Information Specification",
        retired=False
    ),
    "(0010,03D8)": DicomTagDefinition(
        tag="(0010,03D8)",
        group="0010",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_0010_03D8_Keyword",
        name="DICOM Standard Attribute (0010,03D8) for Patient Information Specification",
        retired=False
    ),
    "(0010,03DE)": DicomTagDefinition(
        tag="(0010,03DE)",
        group="0010",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_0010_03DE_Keyword",
        name="DICOM Standard Attribute (0010,03DE) for Patient Information Specification",
        retired=False
    ),
    "(0010,03E4)": DicomTagDefinition(
        tag="(0010,03E4)",
        group="0010",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_0010_03E4_Keyword",
        name="DICOM Standard Attribute (0010,03E4) for Patient Information Specification",
        retired=False
    ),
    "(0010,03EA)": DicomTagDefinition(
        tag="(0010,03EA)",
        group="0010",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_0010_03EA_Keyword",
        name="DICOM Standard Attribute (0010,03EA) for Patient Information Specification",
        retired=False
    ),
    "(0010,03F0)": DicomTagDefinition(
        tag="(0010,03F0)",
        group="0010",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_0010_03F0_Keyword",
        name="DICOM Standard Attribute (0010,03F0) for Patient Information Specification",
        retired=False
    ),
    "(0010,03F6)": DicomTagDefinition(
        tag="(0010,03F6)",
        group="0010",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_0010_03F6_Keyword",
        name="DICOM Standard Attribute (0010,03F6) for Patient Information Specification",
        retired=False
    ),
    "(0010,03FC)": DicomTagDefinition(
        tag="(0010,03FC)",
        group="0010",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_0010_03FC_Keyword",
        name="DICOM Standard Attribute (0010,03FC) for Patient Information Specification",
        retired=False
    ),
    "(0010,0402)": DicomTagDefinition(
        tag="(0010,0402)",
        group="0010",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_0010_0402_Keyword",
        name="DICOM Standard Attribute (0010,0402) for Patient Information Specification",
        retired=True
    ),
    "(0010,0408)": DicomTagDefinition(
        tag="(0010,0408)",
        group="0010",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_0010_0408_Keyword",
        name="DICOM Standard Attribute (0010,0408) for Patient Information Specification",
        retired=False
    ),
    "(0010,040E)": DicomTagDefinition(
        tag="(0010,040E)",
        group="0010",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_0010_040E_Keyword",
        name="DICOM Standard Attribute (0010,040E) for Patient Information Specification",
        retired=False
    ),
    "(0010,0414)": DicomTagDefinition(
        tag="(0010,0414)",
        group="0010",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_0010_0414_Keyword",
        name="DICOM Standard Attribute (0010,0414) for Patient Information Specification",
        retired=False
    ),
    # ========================================================
    # Section Group (0018): Acquisition Parameters
    # ========================================================
    "(0018,0006)": DicomTagDefinition(
        tag="(0018,0006)",
        group="0018",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_0018_0006_Keyword",
        name="DICOM Standard Attribute (0018,0006) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,000C)": DicomTagDefinition(
        tag="(0018,000C)",
        group="0018",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_0018_000C_Keyword",
        name="DICOM Standard Attribute (0018,000C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0012)": DicomTagDefinition(
        tag="(0018,0012)",
        group="0018",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_0018_0012_Keyword",
        name="DICOM Standard Attribute (0018,0012) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0018)": DicomTagDefinition(
        tag="(0018,0018)",
        group="0018",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_0018_0018_Keyword",
        name="DICOM Standard Attribute (0018,0018) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,001E)": DicomTagDefinition(
        tag="(0018,001E)",
        group="0018",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_0018_001E_Keyword",
        name="DICOM Standard Attribute (0018,001E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0024)": DicomTagDefinition(
        tag="(0018,0024)",
        group="0018",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_0018_0024_Keyword",
        name="DICOM Standard Attribute (0018,0024) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,002A)": DicomTagDefinition(
        tag="(0018,002A)",
        group="0018",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_0018_002A_Keyword",
        name="DICOM Standard Attribute (0018,002A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0030)": DicomTagDefinition(
        tag="(0018,0030)",
        group="0018",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_0018_0030_Keyword",
        name="DICOM Standard Attribute (0018,0030) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0036)": DicomTagDefinition(
        tag="(0018,0036)",
        group="0018",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_0018_0036_Keyword",
        name="DICOM Standard Attribute (0018,0036) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,003C)": DicomTagDefinition(
        tag="(0018,003C)",
        group="0018",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_0018_003C_Keyword",
        name="DICOM Standard Attribute (0018,003C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0042)": DicomTagDefinition(
        tag="(0018,0042)",
        group="0018",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_0018_0042_Keyword",
        name="DICOM Standard Attribute (0018,0042) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0048)": DicomTagDefinition(
        tag="(0018,0048)",
        group="0018",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_0018_0048_Keyword",
        name="DICOM Standard Attribute (0018,0048) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,004E)": DicomTagDefinition(
        tag="(0018,004E)",
        group="0018",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_0018_004E_Keyword",
        name="DICOM Standard Attribute (0018,004E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0054)": DicomTagDefinition(
        tag="(0018,0054)",
        group="0018",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_0018_0054_Keyword",
        name="DICOM Standard Attribute (0018,0054) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,005A)": DicomTagDefinition(
        tag="(0018,005A)",
        group="0018",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_0018_005A_Keyword",
        name="DICOM Standard Attribute (0018,005A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0060)": DicomTagDefinition(
        tag="(0018,0060)",
        group="0018",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_0018_0060_Keyword",
        name="DICOM Standard Attribute (0018,0060) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0066)": DicomTagDefinition(
        tag="(0018,0066)",
        group="0018",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_0018_0066_Keyword",
        name="DICOM Standard Attribute (0018,0066) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,006C)": DicomTagDefinition(
        tag="(0018,006C)",
        group="0018",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_0018_006C_Keyword",
        name="DICOM Standard Attribute (0018,006C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0072)": DicomTagDefinition(
        tag="(0018,0072)",
        group="0018",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_0018_0072_Keyword",
        name="DICOM Standard Attribute (0018,0072) for Acquisition Parameters Specification",
        retired=True
    ),
    "(0018,0078)": DicomTagDefinition(
        tag="(0018,0078)",
        group="0018",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_0018_0078_Keyword",
        name="DICOM Standard Attribute (0018,0078) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,007E)": DicomTagDefinition(
        tag="(0018,007E)",
        group="0018",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_0018_007E_Keyword",
        name="DICOM Standard Attribute (0018,007E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0084)": DicomTagDefinition(
        tag="(0018,0084)",
        group="0018",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_0018_0084_Keyword",
        name="DICOM Standard Attribute (0018,0084) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,008A)": DicomTagDefinition(
        tag="(0018,008A)",
        group="0018",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_0018_008A_Keyword",
        name="DICOM Standard Attribute (0018,008A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0090)": DicomTagDefinition(
        tag="(0018,0090)",
        group="0018",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_0018_0090_Keyword",
        name="DICOM Standard Attribute (0018,0090) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0096)": DicomTagDefinition(
        tag="(0018,0096)",
        group="0018",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_0018_0096_Keyword",
        name="DICOM Standard Attribute (0018,0096) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,009C)": DicomTagDefinition(
        tag="(0018,009C)",
        group="0018",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_0018_009C_Keyword",
        name="DICOM Standard Attribute (0018,009C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00A2)": DicomTagDefinition(
        tag="(0018,00A2)",
        group="0018",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_0018_00A2_Keyword",
        name="DICOM Standard Attribute (0018,00A2) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00A8)": DicomTagDefinition(
        tag="(0018,00A8)",
        group="0018",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_0018_00A8_Keyword",
        name="DICOM Standard Attribute (0018,00A8) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00AE)": DicomTagDefinition(
        tag="(0018,00AE)",
        group="0018",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_0018_00AE_Keyword",
        name="DICOM Standard Attribute (0018,00AE) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00B4)": DicomTagDefinition(
        tag="(0018,00B4)",
        group="0018",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_0018_00B4_Keyword",
        name="DICOM Standard Attribute (0018,00B4) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00BA)": DicomTagDefinition(
        tag="(0018,00BA)",
        group="0018",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0018_00BA_Keyword",
        name="DICOM Standard Attribute (0018,00BA) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00C0)": DicomTagDefinition(
        tag="(0018,00C0)",
        group="0018",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_0018_00C0_Keyword",
        name="DICOM Standard Attribute (0018,00C0) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00C6)": DicomTagDefinition(
        tag="(0018,00C6)",
        group="0018",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_0018_00C6_Keyword",
        name="DICOM Standard Attribute (0018,00C6) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00CC)": DicomTagDefinition(
        tag="(0018,00CC)",
        group="0018",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_0018_00CC_Keyword",
        name="DICOM Standard Attribute (0018,00CC) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00D2)": DicomTagDefinition(
        tag="(0018,00D2)",
        group="0018",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_0018_00D2_Keyword",
        name="DICOM Standard Attribute (0018,00D2) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00D8)": DicomTagDefinition(
        tag="(0018,00D8)",
        group="0018",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_0018_00D8_Keyword",
        name="DICOM Standard Attribute (0018,00D8) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00DE)": DicomTagDefinition(
        tag="(0018,00DE)",
        group="0018",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_0018_00DE_Keyword",
        name="DICOM Standard Attribute (0018,00DE) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00E4)": DicomTagDefinition(
        tag="(0018,00E4)",
        group="0018",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_0018_00E4_Keyword",
        name="DICOM Standard Attribute (0018,00E4) for Acquisition Parameters Specification",
        retired=True
    ),
    "(0018,00EA)": DicomTagDefinition(
        tag="(0018,00EA)",
        group="0018",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_0018_00EA_Keyword",
        name="DICOM Standard Attribute (0018,00EA) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00F0)": DicomTagDefinition(
        tag="(0018,00F0)",
        group="0018",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_0018_00F0_Keyword",
        name="DICOM Standard Attribute (0018,00F0) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00F6)": DicomTagDefinition(
        tag="(0018,00F6)",
        group="0018",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_0018_00F6_Keyword",
        name="DICOM Standard Attribute (0018,00F6) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,00FC)": DicomTagDefinition(
        tag="(0018,00FC)",
        group="0018",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_0018_00FC_Keyword",
        name="DICOM Standard Attribute (0018,00FC) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0102)": DicomTagDefinition(
        tag="(0018,0102)",
        group="0018",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_0018_0102_Keyword",
        name="DICOM Standard Attribute (0018,0102) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0108)": DicomTagDefinition(
        tag="(0018,0108)",
        group="0018",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_0018_0108_Keyword",
        name="DICOM Standard Attribute (0018,0108) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,010E)": DicomTagDefinition(
        tag="(0018,010E)",
        group="0018",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_0018_010E_Keyword",
        name="DICOM Standard Attribute (0018,010E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0114)": DicomTagDefinition(
        tag="(0018,0114)",
        group="0018",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_0018_0114_Keyword",
        name="DICOM Standard Attribute (0018,0114) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,011A)": DicomTagDefinition(
        tag="(0018,011A)",
        group="0018",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_0018_011A_Keyword",
        name="DICOM Standard Attribute (0018,011A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0120)": DicomTagDefinition(
        tag="(0018,0120)",
        group="0018",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_0018_0120_Keyword",
        name="DICOM Standard Attribute (0018,0120) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0126)": DicomTagDefinition(
        tag="(0018,0126)",
        group="0018",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_0018_0126_Keyword",
        name="DICOM Standard Attribute (0018,0126) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,012C)": DicomTagDefinition(
        tag="(0018,012C)",
        group="0018",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_0018_012C_Keyword",
        name="DICOM Standard Attribute (0018,012C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0132)": DicomTagDefinition(
        tag="(0018,0132)",
        group="0018",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_0018_0132_Keyword",
        name="DICOM Standard Attribute (0018,0132) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0138)": DicomTagDefinition(
        tag="(0018,0138)",
        group="0018",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_0018_0138_Keyword",
        name="DICOM Standard Attribute (0018,0138) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,013E)": DicomTagDefinition(
        tag="(0018,013E)",
        group="0018",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_0018_013E_Keyword",
        name="DICOM Standard Attribute (0018,013E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0144)": DicomTagDefinition(
        tag="(0018,0144)",
        group="0018",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_0018_0144_Keyword",
        name="DICOM Standard Attribute (0018,0144) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,014A)": DicomTagDefinition(
        tag="(0018,014A)",
        group="0018",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_0018_014A_Keyword",
        name="DICOM Standard Attribute (0018,014A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0150)": DicomTagDefinition(
        tag="(0018,0150)",
        group="0018",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_0018_0150_Keyword",
        name="DICOM Standard Attribute (0018,0150) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0156)": DicomTagDefinition(
        tag="(0018,0156)",
        group="0018",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_0018_0156_Keyword",
        name="DICOM Standard Attribute (0018,0156) for Acquisition Parameters Specification",
        retired=True
    ),
    "(0018,015C)": DicomTagDefinition(
        tag="(0018,015C)",
        group="0018",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_0018_015C_Keyword",
        name="DICOM Standard Attribute (0018,015C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0162)": DicomTagDefinition(
        tag="(0018,0162)",
        group="0018",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_0018_0162_Keyword",
        name="DICOM Standard Attribute (0018,0162) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0168)": DicomTagDefinition(
        tag="(0018,0168)",
        group="0018",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_0018_0168_Keyword",
        name="DICOM Standard Attribute (0018,0168) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,016E)": DicomTagDefinition(
        tag="(0018,016E)",
        group="0018",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_0018_016E_Keyword",
        name="DICOM Standard Attribute (0018,016E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0174)": DicomTagDefinition(
        tag="(0018,0174)",
        group="0018",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_0018_0174_Keyword",
        name="DICOM Standard Attribute (0018,0174) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,017A)": DicomTagDefinition(
        tag="(0018,017A)",
        group="0018",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_0018_017A_Keyword",
        name="DICOM Standard Attribute (0018,017A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0180)": DicomTagDefinition(
        tag="(0018,0180)",
        group="0018",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_0018_0180_Keyword",
        name="DICOM Standard Attribute (0018,0180) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0186)": DicomTagDefinition(
        tag="(0018,0186)",
        group="0018",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_0018_0186_Keyword",
        name="DICOM Standard Attribute (0018,0186) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,018C)": DicomTagDefinition(
        tag="(0018,018C)",
        group="0018",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_0018_018C_Keyword",
        name="DICOM Standard Attribute (0018,018C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0192)": DicomTagDefinition(
        tag="(0018,0192)",
        group="0018",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_0018_0192_Keyword",
        name="DICOM Standard Attribute (0018,0192) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0198)": DicomTagDefinition(
        tag="(0018,0198)",
        group="0018",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_0018_0198_Keyword",
        name="DICOM Standard Attribute (0018,0198) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,019E)": DicomTagDefinition(
        tag="(0018,019E)",
        group="0018",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_0018_019E_Keyword",
        name="DICOM Standard Attribute (0018,019E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01A4)": DicomTagDefinition(
        tag="(0018,01A4)",
        group="0018",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_0018_01A4_Keyword",
        name="DICOM Standard Attribute (0018,01A4) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01AA)": DicomTagDefinition(
        tag="(0018,01AA)",
        group="0018",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_0018_01AA_Keyword",
        name="DICOM Standard Attribute (0018,01AA) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01B0)": DicomTagDefinition(
        tag="(0018,01B0)",
        group="0018",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_0018_01B0_Keyword",
        name="DICOM Standard Attribute (0018,01B0) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01B6)": DicomTagDefinition(
        tag="(0018,01B6)",
        group="0018",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_0018_01B6_Keyword",
        name="DICOM Standard Attribute (0018,01B6) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01BC)": DicomTagDefinition(
        tag="(0018,01BC)",
        group="0018",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_0018_01BC_Keyword",
        name="DICOM Standard Attribute (0018,01BC) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01C2)": DicomTagDefinition(
        tag="(0018,01C2)",
        group="0018",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_0018_01C2_Keyword",
        name="DICOM Standard Attribute (0018,01C2) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01C8)": DicomTagDefinition(
        tag="(0018,01C8)",
        group="0018",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_0018_01C8_Keyword",
        name="DICOM Standard Attribute (0018,01C8) for Acquisition Parameters Specification",
        retired=True
    ),
    "(0018,01CE)": DicomTagDefinition(
        tag="(0018,01CE)",
        group="0018",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_0018_01CE_Keyword",
        name="DICOM Standard Attribute (0018,01CE) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01D4)": DicomTagDefinition(
        tag="(0018,01D4)",
        group="0018",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_0018_01D4_Keyword",
        name="DICOM Standard Attribute (0018,01D4) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01DA)": DicomTagDefinition(
        tag="(0018,01DA)",
        group="0018",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_0018_01DA_Keyword",
        name="DICOM Standard Attribute (0018,01DA) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01E0)": DicomTagDefinition(
        tag="(0018,01E0)",
        group="0018",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_0018_01E0_Keyword",
        name="DICOM Standard Attribute (0018,01E0) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01E6)": DicomTagDefinition(
        tag="(0018,01E6)",
        group="0018",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_0018_01E6_Keyword",
        name="DICOM Standard Attribute (0018,01E6) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01EC)": DicomTagDefinition(
        tag="(0018,01EC)",
        group="0018",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_0018_01EC_Keyword",
        name="DICOM Standard Attribute (0018,01EC) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01F2)": DicomTagDefinition(
        tag="(0018,01F2)",
        group="0018",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_0018_01F2_Keyword",
        name="DICOM Standard Attribute (0018,01F2) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01F8)": DicomTagDefinition(
        tag="(0018,01F8)",
        group="0018",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_0018_01F8_Keyword",
        name="DICOM Standard Attribute (0018,01F8) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,01FE)": DicomTagDefinition(
        tag="(0018,01FE)",
        group="0018",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_0018_01FE_Keyword",
        name="DICOM Standard Attribute (0018,01FE) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0204)": DicomTagDefinition(
        tag="(0018,0204)",
        group="0018",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0018_0204_Keyword",
        name="DICOM Standard Attribute (0018,0204) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,020A)": DicomTagDefinition(
        tag="(0018,020A)",
        group="0018",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_0018_020A_Keyword",
        name="DICOM Standard Attribute (0018,020A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0210)": DicomTagDefinition(
        tag="(0018,0210)",
        group="0018",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_0018_0210_Keyword",
        name="DICOM Standard Attribute (0018,0210) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0216)": DicomTagDefinition(
        tag="(0018,0216)",
        group="0018",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_0018_0216_Keyword",
        name="DICOM Standard Attribute (0018,0216) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,021C)": DicomTagDefinition(
        tag="(0018,021C)",
        group="0018",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_0018_021C_Keyword",
        name="DICOM Standard Attribute (0018,021C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0222)": DicomTagDefinition(
        tag="(0018,0222)",
        group="0018",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_0018_0222_Keyword",
        name="DICOM Standard Attribute (0018,0222) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0228)": DicomTagDefinition(
        tag="(0018,0228)",
        group="0018",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_0018_0228_Keyword",
        name="DICOM Standard Attribute (0018,0228) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,022E)": DicomTagDefinition(
        tag="(0018,022E)",
        group="0018",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_0018_022E_Keyword",
        name="DICOM Standard Attribute (0018,022E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0234)": DicomTagDefinition(
        tag="(0018,0234)",
        group="0018",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_0018_0234_Keyword",
        name="DICOM Standard Attribute (0018,0234) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,023A)": DicomTagDefinition(
        tag="(0018,023A)",
        group="0018",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_0018_023A_Keyword",
        name="DICOM Standard Attribute (0018,023A) for Acquisition Parameters Specification",
        retired=True
    ),
    "(0018,0240)": DicomTagDefinition(
        tag="(0018,0240)",
        group="0018",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_0018_0240_Keyword",
        name="DICOM Standard Attribute (0018,0240) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0246)": DicomTagDefinition(
        tag="(0018,0246)",
        group="0018",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_0018_0246_Keyword",
        name="DICOM Standard Attribute (0018,0246) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,024C)": DicomTagDefinition(
        tag="(0018,024C)",
        group="0018",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_0018_024C_Keyword",
        name="DICOM Standard Attribute (0018,024C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0252)": DicomTagDefinition(
        tag="(0018,0252)",
        group="0018",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_0018_0252_Keyword",
        name="DICOM Standard Attribute (0018,0252) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0258)": DicomTagDefinition(
        tag="(0018,0258)",
        group="0018",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_0018_0258_Keyword",
        name="DICOM Standard Attribute (0018,0258) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,025E)": DicomTagDefinition(
        tag="(0018,025E)",
        group="0018",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_0018_025E_Keyword",
        name="DICOM Standard Attribute (0018,025E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0264)": DicomTagDefinition(
        tag="(0018,0264)",
        group="0018",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_0018_0264_Keyword",
        name="DICOM Standard Attribute (0018,0264) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,026A)": DicomTagDefinition(
        tag="(0018,026A)",
        group="0018",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_0018_026A_Keyword",
        name="DICOM Standard Attribute (0018,026A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0270)": DicomTagDefinition(
        tag="(0018,0270)",
        group="0018",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_0018_0270_Keyword",
        name="DICOM Standard Attribute (0018,0270) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0276)": DicomTagDefinition(
        tag="(0018,0276)",
        group="0018",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_0018_0276_Keyword",
        name="DICOM Standard Attribute (0018,0276) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,027C)": DicomTagDefinition(
        tag="(0018,027C)",
        group="0018",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_0018_027C_Keyword",
        name="DICOM Standard Attribute (0018,027C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0282)": DicomTagDefinition(
        tag="(0018,0282)",
        group="0018",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_0018_0282_Keyword",
        name="DICOM Standard Attribute (0018,0282) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0288)": DicomTagDefinition(
        tag="(0018,0288)",
        group="0018",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_0018_0288_Keyword",
        name="DICOM Standard Attribute (0018,0288) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,028E)": DicomTagDefinition(
        tag="(0018,028E)",
        group="0018",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_0018_028E_Keyword",
        name="DICOM Standard Attribute (0018,028E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0294)": DicomTagDefinition(
        tag="(0018,0294)",
        group="0018",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_0018_0294_Keyword",
        name="DICOM Standard Attribute (0018,0294) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,029A)": DicomTagDefinition(
        tag="(0018,029A)",
        group="0018",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_0018_029A_Keyword",
        name="DICOM Standard Attribute (0018,029A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02A0)": DicomTagDefinition(
        tag="(0018,02A0)",
        group="0018",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_0018_02A0_Keyword",
        name="DICOM Standard Attribute (0018,02A0) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02A6)": DicomTagDefinition(
        tag="(0018,02A6)",
        group="0018",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_0018_02A6_Keyword",
        name="DICOM Standard Attribute (0018,02A6) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02AC)": DicomTagDefinition(
        tag="(0018,02AC)",
        group="0018",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_0018_02AC_Keyword",
        name="DICOM Standard Attribute (0018,02AC) for Acquisition Parameters Specification",
        retired=True
    ),
    "(0018,02B2)": DicomTagDefinition(
        tag="(0018,02B2)",
        group="0018",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_0018_02B2_Keyword",
        name="DICOM Standard Attribute (0018,02B2) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02B8)": DicomTagDefinition(
        tag="(0018,02B8)",
        group="0018",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_0018_02B8_Keyword",
        name="DICOM Standard Attribute (0018,02B8) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02BE)": DicomTagDefinition(
        tag="(0018,02BE)",
        group="0018",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_0018_02BE_Keyword",
        name="DICOM Standard Attribute (0018,02BE) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02C4)": DicomTagDefinition(
        tag="(0018,02C4)",
        group="0018",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_0018_02C4_Keyword",
        name="DICOM Standard Attribute (0018,02C4) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02CA)": DicomTagDefinition(
        tag="(0018,02CA)",
        group="0018",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_0018_02CA_Keyword",
        name="DICOM Standard Attribute (0018,02CA) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02D0)": DicomTagDefinition(
        tag="(0018,02D0)",
        group="0018",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_0018_02D0_Keyword",
        name="DICOM Standard Attribute (0018,02D0) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02D6)": DicomTagDefinition(
        tag="(0018,02D6)",
        group="0018",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_0018_02D6_Keyword",
        name="DICOM Standard Attribute (0018,02D6) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02DC)": DicomTagDefinition(
        tag="(0018,02DC)",
        group="0018",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_0018_02DC_Keyword",
        name="DICOM Standard Attribute (0018,02DC) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02E2)": DicomTagDefinition(
        tag="(0018,02E2)",
        group="0018",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_0018_02E2_Keyword",
        name="DICOM Standard Attribute (0018,02E2) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02E8)": DicomTagDefinition(
        tag="(0018,02E8)",
        group="0018",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_0018_02E8_Keyword",
        name="DICOM Standard Attribute (0018,02E8) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02EE)": DicomTagDefinition(
        tag="(0018,02EE)",
        group="0018",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_0018_02EE_Keyword",
        name="DICOM Standard Attribute (0018,02EE) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02F4)": DicomTagDefinition(
        tag="(0018,02F4)",
        group="0018",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_0018_02F4_Keyword",
        name="DICOM Standard Attribute (0018,02F4) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,02FA)": DicomTagDefinition(
        tag="(0018,02FA)",
        group="0018",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_0018_02FA_Keyword",
        name="DICOM Standard Attribute (0018,02FA) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0300)": DicomTagDefinition(
        tag="(0018,0300)",
        group="0018",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_0018_0300_Keyword",
        name="DICOM Standard Attribute (0018,0300) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0306)": DicomTagDefinition(
        tag="(0018,0306)",
        group="0018",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_0018_0306_Keyword",
        name="DICOM Standard Attribute (0018,0306) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,030C)": DicomTagDefinition(
        tag="(0018,030C)",
        group="0018",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_0018_030C_Keyword",
        name="DICOM Standard Attribute (0018,030C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0312)": DicomTagDefinition(
        tag="(0018,0312)",
        group="0018",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_0018_0312_Keyword",
        name="DICOM Standard Attribute (0018,0312) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0318)": DicomTagDefinition(
        tag="(0018,0318)",
        group="0018",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_0018_0318_Keyword",
        name="DICOM Standard Attribute (0018,0318) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,031E)": DicomTagDefinition(
        tag="(0018,031E)",
        group="0018",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_0018_031E_Keyword",
        name="DICOM Standard Attribute (0018,031E) for Acquisition Parameters Specification",
        retired=True
    ),
    "(0018,0324)": DicomTagDefinition(
        tag="(0018,0324)",
        group="0018",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_0018_0324_Keyword",
        name="DICOM Standard Attribute (0018,0324) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,032A)": DicomTagDefinition(
        tag="(0018,032A)",
        group="0018",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_0018_032A_Keyword",
        name="DICOM Standard Attribute (0018,032A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0330)": DicomTagDefinition(
        tag="(0018,0330)",
        group="0018",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_0018_0330_Keyword",
        name="DICOM Standard Attribute (0018,0330) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0336)": DicomTagDefinition(
        tag="(0018,0336)",
        group="0018",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_0018_0336_Keyword",
        name="DICOM Standard Attribute (0018,0336) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,033C)": DicomTagDefinition(
        tag="(0018,033C)",
        group="0018",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_0018_033C_Keyword",
        name="DICOM Standard Attribute (0018,033C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0342)": DicomTagDefinition(
        tag="(0018,0342)",
        group="0018",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_0018_0342_Keyword",
        name="DICOM Standard Attribute (0018,0342) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0348)": DicomTagDefinition(
        tag="(0018,0348)",
        group="0018",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_0018_0348_Keyword",
        name="DICOM Standard Attribute (0018,0348) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,034E)": DicomTagDefinition(
        tag="(0018,034E)",
        group="0018",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0018_034E_Keyword",
        name="DICOM Standard Attribute (0018,034E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0354)": DicomTagDefinition(
        tag="(0018,0354)",
        group="0018",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_0018_0354_Keyword",
        name="DICOM Standard Attribute (0018,0354) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,035A)": DicomTagDefinition(
        tag="(0018,035A)",
        group="0018",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_0018_035A_Keyword",
        name="DICOM Standard Attribute (0018,035A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0360)": DicomTagDefinition(
        tag="(0018,0360)",
        group="0018",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_0018_0360_Keyword",
        name="DICOM Standard Attribute (0018,0360) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0366)": DicomTagDefinition(
        tag="(0018,0366)",
        group="0018",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_0018_0366_Keyword",
        name="DICOM Standard Attribute (0018,0366) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,036C)": DicomTagDefinition(
        tag="(0018,036C)",
        group="0018",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_0018_036C_Keyword",
        name="DICOM Standard Attribute (0018,036C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0372)": DicomTagDefinition(
        tag="(0018,0372)",
        group="0018",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_0018_0372_Keyword",
        name="DICOM Standard Attribute (0018,0372) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0378)": DicomTagDefinition(
        tag="(0018,0378)",
        group="0018",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_0018_0378_Keyword",
        name="DICOM Standard Attribute (0018,0378) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,037E)": DicomTagDefinition(
        tag="(0018,037E)",
        group="0018",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_0018_037E_Keyword",
        name="DICOM Standard Attribute (0018,037E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0384)": DicomTagDefinition(
        tag="(0018,0384)",
        group="0018",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_0018_0384_Keyword",
        name="DICOM Standard Attribute (0018,0384) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,038A)": DicomTagDefinition(
        tag="(0018,038A)",
        group="0018",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_0018_038A_Keyword",
        name="DICOM Standard Attribute (0018,038A) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0390)": DicomTagDefinition(
        tag="(0018,0390)",
        group="0018",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_0018_0390_Keyword",
        name="DICOM Standard Attribute (0018,0390) for Acquisition Parameters Specification",
        retired=True
    ),
    "(0018,0396)": DicomTagDefinition(
        tag="(0018,0396)",
        group="0018",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_0018_0396_Keyword",
        name="DICOM Standard Attribute (0018,0396) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,039C)": DicomTagDefinition(
        tag="(0018,039C)",
        group="0018",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_0018_039C_Keyword",
        name="DICOM Standard Attribute (0018,039C) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03A2)": DicomTagDefinition(
        tag="(0018,03A2)",
        group="0018",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_0018_03A2_Keyword",
        name="DICOM Standard Attribute (0018,03A2) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03A8)": DicomTagDefinition(
        tag="(0018,03A8)",
        group="0018",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_0018_03A8_Keyword",
        name="DICOM Standard Attribute (0018,03A8) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03AE)": DicomTagDefinition(
        tag="(0018,03AE)",
        group="0018",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_0018_03AE_Keyword",
        name="DICOM Standard Attribute (0018,03AE) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03B4)": DicomTagDefinition(
        tag="(0018,03B4)",
        group="0018",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_0018_03B4_Keyword",
        name="DICOM Standard Attribute (0018,03B4) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03BA)": DicomTagDefinition(
        tag="(0018,03BA)",
        group="0018",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_0018_03BA_Keyword",
        name="DICOM Standard Attribute (0018,03BA) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03C0)": DicomTagDefinition(
        tag="(0018,03C0)",
        group="0018",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_0018_03C0_Keyword",
        name="DICOM Standard Attribute (0018,03C0) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03C6)": DicomTagDefinition(
        tag="(0018,03C6)",
        group="0018",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_0018_03C6_Keyword",
        name="DICOM Standard Attribute (0018,03C6) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03CC)": DicomTagDefinition(
        tag="(0018,03CC)",
        group="0018",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_0018_03CC_Keyword",
        name="DICOM Standard Attribute (0018,03CC) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03D2)": DicomTagDefinition(
        tag="(0018,03D2)",
        group="0018",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_0018_03D2_Keyword",
        name="DICOM Standard Attribute (0018,03D2) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03D8)": DicomTagDefinition(
        tag="(0018,03D8)",
        group="0018",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_0018_03D8_Keyword",
        name="DICOM Standard Attribute (0018,03D8) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03DE)": DicomTagDefinition(
        tag="(0018,03DE)",
        group="0018",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_0018_03DE_Keyword",
        name="DICOM Standard Attribute (0018,03DE) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03E4)": DicomTagDefinition(
        tag="(0018,03E4)",
        group="0018",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_0018_03E4_Keyword",
        name="DICOM Standard Attribute (0018,03E4) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03EA)": DicomTagDefinition(
        tag="(0018,03EA)",
        group="0018",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_0018_03EA_Keyword",
        name="DICOM Standard Attribute (0018,03EA) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03F0)": DicomTagDefinition(
        tag="(0018,03F0)",
        group="0018",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_0018_03F0_Keyword",
        name="DICOM Standard Attribute (0018,03F0) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03F6)": DicomTagDefinition(
        tag="(0018,03F6)",
        group="0018",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_0018_03F6_Keyword",
        name="DICOM Standard Attribute (0018,03F6) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,03FC)": DicomTagDefinition(
        tag="(0018,03FC)",
        group="0018",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_0018_03FC_Keyword",
        name="DICOM Standard Attribute (0018,03FC) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0402)": DicomTagDefinition(
        tag="(0018,0402)",
        group="0018",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_0018_0402_Keyword",
        name="DICOM Standard Attribute (0018,0402) for Acquisition Parameters Specification",
        retired=True
    ),
    "(0018,0408)": DicomTagDefinition(
        tag="(0018,0408)",
        group="0018",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_0018_0408_Keyword",
        name="DICOM Standard Attribute (0018,0408) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,040E)": DicomTagDefinition(
        tag="(0018,040E)",
        group="0018",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_0018_040E_Keyword",
        name="DICOM Standard Attribute (0018,040E) for Acquisition Parameters Specification",
        retired=False
    ),
    "(0018,0414)": DicomTagDefinition(
        tag="(0018,0414)",
        group="0018",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_0018_0414_Keyword",
        name="DICOM Standard Attribute (0018,0414) for Acquisition Parameters Specification",
        retired=False
    ),
    # ========================================================
    # Section Group (0020): Relationship & Study Topology
    # ========================================================
    "(0020,0006)": DicomTagDefinition(
        tag="(0020,0006)",
        group="0020",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_0020_0006_Keyword",
        name="DICOM Standard Attribute (0020,0006) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,000C)": DicomTagDefinition(
        tag="(0020,000C)",
        group="0020",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_0020_000C_Keyword",
        name="DICOM Standard Attribute (0020,000C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0012)": DicomTagDefinition(
        tag="(0020,0012)",
        group="0020",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_0020_0012_Keyword",
        name="DICOM Standard Attribute (0020,0012) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0018)": DicomTagDefinition(
        tag="(0020,0018)",
        group="0020",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_0020_0018_Keyword",
        name="DICOM Standard Attribute (0020,0018) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,001E)": DicomTagDefinition(
        tag="(0020,001E)",
        group="0020",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_0020_001E_Keyword",
        name="DICOM Standard Attribute (0020,001E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0024)": DicomTagDefinition(
        tag="(0020,0024)",
        group="0020",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_0020_0024_Keyword",
        name="DICOM Standard Attribute (0020,0024) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,002A)": DicomTagDefinition(
        tag="(0020,002A)",
        group="0020",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_0020_002A_Keyword",
        name="DICOM Standard Attribute (0020,002A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0030)": DicomTagDefinition(
        tag="(0020,0030)",
        group="0020",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_0020_0030_Keyword",
        name="DICOM Standard Attribute (0020,0030) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0036)": DicomTagDefinition(
        tag="(0020,0036)",
        group="0020",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_0020_0036_Keyword",
        name="DICOM Standard Attribute (0020,0036) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,003C)": DicomTagDefinition(
        tag="(0020,003C)",
        group="0020",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_0020_003C_Keyword",
        name="DICOM Standard Attribute (0020,003C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0042)": DicomTagDefinition(
        tag="(0020,0042)",
        group="0020",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_0020_0042_Keyword",
        name="DICOM Standard Attribute (0020,0042) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0048)": DicomTagDefinition(
        tag="(0020,0048)",
        group="0020",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_0020_0048_Keyword",
        name="DICOM Standard Attribute (0020,0048) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,004E)": DicomTagDefinition(
        tag="(0020,004E)",
        group="0020",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_0020_004E_Keyword",
        name="DICOM Standard Attribute (0020,004E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0054)": DicomTagDefinition(
        tag="(0020,0054)",
        group="0020",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_0020_0054_Keyword",
        name="DICOM Standard Attribute (0020,0054) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,005A)": DicomTagDefinition(
        tag="(0020,005A)",
        group="0020",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_0020_005A_Keyword",
        name="DICOM Standard Attribute (0020,005A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0060)": DicomTagDefinition(
        tag="(0020,0060)",
        group="0020",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_0020_0060_Keyword",
        name="DICOM Standard Attribute (0020,0060) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0066)": DicomTagDefinition(
        tag="(0020,0066)",
        group="0020",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_0020_0066_Keyword",
        name="DICOM Standard Attribute (0020,0066) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,006C)": DicomTagDefinition(
        tag="(0020,006C)",
        group="0020",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_0020_006C_Keyword",
        name="DICOM Standard Attribute (0020,006C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0072)": DicomTagDefinition(
        tag="(0020,0072)",
        group="0020",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_0020_0072_Keyword",
        name="DICOM Standard Attribute (0020,0072) for Relationship & Study Topology Specification",
        retired=True
    ),
    "(0020,0078)": DicomTagDefinition(
        tag="(0020,0078)",
        group="0020",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_0020_0078_Keyword",
        name="DICOM Standard Attribute (0020,0078) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,007E)": DicomTagDefinition(
        tag="(0020,007E)",
        group="0020",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_0020_007E_Keyword",
        name="DICOM Standard Attribute (0020,007E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0084)": DicomTagDefinition(
        tag="(0020,0084)",
        group="0020",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_0020_0084_Keyword",
        name="DICOM Standard Attribute (0020,0084) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,008A)": DicomTagDefinition(
        tag="(0020,008A)",
        group="0020",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_0020_008A_Keyword",
        name="DICOM Standard Attribute (0020,008A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0090)": DicomTagDefinition(
        tag="(0020,0090)",
        group="0020",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_0020_0090_Keyword",
        name="DICOM Standard Attribute (0020,0090) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0096)": DicomTagDefinition(
        tag="(0020,0096)",
        group="0020",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_0020_0096_Keyword",
        name="DICOM Standard Attribute (0020,0096) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,009C)": DicomTagDefinition(
        tag="(0020,009C)",
        group="0020",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_0020_009C_Keyword",
        name="DICOM Standard Attribute (0020,009C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00A2)": DicomTagDefinition(
        tag="(0020,00A2)",
        group="0020",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_0020_00A2_Keyword",
        name="DICOM Standard Attribute (0020,00A2) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00A8)": DicomTagDefinition(
        tag="(0020,00A8)",
        group="0020",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_0020_00A8_Keyword",
        name="DICOM Standard Attribute (0020,00A8) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00AE)": DicomTagDefinition(
        tag="(0020,00AE)",
        group="0020",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_0020_00AE_Keyword",
        name="DICOM Standard Attribute (0020,00AE) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00B4)": DicomTagDefinition(
        tag="(0020,00B4)",
        group="0020",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_0020_00B4_Keyword",
        name="DICOM Standard Attribute (0020,00B4) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00BA)": DicomTagDefinition(
        tag="(0020,00BA)",
        group="0020",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0020_00BA_Keyword",
        name="DICOM Standard Attribute (0020,00BA) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00C0)": DicomTagDefinition(
        tag="(0020,00C0)",
        group="0020",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_0020_00C0_Keyword",
        name="DICOM Standard Attribute (0020,00C0) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00C6)": DicomTagDefinition(
        tag="(0020,00C6)",
        group="0020",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_0020_00C6_Keyword",
        name="DICOM Standard Attribute (0020,00C6) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00CC)": DicomTagDefinition(
        tag="(0020,00CC)",
        group="0020",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_0020_00CC_Keyword",
        name="DICOM Standard Attribute (0020,00CC) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00D2)": DicomTagDefinition(
        tag="(0020,00D2)",
        group="0020",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_0020_00D2_Keyword",
        name="DICOM Standard Attribute (0020,00D2) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00D8)": DicomTagDefinition(
        tag="(0020,00D8)",
        group="0020",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_0020_00D8_Keyword",
        name="DICOM Standard Attribute (0020,00D8) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00DE)": DicomTagDefinition(
        tag="(0020,00DE)",
        group="0020",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_0020_00DE_Keyword",
        name="DICOM Standard Attribute (0020,00DE) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00E4)": DicomTagDefinition(
        tag="(0020,00E4)",
        group="0020",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_0020_00E4_Keyword",
        name="DICOM Standard Attribute (0020,00E4) for Relationship & Study Topology Specification",
        retired=True
    ),
    "(0020,00EA)": DicomTagDefinition(
        tag="(0020,00EA)",
        group="0020",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_0020_00EA_Keyword",
        name="DICOM Standard Attribute (0020,00EA) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00F0)": DicomTagDefinition(
        tag="(0020,00F0)",
        group="0020",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_0020_00F0_Keyword",
        name="DICOM Standard Attribute (0020,00F0) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00F6)": DicomTagDefinition(
        tag="(0020,00F6)",
        group="0020",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_0020_00F6_Keyword",
        name="DICOM Standard Attribute (0020,00F6) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,00FC)": DicomTagDefinition(
        tag="(0020,00FC)",
        group="0020",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_0020_00FC_Keyword",
        name="DICOM Standard Attribute (0020,00FC) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0102)": DicomTagDefinition(
        tag="(0020,0102)",
        group="0020",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_0020_0102_Keyword",
        name="DICOM Standard Attribute (0020,0102) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0108)": DicomTagDefinition(
        tag="(0020,0108)",
        group="0020",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_0020_0108_Keyword",
        name="DICOM Standard Attribute (0020,0108) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,010E)": DicomTagDefinition(
        tag="(0020,010E)",
        group="0020",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_0020_010E_Keyword",
        name="DICOM Standard Attribute (0020,010E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0114)": DicomTagDefinition(
        tag="(0020,0114)",
        group="0020",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_0020_0114_Keyword",
        name="DICOM Standard Attribute (0020,0114) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,011A)": DicomTagDefinition(
        tag="(0020,011A)",
        group="0020",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_0020_011A_Keyword",
        name="DICOM Standard Attribute (0020,011A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0120)": DicomTagDefinition(
        tag="(0020,0120)",
        group="0020",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_0020_0120_Keyword",
        name="DICOM Standard Attribute (0020,0120) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0126)": DicomTagDefinition(
        tag="(0020,0126)",
        group="0020",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_0020_0126_Keyword",
        name="DICOM Standard Attribute (0020,0126) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,012C)": DicomTagDefinition(
        tag="(0020,012C)",
        group="0020",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_0020_012C_Keyword",
        name="DICOM Standard Attribute (0020,012C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0132)": DicomTagDefinition(
        tag="(0020,0132)",
        group="0020",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_0020_0132_Keyword",
        name="DICOM Standard Attribute (0020,0132) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0138)": DicomTagDefinition(
        tag="(0020,0138)",
        group="0020",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_0020_0138_Keyword",
        name="DICOM Standard Attribute (0020,0138) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,013E)": DicomTagDefinition(
        tag="(0020,013E)",
        group="0020",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_0020_013E_Keyword",
        name="DICOM Standard Attribute (0020,013E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0144)": DicomTagDefinition(
        tag="(0020,0144)",
        group="0020",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_0020_0144_Keyword",
        name="DICOM Standard Attribute (0020,0144) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,014A)": DicomTagDefinition(
        tag="(0020,014A)",
        group="0020",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_0020_014A_Keyword",
        name="DICOM Standard Attribute (0020,014A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0150)": DicomTagDefinition(
        tag="(0020,0150)",
        group="0020",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_0020_0150_Keyword",
        name="DICOM Standard Attribute (0020,0150) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0156)": DicomTagDefinition(
        tag="(0020,0156)",
        group="0020",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_0020_0156_Keyword",
        name="DICOM Standard Attribute (0020,0156) for Relationship & Study Topology Specification",
        retired=True
    ),
    "(0020,015C)": DicomTagDefinition(
        tag="(0020,015C)",
        group="0020",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_0020_015C_Keyword",
        name="DICOM Standard Attribute (0020,015C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0162)": DicomTagDefinition(
        tag="(0020,0162)",
        group="0020",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_0020_0162_Keyword",
        name="DICOM Standard Attribute (0020,0162) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0168)": DicomTagDefinition(
        tag="(0020,0168)",
        group="0020",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_0020_0168_Keyword",
        name="DICOM Standard Attribute (0020,0168) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,016E)": DicomTagDefinition(
        tag="(0020,016E)",
        group="0020",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_0020_016E_Keyword",
        name="DICOM Standard Attribute (0020,016E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0174)": DicomTagDefinition(
        tag="(0020,0174)",
        group="0020",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_0020_0174_Keyword",
        name="DICOM Standard Attribute (0020,0174) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,017A)": DicomTagDefinition(
        tag="(0020,017A)",
        group="0020",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_0020_017A_Keyword",
        name="DICOM Standard Attribute (0020,017A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0180)": DicomTagDefinition(
        tag="(0020,0180)",
        group="0020",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_0020_0180_Keyword",
        name="DICOM Standard Attribute (0020,0180) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0186)": DicomTagDefinition(
        tag="(0020,0186)",
        group="0020",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_0020_0186_Keyword",
        name="DICOM Standard Attribute (0020,0186) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,018C)": DicomTagDefinition(
        tag="(0020,018C)",
        group="0020",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_0020_018C_Keyword",
        name="DICOM Standard Attribute (0020,018C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0192)": DicomTagDefinition(
        tag="(0020,0192)",
        group="0020",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_0020_0192_Keyword",
        name="DICOM Standard Attribute (0020,0192) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0198)": DicomTagDefinition(
        tag="(0020,0198)",
        group="0020",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_0020_0198_Keyword",
        name="DICOM Standard Attribute (0020,0198) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,019E)": DicomTagDefinition(
        tag="(0020,019E)",
        group="0020",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_0020_019E_Keyword",
        name="DICOM Standard Attribute (0020,019E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01A4)": DicomTagDefinition(
        tag="(0020,01A4)",
        group="0020",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_0020_01A4_Keyword",
        name="DICOM Standard Attribute (0020,01A4) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01AA)": DicomTagDefinition(
        tag="(0020,01AA)",
        group="0020",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_0020_01AA_Keyword",
        name="DICOM Standard Attribute (0020,01AA) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01B0)": DicomTagDefinition(
        tag="(0020,01B0)",
        group="0020",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_0020_01B0_Keyword",
        name="DICOM Standard Attribute (0020,01B0) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01B6)": DicomTagDefinition(
        tag="(0020,01B6)",
        group="0020",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_0020_01B6_Keyword",
        name="DICOM Standard Attribute (0020,01B6) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01BC)": DicomTagDefinition(
        tag="(0020,01BC)",
        group="0020",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_0020_01BC_Keyword",
        name="DICOM Standard Attribute (0020,01BC) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01C2)": DicomTagDefinition(
        tag="(0020,01C2)",
        group="0020",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_0020_01C2_Keyword",
        name="DICOM Standard Attribute (0020,01C2) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01C8)": DicomTagDefinition(
        tag="(0020,01C8)",
        group="0020",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_0020_01C8_Keyword",
        name="DICOM Standard Attribute (0020,01C8) for Relationship & Study Topology Specification",
        retired=True
    ),
    "(0020,01CE)": DicomTagDefinition(
        tag="(0020,01CE)",
        group="0020",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_0020_01CE_Keyword",
        name="DICOM Standard Attribute (0020,01CE) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01D4)": DicomTagDefinition(
        tag="(0020,01D4)",
        group="0020",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_0020_01D4_Keyword",
        name="DICOM Standard Attribute (0020,01D4) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01DA)": DicomTagDefinition(
        tag="(0020,01DA)",
        group="0020",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_0020_01DA_Keyword",
        name="DICOM Standard Attribute (0020,01DA) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01E0)": DicomTagDefinition(
        tag="(0020,01E0)",
        group="0020",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_0020_01E0_Keyword",
        name="DICOM Standard Attribute (0020,01E0) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01E6)": DicomTagDefinition(
        tag="(0020,01E6)",
        group="0020",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_0020_01E6_Keyword",
        name="DICOM Standard Attribute (0020,01E6) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01EC)": DicomTagDefinition(
        tag="(0020,01EC)",
        group="0020",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_0020_01EC_Keyword",
        name="DICOM Standard Attribute (0020,01EC) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01F2)": DicomTagDefinition(
        tag="(0020,01F2)",
        group="0020",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_0020_01F2_Keyword",
        name="DICOM Standard Attribute (0020,01F2) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01F8)": DicomTagDefinition(
        tag="(0020,01F8)",
        group="0020",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_0020_01F8_Keyword",
        name="DICOM Standard Attribute (0020,01F8) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,01FE)": DicomTagDefinition(
        tag="(0020,01FE)",
        group="0020",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_0020_01FE_Keyword",
        name="DICOM Standard Attribute (0020,01FE) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0204)": DicomTagDefinition(
        tag="(0020,0204)",
        group="0020",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0020_0204_Keyword",
        name="DICOM Standard Attribute (0020,0204) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,020A)": DicomTagDefinition(
        tag="(0020,020A)",
        group="0020",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_0020_020A_Keyword",
        name="DICOM Standard Attribute (0020,020A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0210)": DicomTagDefinition(
        tag="(0020,0210)",
        group="0020",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_0020_0210_Keyword",
        name="DICOM Standard Attribute (0020,0210) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0216)": DicomTagDefinition(
        tag="(0020,0216)",
        group="0020",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_0020_0216_Keyword",
        name="DICOM Standard Attribute (0020,0216) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,021C)": DicomTagDefinition(
        tag="(0020,021C)",
        group="0020",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_0020_021C_Keyword",
        name="DICOM Standard Attribute (0020,021C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0222)": DicomTagDefinition(
        tag="(0020,0222)",
        group="0020",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_0020_0222_Keyword",
        name="DICOM Standard Attribute (0020,0222) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0228)": DicomTagDefinition(
        tag="(0020,0228)",
        group="0020",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_0020_0228_Keyword",
        name="DICOM Standard Attribute (0020,0228) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,022E)": DicomTagDefinition(
        tag="(0020,022E)",
        group="0020",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_0020_022E_Keyword",
        name="DICOM Standard Attribute (0020,022E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0234)": DicomTagDefinition(
        tag="(0020,0234)",
        group="0020",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_0020_0234_Keyword",
        name="DICOM Standard Attribute (0020,0234) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,023A)": DicomTagDefinition(
        tag="(0020,023A)",
        group="0020",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_0020_023A_Keyword",
        name="DICOM Standard Attribute (0020,023A) for Relationship & Study Topology Specification",
        retired=True
    ),
    "(0020,0240)": DicomTagDefinition(
        tag="(0020,0240)",
        group="0020",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_0020_0240_Keyword",
        name="DICOM Standard Attribute (0020,0240) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0246)": DicomTagDefinition(
        tag="(0020,0246)",
        group="0020",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_0020_0246_Keyword",
        name="DICOM Standard Attribute (0020,0246) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,024C)": DicomTagDefinition(
        tag="(0020,024C)",
        group="0020",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_0020_024C_Keyword",
        name="DICOM Standard Attribute (0020,024C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0252)": DicomTagDefinition(
        tag="(0020,0252)",
        group="0020",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_0020_0252_Keyword",
        name="DICOM Standard Attribute (0020,0252) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0258)": DicomTagDefinition(
        tag="(0020,0258)",
        group="0020",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_0020_0258_Keyword",
        name="DICOM Standard Attribute (0020,0258) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,025E)": DicomTagDefinition(
        tag="(0020,025E)",
        group="0020",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_0020_025E_Keyword",
        name="DICOM Standard Attribute (0020,025E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0264)": DicomTagDefinition(
        tag="(0020,0264)",
        group="0020",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_0020_0264_Keyword",
        name="DICOM Standard Attribute (0020,0264) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,026A)": DicomTagDefinition(
        tag="(0020,026A)",
        group="0020",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_0020_026A_Keyword",
        name="DICOM Standard Attribute (0020,026A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0270)": DicomTagDefinition(
        tag="(0020,0270)",
        group="0020",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_0020_0270_Keyword",
        name="DICOM Standard Attribute (0020,0270) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0276)": DicomTagDefinition(
        tag="(0020,0276)",
        group="0020",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_0020_0276_Keyword",
        name="DICOM Standard Attribute (0020,0276) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,027C)": DicomTagDefinition(
        tag="(0020,027C)",
        group="0020",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_0020_027C_Keyword",
        name="DICOM Standard Attribute (0020,027C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0282)": DicomTagDefinition(
        tag="(0020,0282)",
        group="0020",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_0020_0282_Keyword",
        name="DICOM Standard Attribute (0020,0282) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0288)": DicomTagDefinition(
        tag="(0020,0288)",
        group="0020",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_0020_0288_Keyword",
        name="DICOM Standard Attribute (0020,0288) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,028E)": DicomTagDefinition(
        tag="(0020,028E)",
        group="0020",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_0020_028E_Keyword",
        name="DICOM Standard Attribute (0020,028E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0294)": DicomTagDefinition(
        tag="(0020,0294)",
        group="0020",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_0020_0294_Keyword",
        name="DICOM Standard Attribute (0020,0294) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,029A)": DicomTagDefinition(
        tag="(0020,029A)",
        group="0020",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_0020_029A_Keyword",
        name="DICOM Standard Attribute (0020,029A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02A0)": DicomTagDefinition(
        tag="(0020,02A0)",
        group="0020",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_0020_02A0_Keyword",
        name="DICOM Standard Attribute (0020,02A0) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02A6)": DicomTagDefinition(
        tag="(0020,02A6)",
        group="0020",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_0020_02A6_Keyword",
        name="DICOM Standard Attribute (0020,02A6) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02AC)": DicomTagDefinition(
        tag="(0020,02AC)",
        group="0020",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_0020_02AC_Keyword",
        name="DICOM Standard Attribute (0020,02AC) for Relationship & Study Topology Specification",
        retired=True
    ),
    "(0020,02B2)": DicomTagDefinition(
        tag="(0020,02B2)",
        group="0020",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_0020_02B2_Keyword",
        name="DICOM Standard Attribute (0020,02B2) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02B8)": DicomTagDefinition(
        tag="(0020,02B8)",
        group="0020",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_0020_02B8_Keyword",
        name="DICOM Standard Attribute (0020,02B8) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02BE)": DicomTagDefinition(
        tag="(0020,02BE)",
        group="0020",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_0020_02BE_Keyword",
        name="DICOM Standard Attribute (0020,02BE) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02C4)": DicomTagDefinition(
        tag="(0020,02C4)",
        group="0020",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_0020_02C4_Keyword",
        name="DICOM Standard Attribute (0020,02C4) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02CA)": DicomTagDefinition(
        tag="(0020,02CA)",
        group="0020",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_0020_02CA_Keyword",
        name="DICOM Standard Attribute (0020,02CA) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02D0)": DicomTagDefinition(
        tag="(0020,02D0)",
        group="0020",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_0020_02D0_Keyword",
        name="DICOM Standard Attribute (0020,02D0) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02D6)": DicomTagDefinition(
        tag="(0020,02D6)",
        group="0020",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_0020_02D6_Keyword",
        name="DICOM Standard Attribute (0020,02D6) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02DC)": DicomTagDefinition(
        tag="(0020,02DC)",
        group="0020",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_0020_02DC_Keyword",
        name="DICOM Standard Attribute (0020,02DC) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02E2)": DicomTagDefinition(
        tag="(0020,02E2)",
        group="0020",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_0020_02E2_Keyword",
        name="DICOM Standard Attribute (0020,02E2) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02E8)": DicomTagDefinition(
        tag="(0020,02E8)",
        group="0020",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_0020_02E8_Keyword",
        name="DICOM Standard Attribute (0020,02E8) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02EE)": DicomTagDefinition(
        tag="(0020,02EE)",
        group="0020",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_0020_02EE_Keyword",
        name="DICOM Standard Attribute (0020,02EE) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02F4)": DicomTagDefinition(
        tag="(0020,02F4)",
        group="0020",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_0020_02F4_Keyword",
        name="DICOM Standard Attribute (0020,02F4) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,02FA)": DicomTagDefinition(
        tag="(0020,02FA)",
        group="0020",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_0020_02FA_Keyword",
        name="DICOM Standard Attribute (0020,02FA) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0300)": DicomTagDefinition(
        tag="(0020,0300)",
        group="0020",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_0020_0300_Keyword",
        name="DICOM Standard Attribute (0020,0300) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0306)": DicomTagDefinition(
        tag="(0020,0306)",
        group="0020",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_0020_0306_Keyword",
        name="DICOM Standard Attribute (0020,0306) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,030C)": DicomTagDefinition(
        tag="(0020,030C)",
        group="0020",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_0020_030C_Keyword",
        name="DICOM Standard Attribute (0020,030C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0312)": DicomTagDefinition(
        tag="(0020,0312)",
        group="0020",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_0020_0312_Keyword",
        name="DICOM Standard Attribute (0020,0312) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0318)": DicomTagDefinition(
        tag="(0020,0318)",
        group="0020",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_0020_0318_Keyword",
        name="DICOM Standard Attribute (0020,0318) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,031E)": DicomTagDefinition(
        tag="(0020,031E)",
        group="0020",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_0020_031E_Keyword",
        name="DICOM Standard Attribute (0020,031E) for Relationship & Study Topology Specification",
        retired=True
    ),
    "(0020,0324)": DicomTagDefinition(
        tag="(0020,0324)",
        group="0020",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_0020_0324_Keyword",
        name="DICOM Standard Attribute (0020,0324) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,032A)": DicomTagDefinition(
        tag="(0020,032A)",
        group="0020",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_0020_032A_Keyword",
        name="DICOM Standard Attribute (0020,032A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0330)": DicomTagDefinition(
        tag="(0020,0330)",
        group="0020",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_0020_0330_Keyword",
        name="DICOM Standard Attribute (0020,0330) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0336)": DicomTagDefinition(
        tag="(0020,0336)",
        group="0020",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_0020_0336_Keyword",
        name="DICOM Standard Attribute (0020,0336) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,033C)": DicomTagDefinition(
        tag="(0020,033C)",
        group="0020",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_0020_033C_Keyword",
        name="DICOM Standard Attribute (0020,033C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0342)": DicomTagDefinition(
        tag="(0020,0342)",
        group="0020",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_0020_0342_Keyword",
        name="DICOM Standard Attribute (0020,0342) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0348)": DicomTagDefinition(
        tag="(0020,0348)",
        group="0020",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_0020_0348_Keyword",
        name="DICOM Standard Attribute (0020,0348) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,034E)": DicomTagDefinition(
        tag="(0020,034E)",
        group="0020",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0020_034E_Keyword",
        name="DICOM Standard Attribute (0020,034E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0354)": DicomTagDefinition(
        tag="(0020,0354)",
        group="0020",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_0020_0354_Keyword",
        name="DICOM Standard Attribute (0020,0354) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,035A)": DicomTagDefinition(
        tag="(0020,035A)",
        group="0020",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_0020_035A_Keyword",
        name="DICOM Standard Attribute (0020,035A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0360)": DicomTagDefinition(
        tag="(0020,0360)",
        group="0020",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_0020_0360_Keyword",
        name="DICOM Standard Attribute (0020,0360) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0366)": DicomTagDefinition(
        tag="(0020,0366)",
        group="0020",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_0020_0366_Keyword",
        name="DICOM Standard Attribute (0020,0366) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,036C)": DicomTagDefinition(
        tag="(0020,036C)",
        group="0020",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_0020_036C_Keyword",
        name="DICOM Standard Attribute (0020,036C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0372)": DicomTagDefinition(
        tag="(0020,0372)",
        group="0020",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_0020_0372_Keyword",
        name="DICOM Standard Attribute (0020,0372) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0378)": DicomTagDefinition(
        tag="(0020,0378)",
        group="0020",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_0020_0378_Keyword",
        name="DICOM Standard Attribute (0020,0378) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,037E)": DicomTagDefinition(
        tag="(0020,037E)",
        group="0020",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_0020_037E_Keyword",
        name="DICOM Standard Attribute (0020,037E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0384)": DicomTagDefinition(
        tag="(0020,0384)",
        group="0020",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_0020_0384_Keyword",
        name="DICOM Standard Attribute (0020,0384) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,038A)": DicomTagDefinition(
        tag="(0020,038A)",
        group="0020",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_0020_038A_Keyword",
        name="DICOM Standard Attribute (0020,038A) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0390)": DicomTagDefinition(
        tag="(0020,0390)",
        group="0020",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_0020_0390_Keyword",
        name="DICOM Standard Attribute (0020,0390) for Relationship & Study Topology Specification",
        retired=True
    ),
    "(0020,0396)": DicomTagDefinition(
        tag="(0020,0396)",
        group="0020",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_0020_0396_Keyword",
        name="DICOM Standard Attribute (0020,0396) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,039C)": DicomTagDefinition(
        tag="(0020,039C)",
        group="0020",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_0020_039C_Keyword",
        name="DICOM Standard Attribute (0020,039C) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03A2)": DicomTagDefinition(
        tag="(0020,03A2)",
        group="0020",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_0020_03A2_Keyword",
        name="DICOM Standard Attribute (0020,03A2) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03A8)": DicomTagDefinition(
        tag="(0020,03A8)",
        group="0020",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_0020_03A8_Keyword",
        name="DICOM Standard Attribute (0020,03A8) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03AE)": DicomTagDefinition(
        tag="(0020,03AE)",
        group="0020",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_0020_03AE_Keyword",
        name="DICOM Standard Attribute (0020,03AE) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03B4)": DicomTagDefinition(
        tag="(0020,03B4)",
        group="0020",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_0020_03B4_Keyword",
        name="DICOM Standard Attribute (0020,03B4) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03BA)": DicomTagDefinition(
        tag="(0020,03BA)",
        group="0020",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_0020_03BA_Keyword",
        name="DICOM Standard Attribute (0020,03BA) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03C0)": DicomTagDefinition(
        tag="(0020,03C0)",
        group="0020",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_0020_03C0_Keyword",
        name="DICOM Standard Attribute (0020,03C0) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03C6)": DicomTagDefinition(
        tag="(0020,03C6)",
        group="0020",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_0020_03C6_Keyword",
        name="DICOM Standard Attribute (0020,03C6) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03CC)": DicomTagDefinition(
        tag="(0020,03CC)",
        group="0020",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_0020_03CC_Keyword",
        name="DICOM Standard Attribute (0020,03CC) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03D2)": DicomTagDefinition(
        tag="(0020,03D2)",
        group="0020",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_0020_03D2_Keyword",
        name="DICOM Standard Attribute (0020,03D2) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03D8)": DicomTagDefinition(
        tag="(0020,03D8)",
        group="0020",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_0020_03D8_Keyword",
        name="DICOM Standard Attribute (0020,03D8) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03DE)": DicomTagDefinition(
        tag="(0020,03DE)",
        group="0020",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_0020_03DE_Keyword",
        name="DICOM Standard Attribute (0020,03DE) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03E4)": DicomTagDefinition(
        tag="(0020,03E4)",
        group="0020",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_0020_03E4_Keyword",
        name="DICOM Standard Attribute (0020,03E4) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03EA)": DicomTagDefinition(
        tag="(0020,03EA)",
        group="0020",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_0020_03EA_Keyword",
        name="DICOM Standard Attribute (0020,03EA) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03F0)": DicomTagDefinition(
        tag="(0020,03F0)",
        group="0020",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_0020_03F0_Keyword",
        name="DICOM Standard Attribute (0020,03F0) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03F6)": DicomTagDefinition(
        tag="(0020,03F6)",
        group="0020",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_0020_03F6_Keyword",
        name="DICOM Standard Attribute (0020,03F6) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,03FC)": DicomTagDefinition(
        tag="(0020,03FC)",
        group="0020",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_0020_03FC_Keyword",
        name="DICOM Standard Attribute (0020,03FC) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0402)": DicomTagDefinition(
        tag="(0020,0402)",
        group="0020",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_0020_0402_Keyword",
        name="DICOM Standard Attribute (0020,0402) for Relationship & Study Topology Specification",
        retired=True
    ),
    "(0020,0408)": DicomTagDefinition(
        tag="(0020,0408)",
        group="0020",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_0020_0408_Keyword",
        name="DICOM Standard Attribute (0020,0408) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,040E)": DicomTagDefinition(
        tag="(0020,040E)",
        group="0020",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_0020_040E_Keyword",
        name="DICOM Standard Attribute (0020,040E) for Relationship & Study Topology Specification",
        retired=False
    ),
    "(0020,0414)": DicomTagDefinition(
        tag="(0020,0414)",
        group="0020",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_0020_0414_Keyword",
        name="DICOM Standard Attribute (0020,0414) for Relationship & Study Topology Specification",
        retired=False
    ),
    # ========================================================
    # Section Group (0028): Image Presentation & Pixel Formats
    # ========================================================
    "(0028,0006)": DicomTagDefinition(
        tag="(0028,0006)",
        group="0028",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_0028_0006_Keyword",
        name="DICOM Standard Attribute (0028,0006) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,000C)": DicomTagDefinition(
        tag="(0028,000C)",
        group="0028",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_0028_000C_Keyword",
        name="DICOM Standard Attribute (0028,000C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0012)": DicomTagDefinition(
        tag="(0028,0012)",
        group="0028",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_0028_0012_Keyword",
        name="DICOM Standard Attribute (0028,0012) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0018)": DicomTagDefinition(
        tag="(0028,0018)",
        group="0028",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_0028_0018_Keyword",
        name="DICOM Standard Attribute (0028,0018) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,001E)": DicomTagDefinition(
        tag="(0028,001E)",
        group="0028",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_0028_001E_Keyword",
        name="DICOM Standard Attribute (0028,001E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0024)": DicomTagDefinition(
        tag="(0028,0024)",
        group="0028",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_0028_0024_Keyword",
        name="DICOM Standard Attribute (0028,0024) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,002A)": DicomTagDefinition(
        tag="(0028,002A)",
        group="0028",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_0028_002A_Keyword",
        name="DICOM Standard Attribute (0028,002A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0030)": DicomTagDefinition(
        tag="(0028,0030)",
        group="0028",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_0028_0030_Keyword",
        name="DICOM Standard Attribute (0028,0030) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0036)": DicomTagDefinition(
        tag="(0028,0036)",
        group="0028",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_0028_0036_Keyword",
        name="DICOM Standard Attribute (0028,0036) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,003C)": DicomTagDefinition(
        tag="(0028,003C)",
        group="0028",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_0028_003C_Keyword",
        name="DICOM Standard Attribute (0028,003C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0042)": DicomTagDefinition(
        tag="(0028,0042)",
        group="0028",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_0028_0042_Keyword",
        name="DICOM Standard Attribute (0028,0042) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0048)": DicomTagDefinition(
        tag="(0028,0048)",
        group="0028",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_0028_0048_Keyword",
        name="DICOM Standard Attribute (0028,0048) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,004E)": DicomTagDefinition(
        tag="(0028,004E)",
        group="0028",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_0028_004E_Keyword",
        name="DICOM Standard Attribute (0028,004E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0054)": DicomTagDefinition(
        tag="(0028,0054)",
        group="0028",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_0028_0054_Keyword",
        name="DICOM Standard Attribute (0028,0054) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,005A)": DicomTagDefinition(
        tag="(0028,005A)",
        group="0028",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_0028_005A_Keyword",
        name="DICOM Standard Attribute (0028,005A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0060)": DicomTagDefinition(
        tag="(0028,0060)",
        group="0028",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_0028_0060_Keyword",
        name="DICOM Standard Attribute (0028,0060) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0066)": DicomTagDefinition(
        tag="(0028,0066)",
        group="0028",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_0028_0066_Keyword",
        name="DICOM Standard Attribute (0028,0066) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,006C)": DicomTagDefinition(
        tag="(0028,006C)",
        group="0028",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_0028_006C_Keyword",
        name="DICOM Standard Attribute (0028,006C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0072)": DicomTagDefinition(
        tag="(0028,0072)",
        group="0028",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_0028_0072_Keyword",
        name="DICOM Standard Attribute (0028,0072) for Image Presentation & Pixel Formats Specification",
        retired=True
    ),
    "(0028,0078)": DicomTagDefinition(
        tag="(0028,0078)",
        group="0028",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_0028_0078_Keyword",
        name="DICOM Standard Attribute (0028,0078) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,007E)": DicomTagDefinition(
        tag="(0028,007E)",
        group="0028",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_0028_007E_Keyword",
        name="DICOM Standard Attribute (0028,007E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0084)": DicomTagDefinition(
        tag="(0028,0084)",
        group="0028",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_0028_0084_Keyword",
        name="DICOM Standard Attribute (0028,0084) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,008A)": DicomTagDefinition(
        tag="(0028,008A)",
        group="0028",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_0028_008A_Keyword",
        name="DICOM Standard Attribute (0028,008A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0090)": DicomTagDefinition(
        tag="(0028,0090)",
        group="0028",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_0028_0090_Keyword",
        name="DICOM Standard Attribute (0028,0090) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0096)": DicomTagDefinition(
        tag="(0028,0096)",
        group="0028",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_0028_0096_Keyword",
        name="DICOM Standard Attribute (0028,0096) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,009C)": DicomTagDefinition(
        tag="(0028,009C)",
        group="0028",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_0028_009C_Keyword",
        name="DICOM Standard Attribute (0028,009C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00A2)": DicomTagDefinition(
        tag="(0028,00A2)",
        group="0028",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_0028_00A2_Keyword",
        name="DICOM Standard Attribute (0028,00A2) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00A8)": DicomTagDefinition(
        tag="(0028,00A8)",
        group="0028",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_0028_00A8_Keyword",
        name="DICOM Standard Attribute (0028,00A8) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00AE)": DicomTagDefinition(
        tag="(0028,00AE)",
        group="0028",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_0028_00AE_Keyword",
        name="DICOM Standard Attribute (0028,00AE) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00B4)": DicomTagDefinition(
        tag="(0028,00B4)",
        group="0028",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_0028_00B4_Keyword",
        name="DICOM Standard Attribute (0028,00B4) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00BA)": DicomTagDefinition(
        tag="(0028,00BA)",
        group="0028",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0028_00BA_Keyword",
        name="DICOM Standard Attribute (0028,00BA) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00C0)": DicomTagDefinition(
        tag="(0028,00C0)",
        group="0028",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_0028_00C0_Keyword",
        name="DICOM Standard Attribute (0028,00C0) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00C6)": DicomTagDefinition(
        tag="(0028,00C6)",
        group="0028",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_0028_00C6_Keyword",
        name="DICOM Standard Attribute (0028,00C6) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00CC)": DicomTagDefinition(
        tag="(0028,00CC)",
        group="0028",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_0028_00CC_Keyword",
        name="DICOM Standard Attribute (0028,00CC) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00D2)": DicomTagDefinition(
        tag="(0028,00D2)",
        group="0028",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_0028_00D2_Keyword",
        name="DICOM Standard Attribute (0028,00D2) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00D8)": DicomTagDefinition(
        tag="(0028,00D8)",
        group="0028",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_0028_00D8_Keyword",
        name="DICOM Standard Attribute (0028,00D8) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00DE)": DicomTagDefinition(
        tag="(0028,00DE)",
        group="0028",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_0028_00DE_Keyword",
        name="DICOM Standard Attribute (0028,00DE) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00E4)": DicomTagDefinition(
        tag="(0028,00E4)",
        group="0028",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_0028_00E4_Keyword",
        name="DICOM Standard Attribute (0028,00E4) for Image Presentation & Pixel Formats Specification",
        retired=True
    ),
    "(0028,00EA)": DicomTagDefinition(
        tag="(0028,00EA)",
        group="0028",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_0028_00EA_Keyword",
        name="DICOM Standard Attribute (0028,00EA) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00F0)": DicomTagDefinition(
        tag="(0028,00F0)",
        group="0028",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_0028_00F0_Keyword",
        name="DICOM Standard Attribute (0028,00F0) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00F6)": DicomTagDefinition(
        tag="(0028,00F6)",
        group="0028",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_0028_00F6_Keyword",
        name="DICOM Standard Attribute (0028,00F6) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,00FC)": DicomTagDefinition(
        tag="(0028,00FC)",
        group="0028",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_0028_00FC_Keyword",
        name="DICOM Standard Attribute (0028,00FC) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0102)": DicomTagDefinition(
        tag="(0028,0102)",
        group="0028",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_0028_0102_Keyword",
        name="DICOM Standard Attribute (0028,0102) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0108)": DicomTagDefinition(
        tag="(0028,0108)",
        group="0028",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_0028_0108_Keyword",
        name="DICOM Standard Attribute (0028,0108) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,010E)": DicomTagDefinition(
        tag="(0028,010E)",
        group="0028",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_0028_010E_Keyword",
        name="DICOM Standard Attribute (0028,010E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0114)": DicomTagDefinition(
        tag="(0028,0114)",
        group="0028",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_0028_0114_Keyword",
        name="DICOM Standard Attribute (0028,0114) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,011A)": DicomTagDefinition(
        tag="(0028,011A)",
        group="0028",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_0028_011A_Keyword",
        name="DICOM Standard Attribute (0028,011A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0120)": DicomTagDefinition(
        tag="(0028,0120)",
        group="0028",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_0028_0120_Keyword",
        name="DICOM Standard Attribute (0028,0120) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0126)": DicomTagDefinition(
        tag="(0028,0126)",
        group="0028",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_0028_0126_Keyword",
        name="DICOM Standard Attribute (0028,0126) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,012C)": DicomTagDefinition(
        tag="(0028,012C)",
        group="0028",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_0028_012C_Keyword",
        name="DICOM Standard Attribute (0028,012C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0132)": DicomTagDefinition(
        tag="(0028,0132)",
        group="0028",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_0028_0132_Keyword",
        name="DICOM Standard Attribute (0028,0132) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0138)": DicomTagDefinition(
        tag="(0028,0138)",
        group="0028",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_0028_0138_Keyword",
        name="DICOM Standard Attribute (0028,0138) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,013E)": DicomTagDefinition(
        tag="(0028,013E)",
        group="0028",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_0028_013E_Keyword",
        name="DICOM Standard Attribute (0028,013E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0144)": DicomTagDefinition(
        tag="(0028,0144)",
        group="0028",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_0028_0144_Keyword",
        name="DICOM Standard Attribute (0028,0144) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,014A)": DicomTagDefinition(
        tag="(0028,014A)",
        group="0028",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_0028_014A_Keyword",
        name="DICOM Standard Attribute (0028,014A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0150)": DicomTagDefinition(
        tag="(0028,0150)",
        group="0028",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_0028_0150_Keyword",
        name="DICOM Standard Attribute (0028,0150) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0156)": DicomTagDefinition(
        tag="(0028,0156)",
        group="0028",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_0028_0156_Keyword",
        name="DICOM Standard Attribute (0028,0156) for Image Presentation & Pixel Formats Specification",
        retired=True
    ),
    "(0028,015C)": DicomTagDefinition(
        tag="(0028,015C)",
        group="0028",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_0028_015C_Keyword",
        name="DICOM Standard Attribute (0028,015C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0162)": DicomTagDefinition(
        tag="(0028,0162)",
        group="0028",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_0028_0162_Keyword",
        name="DICOM Standard Attribute (0028,0162) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0168)": DicomTagDefinition(
        tag="(0028,0168)",
        group="0028",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_0028_0168_Keyword",
        name="DICOM Standard Attribute (0028,0168) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,016E)": DicomTagDefinition(
        tag="(0028,016E)",
        group="0028",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_0028_016E_Keyword",
        name="DICOM Standard Attribute (0028,016E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0174)": DicomTagDefinition(
        tag="(0028,0174)",
        group="0028",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_0028_0174_Keyword",
        name="DICOM Standard Attribute (0028,0174) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,017A)": DicomTagDefinition(
        tag="(0028,017A)",
        group="0028",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_0028_017A_Keyword",
        name="DICOM Standard Attribute (0028,017A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0180)": DicomTagDefinition(
        tag="(0028,0180)",
        group="0028",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_0028_0180_Keyword",
        name="DICOM Standard Attribute (0028,0180) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0186)": DicomTagDefinition(
        tag="(0028,0186)",
        group="0028",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_0028_0186_Keyword",
        name="DICOM Standard Attribute (0028,0186) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,018C)": DicomTagDefinition(
        tag="(0028,018C)",
        group="0028",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_0028_018C_Keyword",
        name="DICOM Standard Attribute (0028,018C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0192)": DicomTagDefinition(
        tag="(0028,0192)",
        group="0028",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_0028_0192_Keyword",
        name="DICOM Standard Attribute (0028,0192) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0198)": DicomTagDefinition(
        tag="(0028,0198)",
        group="0028",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_0028_0198_Keyword",
        name="DICOM Standard Attribute (0028,0198) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,019E)": DicomTagDefinition(
        tag="(0028,019E)",
        group="0028",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_0028_019E_Keyword",
        name="DICOM Standard Attribute (0028,019E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01A4)": DicomTagDefinition(
        tag="(0028,01A4)",
        group="0028",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_0028_01A4_Keyword",
        name="DICOM Standard Attribute (0028,01A4) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01AA)": DicomTagDefinition(
        tag="(0028,01AA)",
        group="0028",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_0028_01AA_Keyword",
        name="DICOM Standard Attribute (0028,01AA) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01B0)": DicomTagDefinition(
        tag="(0028,01B0)",
        group="0028",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_0028_01B0_Keyword",
        name="DICOM Standard Attribute (0028,01B0) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01B6)": DicomTagDefinition(
        tag="(0028,01B6)",
        group="0028",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_0028_01B6_Keyword",
        name="DICOM Standard Attribute (0028,01B6) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01BC)": DicomTagDefinition(
        tag="(0028,01BC)",
        group="0028",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_0028_01BC_Keyword",
        name="DICOM Standard Attribute (0028,01BC) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01C2)": DicomTagDefinition(
        tag="(0028,01C2)",
        group="0028",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_0028_01C2_Keyword",
        name="DICOM Standard Attribute (0028,01C2) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01C8)": DicomTagDefinition(
        tag="(0028,01C8)",
        group="0028",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_0028_01C8_Keyword",
        name="DICOM Standard Attribute (0028,01C8) for Image Presentation & Pixel Formats Specification",
        retired=True
    ),
    "(0028,01CE)": DicomTagDefinition(
        tag="(0028,01CE)",
        group="0028",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_0028_01CE_Keyword",
        name="DICOM Standard Attribute (0028,01CE) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01D4)": DicomTagDefinition(
        tag="(0028,01D4)",
        group="0028",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_0028_01D4_Keyword",
        name="DICOM Standard Attribute (0028,01D4) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01DA)": DicomTagDefinition(
        tag="(0028,01DA)",
        group="0028",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_0028_01DA_Keyword",
        name="DICOM Standard Attribute (0028,01DA) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01E0)": DicomTagDefinition(
        tag="(0028,01E0)",
        group="0028",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_0028_01E0_Keyword",
        name="DICOM Standard Attribute (0028,01E0) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01E6)": DicomTagDefinition(
        tag="(0028,01E6)",
        group="0028",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_0028_01E6_Keyword",
        name="DICOM Standard Attribute (0028,01E6) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01EC)": DicomTagDefinition(
        tag="(0028,01EC)",
        group="0028",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_0028_01EC_Keyword",
        name="DICOM Standard Attribute (0028,01EC) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01F2)": DicomTagDefinition(
        tag="(0028,01F2)",
        group="0028",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_0028_01F2_Keyword",
        name="DICOM Standard Attribute (0028,01F2) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01F8)": DicomTagDefinition(
        tag="(0028,01F8)",
        group="0028",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_0028_01F8_Keyword",
        name="DICOM Standard Attribute (0028,01F8) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,01FE)": DicomTagDefinition(
        tag="(0028,01FE)",
        group="0028",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_0028_01FE_Keyword",
        name="DICOM Standard Attribute (0028,01FE) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0204)": DicomTagDefinition(
        tag="(0028,0204)",
        group="0028",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0028_0204_Keyword",
        name="DICOM Standard Attribute (0028,0204) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,020A)": DicomTagDefinition(
        tag="(0028,020A)",
        group="0028",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_0028_020A_Keyword",
        name="DICOM Standard Attribute (0028,020A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0210)": DicomTagDefinition(
        tag="(0028,0210)",
        group="0028",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_0028_0210_Keyword",
        name="DICOM Standard Attribute (0028,0210) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0216)": DicomTagDefinition(
        tag="(0028,0216)",
        group="0028",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_0028_0216_Keyword",
        name="DICOM Standard Attribute (0028,0216) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,021C)": DicomTagDefinition(
        tag="(0028,021C)",
        group="0028",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_0028_021C_Keyword",
        name="DICOM Standard Attribute (0028,021C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0222)": DicomTagDefinition(
        tag="(0028,0222)",
        group="0028",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_0028_0222_Keyword",
        name="DICOM Standard Attribute (0028,0222) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0228)": DicomTagDefinition(
        tag="(0028,0228)",
        group="0028",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_0028_0228_Keyword",
        name="DICOM Standard Attribute (0028,0228) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,022E)": DicomTagDefinition(
        tag="(0028,022E)",
        group="0028",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_0028_022E_Keyword",
        name="DICOM Standard Attribute (0028,022E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0234)": DicomTagDefinition(
        tag="(0028,0234)",
        group="0028",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_0028_0234_Keyword",
        name="DICOM Standard Attribute (0028,0234) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,023A)": DicomTagDefinition(
        tag="(0028,023A)",
        group="0028",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_0028_023A_Keyword",
        name="DICOM Standard Attribute (0028,023A) for Image Presentation & Pixel Formats Specification",
        retired=True
    ),
    "(0028,0240)": DicomTagDefinition(
        tag="(0028,0240)",
        group="0028",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_0028_0240_Keyword",
        name="DICOM Standard Attribute (0028,0240) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0246)": DicomTagDefinition(
        tag="(0028,0246)",
        group="0028",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_0028_0246_Keyword",
        name="DICOM Standard Attribute (0028,0246) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,024C)": DicomTagDefinition(
        tag="(0028,024C)",
        group="0028",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_0028_024C_Keyword",
        name="DICOM Standard Attribute (0028,024C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0252)": DicomTagDefinition(
        tag="(0028,0252)",
        group="0028",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_0028_0252_Keyword",
        name="DICOM Standard Attribute (0028,0252) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0258)": DicomTagDefinition(
        tag="(0028,0258)",
        group="0028",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_0028_0258_Keyword",
        name="DICOM Standard Attribute (0028,0258) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,025E)": DicomTagDefinition(
        tag="(0028,025E)",
        group="0028",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_0028_025E_Keyword",
        name="DICOM Standard Attribute (0028,025E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0264)": DicomTagDefinition(
        tag="(0028,0264)",
        group="0028",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_0028_0264_Keyword",
        name="DICOM Standard Attribute (0028,0264) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,026A)": DicomTagDefinition(
        tag="(0028,026A)",
        group="0028",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_0028_026A_Keyword",
        name="DICOM Standard Attribute (0028,026A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0270)": DicomTagDefinition(
        tag="(0028,0270)",
        group="0028",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_0028_0270_Keyword",
        name="DICOM Standard Attribute (0028,0270) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0276)": DicomTagDefinition(
        tag="(0028,0276)",
        group="0028",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_0028_0276_Keyword",
        name="DICOM Standard Attribute (0028,0276) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,027C)": DicomTagDefinition(
        tag="(0028,027C)",
        group="0028",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_0028_027C_Keyword",
        name="DICOM Standard Attribute (0028,027C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0282)": DicomTagDefinition(
        tag="(0028,0282)",
        group="0028",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_0028_0282_Keyword",
        name="DICOM Standard Attribute (0028,0282) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0288)": DicomTagDefinition(
        tag="(0028,0288)",
        group="0028",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_0028_0288_Keyword",
        name="DICOM Standard Attribute (0028,0288) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,028E)": DicomTagDefinition(
        tag="(0028,028E)",
        group="0028",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_0028_028E_Keyword",
        name="DICOM Standard Attribute (0028,028E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0294)": DicomTagDefinition(
        tag="(0028,0294)",
        group="0028",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_0028_0294_Keyword",
        name="DICOM Standard Attribute (0028,0294) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,029A)": DicomTagDefinition(
        tag="(0028,029A)",
        group="0028",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_0028_029A_Keyword",
        name="DICOM Standard Attribute (0028,029A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02A0)": DicomTagDefinition(
        tag="(0028,02A0)",
        group="0028",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_0028_02A0_Keyword",
        name="DICOM Standard Attribute (0028,02A0) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02A6)": DicomTagDefinition(
        tag="(0028,02A6)",
        group="0028",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_0028_02A6_Keyword",
        name="DICOM Standard Attribute (0028,02A6) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02AC)": DicomTagDefinition(
        tag="(0028,02AC)",
        group="0028",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_0028_02AC_Keyword",
        name="DICOM Standard Attribute (0028,02AC) for Image Presentation & Pixel Formats Specification",
        retired=True
    ),
    "(0028,02B2)": DicomTagDefinition(
        tag="(0028,02B2)",
        group="0028",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_0028_02B2_Keyword",
        name="DICOM Standard Attribute (0028,02B2) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02B8)": DicomTagDefinition(
        tag="(0028,02B8)",
        group="0028",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_0028_02B8_Keyword",
        name="DICOM Standard Attribute (0028,02B8) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02BE)": DicomTagDefinition(
        tag="(0028,02BE)",
        group="0028",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_0028_02BE_Keyword",
        name="DICOM Standard Attribute (0028,02BE) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02C4)": DicomTagDefinition(
        tag="(0028,02C4)",
        group="0028",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_0028_02C4_Keyword",
        name="DICOM Standard Attribute (0028,02C4) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02CA)": DicomTagDefinition(
        tag="(0028,02CA)",
        group="0028",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_0028_02CA_Keyword",
        name="DICOM Standard Attribute (0028,02CA) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02D0)": DicomTagDefinition(
        tag="(0028,02D0)",
        group="0028",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_0028_02D0_Keyword",
        name="DICOM Standard Attribute (0028,02D0) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02D6)": DicomTagDefinition(
        tag="(0028,02D6)",
        group="0028",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_0028_02D6_Keyword",
        name="DICOM Standard Attribute (0028,02D6) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02DC)": DicomTagDefinition(
        tag="(0028,02DC)",
        group="0028",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_0028_02DC_Keyword",
        name="DICOM Standard Attribute (0028,02DC) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02E2)": DicomTagDefinition(
        tag="(0028,02E2)",
        group="0028",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_0028_02E2_Keyword",
        name="DICOM Standard Attribute (0028,02E2) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02E8)": DicomTagDefinition(
        tag="(0028,02E8)",
        group="0028",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_0028_02E8_Keyword",
        name="DICOM Standard Attribute (0028,02E8) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02EE)": DicomTagDefinition(
        tag="(0028,02EE)",
        group="0028",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_0028_02EE_Keyword",
        name="DICOM Standard Attribute (0028,02EE) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02F4)": DicomTagDefinition(
        tag="(0028,02F4)",
        group="0028",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_0028_02F4_Keyword",
        name="DICOM Standard Attribute (0028,02F4) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,02FA)": DicomTagDefinition(
        tag="(0028,02FA)",
        group="0028",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_0028_02FA_Keyword",
        name="DICOM Standard Attribute (0028,02FA) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0300)": DicomTagDefinition(
        tag="(0028,0300)",
        group="0028",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_0028_0300_Keyword",
        name="DICOM Standard Attribute (0028,0300) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0306)": DicomTagDefinition(
        tag="(0028,0306)",
        group="0028",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_0028_0306_Keyword",
        name="DICOM Standard Attribute (0028,0306) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,030C)": DicomTagDefinition(
        tag="(0028,030C)",
        group="0028",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_0028_030C_Keyword",
        name="DICOM Standard Attribute (0028,030C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0312)": DicomTagDefinition(
        tag="(0028,0312)",
        group="0028",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_0028_0312_Keyword",
        name="DICOM Standard Attribute (0028,0312) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0318)": DicomTagDefinition(
        tag="(0028,0318)",
        group="0028",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_0028_0318_Keyword",
        name="DICOM Standard Attribute (0028,0318) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,031E)": DicomTagDefinition(
        tag="(0028,031E)",
        group="0028",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_0028_031E_Keyword",
        name="DICOM Standard Attribute (0028,031E) for Image Presentation & Pixel Formats Specification",
        retired=True
    ),
    "(0028,0324)": DicomTagDefinition(
        tag="(0028,0324)",
        group="0028",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_0028_0324_Keyword",
        name="DICOM Standard Attribute (0028,0324) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,032A)": DicomTagDefinition(
        tag="(0028,032A)",
        group="0028",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_0028_032A_Keyword",
        name="DICOM Standard Attribute (0028,032A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0330)": DicomTagDefinition(
        tag="(0028,0330)",
        group="0028",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_0028_0330_Keyword",
        name="DICOM Standard Attribute (0028,0330) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0336)": DicomTagDefinition(
        tag="(0028,0336)",
        group="0028",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_0028_0336_Keyword",
        name="DICOM Standard Attribute (0028,0336) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,033C)": DicomTagDefinition(
        tag="(0028,033C)",
        group="0028",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_0028_033C_Keyword",
        name="DICOM Standard Attribute (0028,033C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0342)": DicomTagDefinition(
        tag="(0028,0342)",
        group="0028",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_0028_0342_Keyword",
        name="DICOM Standard Attribute (0028,0342) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0348)": DicomTagDefinition(
        tag="(0028,0348)",
        group="0028",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_0028_0348_Keyword",
        name="DICOM Standard Attribute (0028,0348) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,034E)": DicomTagDefinition(
        tag="(0028,034E)",
        group="0028",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0028_034E_Keyword",
        name="DICOM Standard Attribute (0028,034E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0354)": DicomTagDefinition(
        tag="(0028,0354)",
        group="0028",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_0028_0354_Keyword",
        name="DICOM Standard Attribute (0028,0354) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,035A)": DicomTagDefinition(
        tag="(0028,035A)",
        group="0028",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_0028_035A_Keyword",
        name="DICOM Standard Attribute (0028,035A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0360)": DicomTagDefinition(
        tag="(0028,0360)",
        group="0028",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_0028_0360_Keyword",
        name="DICOM Standard Attribute (0028,0360) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0366)": DicomTagDefinition(
        tag="(0028,0366)",
        group="0028",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_0028_0366_Keyword",
        name="DICOM Standard Attribute (0028,0366) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,036C)": DicomTagDefinition(
        tag="(0028,036C)",
        group="0028",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_0028_036C_Keyword",
        name="DICOM Standard Attribute (0028,036C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0372)": DicomTagDefinition(
        tag="(0028,0372)",
        group="0028",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_0028_0372_Keyword",
        name="DICOM Standard Attribute (0028,0372) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0378)": DicomTagDefinition(
        tag="(0028,0378)",
        group="0028",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_0028_0378_Keyword",
        name="DICOM Standard Attribute (0028,0378) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,037E)": DicomTagDefinition(
        tag="(0028,037E)",
        group="0028",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_0028_037E_Keyword",
        name="DICOM Standard Attribute (0028,037E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0384)": DicomTagDefinition(
        tag="(0028,0384)",
        group="0028",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_0028_0384_Keyword",
        name="DICOM Standard Attribute (0028,0384) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,038A)": DicomTagDefinition(
        tag="(0028,038A)",
        group="0028",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_0028_038A_Keyword",
        name="DICOM Standard Attribute (0028,038A) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0390)": DicomTagDefinition(
        tag="(0028,0390)",
        group="0028",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_0028_0390_Keyword",
        name="DICOM Standard Attribute (0028,0390) for Image Presentation & Pixel Formats Specification",
        retired=True
    ),
    "(0028,0396)": DicomTagDefinition(
        tag="(0028,0396)",
        group="0028",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_0028_0396_Keyword",
        name="DICOM Standard Attribute (0028,0396) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,039C)": DicomTagDefinition(
        tag="(0028,039C)",
        group="0028",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_0028_039C_Keyword",
        name="DICOM Standard Attribute (0028,039C) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03A2)": DicomTagDefinition(
        tag="(0028,03A2)",
        group="0028",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_0028_03A2_Keyword",
        name="DICOM Standard Attribute (0028,03A2) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03A8)": DicomTagDefinition(
        tag="(0028,03A8)",
        group="0028",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_0028_03A8_Keyword",
        name="DICOM Standard Attribute (0028,03A8) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03AE)": DicomTagDefinition(
        tag="(0028,03AE)",
        group="0028",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_0028_03AE_Keyword",
        name="DICOM Standard Attribute (0028,03AE) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03B4)": DicomTagDefinition(
        tag="(0028,03B4)",
        group="0028",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_0028_03B4_Keyword",
        name="DICOM Standard Attribute (0028,03B4) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03BA)": DicomTagDefinition(
        tag="(0028,03BA)",
        group="0028",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_0028_03BA_Keyword",
        name="DICOM Standard Attribute (0028,03BA) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03C0)": DicomTagDefinition(
        tag="(0028,03C0)",
        group="0028",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_0028_03C0_Keyword",
        name="DICOM Standard Attribute (0028,03C0) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03C6)": DicomTagDefinition(
        tag="(0028,03C6)",
        group="0028",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_0028_03C6_Keyword",
        name="DICOM Standard Attribute (0028,03C6) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03CC)": DicomTagDefinition(
        tag="(0028,03CC)",
        group="0028",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_0028_03CC_Keyword",
        name="DICOM Standard Attribute (0028,03CC) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03D2)": DicomTagDefinition(
        tag="(0028,03D2)",
        group="0028",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_0028_03D2_Keyword",
        name="DICOM Standard Attribute (0028,03D2) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03D8)": DicomTagDefinition(
        tag="(0028,03D8)",
        group="0028",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_0028_03D8_Keyword",
        name="DICOM Standard Attribute (0028,03D8) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03DE)": DicomTagDefinition(
        tag="(0028,03DE)",
        group="0028",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_0028_03DE_Keyword",
        name="DICOM Standard Attribute (0028,03DE) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03E4)": DicomTagDefinition(
        tag="(0028,03E4)",
        group="0028",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_0028_03E4_Keyword",
        name="DICOM Standard Attribute (0028,03E4) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03EA)": DicomTagDefinition(
        tag="(0028,03EA)",
        group="0028",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_0028_03EA_Keyword",
        name="DICOM Standard Attribute (0028,03EA) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03F0)": DicomTagDefinition(
        tag="(0028,03F0)",
        group="0028",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_0028_03F0_Keyword",
        name="DICOM Standard Attribute (0028,03F0) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03F6)": DicomTagDefinition(
        tag="(0028,03F6)",
        group="0028",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_0028_03F6_Keyword",
        name="DICOM Standard Attribute (0028,03F6) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,03FC)": DicomTagDefinition(
        tag="(0028,03FC)",
        group="0028",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_0028_03FC_Keyword",
        name="DICOM Standard Attribute (0028,03FC) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0402)": DicomTagDefinition(
        tag="(0028,0402)",
        group="0028",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_0028_0402_Keyword",
        name="DICOM Standard Attribute (0028,0402) for Image Presentation & Pixel Formats Specification",
        retired=True
    ),
    "(0028,0408)": DicomTagDefinition(
        tag="(0028,0408)",
        group="0028",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_0028_0408_Keyword",
        name="DICOM Standard Attribute (0028,0408) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,040E)": DicomTagDefinition(
        tag="(0028,040E)",
        group="0028",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_0028_040E_Keyword",
        name="DICOM Standard Attribute (0028,040E) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    "(0028,0414)": DicomTagDefinition(
        tag="(0028,0414)",
        group="0028",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_0028_0414_Keyword",
        name="DICOM Standard Attribute (0028,0414) for Image Presentation & Pixel Formats Specification",
        retired=False
    ),
    # ========================================================
    # Section Group (0040): Modality Worklist (MWL) & Procedures
    # ========================================================
    "(0040,0006)": DicomTagDefinition(
        tag="(0040,0006)",
        group="0040",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_0040_0006_Keyword",
        name="DICOM Standard Attribute (0040,0006) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,000C)": DicomTagDefinition(
        tag="(0040,000C)",
        group="0040",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_0040_000C_Keyword",
        name="DICOM Standard Attribute (0040,000C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0012)": DicomTagDefinition(
        tag="(0040,0012)",
        group="0040",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_0040_0012_Keyword",
        name="DICOM Standard Attribute (0040,0012) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0018)": DicomTagDefinition(
        tag="(0040,0018)",
        group="0040",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_0040_0018_Keyword",
        name="DICOM Standard Attribute (0040,0018) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,001E)": DicomTagDefinition(
        tag="(0040,001E)",
        group="0040",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_0040_001E_Keyword",
        name="DICOM Standard Attribute (0040,001E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0024)": DicomTagDefinition(
        tag="(0040,0024)",
        group="0040",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_0040_0024_Keyword",
        name="DICOM Standard Attribute (0040,0024) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,002A)": DicomTagDefinition(
        tag="(0040,002A)",
        group="0040",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_0040_002A_Keyword",
        name="DICOM Standard Attribute (0040,002A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0030)": DicomTagDefinition(
        tag="(0040,0030)",
        group="0040",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_0040_0030_Keyword",
        name="DICOM Standard Attribute (0040,0030) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0036)": DicomTagDefinition(
        tag="(0040,0036)",
        group="0040",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_0040_0036_Keyword",
        name="DICOM Standard Attribute (0040,0036) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,003C)": DicomTagDefinition(
        tag="(0040,003C)",
        group="0040",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_0040_003C_Keyword",
        name="DICOM Standard Attribute (0040,003C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0042)": DicomTagDefinition(
        tag="(0040,0042)",
        group="0040",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_0040_0042_Keyword",
        name="DICOM Standard Attribute (0040,0042) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0048)": DicomTagDefinition(
        tag="(0040,0048)",
        group="0040",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_0040_0048_Keyword",
        name="DICOM Standard Attribute (0040,0048) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,004E)": DicomTagDefinition(
        tag="(0040,004E)",
        group="0040",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_0040_004E_Keyword",
        name="DICOM Standard Attribute (0040,004E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0054)": DicomTagDefinition(
        tag="(0040,0054)",
        group="0040",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_0040_0054_Keyword",
        name="DICOM Standard Attribute (0040,0054) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,005A)": DicomTagDefinition(
        tag="(0040,005A)",
        group="0040",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_0040_005A_Keyword",
        name="DICOM Standard Attribute (0040,005A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0060)": DicomTagDefinition(
        tag="(0040,0060)",
        group="0040",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_0040_0060_Keyword",
        name="DICOM Standard Attribute (0040,0060) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0066)": DicomTagDefinition(
        tag="(0040,0066)",
        group="0040",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_0040_0066_Keyword",
        name="DICOM Standard Attribute (0040,0066) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,006C)": DicomTagDefinition(
        tag="(0040,006C)",
        group="0040",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_0040_006C_Keyword",
        name="DICOM Standard Attribute (0040,006C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0072)": DicomTagDefinition(
        tag="(0040,0072)",
        group="0040",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_0040_0072_Keyword",
        name="DICOM Standard Attribute (0040,0072) for Modality Worklist (MWL) & Procedures Specification",
        retired=True
    ),
    "(0040,0078)": DicomTagDefinition(
        tag="(0040,0078)",
        group="0040",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_0040_0078_Keyword",
        name="DICOM Standard Attribute (0040,0078) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,007E)": DicomTagDefinition(
        tag="(0040,007E)",
        group="0040",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_0040_007E_Keyword",
        name="DICOM Standard Attribute (0040,007E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0084)": DicomTagDefinition(
        tag="(0040,0084)",
        group="0040",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_0040_0084_Keyword",
        name="DICOM Standard Attribute (0040,0084) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,008A)": DicomTagDefinition(
        tag="(0040,008A)",
        group="0040",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_0040_008A_Keyword",
        name="DICOM Standard Attribute (0040,008A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0090)": DicomTagDefinition(
        tag="(0040,0090)",
        group="0040",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_0040_0090_Keyword",
        name="DICOM Standard Attribute (0040,0090) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0096)": DicomTagDefinition(
        tag="(0040,0096)",
        group="0040",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_0040_0096_Keyword",
        name="DICOM Standard Attribute (0040,0096) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,009C)": DicomTagDefinition(
        tag="(0040,009C)",
        group="0040",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_0040_009C_Keyword",
        name="DICOM Standard Attribute (0040,009C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00A2)": DicomTagDefinition(
        tag="(0040,00A2)",
        group="0040",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_0040_00A2_Keyword",
        name="DICOM Standard Attribute (0040,00A2) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00A8)": DicomTagDefinition(
        tag="(0040,00A8)",
        group="0040",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_0040_00A8_Keyword",
        name="DICOM Standard Attribute (0040,00A8) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00AE)": DicomTagDefinition(
        tag="(0040,00AE)",
        group="0040",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_0040_00AE_Keyword",
        name="DICOM Standard Attribute (0040,00AE) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00B4)": DicomTagDefinition(
        tag="(0040,00B4)",
        group="0040",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_0040_00B4_Keyword",
        name="DICOM Standard Attribute (0040,00B4) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00BA)": DicomTagDefinition(
        tag="(0040,00BA)",
        group="0040",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0040_00BA_Keyword",
        name="DICOM Standard Attribute (0040,00BA) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00C0)": DicomTagDefinition(
        tag="(0040,00C0)",
        group="0040",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_0040_00C0_Keyword",
        name="DICOM Standard Attribute (0040,00C0) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00C6)": DicomTagDefinition(
        tag="(0040,00C6)",
        group="0040",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_0040_00C6_Keyword",
        name="DICOM Standard Attribute (0040,00C6) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00CC)": DicomTagDefinition(
        tag="(0040,00CC)",
        group="0040",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_0040_00CC_Keyword",
        name="DICOM Standard Attribute (0040,00CC) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00D2)": DicomTagDefinition(
        tag="(0040,00D2)",
        group="0040",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_0040_00D2_Keyword",
        name="DICOM Standard Attribute (0040,00D2) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00D8)": DicomTagDefinition(
        tag="(0040,00D8)",
        group="0040",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_0040_00D8_Keyword",
        name="DICOM Standard Attribute (0040,00D8) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00DE)": DicomTagDefinition(
        tag="(0040,00DE)",
        group="0040",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_0040_00DE_Keyword",
        name="DICOM Standard Attribute (0040,00DE) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00E4)": DicomTagDefinition(
        tag="(0040,00E4)",
        group="0040",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_0040_00E4_Keyword",
        name="DICOM Standard Attribute (0040,00E4) for Modality Worklist (MWL) & Procedures Specification",
        retired=True
    ),
    "(0040,00EA)": DicomTagDefinition(
        tag="(0040,00EA)",
        group="0040",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_0040_00EA_Keyword",
        name="DICOM Standard Attribute (0040,00EA) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00F0)": DicomTagDefinition(
        tag="(0040,00F0)",
        group="0040",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_0040_00F0_Keyword",
        name="DICOM Standard Attribute (0040,00F0) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00F6)": DicomTagDefinition(
        tag="(0040,00F6)",
        group="0040",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_0040_00F6_Keyword",
        name="DICOM Standard Attribute (0040,00F6) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,00FC)": DicomTagDefinition(
        tag="(0040,00FC)",
        group="0040",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_0040_00FC_Keyword",
        name="DICOM Standard Attribute (0040,00FC) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0102)": DicomTagDefinition(
        tag="(0040,0102)",
        group="0040",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_0040_0102_Keyword",
        name="DICOM Standard Attribute (0040,0102) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0108)": DicomTagDefinition(
        tag="(0040,0108)",
        group="0040",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_0040_0108_Keyword",
        name="DICOM Standard Attribute (0040,0108) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,010E)": DicomTagDefinition(
        tag="(0040,010E)",
        group="0040",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_0040_010E_Keyword",
        name="DICOM Standard Attribute (0040,010E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0114)": DicomTagDefinition(
        tag="(0040,0114)",
        group="0040",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_0040_0114_Keyword",
        name="DICOM Standard Attribute (0040,0114) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,011A)": DicomTagDefinition(
        tag="(0040,011A)",
        group="0040",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_0040_011A_Keyword",
        name="DICOM Standard Attribute (0040,011A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0120)": DicomTagDefinition(
        tag="(0040,0120)",
        group="0040",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_0040_0120_Keyword",
        name="DICOM Standard Attribute (0040,0120) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0126)": DicomTagDefinition(
        tag="(0040,0126)",
        group="0040",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_0040_0126_Keyword",
        name="DICOM Standard Attribute (0040,0126) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,012C)": DicomTagDefinition(
        tag="(0040,012C)",
        group="0040",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_0040_012C_Keyword",
        name="DICOM Standard Attribute (0040,012C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0132)": DicomTagDefinition(
        tag="(0040,0132)",
        group="0040",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_0040_0132_Keyword",
        name="DICOM Standard Attribute (0040,0132) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0138)": DicomTagDefinition(
        tag="(0040,0138)",
        group="0040",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_0040_0138_Keyword",
        name="DICOM Standard Attribute (0040,0138) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,013E)": DicomTagDefinition(
        tag="(0040,013E)",
        group="0040",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_0040_013E_Keyword",
        name="DICOM Standard Attribute (0040,013E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0144)": DicomTagDefinition(
        tag="(0040,0144)",
        group="0040",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_0040_0144_Keyword",
        name="DICOM Standard Attribute (0040,0144) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,014A)": DicomTagDefinition(
        tag="(0040,014A)",
        group="0040",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_0040_014A_Keyword",
        name="DICOM Standard Attribute (0040,014A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0150)": DicomTagDefinition(
        tag="(0040,0150)",
        group="0040",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_0040_0150_Keyword",
        name="DICOM Standard Attribute (0040,0150) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0156)": DicomTagDefinition(
        tag="(0040,0156)",
        group="0040",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_0040_0156_Keyword",
        name="DICOM Standard Attribute (0040,0156) for Modality Worklist (MWL) & Procedures Specification",
        retired=True
    ),
    "(0040,015C)": DicomTagDefinition(
        tag="(0040,015C)",
        group="0040",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_0040_015C_Keyword",
        name="DICOM Standard Attribute (0040,015C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0162)": DicomTagDefinition(
        tag="(0040,0162)",
        group="0040",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_0040_0162_Keyword",
        name="DICOM Standard Attribute (0040,0162) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0168)": DicomTagDefinition(
        tag="(0040,0168)",
        group="0040",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_0040_0168_Keyword",
        name="DICOM Standard Attribute (0040,0168) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,016E)": DicomTagDefinition(
        tag="(0040,016E)",
        group="0040",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_0040_016E_Keyword",
        name="DICOM Standard Attribute (0040,016E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0174)": DicomTagDefinition(
        tag="(0040,0174)",
        group="0040",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_0040_0174_Keyword",
        name="DICOM Standard Attribute (0040,0174) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,017A)": DicomTagDefinition(
        tag="(0040,017A)",
        group="0040",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_0040_017A_Keyword",
        name="DICOM Standard Attribute (0040,017A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0180)": DicomTagDefinition(
        tag="(0040,0180)",
        group="0040",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_0040_0180_Keyword",
        name="DICOM Standard Attribute (0040,0180) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0186)": DicomTagDefinition(
        tag="(0040,0186)",
        group="0040",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_0040_0186_Keyword",
        name="DICOM Standard Attribute (0040,0186) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,018C)": DicomTagDefinition(
        tag="(0040,018C)",
        group="0040",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_0040_018C_Keyword",
        name="DICOM Standard Attribute (0040,018C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0192)": DicomTagDefinition(
        tag="(0040,0192)",
        group="0040",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_0040_0192_Keyword",
        name="DICOM Standard Attribute (0040,0192) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0198)": DicomTagDefinition(
        tag="(0040,0198)",
        group="0040",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_0040_0198_Keyword",
        name="DICOM Standard Attribute (0040,0198) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,019E)": DicomTagDefinition(
        tag="(0040,019E)",
        group="0040",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_0040_019E_Keyword",
        name="DICOM Standard Attribute (0040,019E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01A4)": DicomTagDefinition(
        tag="(0040,01A4)",
        group="0040",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_0040_01A4_Keyword",
        name="DICOM Standard Attribute (0040,01A4) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01AA)": DicomTagDefinition(
        tag="(0040,01AA)",
        group="0040",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_0040_01AA_Keyword",
        name="DICOM Standard Attribute (0040,01AA) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01B0)": DicomTagDefinition(
        tag="(0040,01B0)",
        group="0040",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_0040_01B0_Keyword",
        name="DICOM Standard Attribute (0040,01B0) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01B6)": DicomTagDefinition(
        tag="(0040,01B6)",
        group="0040",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_0040_01B6_Keyword",
        name="DICOM Standard Attribute (0040,01B6) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01BC)": DicomTagDefinition(
        tag="(0040,01BC)",
        group="0040",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_0040_01BC_Keyword",
        name="DICOM Standard Attribute (0040,01BC) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01C2)": DicomTagDefinition(
        tag="(0040,01C2)",
        group="0040",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_0040_01C2_Keyword",
        name="DICOM Standard Attribute (0040,01C2) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01C8)": DicomTagDefinition(
        tag="(0040,01C8)",
        group="0040",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_0040_01C8_Keyword",
        name="DICOM Standard Attribute (0040,01C8) for Modality Worklist (MWL) & Procedures Specification",
        retired=True
    ),
    "(0040,01CE)": DicomTagDefinition(
        tag="(0040,01CE)",
        group="0040",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_0040_01CE_Keyword",
        name="DICOM Standard Attribute (0040,01CE) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01D4)": DicomTagDefinition(
        tag="(0040,01D4)",
        group="0040",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_0040_01D4_Keyword",
        name="DICOM Standard Attribute (0040,01D4) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01DA)": DicomTagDefinition(
        tag="(0040,01DA)",
        group="0040",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_0040_01DA_Keyword",
        name="DICOM Standard Attribute (0040,01DA) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01E0)": DicomTagDefinition(
        tag="(0040,01E0)",
        group="0040",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_0040_01E0_Keyword",
        name="DICOM Standard Attribute (0040,01E0) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01E6)": DicomTagDefinition(
        tag="(0040,01E6)",
        group="0040",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_0040_01E6_Keyword",
        name="DICOM Standard Attribute (0040,01E6) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01EC)": DicomTagDefinition(
        tag="(0040,01EC)",
        group="0040",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_0040_01EC_Keyword",
        name="DICOM Standard Attribute (0040,01EC) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01F2)": DicomTagDefinition(
        tag="(0040,01F2)",
        group="0040",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_0040_01F2_Keyword",
        name="DICOM Standard Attribute (0040,01F2) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01F8)": DicomTagDefinition(
        tag="(0040,01F8)",
        group="0040",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_0040_01F8_Keyword",
        name="DICOM Standard Attribute (0040,01F8) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,01FE)": DicomTagDefinition(
        tag="(0040,01FE)",
        group="0040",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_0040_01FE_Keyword",
        name="DICOM Standard Attribute (0040,01FE) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0204)": DicomTagDefinition(
        tag="(0040,0204)",
        group="0040",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0040_0204_Keyword",
        name="DICOM Standard Attribute (0040,0204) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,020A)": DicomTagDefinition(
        tag="(0040,020A)",
        group="0040",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_0040_020A_Keyword",
        name="DICOM Standard Attribute (0040,020A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0210)": DicomTagDefinition(
        tag="(0040,0210)",
        group="0040",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_0040_0210_Keyword",
        name="DICOM Standard Attribute (0040,0210) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0216)": DicomTagDefinition(
        tag="(0040,0216)",
        group="0040",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_0040_0216_Keyword",
        name="DICOM Standard Attribute (0040,0216) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,021C)": DicomTagDefinition(
        tag="(0040,021C)",
        group="0040",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_0040_021C_Keyword",
        name="DICOM Standard Attribute (0040,021C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0222)": DicomTagDefinition(
        tag="(0040,0222)",
        group="0040",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_0040_0222_Keyword",
        name="DICOM Standard Attribute (0040,0222) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0228)": DicomTagDefinition(
        tag="(0040,0228)",
        group="0040",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_0040_0228_Keyword",
        name="DICOM Standard Attribute (0040,0228) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,022E)": DicomTagDefinition(
        tag="(0040,022E)",
        group="0040",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_0040_022E_Keyword",
        name="DICOM Standard Attribute (0040,022E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0234)": DicomTagDefinition(
        tag="(0040,0234)",
        group="0040",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_0040_0234_Keyword",
        name="DICOM Standard Attribute (0040,0234) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,023A)": DicomTagDefinition(
        tag="(0040,023A)",
        group="0040",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_0040_023A_Keyword",
        name="DICOM Standard Attribute (0040,023A) for Modality Worklist (MWL) & Procedures Specification",
        retired=True
    ),
    "(0040,0240)": DicomTagDefinition(
        tag="(0040,0240)",
        group="0040",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_0040_0240_Keyword",
        name="DICOM Standard Attribute (0040,0240) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0246)": DicomTagDefinition(
        tag="(0040,0246)",
        group="0040",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_0040_0246_Keyword",
        name="DICOM Standard Attribute (0040,0246) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,024C)": DicomTagDefinition(
        tag="(0040,024C)",
        group="0040",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_0040_024C_Keyword",
        name="DICOM Standard Attribute (0040,024C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0252)": DicomTagDefinition(
        tag="(0040,0252)",
        group="0040",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_0040_0252_Keyword",
        name="DICOM Standard Attribute (0040,0252) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0258)": DicomTagDefinition(
        tag="(0040,0258)",
        group="0040",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_0040_0258_Keyword",
        name="DICOM Standard Attribute (0040,0258) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,025E)": DicomTagDefinition(
        tag="(0040,025E)",
        group="0040",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_0040_025E_Keyword",
        name="DICOM Standard Attribute (0040,025E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0264)": DicomTagDefinition(
        tag="(0040,0264)",
        group="0040",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_0040_0264_Keyword",
        name="DICOM Standard Attribute (0040,0264) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,026A)": DicomTagDefinition(
        tag="(0040,026A)",
        group="0040",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_0040_026A_Keyword",
        name="DICOM Standard Attribute (0040,026A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0270)": DicomTagDefinition(
        tag="(0040,0270)",
        group="0040",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_0040_0270_Keyword",
        name="DICOM Standard Attribute (0040,0270) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0276)": DicomTagDefinition(
        tag="(0040,0276)",
        group="0040",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_0040_0276_Keyword",
        name="DICOM Standard Attribute (0040,0276) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,027C)": DicomTagDefinition(
        tag="(0040,027C)",
        group="0040",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_0040_027C_Keyword",
        name="DICOM Standard Attribute (0040,027C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0282)": DicomTagDefinition(
        tag="(0040,0282)",
        group="0040",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_0040_0282_Keyword",
        name="DICOM Standard Attribute (0040,0282) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0288)": DicomTagDefinition(
        tag="(0040,0288)",
        group="0040",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_0040_0288_Keyword",
        name="DICOM Standard Attribute (0040,0288) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,028E)": DicomTagDefinition(
        tag="(0040,028E)",
        group="0040",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_0040_028E_Keyword",
        name="DICOM Standard Attribute (0040,028E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0294)": DicomTagDefinition(
        tag="(0040,0294)",
        group="0040",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_0040_0294_Keyword",
        name="DICOM Standard Attribute (0040,0294) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,029A)": DicomTagDefinition(
        tag="(0040,029A)",
        group="0040",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_0040_029A_Keyword",
        name="DICOM Standard Attribute (0040,029A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02A0)": DicomTagDefinition(
        tag="(0040,02A0)",
        group="0040",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_0040_02A0_Keyword",
        name="DICOM Standard Attribute (0040,02A0) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02A6)": DicomTagDefinition(
        tag="(0040,02A6)",
        group="0040",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_0040_02A6_Keyword",
        name="DICOM Standard Attribute (0040,02A6) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02AC)": DicomTagDefinition(
        tag="(0040,02AC)",
        group="0040",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_0040_02AC_Keyword",
        name="DICOM Standard Attribute (0040,02AC) for Modality Worklist (MWL) & Procedures Specification",
        retired=True
    ),
    "(0040,02B2)": DicomTagDefinition(
        tag="(0040,02B2)",
        group="0040",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_0040_02B2_Keyword",
        name="DICOM Standard Attribute (0040,02B2) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02B8)": DicomTagDefinition(
        tag="(0040,02B8)",
        group="0040",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_0040_02B8_Keyword",
        name="DICOM Standard Attribute (0040,02B8) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02BE)": DicomTagDefinition(
        tag="(0040,02BE)",
        group="0040",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_0040_02BE_Keyword",
        name="DICOM Standard Attribute (0040,02BE) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02C4)": DicomTagDefinition(
        tag="(0040,02C4)",
        group="0040",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_0040_02C4_Keyword",
        name="DICOM Standard Attribute (0040,02C4) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02CA)": DicomTagDefinition(
        tag="(0040,02CA)",
        group="0040",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_0040_02CA_Keyword",
        name="DICOM Standard Attribute (0040,02CA) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02D0)": DicomTagDefinition(
        tag="(0040,02D0)",
        group="0040",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_0040_02D0_Keyword",
        name="DICOM Standard Attribute (0040,02D0) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02D6)": DicomTagDefinition(
        tag="(0040,02D6)",
        group="0040",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_0040_02D6_Keyword",
        name="DICOM Standard Attribute (0040,02D6) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02DC)": DicomTagDefinition(
        tag="(0040,02DC)",
        group="0040",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_0040_02DC_Keyword",
        name="DICOM Standard Attribute (0040,02DC) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02E2)": DicomTagDefinition(
        tag="(0040,02E2)",
        group="0040",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_0040_02E2_Keyword",
        name="DICOM Standard Attribute (0040,02E2) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02E8)": DicomTagDefinition(
        tag="(0040,02E8)",
        group="0040",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_0040_02E8_Keyword",
        name="DICOM Standard Attribute (0040,02E8) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02EE)": DicomTagDefinition(
        tag="(0040,02EE)",
        group="0040",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_0040_02EE_Keyword",
        name="DICOM Standard Attribute (0040,02EE) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02F4)": DicomTagDefinition(
        tag="(0040,02F4)",
        group="0040",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_0040_02F4_Keyword",
        name="DICOM Standard Attribute (0040,02F4) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,02FA)": DicomTagDefinition(
        tag="(0040,02FA)",
        group="0040",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_0040_02FA_Keyword",
        name="DICOM Standard Attribute (0040,02FA) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0300)": DicomTagDefinition(
        tag="(0040,0300)",
        group="0040",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_0040_0300_Keyword",
        name="DICOM Standard Attribute (0040,0300) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0306)": DicomTagDefinition(
        tag="(0040,0306)",
        group="0040",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_0040_0306_Keyword",
        name="DICOM Standard Attribute (0040,0306) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,030C)": DicomTagDefinition(
        tag="(0040,030C)",
        group="0040",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_0040_030C_Keyword",
        name="DICOM Standard Attribute (0040,030C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0312)": DicomTagDefinition(
        tag="(0040,0312)",
        group="0040",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_0040_0312_Keyword",
        name="DICOM Standard Attribute (0040,0312) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0318)": DicomTagDefinition(
        tag="(0040,0318)",
        group="0040",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_0040_0318_Keyword",
        name="DICOM Standard Attribute (0040,0318) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,031E)": DicomTagDefinition(
        tag="(0040,031E)",
        group="0040",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_0040_031E_Keyword",
        name="DICOM Standard Attribute (0040,031E) for Modality Worklist (MWL) & Procedures Specification",
        retired=True
    ),
    "(0040,0324)": DicomTagDefinition(
        tag="(0040,0324)",
        group="0040",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_0040_0324_Keyword",
        name="DICOM Standard Attribute (0040,0324) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,032A)": DicomTagDefinition(
        tag="(0040,032A)",
        group="0040",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_0040_032A_Keyword",
        name="DICOM Standard Attribute (0040,032A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0330)": DicomTagDefinition(
        tag="(0040,0330)",
        group="0040",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_0040_0330_Keyword",
        name="DICOM Standard Attribute (0040,0330) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0336)": DicomTagDefinition(
        tag="(0040,0336)",
        group="0040",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_0040_0336_Keyword",
        name="DICOM Standard Attribute (0040,0336) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,033C)": DicomTagDefinition(
        tag="(0040,033C)",
        group="0040",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_0040_033C_Keyword",
        name="DICOM Standard Attribute (0040,033C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0342)": DicomTagDefinition(
        tag="(0040,0342)",
        group="0040",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_0040_0342_Keyword",
        name="DICOM Standard Attribute (0040,0342) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0348)": DicomTagDefinition(
        tag="(0040,0348)",
        group="0040",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_0040_0348_Keyword",
        name="DICOM Standard Attribute (0040,0348) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,034E)": DicomTagDefinition(
        tag="(0040,034E)",
        group="0040",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0040_034E_Keyword",
        name="DICOM Standard Attribute (0040,034E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0354)": DicomTagDefinition(
        tag="(0040,0354)",
        group="0040",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_0040_0354_Keyword",
        name="DICOM Standard Attribute (0040,0354) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,035A)": DicomTagDefinition(
        tag="(0040,035A)",
        group="0040",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_0040_035A_Keyword",
        name="DICOM Standard Attribute (0040,035A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0360)": DicomTagDefinition(
        tag="(0040,0360)",
        group="0040",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_0040_0360_Keyword",
        name="DICOM Standard Attribute (0040,0360) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0366)": DicomTagDefinition(
        tag="(0040,0366)",
        group="0040",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_0040_0366_Keyword",
        name="DICOM Standard Attribute (0040,0366) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,036C)": DicomTagDefinition(
        tag="(0040,036C)",
        group="0040",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_0040_036C_Keyword",
        name="DICOM Standard Attribute (0040,036C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0372)": DicomTagDefinition(
        tag="(0040,0372)",
        group="0040",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_0040_0372_Keyword",
        name="DICOM Standard Attribute (0040,0372) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0378)": DicomTagDefinition(
        tag="(0040,0378)",
        group="0040",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_0040_0378_Keyword",
        name="DICOM Standard Attribute (0040,0378) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,037E)": DicomTagDefinition(
        tag="(0040,037E)",
        group="0040",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_0040_037E_Keyword",
        name="DICOM Standard Attribute (0040,037E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0384)": DicomTagDefinition(
        tag="(0040,0384)",
        group="0040",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_0040_0384_Keyword",
        name="DICOM Standard Attribute (0040,0384) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,038A)": DicomTagDefinition(
        tag="(0040,038A)",
        group="0040",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_0040_038A_Keyword",
        name="DICOM Standard Attribute (0040,038A) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0390)": DicomTagDefinition(
        tag="(0040,0390)",
        group="0040",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_0040_0390_Keyword",
        name="DICOM Standard Attribute (0040,0390) for Modality Worklist (MWL) & Procedures Specification",
        retired=True
    ),
    "(0040,0396)": DicomTagDefinition(
        tag="(0040,0396)",
        group="0040",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_0040_0396_Keyword",
        name="DICOM Standard Attribute (0040,0396) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,039C)": DicomTagDefinition(
        tag="(0040,039C)",
        group="0040",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_0040_039C_Keyword",
        name="DICOM Standard Attribute (0040,039C) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03A2)": DicomTagDefinition(
        tag="(0040,03A2)",
        group="0040",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_0040_03A2_Keyword",
        name="DICOM Standard Attribute (0040,03A2) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03A8)": DicomTagDefinition(
        tag="(0040,03A8)",
        group="0040",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_0040_03A8_Keyword",
        name="DICOM Standard Attribute (0040,03A8) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03AE)": DicomTagDefinition(
        tag="(0040,03AE)",
        group="0040",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_0040_03AE_Keyword",
        name="DICOM Standard Attribute (0040,03AE) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03B4)": DicomTagDefinition(
        tag="(0040,03B4)",
        group="0040",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_0040_03B4_Keyword",
        name="DICOM Standard Attribute (0040,03B4) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03BA)": DicomTagDefinition(
        tag="(0040,03BA)",
        group="0040",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_0040_03BA_Keyword",
        name="DICOM Standard Attribute (0040,03BA) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03C0)": DicomTagDefinition(
        tag="(0040,03C0)",
        group="0040",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_0040_03C0_Keyword",
        name="DICOM Standard Attribute (0040,03C0) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03C6)": DicomTagDefinition(
        tag="(0040,03C6)",
        group="0040",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_0040_03C6_Keyword",
        name="DICOM Standard Attribute (0040,03C6) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03CC)": DicomTagDefinition(
        tag="(0040,03CC)",
        group="0040",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_0040_03CC_Keyword",
        name="DICOM Standard Attribute (0040,03CC) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03D2)": DicomTagDefinition(
        tag="(0040,03D2)",
        group="0040",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_0040_03D2_Keyword",
        name="DICOM Standard Attribute (0040,03D2) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03D8)": DicomTagDefinition(
        tag="(0040,03D8)",
        group="0040",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_0040_03D8_Keyword",
        name="DICOM Standard Attribute (0040,03D8) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03DE)": DicomTagDefinition(
        tag="(0040,03DE)",
        group="0040",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_0040_03DE_Keyword",
        name="DICOM Standard Attribute (0040,03DE) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03E4)": DicomTagDefinition(
        tag="(0040,03E4)",
        group="0040",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_0040_03E4_Keyword",
        name="DICOM Standard Attribute (0040,03E4) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03EA)": DicomTagDefinition(
        tag="(0040,03EA)",
        group="0040",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_0040_03EA_Keyword",
        name="DICOM Standard Attribute (0040,03EA) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03F0)": DicomTagDefinition(
        tag="(0040,03F0)",
        group="0040",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_0040_03F0_Keyword",
        name="DICOM Standard Attribute (0040,03F0) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03F6)": DicomTagDefinition(
        tag="(0040,03F6)",
        group="0040",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_0040_03F6_Keyword",
        name="DICOM Standard Attribute (0040,03F6) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,03FC)": DicomTagDefinition(
        tag="(0040,03FC)",
        group="0040",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_0040_03FC_Keyword",
        name="DICOM Standard Attribute (0040,03FC) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0402)": DicomTagDefinition(
        tag="(0040,0402)",
        group="0040",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_0040_0402_Keyword",
        name="DICOM Standard Attribute (0040,0402) for Modality Worklist (MWL) & Procedures Specification",
        retired=True
    ),
    "(0040,0408)": DicomTagDefinition(
        tag="(0040,0408)",
        group="0040",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_0040_0408_Keyword",
        name="DICOM Standard Attribute (0040,0408) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,040E)": DicomTagDefinition(
        tag="(0040,040E)",
        group="0040",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_0040_040E_Keyword",
        name="DICOM Standard Attribute (0040,040E) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    "(0040,0414)": DicomTagDefinition(
        tag="(0040,0414)",
        group="0040",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_0040_0414_Keyword",
        name="DICOM Standard Attribute (0040,0414) for Modality Worklist (MWL) & Procedures Specification",
        retired=False
    ),
    # ========================================================
    # Section Group (0054): Nuclear Medicine & Molecular Imaging
    # ========================================================
    "(0054,0006)": DicomTagDefinition(
        tag="(0054,0006)",
        group="0054",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_0054_0006_Keyword",
        name="DICOM Standard Attribute (0054,0006) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,000C)": DicomTagDefinition(
        tag="(0054,000C)",
        group="0054",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_0054_000C_Keyword",
        name="DICOM Standard Attribute (0054,000C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0012)": DicomTagDefinition(
        tag="(0054,0012)",
        group="0054",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_0054_0012_Keyword",
        name="DICOM Standard Attribute (0054,0012) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0018)": DicomTagDefinition(
        tag="(0054,0018)",
        group="0054",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_0054_0018_Keyword",
        name="DICOM Standard Attribute (0054,0018) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,001E)": DicomTagDefinition(
        tag="(0054,001E)",
        group="0054",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_0054_001E_Keyword",
        name="DICOM Standard Attribute (0054,001E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0024)": DicomTagDefinition(
        tag="(0054,0024)",
        group="0054",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_0054_0024_Keyword",
        name="DICOM Standard Attribute (0054,0024) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,002A)": DicomTagDefinition(
        tag="(0054,002A)",
        group="0054",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_0054_002A_Keyword",
        name="DICOM Standard Attribute (0054,002A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0030)": DicomTagDefinition(
        tag="(0054,0030)",
        group="0054",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_0054_0030_Keyword",
        name="DICOM Standard Attribute (0054,0030) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0036)": DicomTagDefinition(
        tag="(0054,0036)",
        group="0054",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_0054_0036_Keyword",
        name="DICOM Standard Attribute (0054,0036) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,003C)": DicomTagDefinition(
        tag="(0054,003C)",
        group="0054",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_0054_003C_Keyword",
        name="DICOM Standard Attribute (0054,003C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0042)": DicomTagDefinition(
        tag="(0054,0042)",
        group="0054",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_0054_0042_Keyword",
        name="DICOM Standard Attribute (0054,0042) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0048)": DicomTagDefinition(
        tag="(0054,0048)",
        group="0054",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_0054_0048_Keyword",
        name="DICOM Standard Attribute (0054,0048) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,004E)": DicomTagDefinition(
        tag="(0054,004E)",
        group="0054",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_0054_004E_Keyword",
        name="DICOM Standard Attribute (0054,004E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0054)": DicomTagDefinition(
        tag="(0054,0054)",
        group="0054",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_0054_0054_Keyword",
        name="DICOM Standard Attribute (0054,0054) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,005A)": DicomTagDefinition(
        tag="(0054,005A)",
        group="0054",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_0054_005A_Keyword",
        name="DICOM Standard Attribute (0054,005A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0060)": DicomTagDefinition(
        tag="(0054,0060)",
        group="0054",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_0054_0060_Keyword",
        name="DICOM Standard Attribute (0054,0060) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0066)": DicomTagDefinition(
        tag="(0054,0066)",
        group="0054",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_0054_0066_Keyword",
        name="DICOM Standard Attribute (0054,0066) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,006C)": DicomTagDefinition(
        tag="(0054,006C)",
        group="0054",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_0054_006C_Keyword",
        name="DICOM Standard Attribute (0054,006C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0072)": DicomTagDefinition(
        tag="(0054,0072)",
        group="0054",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_0054_0072_Keyword",
        name="DICOM Standard Attribute (0054,0072) for Nuclear Medicine & Molecular Imaging Specification",
        retired=True
    ),
    "(0054,0078)": DicomTagDefinition(
        tag="(0054,0078)",
        group="0054",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_0054_0078_Keyword",
        name="DICOM Standard Attribute (0054,0078) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,007E)": DicomTagDefinition(
        tag="(0054,007E)",
        group="0054",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_0054_007E_Keyword",
        name="DICOM Standard Attribute (0054,007E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0084)": DicomTagDefinition(
        tag="(0054,0084)",
        group="0054",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_0054_0084_Keyword",
        name="DICOM Standard Attribute (0054,0084) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,008A)": DicomTagDefinition(
        tag="(0054,008A)",
        group="0054",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_0054_008A_Keyword",
        name="DICOM Standard Attribute (0054,008A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0090)": DicomTagDefinition(
        tag="(0054,0090)",
        group="0054",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_0054_0090_Keyword",
        name="DICOM Standard Attribute (0054,0090) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0096)": DicomTagDefinition(
        tag="(0054,0096)",
        group="0054",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_0054_0096_Keyword",
        name="DICOM Standard Attribute (0054,0096) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,009C)": DicomTagDefinition(
        tag="(0054,009C)",
        group="0054",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_0054_009C_Keyword",
        name="DICOM Standard Attribute (0054,009C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00A2)": DicomTagDefinition(
        tag="(0054,00A2)",
        group="0054",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_0054_00A2_Keyword",
        name="DICOM Standard Attribute (0054,00A2) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00A8)": DicomTagDefinition(
        tag="(0054,00A8)",
        group="0054",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_0054_00A8_Keyword",
        name="DICOM Standard Attribute (0054,00A8) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00AE)": DicomTagDefinition(
        tag="(0054,00AE)",
        group="0054",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_0054_00AE_Keyword",
        name="DICOM Standard Attribute (0054,00AE) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00B4)": DicomTagDefinition(
        tag="(0054,00B4)",
        group="0054",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_0054_00B4_Keyword",
        name="DICOM Standard Attribute (0054,00B4) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00BA)": DicomTagDefinition(
        tag="(0054,00BA)",
        group="0054",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0054_00BA_Keyword",
        name="DICOM Standard Attribute (0054,00BA) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00C0)": DicomTagDefinition(
        tag="(0054,00C0)",
        group="0054",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_0054_00C0_Keyword",
        name="DICOM Standard Attribute (0054,00C0) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00C6)": DicomTagDefinition(
        tag="(0054,00C6)",
        group="0054",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_0054_00C6_Keyword",
        name="DICOM Standard Attribute (0054,00C6) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00CC)": DicomTagDefinition(
        tag="(0054,00CC)",
        group="0054",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_0054_00CC_Keyword",
        name="DICOM Standard Attribute (0054,00CC) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00D2)": DicomTagDefinition(
        tag="(0054,00D2)",
        group="0054",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_0054_00D2_Keyword",
        name="DICOM Standard Attribute (0054,00D2) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00D8)": DicomTagDefinition(
        tag="(0054,00D8)",
        group="0054",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_0054_00D8_Keyword",
        name="DICOM Standard Attribute (0054,00D8) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00DE)": DicomTagDefinition(
        tag="(0054,00DE)",
        group="0054",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_0054_00DE_Keyword",
        name="DICOM Standard Attribute (0054,00DE) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00E4)": DicomTagDefinition(
        tag="(0054,00E4)",
        group="0054",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_0054_00E4_Keyword",
        name="DICOM Standard Attribute (0054,00E4) for Nuclear Medicine & Molecular Imaging Specification",
        retired=True
    ),
    "(0054,00EA)": DicomTagDefinition(
        tag="(0054,00EA)",
        group="0054",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_0054_00EA_Keyword",
        name="DICOM Standard Attribute (0054,00EA) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00F0)": DicomTagDefinition(
        tag="(0054,00F0)",
        group="0054",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_0054_00F0_Keyword",
        name="DICOM Standard Attribute (0054,00F0) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00F6)": DicomTagDefinition(
        tag="(0054,00F6)",
        group="0054",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_0054_00F6_Keyword",
        name="DICOM Standard Attribute (0054,00F6) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,00FC)": DicomTagDefinition(
        tag="(0054,00FC)",
        group="0054",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_0054_00FC_Keyword",
        name="DICOM Standard Attribute (0054,00FC) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0102)": DicomTagDefinition(
        tag="(0054,0102)",
        group="0054",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_0054_0102_Keyword",
        name="DICOM Standard Attribute (0054,0102) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0108)": DicomTagDefinition(
        tag="(0054,0108)",
        group="0054",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_0054_0108_Keyword",
        name="DICOM Standard Attribute (0054,0108) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,010E)": DicomTagDefinition(
        tag="(0054,010E)",
        group="0054",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_0054_010E_Keyword",
        name="DICOM Standard Attribute (0054,010E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0114)": DicomTagDefinition(
        tag="(0054,0114)",
        group="0054",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_0054_0114_Keyword",
        name="DICOM Standard Attribute (0054,0114) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,011A)": DicomTagDefinition(
        tag="(0054,011A)",
        group="0054",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_0054_011A_Keyword",
        name="DICOM Standard Attribute (0054,011A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0120)": DicomTagDefinition(
        tag="(0054,0120)",
        group="0054",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_0054_0120_Keyword",
        name="DICOM Standard Attribute (0054,0120) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0126)": DicomTagDefinition(
        tag="(0054,0126)",
        group="0054",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_0054_0126_Keyword",
        name="DICOM Standard Attribute (0054,0126) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,012C)": DicomTagDefinition(
        tag="(0054,012C)",
        group="0054",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_0054_012C_Keyword",
        name="DICOM Standard Attribute (0054,012C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0132)": DicomTagDefinition(
        tag="(0054,0132)",
        group="0054",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_0054_0132_Keyword",
        name="DICOM Standard Attribute (0054,0132) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0138)": DicomTagDefinition(
        tag="(0054,0138)",
        group="0054",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_0054_0138_Keyword",
        name="DICOM Standard Attribute (0054,0138) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,013E)": DicomTagDefinition(
        tag="(0054,013E)",
        group="0054",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_0054_013E_Keyword",
        name="DICOM Standard Attribute (0054,013E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0144)": DicomTagDefinition(
        tag="(0054,0144)",
        group="0054",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_0054_0144_Keyword",
        name="DICOM Standard Attribute (0054,0144) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,014A)": DicomTagDefinition(
        tag="(0054,014A)",
        group="0054",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_0054_014A_Keyword",
        name="DICOM Standard Attribute (0054,014A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0150)": DicomTagDefinition(
        tag="(0054,0150)",
        group="0054",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_0054_0150_Keyword",
        name="DICOM Standard Attribute (0054,0150) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0156)": DicomTagDefinition(
        tag="(0054,0156)",
        group="0054",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_0054_0156_Keyword",
        name="DICOM Standard Attribute (0054,0156) for Nuclear Medicine & Molecular Imaging Specification",
        retired=True
    ),
    "(0054,015C)": DicomTagDefinition(
        tag="(0054,015C)",
        group="0054",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_0054_015C_Keyword",
        name="DICOM Standard Attribute (0054,015C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0162)": DicomTagDefinition(
        tag="(0054,0162)",
        group="0054",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_0054_0162_Keyword",
        name="DICOM Standard Attribute (0054,0162) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0168)": DicomTagDefinition(
        tag="(0054,0168)",
        group="0054",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_0054_0168_Keyword",
        name="DICOM Standard Attribute (0054,0168) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,016E)": DicomTagDefinition(
        tag="(0054,016E)",
        group="0054",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_0054_016E_Keyword",
        name="DICOM Standard Attribute (0054,016E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0174)": DicomTagDefinition(
        tag="(0054,0174)",
        group="0054",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_0054_0174_Keyword",
        name="DICOM Standard Attribute (0054,0174) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,017A)": DicomTagDefinition(
        tag="(0054,017A)",
        group="0054",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_0054_017A_Keyword",
        name="DICOM Standard Attribute (0054,017A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0180)": DicomTagDefinition(
        tag="(0054,0180)",
        group="0054",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_0054_0180_Keyword",
        name="DICOM Standard Attribute (0054,0180) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0186)": DicomTagDefinition(
        tag="(0054,0186)",
        group="0054",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_0054_0186_Keyword",
        name="DICOM Standard Attribute (0054,0186) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,018C)": DicomTagDefinition(
        tag="(0054,018C)",
        group="0054",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_0054_018C_Keyword",
        name="DICOM Standard Attribute (0054,018C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0192)": DicomTagDefinition(
        tag="(0054,0192)",
        group="0054",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_0054_0192_Keyword",
        name="DICOM Standard Attribute (0054,0192) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0198)": DicomTagDefinition(
        tag="(0054,0198)",
        group="0054",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_0054_0198_Keyword",
        name="DICOM Standard Attribute (0054,0198) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,019E)": DicomTagDefinition(
        tag="(0054,019E)",
        group="0054",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_0054_019E_Keyword",
        name="DICOM Standard Attribute (0054,019E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01A4)": DicomTagDefinition(
        tag="(0054,01A4)",
        group="0054",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_0054_01A4_Keyword",
        name="DICOM Standard Attribute (0054,01A4) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01AA)": DicomTagDefinition(
        tag="(0054,01AA)",
        group="0054",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_0054_01AA_Keyword",
        name="DICOM Standard Attribute (0054,01AA) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01B0)": DicomTagDefinition(
        tag="(0054,01B0)",
        group="0054",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_0054_01B0_Keyword",
        name="DICOM Standard Attribute (0054,01B0) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01B6)": DicomTagDefinition(
        tag="(0054,01B6)",
        group="0054",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_0054_01B6_Keyword",
        name="DICOM Standard Attribute (0054,01B6) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01BC)": DicomTagDefinition(
        tag="(0054,01BC)",
        group="0054",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_0054_01BC_Keyword",
        name="DICOM Standard Attribute (0054,01BC) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01C2)": DicomTagDefinition(
        tag="(0054,01C2)",
        group="0054",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_0054_01C2_Keyword",
        name="DICOM Standard Attribute (0054,01C2) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01C8)": DicomTagDefinition(
        tag="(0054,01C8)",
        group="0054",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_0054_01C8_Keyword",
        name="DICOM Standard Attribute (0054,01C8) for Nuclear Medicine & Molecular Imaging Specification",
        retired=True
    ),
    "(0054,01CE)": DicomTagDefinition(
        tag="(0054,01CE)",
        group="0054",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_0054_01CE_Keyword",
        name="DICOM Standard Attribute (0054,01CE) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01D4)": DicomTagDefinition(
        tag="(0054,01D4)",
        group="0054",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_0054_01D4_Keyword",
        name="DICOM Standard Attribute (0054,01D4) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01DA)": DicomTagDefinition(
        tag="(0054,01DA)",
        group="0054",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_0054_01DA_Keyword",
        name="DICOM Standard Attribute (0054,01DA) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01E0)": DicomTagDefinition(
        tag="(0054,01E0)",
        group="0054",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_0054_01E0_Keyword",
        name="DICOM Standard Attribute (0054,01E0) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01E6)": DicomTagDefinition(
        tag="(0054,01E6)",
        group="0054",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_0054_01E6_Keyword",
        name="DICOM Standard Attribute (0054,01E6) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01EC)": DicomTagDefinition(
        tag="(0054,01EC)",
        group="0054",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_0054_01EC_Keyword",
        name="DICOM Standard Attribute (0054,01EC) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01F2)": DicomTagDefinition(
        tag="(0054,01F2)",
        group="0054",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_0054_01F2_Keyword",
        name="DICOM Standard Attribute (0054,01F2) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01F8)": DicomTagDefinition(
        tag="(0054,01F8)",
        group="0054",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_0054_01F8_Keyword",
        name="DICOM Standard Attribute (0054,01F8) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,01FE)": DicomTagDefinition(
        tag="(0054,01FE)",
        group="0054",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_0054_01FE_Keyword",
        name="DICOM Standard Attribute (0054,01FE) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0204)": DicomTagDefinition(
        tag="(0054,0204)",
        group="0054",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0054_0204_Keyword",
        name="DICOM Standard Attribute (0054,0204) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,020A)": DicomTagDefinition(
        tag="(0054,020A)",
        group="0054",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_0054_020A_Keyword",
        name="DICOM Standard Attribute (0054,020A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0210)": DicomTagDefinition(
        tag="(0054,0210)",
        group="0054",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_0054_0210_Keyword",
        name="DICOM Standard Attribute (0054,0210) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0216)": DicomTagDefinition(
        tag="(0054,0216)",
        group="0054",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_0054_0216_Keyword",
        name="DICOM Standard Attribute (0054,0216) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,021C)": DicomTagDefinition(
        tag="(0054,021C)",
        group="0054",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_0054_021C_Keyword",
        name="DICOM Standard Attribute (0054,021C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0222)": DicomTagDefinition(
        tag="(0054,0222)",
        group="0054",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_0054_0222_Keyword",
        name="DICOM Standard Attribute (0054,0222) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0228)": DicomTagDefinition(
        tag="(0054,0228)",
        group="0054",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_0054_0228_Keyword",
        name="DICOM Standard Attribute (0054,0228) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,022E)": DicomTagDefinition(
        tag="(0054,022E)",
        group="0054",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_0054_022E_Keyword",
        name="DICOM Standard Attribute (0054,022E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0234)": DicomTagDefinition(
        tag="(0054,0234)",
        group="0054",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_0054_0234_Keyword",
        name="DICOM Standard Attribute (0054,0234) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,023A)": DicomTagDefinition(
        tag="(0054,023A)",
        group="0054",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_0054_023A_Keyword",
        name="DICOM Standard Attribute (0054,023A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=True
    ),
    "(0054,0240)": DicomTagDefinition(
        tag="(0054,0240)",
        group="0054",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_0054_0240_Keyword",
        name="DICOM Standard Attribute (0054,0240) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0246)": DicomTagDefinition(
        tag="(0054,0246)",
        group="0054",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_0054_0246_Keyword",
        name="DICOM Standard Attribute (0054,0246) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,024C)": DicomTagDefinition(
        tag="(0054,024C)",
        group="0054",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_0054_024C_Keyword",
        name="DICOM Standard Attribute (0054,024C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0252)": DicomTagDefinition(
        tag="(0054,0252)",
        group="0054",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_0054_0252_Keyword",
        name="DICOM Standard Attribute (0054,0252) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0258)": DicomTagDefinition(
        tag="(0054,0258)",
        group="0054",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_0054_0258_Keyword",
        name="DICOM Standard Attribute (0054,0258) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,025E)": DicomTagDefinition(
        tag="(0054,025E)",
        group="0054",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_0054_025E_Keyword",
        name="DICOM Standard Attribute (0054,025E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0264)": DicomTagDefinition(
        tag="(0054,0264)",
        group="0054",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_0054_0264_Keyword",
        name="DICOM Standard Attribute (0054,0264) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,026A)": DicomTagDefinition(
        tag="(0054,026A)",
        group="0054",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_0054_026A_Keyword",
        name="DICOM Standard Attribute (0054,026A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0270)": DicomTagDefinition(
        tag="(0054,0270)",
        group="0054",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_0054_0270_Keyword",
        name="DICOM Standard Attribute (0054,0270) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0276)": DicomTagDefinition(
        tag="(0054,0276)",
        group="0054",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_0054_0276_Keyword",
        name="DICOM Standard Attribute (0054,0276) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,027C)": DicomTagDefinition(
        tag="(0054,027C)",
        group="0054",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_0054_027C_Keyword",
        name="DICOM Standard Attribute (0054,027C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0282)": DicomTagDefinition(
        tag="(0054,0282)",
        group="0054",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_0054_0282_Keyword",
        name="DICOM Standard Attribute (0054,0282) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0288)": DicomTagDefinition(
        tag="(0054,0288)",
        group="0054",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_0054_0288_Keyword",
        name="DICOM Standard Attribute (0054,0288) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,028E)": DicomTagDefinition(
        tag="(0054,028E)",
        group="0054",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_0054_028E_Keyword",
        name="DICOM Standard Attribute (0054,028E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0294)": DicomTagDefinition(
        tag="(0054,0294)",
        group="0054",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_0054_0294_Keyword",
        name="DICOM Standard Attribute (0054,0294) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,029A)": DicomTagDefinition(
        tag="(0054,029A)",
        group="0054",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_0054_029A_Keyword",
        name="DICOM Standard Attribute (0054,029A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02A0)": DicomTagDefinition(
        tag="(0054,02A0)",
        group="0054",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_0054_02A0_Keyword",
        name="DICOM Standard Attribute (0054,02A0) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02A6)": DicomTagDefinition(
        tag="(0054,02A6)",
        group="0054",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_0054_02A6_Keyword",
        name="DICOM Standard Attribute (0054,02A6) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02AC)": DicomTagDefinition(
        tag="(0054,02AC)",
        group="0054",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_0054_02AC_Keyword",
        name="DICOM Standard Attribute (0054,02AC) for Nuclear Medicine & Molecular Imaging Specification",
        retired=True
    ),
    "(0054,02B2)": DicomTagDefinition(
        tag="(0054,02B2)",
        group="0054",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_0054_02B2_Keyword",
        name="DICOM Standard Attribute (0054,02B2) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02B8)": DicomTagDefinition(
        tag="(0054,02B8)",
        group="0054",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_0054_02B8_Keyword",
        name="DICOM Standard Attribute (0054,02B8) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02BE)": DicomTagDefinition(
        tag="(0054,02BE)",
        group="0054",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_0054_02BE_Keyword",
        name="DICOM Standard Attribute (0054,02BE) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02C4)": DicomTagDefinition(
        tag="(0054,02C4)",
        group="0054",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_0054_02C4_Keyword",
        name="DICOM Standard Attribute (0054,02C4) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02CA)": DicomTagDefinition(
        tag="(0054,02CA)",
        group="0054",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_0054_02CA_Keyword",
        name="DICOM Standard Attribute (0054,02CA) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02D0)": DicomTagDefinition(
        tag="(0054,02D0)",
        group="0054",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_0054_02D0_Keyword",
        name="DICOM Standard Attribute (0054,02D0) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02D6)": DicomTagDefinition(
        tag="(0054,02D6)",
        group="0054",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_0054_02D6_Keyword",
        name="DICOM Standard Attribute (0054,02D6) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02DC)": DicomTagDefinition(
        tag="(0054,02DC)",
        group="0054",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_0054_02DC_Keyword",
        name="DICOM Standard Attribute (0054,02DC) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02E2)": DicomTagDefinition(
        tag="(0054,02E2)",
        group="0054",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_0054_02E2_Keyword",
        name="DICOM Standard Attribute (0054,02E2) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02E8)": DicomTagDefinition(
        tag="(0054,02E8)",
        group="0054",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_0054_02E8_Keyword",
        name="DICOM Standard Attribute (0054,02E8) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02EE)": DicomTagDefinition(
        tag="(0054,02EE)",
        group="0054",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_0054_02EE_Keyword",
        name="DICOM Standard Attribute (0054,02EE) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02F4)": DicomTagDefinition(
        tag="(0054,02F4)",
        group="0054",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_0054_02F4_Keyword",
        name="DICOM Standard Attribute (0054,02F4) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,02FA)": DicomTagDefinition(
        tag="(0054,02FA)",
        group="0054",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_0054_02FA_Keyword",
        name="DICOM Standard Attribute (0054,02FA) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0300)": DicomTagDefinition(
        tag="(0054,0300)",
        group="0054",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_0054_0300_Keyword",
        name="DICOM Standard Attribute (0054,0300) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0306)": DicomTagDefinition(
        tag="(0054,0306)",
        group="0054",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_0054_0306_Keyword",
        name="DICOM Standard Attribute (0054,0306) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,030C)": DicomTagDefinition(
        tag="(0054,030C)",
        group="0054",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_0054_030C_Keyword",
        name="DICOM Standard Attribute (0054,030C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0312)": DicomTagDefinition(
        tag="(0054,0312)",
        group="0054",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_0054_0312_Keyword",
        name="DICOM Standard Attribute (0054,0312) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0318)": DicomTagDefinition(
        tag="(0054,0318)",
        group="0054",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_0054_0318_Keyword",
        name="DICOM Standard Attribute (0054,0318) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,031E)": DicomTagDefinition(
        tag="(0054,031E)",
        group="0054",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_0054_031E_Keyword",
        name="DICOM Standard Attribute (0054,031E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=True
    ),
    "(0054,0324)": DicomTagDefinition(
        tag="(0054,0324)",
        group="0054",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_0054_0324_Keyword",
        name="DICOM Standard Attribute (0054,0324) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,032A)": DicomTagDefinition(
        tag="(0054,032A)",
        group="0054",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_0054_032A_Keyword",
        name="DICOM Standard Attribute (0054,032A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0330)": DicomTagDefinition(
        tag="(0054,0330)",
        group="0054",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_0054_0330_Keyword",
        name="DICOM Standard Attribute (0054,0330) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0336)": DicomTagDefinition(
        tag="(0054,0336)",
        group="0054",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_0054_0336_Keyword",
        name="DICOM Standard Attribute (0054,0336) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,033C)": DicomTagDefinition(
        tag="(0054,033C)",
        group="0054",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_0054_033C_Keyword",
        name="DICOM Standard Attribute (0054,033C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0342)": DicomTagDefinition(
        tag="(0054,0342)",
        group="0054",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_0054_0342_Keyword",
        name="DICOM Standard Attribute (0054,0342) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0348)": DicomTagDefinition(
        tag="(0054,0348)",
        group="0054",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_0054_0348_Keyword",
        name="DICOM Standard Attribute (0054,0348) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,034E)": DicomTagDefinition(
        tag="(0054,034E)",
        group="0054",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0054_034E_Keyword",
        name="DICOM Standard Attribute (0054,034E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0354)": DicomTagDefinition(
        tag="(0054,0354)",
        group="0054",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_0054_0354_Keyword",
        name="DICOM Standard Attribute (0054,0354) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,035A)": DicomTagDefinition(
        tag="(0054,035A)",
        group="0054",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_0054_035A_Keyword",
        name="DICOM Standard Attribute (0054,035A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0360)": DicomTagDefinition(
        tag="(0054,0360)",
        group="0054",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_0054_0360_Keyword",
        name="DICOM Standard Attribute (0054,0360) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0366)": DicomTagDefinition(
        tag="(0054,0366)",
        group="0054",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_0054_0366_Keyword",
        name="DICOM Standard Attribute (0054,0366) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,036C)": DicomTagDefinition(
        tag="(0054,036C)",
        group="0054",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_0054_036C_Keyword",
        name="DICOM Standard Attribute (0054,036C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0372)": DicomTagDefinition(
        tag="(0054,0372)",
        group="0054",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_0054_0372_Keyword",
        name="DICOM Standard Attribute (0054,0372) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0378)": DicomTagDefinition(
        tag="(0054,0378)",
        group="0054",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_0054_0378_Keyword",
        name="DICOM Standard Attribute (0054,0378) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,037E)": DicomTagDefinition(
        tag="(0054,037E)",
        group="0054",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_0054_037E_Keyword",
        name="DICOM Standard Attribute (0054,037E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0384)": DicomTagDefinition(
        tag="(0054,0384)",
        group="0054",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_0054_0384_Keyword",
        name="DICOM Standard Attribute (0054,0384) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,038A)": DicomTagDefinition(
        tag="(0054,038A)",
        group="0054",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_0054_038A_Keyword",
        name="DICOM Standard Attribute (0054,038A) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0390)": DicomTagDefinition(
        tag="(0054,0390)",
        group="0054",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_0054_0390_Keyword",
        name="DICOM Standard Attribute (0054,0390) for Nuclear Medicine & Molecular Imaging Specification",
        retired=True
    ),
    "(0054,0396)": DicomTagDefinition(
        tag="(0054,0396)",
        group="0054",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_0054_0396_Keyword",
        name="DICOM Standard Attribute (0054,0396) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,039C)": DicomTagDefinition(
        tag="(0054,039C)",
        group="0054",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_0054_039C_Keyword",
        name="DICOM Standard Attribute (0054,039C) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03A2)": DicomTagDefinition(
        tag="(0054,03A2)",
        group="0054",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_0054_03A2_Keyword",
        name="DICOM Standard Attribute (0054,03A2) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03A8)": DicomTagDefinition(
        tag="(0054,03A8)",
        group="0054",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_0054_03A8_Keyword",
        name="DICOM Standard Attribute (0054,03A8) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03AE)": DicomTagDefinition(
        tag="(0054,03AE)",
        group="0054",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_0054_03AE_Keyword",
        name="DICOM Standard Attribute (0054,03AE) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03B4)": DicomTagDefinition(
        tag="(0054,03B4)",
        group="0054",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_0054_03B4_Keyword",
        name="DICOM Standard Attribute (0054,03B4) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03BA)": DicomTagDefinition(
        tag="(0054,03BA)",
        group="0054",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_0054_03BA_Keyword",
        name="DICOM Standard Attribute (0054,03BA) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03C0)": DicomTagDefinition(
        tag="(0054,03C0)",
        group="0054",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_0054_03C0_Keyword",
        name="DICOM Standard Attribute (0054,03C0) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03C6)": DicomTagDefinition(
        tag="(0054,03C6)",
        group="0054",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_0054_03C6_Keyword",
        name="DICOM Standard Attribute (0054,03C6) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03CC)": DicomTagDefinition(
        tag="(0054,03CC)",
        group="0054",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_0054_03CC_Keyword",
        name="DICOM Standard Attribute (0054,03CC) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03D2)": DicomTagDefinition(
        tag="(0054,03D2)",
        group="0054",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_0054_03D2_Keyword",
        name="DICOM Standard Attribute (0054,03D2) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03D8)": DicomTagDefinition(
        tag="(0054,03D8)",
        group="0054",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_0054_03D8_Keyword",
        name="DICOM Standard Attribute (0054,03D8) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03DE)": DicomTagDefinition(
        tag="(0054,03DE)",
        group="0054",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_0054_03DE_Keyword",
        name="DICOM Standard Attribute (0054,03DE) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03E4)": DicomTagDefinition(
        tag="(0054,03E4)",
        group="0054",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_0054_03E4_Keyword",
        name="DICOM Standard Attribute (0054,03E4) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03EA)": DicomTagDefinition(
        tag="(0054,03EA)",
        group="0054",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_0054_03EA_Keyword",
        name="DICOM Standard Attribute (0054,03EA) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03F0)": DicomTagDefinition(
        tag="(0054,03F0)",
        group="0054",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_0054_03F0_Keyword",
        name="DICOM Standard Attribute (0054,03F0) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03F6)": DicomTagDefinition(
        tag="(0054,03F6)",
        group="0054",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_0054_03F6_Keyword",
        name="DICOM Standard Attribute (0054,03F6) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,03FC)": DicomTagDefinition(
        tag="(0054,03FC)",
        group="0054",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_0054_03FC_Keyword",
        name="DICOM Standard Attribute (0054,03FC) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0402)": DicomTagDefinition(
        tag="(0054,0402)",
        group="0054",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_0054_0402_Keyword",
        name="DICOM Standard Attribute (0054,0402) for Nuclear Medicine & Molecular Imaging Specification",
        retired=True
    ),
    "(0054,0408)": DicomTagDefinition(
        tag="(0054,0408)",
        group="0054",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_0054_0408_Keyword",
        name="DICOM Standard Attribute (0054,0408) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,040E)": DicomTagDefinition(
        tag="(0054,040E)",
        group="0054",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_0054_040E_Keyword",
        name="DICOM Standard Attribute (0054,040E) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    "(0054,0414)": DicomTagDefinition(
        tag="(0054,0414)",
        group="0054",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_0054_0414_Keyword",
        name="DICOM Standard Attribute (0054,0414) for Nuclear Medicine & Molecular Imaging Specification",
        retired=False
    ),
    # ========================================================
    # Section Group (0060): Digital Radiography Detectors
    # ========================================================
    "(0060,0006)": DicomTagDefinition(
        tag="(0060,0006)",
        group="0060",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_0060_0006_Keyword",
        name="DICOM Standard Attribute (0060,0006) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,000C)": DicomTagDefinition(
        tag="(0060,000C)",
        group="0060",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_0060_000C_Keyword",
        name="DICOM Standard Attribute (0060,000C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0012)": DicomTagDefinition(
        tag="(0060,0012)",
        group="0060",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_0060_0012_Keyword",
        name="DICOM Standard Attribute (0060,0012) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0018)": DicomTagDefinition(
        tag="(0060,0018)",
        group="0060",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_0060_0018_Keyword",
        name="DICOM Standard Attribute (0060,0018) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,001E)": DicomTagDefinition(
        tag="(0060,001E)",
        group="0060",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_0060_001E_Keyword",
        name="DICOM Standard Attribute (0060,001E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0024)": DicomTagDefinition(
        tag="(0060,0024)",
        group="0060",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_0060_0024_Keyword",
        name="DICOM Standard Attribute (0060,0024) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,002A)": DicomTagDefinition(
        tag="(0060,002A)",
        group="0060",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_0060_002A_Keyword",
        name="DICOM Standard Attribute (0060,002A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0030)": DicomTagDefinition(
        tag="(0060,0030)",
        group="0060",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_0060_0030_Keyword",
        name="DICOM Standard Attribute (0060,0030) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0036)": DicomTagDefinition(
        tag="(0060,0036)",
        group="0060",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_0060_0036_Keyword",
        name="DICOM Standard Attribute (0060,0036) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,003C)": DicomTagDefinition(
        tag="(0060,003C)",
        group="0060",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_0060_003C_Keyword",
        name="DICOM Standard Attribute (0060,003C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0042)": DicomTagDefinition(
        tag="(0060,0042)",
        group="0060",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_0060_0042_Keyword",
        name="DICOM Standard Attribute (0060,0042) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0048)": DicomTagDefinition(
        tag="(0060,0048)",
        group="0060",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_0060_0048_Keyword",
        name="DICOM Standard Attribute (0060,0048) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,004E)": DicomTagDefinition(
        tag="(0060,004E)",
        group="0060",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_0060_004E_Keyword",
        name="DICOM Standard Attribute (0060,004E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0054)": DicomTagDefinition(
        tag="(0060,0054)",
        group="0060",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_0060_0054_Keyword",
        name="DICOM Standard Attribute (0060,0054) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,005A)": DicomTagDefinition(
        tag="(0060,005A)",
        group="0060",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_0060_005A_Keyword",
        name="DICOM Standard Attribute (0060,005A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0060)": DicomTagDefinition(
        tag="(0060,0060)",
        group="0060",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_0060_0060_Keyword",
        name="DICOM Standard Attribute (0060,0060) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0066)": DicomTagDefinition(
        tag="(0060,0066)",
        group="0060",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_0060_0066_Keyword",
        name="DICOM Standard Attribute (0060,0066) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,006C)": DicomTagDefinition(
        tag="(0060,006C)",
        group="0060",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_0060_006C_Keyword",
        name="DICOM Standard Attribute (0060,006C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0072)": DicomTagDefinition(
        tag="(0060,0072)",
        group="0060",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_0060_0072_Keyword",
        name="DICOM Standard Attribute (0060,0072) for Digital Radiography Detectors Specification",
        retired=True
    ),
    "(0060,0078)": DicomTagDefinition(
        tag="(0060,0078)",
        group="0060",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_0060_0078_Keyword",
        name="DICOM Standard Attribute (0060,0078) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,007E)": DicomTagDefinition(
        tag="(0060,007E)",
        group="0060",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_0060_007E_Keyword",
        name="DICOM Standard Attribute (0060,007E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0084)": DicomTagDefinition(
        tag="(0060,0084)",
        group="0060",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_0060_0084_Keyword",
        name="DICOM Standard Attribute (0060,0084) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,008A)": DicomTagDefinition(
        tag="(0060,008A)",
        group="0060",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_0060_008A_Keyword",
        name="DICOM Standard Attribute (0060,008A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0090)": DicomTagDefinition(
        tag="(0060,0090)",
        group="0060",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_0060_0090_Keyword",
        name="DICOM Standard Attribute (0060,0090) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0096)": DicomTagDefinition(
        tag="(0060,0096)",
        group="0060",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_0060_0096_Keyword",
        name="DICOM Standard Attribute (0060,0096) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,009C)": DicomTagDefinition(
        tag="(0060,009C)",
        group="0060",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_0060_009C_Keyword",
        name="DICOM Standard Attribute (0060,009C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00A2)": DicomTagDefinition(
        tag="(0060,00A2)",
        group="0060",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_0060_00A2_Keyword",
        name="DICOM Standard Attribute (0060,00A2) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00A8)": DicomTagDefinition(
        tag="(0060,00A8)",
        group="0060",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_0060_00A8_Keyword",
        name="DICOM Standard Attribute (0060,00A8) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00AE)": DicomTagDefinition(
        tag="(0060,00AE)",
        group="0060",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_0060_00AE_Keyword",
        name="DICOM Standard Attribute (0060,00AE) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00B4)": DicomTagDefinition(
        tag="(0060,00B4)",
        group="0060",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_0060_00B4_Keyword",
        name="DICOM Standard Attribute (0060,00B4) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00BA)": DicomTagDefinition(
        tag="(0060,00BA)",
        group="0060",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0060_00BA_Keyword",
        name="DICOM Standard Attribute (0060,00BA) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00C0)": DicomTagDefinition(
        tag="(0060,00C0)",
        group="0060",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_0060_00C0_Keyword",
        name="DICOM Standard Attribute (0060,00C0) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00C6)": DicomTagDefinition(
        tag="(0060,00C6)",
        group="0060",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_0060_00C6_Keyword",
        name="DICOM Standard Attribute (0060,00C6) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00CC)": DicomTagDefinition(
        tag="(0060,00CC)",
        group="0060",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_0060_00CC_Keyword",
        name="DICOM Standard Attribute (0060,00CC) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00D2)": DicomTagDefinition(
        tag="(0060,00D2)",
        group="0060",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_0060_00D2_Keyword",
        name="DICOM Standard Attribute (0060,00D2) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00D8)": DicomTagDefinition(
        tag="(0060,00D8)",
        group="0060",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_0060_00D8_Keyword",
        name="DICOM Standard Attribute (0060,00D8) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00DE)": DicomTagDefinition(
        tag="(0060,00DE)",
        group="0060",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_0060_00DE_Keyword",
        name="DICOM Standard Attribute (0060,00DE) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00E4)": DicomTagDefinition(
        tag="(0060,00E4)",
        group="0060",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_0060_00E4_Keyword",
        name="DICOM Standard Attribute (0060,00E4) for Digital Radiography Detectors Specification",
        retired=True
    ),
    "(0060,00EA)": DicomTagDefinition(
        tag="(0060,00EA)",
        group="0060",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_0060_00EA_Keyword",
        name="DICOM Standard Attribute (0060,00EA) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00F0)": DicomTagDefinition(
        tag="(0060,00F0)",
        group="0060",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_0060_00F0_Keyword",
        name="DICOM Standard Attribute (0060,00F0) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00F6)": DicomTagDefinition(
        tag="(0060,00F6)",
        group="0060",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_0060_00F6_Keyword",
        name="DICOM Standard Attribute (0060,00F6) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,00FC)": DicomTagDefinition(
        tag="(0060,00FC)",
        group="0060",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_0060_00FC_Keyword",
        name="DICOM Standard Attribute (0060,00FC) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0102)": DicomTagDefinition(
        tag="(0060,0102)",
        group="0060",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_0060_0102_Keyword",
        name="DICOM Standard Attribute (0060,0102) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0108)": DicomTagDefinition(
        tag="(0060,0108)",
        group="0060",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_0060_0108_Keyword",
        name="DICOM Standard Attribute (0060,0108) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,010E)": DicomTagDefinition(
        tag="(0060,010E)",
        group="0060",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_0060_010E_Keyword",
        name="DICOM Standard Attribute (0060,010E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0114)": DicomTagDefinition(
        tag="(0060,0114)",
        group="0060",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_0060_0114_Keyword",
        name="DICOM Standard Attribute (0060,0114) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,011A)": DicomTagDefinition(
        tag="(0060,011A)",
        group="0060",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_0060_011A_Keyword",
        name="DICOM Standard Attribute (0060,011A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0120)": DicomTagDefinition(
        tag="(0060,0120)",
        group="0060",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_0060_0120_Keyword",
        name="DICOM Standard Attribute (0060,0120) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0126)": DicomTagDefinition(
        tag="(0060,0126)",
        group="0060",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_0060_0126_Keyword",
        name="DICOM Standard Attribute (0060,0126) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,012C)": DicomTagDefinition(
        tag="(0060,012C)",
        group="0060",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_0060_012C_Keyword",
        name="DICOM Standard Attribute (0060,012C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0132)": DicomTagDefinition(
        tag="(0060,0132)",
        group="0060",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_0060_0132_Keyword",
        name="DICOM Standard Attribute (0060,0132) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0138)": DicomTagDefinition(
        tag="(0060,0138)",
        group="0060",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_0060_0138_Keyword",
        name="DICOM Standard Attribute (0060,0138) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,013E)": DicomTagDefinition(
        tag="(0060,013E)",
        group="0060",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_0060_013E_Keyword",
        name="DICOM Standard Attribute (0060,013E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0144)": DicomTagDefinition(
        tag="(0060,0144)",
        group="0060",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_0060_0144_Keyword",
        name="DICOM Standard Attribute (0060,0144) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,014A)": DicomTagDefinition(
        tag="(0060,014A)",
        group="0060",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_0060_014A_Keyword",
        name="DICOM Standard Attribute (0060,014A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0150)": DicomTagDefinition(
        tag="(0060,0150)",
        group="0060",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_0060_0150_Keyword",
        name="DICOM Standard Attribute (0060,0150) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0156)": DicomTagDefinition(
        tag="(0060,0156)",
        group="0060",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_0060_0156_Keyword",
        name="DICOM Standard Attribute (0060,0156) for Digital Radiography Detectors Specification",
        retired=True
    ),
    "(0060,015C)": DicomTagDefinition(
        tag="(0060,015C)",
        group="0060",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_0060_015C_Keyword",
        name="DICOM Standard Attribute (0060,015C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0162)": DicomTagDefinition(
        tag="(0060,0162)",
        group="0060",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_0060_0162_Keyword",
        name="DICOM Standard Attribute (0060,0162) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0168)": DicomTagDefinition(
        tag="(0060,0168)",
        group="0060",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_0060_0168_Keyword",
        name="DICOM Standard Attribute (0060,0168) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,016E)": DicomTagDefinition(
        tag="(0060,016E)",
        group="0060",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_0060_016E_Keyword",
        name="DICOM Standard Attribute (0060,016E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0174)": DicomTagDefinition(
        tag="(0060,0174)",
        group="0060",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_0060_0174_Keyword",
        name="DICOM Standard Attribute (0060,0174) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,017A)": DicomTagDefinition(
        tag="(0060,017A)",
        group="0060",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_0060_017A_Keyword",
        name="DICOM Standard Attribute (0060,017A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0180)": DicomTagDefinition(
        tag="(0060,0180)",
        group="0060",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_0060_0180_Keyword",
        name="DICOM Standard Attribute (0060,0180) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0186)": DicomTagDefinition(
        tag="(0060,0186)",
        group="0060",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_0060_0186_Keyword",
        name="DICOM Standard Attribute (0060,0186) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,018C)": DicomTagDefinition(
        tag="(0060,018C)",
        group="0060",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_0060_018C_Keyword",
        name="DICOM Standard Attribute (0060,018C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0192)": DicomTagDefinition(
        tag="(0060,0192)",
        group="0060",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_0060_0192_Keyword",
        name="DICOM Standard Attribute (0060,0192) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0198)": DicomTagDefinition(
        tag="(0060,0198)",
        group="0060",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_0060_0198_Keyword",
        name="DICOM Standard Attribute (0060,0198) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,019E)": DicomTagDefinition(
        tag="(0060,019E)",
        group="0060",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_0060_019E_Keyword",
        name="DICOM Standard Attribute (0060,019E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01A4)": DicomTagDefinition(
        tag="(0060,01A4)",
        group="0060",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_0060_01A4_Keyword",
        name="DICOM Standard Attribute (0060,01A4) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01AA)": DicomTagDefinition(
        tag="(0060,01AA)",
        group="0060",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_0060_01AA_Keyword",
        name="DICOM Standard Attribute (0060,01AA) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01B0)": DicomTagDefinition(
        tag="(0060,01B0)",
        group="0060",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_0060_01B0_Keyword",
        name="DICOM Standard Attribute (0060,01B0) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01B6)": DicomTagDefinition(
        tag="(0060,01B6)",
        group="0060",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_0060_01B6_Keyword",
        name="DICOM Standard Attribute (0060,01B6) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01BC)": DicomTagDefinition(
        tag="(0060,01BC)",
        group="0060",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_0060_01BC_Keyword",
        name="DICOM Standard Attribute (0060,01BC) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01C2)": DicomTagDefinition(
        tag="(0060,01C2)",
        group="0060",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_0060_01C2_Keyword",
        name="DICOM Standard Attribute (0060,01C2) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01C8)": DicomTagDefinition(
        tag="(0060,01C8)",
        group="0060",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_0060_01C8_Keyword",
        name="DICOM Standard Attribute (0060,01C8) for Digital Radiography Detectors Specification",
        retired=True
    ),
    "(0060,01CE)": DicomTagDefinition(
        tag="(0060,01CE)",
        group="0060",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_0060_01CE_Keyword",
        name="DICOM Standard Attribute (0060,01CE) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01D4)": DicomTagDefinition(
        tag="(0060,01D4)",
        group="0060",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_0060_01D4_Keyword",
        name="DICOM Standard Attribute (0060,01D4) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01DA)": DicomTagDefinition(
        tag="(0060,01DA)",
        group="0060",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_0060_01DA_Keyword",
        name="DICOM Standard Attribute (0060,01DA) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01E0)": DicomTagDefinition(
        tag="(0060,01E0)",
        group="0060",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_0060_01E0_Keyword",
        name="DICOM Standard Attribute (0060,01E0) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01E6)": DicomTagDefinition(
        tag="(0060,01E6)",
        group="0060",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_0060_01E6_Keyword",
        name="DICOM Standard Attribute (0060,01E6) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01EC)": DicomTagDefinition(
        tag="(0060,01EC)",
        group="0060",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_0060_01EC_Keyword",
        name="DICOM Standard Attribute (0060,01EC) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01F2)": DicomTagDefinition(
        tag="(0060,01F2)",
        group="0060",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_0060_01F2_Keyword",
        name="DICOM Standard Attribute (0060,01F2) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01F8)": DicomTagDefinition(
        tag="(0060,01F8)",
        group="0060",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_0060_01F8_Keyword",
        name="DICOM Standard Attribute (0060,01F8) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,01FE)": DicomTagDefinition(
        tag="(0060,01FE)",
        group="0060",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_0060_01FE_Keyword",
        name="DICOM Standard Attribute (0060,01FE) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0204)": DicomTagDefinition(
        tag="(0060,0204)",
        group="0060",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0060_0204_Keyword",
        name="DICOM Standard Attribute (0060,0204) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,020A)": DicomTagDefinition(
        tag="(0060,020A)",
        group="0060",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_0060_020A_Keyword",
        name="DICOM Standard Attribute (0060,020A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0210)": DicomTagDefinition(
        tag="(0060,0210)",
        group="0060",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_0060_0210_Keyword",
        name="DICOM Standard Attribute (0060,0210) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0216)": DicomTagDefinition(
        tag="(0060,0216)",
        group="0060",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_0060_0216_Keyword",
        name="DICOM Standard Attribute (0060,0216) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,021C)": DicomTagDefinition(
        tag="(0060,021C)",
        group="0060",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_0060_021C_Keyword",
        name="DICOM Standard Attribute (0060,021C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0222)": DicomTagDefinition(
        tag="(0060,0222)",
        group="0060",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_0060_0222_Keyword",
        name="DICOM Standard Attribute (0060,0222) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0228)": DicomTagDefinition(
        tag="(0060,0228)",
        group="0060",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_0060_0228_Keyword",
        name="DICOM Standard Attribute (0060,0228) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,022E)": DicomTagDefinition(
        tag="(0060,022E)",
        group="0060",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_0060_022E_Keyword",
        name="DICOM Standard Attribute (0060,022E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0234)": DicomTagDefinition(
        tag="(0060,0234)",
        group="0060",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_0060_0234_Keyword",
        name="DICOM Standard Attribute (0060,0234) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,023A)": DicomTagDefinition(
        tag="(0060,023A)",
        group="0060",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_0060_023A_Keyword",
        name="DICOM Standard Attribute (0060,023A) for Digital Radiography Detectors Specification",
        retired=True
    ),
    "(0060,0240)": DicomTagDefinition(
        tag="(0060,0240)",
        group="0060",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_0060_0240_Keyword",
        name="DICOM Standard Attribute (0060,0240) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0246)": DicomTagDefinition(
        tag="(0060,0246)",
        group="0060",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_0060_0246_Keyword",
        name="DICOM Standard Attribute (0060,0246) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,024C)": DicomTagDefinition(
        tag="(0060,024C)",
        group="0060",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_0060_024C_Keyword",
        name="DICOM Standard Attribute (0060,024C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0252)": DicomTagDefinition(
        tag="(0060,0252)",
        group="0060",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_0060_0252_Keyword",
        name="DICOM Standard Attribute (0060,0252) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0258)": DicomTagDefinition(
        tag="(0060,0258)",
        group="0060",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_0060_0258_Keyword",
        name="DICOM Standard Attribute (0060,0258) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,025E)": DicomTagDefinition(
        tag="(0060,025E)",
        group="0060",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_0060_025E_Keyword",
        name="DICOM Standard Attribute (0060,025E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0264)": DicomTagDefinition(
        tag="(0060,0264)",
        group="0060",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_0060_0264_Keyword",
        name="DICOM Standard Attribute (0060,0264) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,026A)": DicomTagDefinition(
        tag="(0060,026A)",
        group="0060",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_0060_026A_Keyword",
        name="DICOM Standard Attribute (0060,026A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0270)": DicomTagDefinition(
        tag="(0060,0270)",
        group="0060",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_0060_0270_Keyword",
        name="DICOM Standard Attribute (0060,0270) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0276)": DicomTagDefinition(
        tag="(0060,0276)",
        group="0060",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_0060_0276_Keyword",
        name="DICOM Standard Attribute (0060,0276) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,027C)": DicomTagDefinition(
        tag="(0060,027C)",
        group="0060",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_0060_027C_Keyword",
        name="DICOM Standard Attribute (0060,027C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0282)": DicomTagDefinition(
        tag="(0060,0282)",
        group="0060",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_0060_0282_Keyword",
        name="DICOM Standard Attribute (0060,0282) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0288)": DicomTagDefinition(
        tag="(0060,0288)",
        group="0060",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_0060_0288_Keyword",
        name="DICOM Standard Attribute (0060,0288) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,028E)": DicomTagDefinition(
        tag="(0060,028E)",
        group="0060",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_0060_028E_Keyword",
        name="DICOM Standard Attribute (0060,028E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0294)": DicomTagDefinition(
        tag="(0060,0294)",
        group="0060",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_0060_0294_Keyword",
        name="DICOM Standard Attribute (0060,0294) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,029A)": DicomTagDefinition(
        tag="(0060,029A)",
        group="0060",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_0060_029A_Keyword",
        name="DICOM Standard Attribute (0060,029A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02A0)": DicomTagDefinition(
        tag="(0060,02A0)",
        group="0060",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_0060_02A0_Keyword",
        name="DICOM Standard Attribute (0060,02A0) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02A6)": DicomTagDefinition(
        tag="(0060,02A6)",
        group="0060",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_0060_02A6_Keyword",
        name="DICOM Standard Attribute (0060,02A6) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02AC)": DicomTagDefinition(
        tag="(0060,02AC)",
        group="0060",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_0060_02AC_Keyword",
        name="DICOM Standard Attribute (0060,02AC) for Digital Radiography Detectors Specification",
        retired=True
    ),
    "(0060,02B2)": DicomTagDefinition(
        tag="(0060,02B2)",
        group="0060",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_0060_02B2_Keyword",
        name="DICOM Standard Attribute (0060,02B2) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02B8)": DicomTagDefinition(
        tag="(0060,02B8)",
        group="0060",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_0060_02B8_Keyword",
        name="DICOM Standard Attribute (0060,02B8) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02BE)": DicomTagDefinition(
        tag="(0060,02BE)",
        group="0060",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_0060_02BE_Keyword",
        name="DICOM Standard Attribute (0060,02BE) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02C4)": DicomTagDefinition(
        tag="(0060,02C4)",
        group="0060",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_0060_02C4_Keyword",
        name="DICOM Standard Attribute (0060,02C4) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02CA)": DicomTagDefinition(
        tag="(0060,02CA)",
        group="0060",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_0060_02CA_Keyword",
        name="DICOM Standard Attribute (0060,02CA) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02D0)": DicomTagDefinition(
        tag="(0060,02D0)",
        group="0060",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_0060_02D0_Keyword",
        name="DICOM Standard Attribute (0060,02D0) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02D6)": DicomTagDefinition(
        tag="(0060,02D6)",
        group="0060",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_0060_02D6_Keyword",
        name="DICOM Standard Attribute (0060,02D6) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02DC)": DicomTagDefinition(
        tag="(0060,02DC)",
        group="0060",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_0060_02DC_Keyword",
        name="DICOM Standard Attribute (0060,02DC) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02E2)": DicomTagDefinition(
        tag="(0060,02E2)",
        group="0060",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_0060_02E2_Keyword",
        name="DICOM Standard Attribute (0060,02E2) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02E8)": DicomTagDefinition(
        tag="(0060,02E8)",
        group="0060",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_0060_02E8_Keyword",
        name="DICOM Standard Attribute (0060,02E8) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02EE)": DicomTagDefinition(
        tag="(0060,02EE)",
        group="0060",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_0060_02EE_Keyword",
        name="DICOM Standard Attribute (0060,02EE) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02F4)": DicomTagDefinition(
        tag="(0060,02F4)",
        group="0060",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_0060_02F4_Keyword",
        name="DICOM Standard Attribute (0060,02F4) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,02FA)": DicomTagDefinition(
        tag="(0060,02FA)",
        group="0060",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_0060_02FA_Keyword",
        name="DICOM Standard Attribute (0060,02FA) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0300)": DicomTagDefinition(
        tag="(0060,0300)",
        group="0060",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_0060_0300_Keyword",
        name="DICOM Standard Attribute (0060,0300) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0306)": DicomTagDefinition(
        tag="(0060,0306)",
        group="0060",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_0060_0306_Keyword",
        name="DICOM Standard Attribute (0060,0306) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,030C)": DicomTagDefinition(
        tag="(0060,030C)",
        group="0060",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_0060_030C_Keyword",
        name="DICOM Standard Attribute (0060,030C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0312)": DicomTagDefinition(
        tag="(0060,0312)",
        group="0060",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_0060_0312_Keyword",
        name="DICOM Standard Attribute (0060,0312) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0318)": DicomTagDefinition(
        tag="(0060,0318)",
        group="0060",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_0060_0318_Keyword",
        name="DICOM Standard Attribute (0060,0318) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,031E)": DicomTagDefinition(
        tag="(0060,031E)",
        group="0060",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_0060_031E_Keyword",
        name="DICOM Standard Attribute (0060,031E) for Digital Radiography Detectors Specification",
        retired=True
    ),
    "(0060,0324)": DicomTagDefinition(
        tag="(0060,0324)",
        group="0060",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_0060_0324_Keyword",
        name="DICOM Standard Attribute (0060,0324) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,032A)": DicomTagDefinition(
        tag="(0060,032A)",
        group="0060",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_0060_032A_Keyword",
        name="DICOM Standard Attribute (0060,032A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0330)": DicomTagDefinition(
        tag="(0060,0330)",
        group="0060",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_0060_0330_Keyword",
        name="DICOM Standard Attribute (0060,0330) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0336)": DicomTagDefinition(
        tag="(0060,0336)",
        group="0060",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_0060_0336_Keyword",
        name="DICOM Standard Attribute (0060,0336) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,033C)": DicomTagDefinition(
        tag="(0060,033C)",
        group="0060",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_0060_033C_Keyword",
        name="DICOM Standard Attribute (0060,033C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0342)": DicomTagDefinition(
        tag="(0060,0342)",
        group="0060",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_0060_0342_Keyword",
        name="DICOM Standard Attribute (0060,0342) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0348)": DicomTagDefinition(
        tag="(0060,0348)",
        group="0060",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_0060_0348_Keyword",
        name="DICOM Standard Attribute (0060,0348) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,034E)": DicomTagDefinition(
        tag="(0060,034E)",
        group="0060",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0060_034E_Keyword",
        name="DICOM Standard Attribute (0060,034E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0354)": DicomTagDefinition(
        tag="(0060,0354)",
        group="0060",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_0060_0354_Keyword",
        name="DICOM Standard Attribute (0060,0354) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,035A)": DicomTagDefinition(
        tag="(0060,035A)",
        group="0060",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_0060_035A_Keyword",
        name="DICOM Standard Attribute (0060,035A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0360)": DicomTagDefinition(
        tag="(0060,0360)",
        group="0060",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_0060_0360_Keyword",
        name="DICOM Standard Attribute (0060,0360) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0366)": DicomTagDefinition(
        tag="(0060,0366)",
        group="0060",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_0060_0366_Keyword",
        name="DICOM Standard Attribute (0060,0366) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,036C)": DicomTagDefinition(
        tag="(0060,036C)",
        group="0060",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_0060_036C_Keyword",
        name="DICOM Standard Attribute (0060,036C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0372)": DicomTagDefinition(
        tag="(0060,0372)",
        group="0060",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_0060_0372_Keyword",
        name="DICOM Standard Attribute (0060,0372) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0378)": DicomTagDefinition(
        tag="(0060,0378)",
        group="0060",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_0060_0378_Keyword",
        name="DICOM Standard Attribute (0060,0378) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,037E)": DicomTagDefinition(
        tag="(0060,037E)",
        group="0060",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_0060_037E_Keyword",
        name="DICOM Standard Attribute (0060,037E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0384)": DicomTagDefinition(
        tag="(0060,0384)",
        group="0060",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_0060_0384_Keyword",
        name="DICOM Standard Attribute (0060,0384) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,038A)": DicomTagDefinition(
        tag="(0060,038A)",
        group="0060",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_0060_038A_Keyword",
        name="DICOM Standard Attribute (0060,038A) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0390)": DicomTagDefinition(
        tag="(0060,0390)",
        group="0060",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_0060_0390_Keyword",
        name="DICOM Standard Attribute (0060,0390) for Digital Radiography Detectors Specification",
        retired=True
    ),
    "(0060,0396)": DicomTagDefinition(
        tag="(0060,0396)",
        group="0060",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_0060_0396_Keyword",
        name="DICOM Standard Attribute (0060,0396) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,039C)": DicomTagDefinition(
        tag="(0060,039C)",
        group="0060",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_0060_039C_Keyword",
        name="DICOM Standard Attribute (0060,039C) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03A2)": DicomTagDefinition(
        tag="(0060,03A2)",
        group="0060",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_0060_03A2_Keyword",
        name="DICOM Standard Attribute (0060,03A2) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03A8)": DicomTagDefinition(
        tag="(0060,03A8)",
        group="0060",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_0060_03A8_Keyword",
        name="DICOM Standard Attribute (0060,03A8) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03AE)": DicomTagDefinition(
        tag="(0060,03AE)",
        group="0060",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_0060_03AE_Keyword",
        name="DICOM Standard Attribute (0060,03AE) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03B4)": DicomTagDefinition(
        tag="(0060,03B4)",
        group="0060",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_0060_03B4_Keyword",
        name="DICOM Standard Attribute (0060,03B4) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03BA)": DicomTagDefinition(
        tag="(0060,03BA)",
        group="0060",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_0060_03BA_Keyword",
        name="DICOM Standard Attribute (0060,03BA) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03C0)": DicomTagDefinition(
        tag="(0060,03C0)",
        group="0060",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_0060_03C0_Keyword",
        name="DICOM Standard Attribute (0060,03C0) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03C6)": DicomTagDefinition(
        tag="(0060,03C6)",
        group="0060",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_0060_03C6_Keyword",
        name="DICOM Standard Attribute (0060,03C6) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03CC)": DicomTagDefinition(
        tag="(0060,03CC)",
        group="0060",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_0060_03CC_Keyword",
        name="DICOM Standard Attribute (0060,03CC) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03D2)": DicomTagDefinition(
        tag="(0060,03D2)",
        group="0060",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_0060_03D2_Keyword",
        name="DICOM Standard Attribute (0060,03D2) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03D8)": DicomTagDefinition(
        tag="(0060,03D8)",
        group="0060",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_0060_03D8_Keyword",
        name="DICOM Standard Attribute (0060,03D8) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03DE)": DicomTagDefinition(
        tag="(0060,03DE)",
        group="0060",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_0060_03DE_Keyword",
        name="DICOM Standard Attribute (0060,03DE) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03E4)": DicomTagDefinition(
        tag="(0060,03E4)",
        group="0060",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_0060_03E4_Keyword",
        name="DICOM Standard Attribute (0060,03E4) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03EA)": DicomTagDefinition(
        tag="(0060,03EA)",
        group="0060",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_0060_03EA_Keyword",
        name="DICOM Standard Attribute (0060,03EA) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03F0)": DicomTagDefinition(
        tag="(0060,03F0)",
        group="0060",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_0060_03F0_Keyword",
        name="DICOM Standard Attribute (0060,03F0) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03F6)": DicomTagDefinition(
        tag="(0060,03F6)",
        group="0060",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_0060_03F6_Keyword",
        name="DICOM Standard Attribute (0060,03F6) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,03FC)": DicomTagDefinition(
        tag="(0060,03FC)",
        group="0060",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_0060_03FC_Keyword",
        name="DICOM Standard Attribute (0060,03FC) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0402)": DicomTagDefinition(
        tag="(0060,0402)",
        group="0060",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_0060_0402_Keyword",
        name="DICOM Standard Attribute (0060,0402) for Digital Radiography Detectors Specification",
        retired=True
    ),
    "(0060,0408)": DicomTagDefinition(
        tag="(0060,0408)",
        group="0060",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_0060_0408_Keyword",
        name="DICOM Standard Attribute (0060,0408) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,040E)": DicomTagDefinition(
        tag="(0060,040E)",
        group="0060",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_0060_040E_Keyword",
        name="DICOM Standard Attribute (0060,040E) for Digital Radiography Detectors Specification",
        retired=False
    ),
    "(0060,0414)": DicomTagDefinition(
        tag="(0060,0414)",
        group="0060",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_0060_0414_Keyword",
        name="DICOM Standard Attribute (0060,0414) for Digital Radiography Detectors Specification",
        retired=False
    ),
    # ========================================================
    # Section Group (0070): Softcopy Presentation States
    # ========================================================
    "(0070,0006)": DicomTagDefinition(
        tag="(0070,0006)",
        group="0070",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_0070_0006_Keyword",
        name="DICOM Standard Attribute (0070,0006) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,000C)": DicomTagDefinition(
        tag="(0070,000C)",
        group="0070",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_0070_000C_Keyword",
        name="DICOM Standard Attribute (0070,000C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0012)": DicomTagDefinition(
        tag="(0070,0012)",
        group="0070",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_0070_0012_Keyword",
        name="DICOM Standard Attribute (0070,0012) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0018)": DicomTagDefinition(
        tag="(0070,0018)",
        group="0070",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_0070_0018_Keyword",
        name="DICOM Standard Attribute (0070,0018) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,001E)": DicomTagDefinition(
        tag="(0070,001E)",
        group="0070",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_0070_001E_Keyword",
        name="DICOM Standard Attribute (0070,001E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0024)": DicomTagDefinition(
        tag="(0070,0024)",
        group="0070",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_0070_0024_Keyword",
        name="DICOM Standard Attribute (0070,0024) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,002A)": DicomTagDefinition(
        tag="(0070,002A)",
        group="0070",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_0070_002A_Keyword",
        name="DICOM Standard Attribute (0070,002A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0030)": DicomTagDefinition(
        tag="(0070,0030)",
        group="0070",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_0070_0030_Keyword",
        name="DICOM Standard Attribute (0070,0030) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0036)": DicomTagDefinition(
        tag="(0070,0036)",
        group="0070",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_0070_0036_Keyword",
        name="DICOM Standard Attribute (0070,0036) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,003C)": DicomTagDefinition(
        tag="(0070,003C)",
        group="0070",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_0070_003C_Keyword",
        name="DICOM Standard Attribute (0070,003C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0042)": DicomTagDefinition(
        tag="(0070,0042)",
        group="0070",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_0070_0042_Keyword",
        name="DICOM Standard Attribute (0070,0042) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0048)": DicomTagDefinition(
        tag="(0070,0048)",
        group="0070",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_0070_0048_Keyword",
        name="DICOM Standard Attribute (0070,0048) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,004E)": DicomTagDefinition(
        tag="(0070,004E)",
        group="0070",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_0070_004E_Keyword",
        name="DICOM Standard Attribute (0070,004E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0054)": DicomTagDefinition(
        tag="(0070,0054)",
        group="0070",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_0070_0054_Keyword",
        name="DICOM Standard Attribute (0070,0054) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,005A)": DicomTagDefinition(
        tag="(0070,005A)",
        group="0070",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_0070_005A_Keyword",
        name="DICOM Standard Attribute (0070,005A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0060)": DicomTagDefinition(
        tag="(0070,0060)",
        group="0070",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_0070_0060_Keyword",
        name="DICOM Standard Attribute (0070,0060) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0066)": DicomTagDefinition(
        tag="(0070,0066)",
        group="0070",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_0070_0066_Keyword",
        name="DICOM Standard Attribute (0070,0066) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,006C)": DicomTagDefinition(
        tag="(0070,006C)",
        group="0070",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_0070_006C_Keyword",
        name="DICOM Standard Attribute (0070,006C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0072)": DicomTagDefinition(
        tag="(0070,0072)",
        group="0070",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_0070_0072_Keyword",
        name="DICOM Standard Attribute (0070,0072) for Softcopy Presentation States Specification",
        retired=True
    ),
    "(0070,0078)": DicomTagDefinition(
        tag="(0070,0078)",
        group="0070",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_0070_0078_Keyword",
        name="DICOM Standard Attribute (0070,0078) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,007E)": DicomTagDefinition(
        tag="(0070,007E)",
        group="0070",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_0070_007E_Keyword",
        name="DICOM Standard Attribute (0070,007E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0084)": DicomTagDefinition(
        tag="(0070,0084)",
        group="0070",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_0070_0084_Keyword",
        name="DICOM Standard Attribute (0070,0084) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,008A)": DicomTagDefinition(
        tag="(0070,008A)",
        group="0070",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_0070_008A_Keyword",
        name="DICOM Standard Attribute (0070,008A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0090)": DicomTagDefinition(
        tag="(0070,0090)",
        group="0070",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_0070_0090_Keyword",
        name="DICOM Standard Attribute (0070,0090) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0096)": DicomTagDefinition(
        tag="(0070,0096)",
        group="0070",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_0070_0096_Keyword",
        name="DICOM Standard Attribute (0070,0096) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,009C)": DicomTagDefinition(
        tag="(0070,009C)",
        group="0070",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_0070_009C_Keyword",
        name="DICOM Standard Attribute (0070,009C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00A2)": DicomTagDefinition(
        tag="(0070,00A2)",
        group="0070",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_0070_00A2_Keyword",
        name="DICOM Standard Attribute (0070,00A2) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00A8)": DicomTagDefinition(
        tag="(0070,00A8)",
        group="0070",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_0070_00A8_Keyword",
        name="DICOM Standard Attribute (0070,00A8) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00AE)": DicomTagDefinition(
        tag="(0070,00AE)",
        group="0070",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_0070_00AE_Keyword",
        name="DICOM Standard Attribute (0070,00AE) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00B4)": DicomTagDefinition(
        tag="(0070,00B4)",
        group="0070",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_0070_00B4_Keyword",
        name="DICOM Standard Attribute (0070,00B4) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00BA)": DicomTagDefinition(
        tag="(0070,00BA)",
        group="0070",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0070_00BA_Keyword",
        name="DICOM Standard Attribute (0070,00BA) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00C0)": DicomTagDefinition(
        tag="(0070,00C0)",
        group="0070",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_0070_00C0_Keyword",
        name="DICOM Standard Attribute (0070,00C0) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00C6)": DicomTagDefinition(
        tag="(0070,00C6)",
        group="0070",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_0070_00C6_Keyword",
        name="DICOM Standard Attribute (0070,00C6) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00CC)": DicomTagDefinition(
        tag="(0070,00CC)",
        group="0070",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_0070_00CC_Keyword",
        name="DICOM Standard Attribute (0070,00CC) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00D2)": DicomTagDefinition(
        tag="(0070,00D2)",
        group="0070",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_0070_00D2_Keyword",
        name="DICOM Standard Attribute (0070,00D2) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00D8)": DicomTagDefinition(
        tag="(0070,00D8)",
        group="0070",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_0070_00D8_Keyword",
        name="DICOM Standard Attribute (0070,00D8) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00DE)": DicomTagDefinition(
        tag="(0070,00DE)",
        group="0070",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_0070_00DE_Keyword",
        name="DICOM Standard Attribute (0070,00DE) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00E4)": DicomTagDefinition(
        tag="(0070,00E4)",
        group="0070",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_0070_00E4_Keyword",
        name="DICOM Standard Attribute (0070,00E4) for Softcopy Presentation States Specification",
        retired=True
    ),
    "(0070,00EA)": DicomTagDefinition(
        tag="(0070,00EA)",
        group="0070",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_0070_00EA_Keyword",
        name="DICOM Standard Attribute (0070,00EA) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00F0)": DicomTagDefinition(
        tag="(0070,00F0)",
        group="0070",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_0070_00F0_Keyword",
        name="DICOM Standard Attribute (0070,00F0) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00F6)": DicomTagDefinition(
        tag="(0070,00F6)",
        group="0070",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_0070_00F6_Keyword",
        name="DICOM Standard Attribute (0070,00F6) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,00FC)": DicomTagDefinition(
        tag="(0070,00FC)",
        group="0070",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_0070_00FC_Keyword",
        name="DICOM Standard Attribute (0070,00FC) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0102)": DicomTagDefinition(
        tag="(0070,0102)",
        group="0070",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_0070_0102_Keyword",
        name="DICOM Standard Attribute (0070,0102) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0108)": DicomTagDefinition(
        tag="(0070,0108)",
        group="0070",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_0070_0108_Keyword",
        name="DICOM Standard Attribute (0070,0108) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,010E)": DicomTagDefinition(
        tag="(0070,010E)",
        group="0070",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_0070_010E_Keyword",
        name="DICOM Standard Attribute (0070,010E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0114)": DicomTagDefinition(
        tag="(0070,0114)",
        group="0070",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_0070_0114_Keyword",
        name="DICOM Standard Attribute (0070,0114) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,011A)": DicomTagDefinition(
        tag="(0070,011A)",
        group="0070",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_0070_011A_Keyword",
        name="DICOM Standard Attribute (0070,011A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0120)": DicomTagDefinition(
        tag="(0070,0120)",
        group="0070",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_0070_0120_Keyword",
        name="DICOM Standard Attribute (0070,0120) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0126)": DicomTagDefinition(
        tag="(0070,0126)",
        group="0070",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_0070_0126_Keyword",
        name="DICOM Standard Attribute (0070,0126) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,012C)": DicomTagDefinition(
        tag="(0070,012C)",
        group="0070",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_0070_012C_Keyword",
        name="DICOM Standard Attribute (0070,012C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0132)": DicomTagDefinition(
        tag="(0070,0132)",
        group="0070",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_0070_0132_Keyword",
        name="DICOM Standard Attribute (0070,0132) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0138)": DicomTagDefinition(
        tag="(0070,0138)",
        group="0070",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_0070_0138_Keyword",
        name="DICOM Standard Attribute (0070,0138) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,013E)": DicomTagDefinition(
        tag="(0070,013E)",
        group="0070",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_0070_013E_Keyword",
        name="DICOM Standard Attribute (0070,013E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0144)": DicomTagDefinition(
        tag="(0070,0144)",
        group="0070",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_0070_0144_Keyword",
        name="DICOM Standard Attribute (0070,0144) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,014A)": DicomTagDefinition(
        tag="(0070,014A)",
        group="0070",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_0070_014A_Keyword",
        name="DICOM Standard Attribute (0070,014A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0150)": DicomTagDefinition(
        tag="(0070,0150)",
        group="0070",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_0070_0150_Keyword",
        name="DICOM Standard Attribute (0070,0150) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0156)": DicomTagDefinition(
        tag="(0070,0156)",
        group="0070",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_0070_0156_Keyword",
        name="DICOM Standard Attribute (0070,0156) for Softcopy Presentation States Specification",
        retired=True
    ),
    "(0070,015C)": DicomTagDefinition(
        tag="(0070,015C)",
        group="0070",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_0070_015C_Keyword",
        name="DICOM Standard Attribute (0070,015C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0162)": DicomTagDefinition(
        tag="(0070,0162)",
        group="0070",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_0070_0162_Keyword",
        name="DICOM Standard Attribute (0070,0162) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0168)": DicomTagDefinition(
        tag="(0070,0168)",
        group="0070",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_0070_0168_Keyword",
        name="DICOM Standard Attribute (0070,0168) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,016E)": DicomTagDefinition(
        tag="(0070,016E)",
        group="0070",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_0070_016E_Keyword",
        name="DICOM Standard Attribute (0070,016E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0174)": DicomTagDefinition(
        tag="(0070,0174)",
        group="0070",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_0070_0174_Keyword",
        name="DICOM Standard Attribute (0070,0174) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,017A)": DicomTagDefinition(
        tag="(0070,017A)",
        group="0070",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_0070_017A_Keyword",
        name="DICOM Standard Attribute (0070,017A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0180)": DicomTagDefinition(
        tag="(0070,0180)",
        group="0070",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_0070_0180_Keyword",
        name="DICOM Standard Attribute (0070,0180) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0186)": DicomTagDefinition(
        tag="(0070,0186)",
        group="0070",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_0070_0186_Keyword",
        name="DICOM Standard Attribute (0070,0186) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,018C)": DicomTagDefinition(
        tag="(0070,018C)",
        group="0070",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_0070_018C_Keyword",
        name="DICOM Standard Attribute (0070,018C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0192)": DicomTagDefinition(
        tag="(0070,0192)",
        group="0070",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_0070_0192_Keyword",
        name="DICOM Standard Attribute (0070,0192) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0198)": DicomTagDefinition(
        tag="(0070,0198)",
        group="0070",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_0070_0198_Keyword",
        name="DICOM Standard Attribute (0070,0198) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,019E)": DicomTagDefinition(
        tag="(0070,019E)",
        group="0070",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_0070_019E_Keyword",
        name="DICOM Standard Attribute (0070,019E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01A4)": DicomTagDefinition(
        tag="(0070,01A4)",
        group="0070",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_0070_01A4_Keyword",
        name="DICOM Standard Attribute (0070,01A4) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01AA)": DicomTagDefinition(
        tag="(0070,01AA)",
        group="0070",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_0070_01AA_Keyword",
        name="DICOM Standard Attribute (0070,01AA) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01B0)": DicomTagDefinition(
        tag="(0070,01B0)",
        group="0070",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_0070_01B0_Keyword",
        name="DICOM Standard Attribute (0070,01B0) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01B6)": DicomTagDefinition(
        tag="(0070,01B6)",
        group="0070",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_0070_01B6_Keyword",
        name="DICOM Standard Attribute (0070,01B6) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01BC)": DicomTagDefinition(
        tag="(0070,01BC)",
        group="0070",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_0070_01BC_Keyword",
        name="DICOM Standard Attribute (0070,01BC) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01C2)": DicomTagDefinition(
        tag="(0070,01C2)",
        group="0070",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_0070_01C2_Keyword",
        name="DICOM Standard Attribute (0070,01C2) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01C8)": DicomTagDefinition(
        tag="(0070,01C8)",
        group="0070",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_0070_01C8_Keyword",
        name="DICOM Standard Attribute (0070,01C8) for Softcopy Presentation States Specification",
        retired=True
    ),
    "(0070,01CE)": DicomTagDefinition(
        tag="(0070,01CE)",
        group="0070",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_0070_01CE_Keyword",
        name="DICOM Standard Attribute (0070,01CE) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01D4)": DicomTagDefinition(
        tag="(0070,01D4)",
        group="0070",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_0070_01D4_Keyword",
        name="DICOM Standard Attribute (0070,01D4) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01DA)": DicomTagDefinition(
        tag="(0070,01DA)",
        group="0070",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_0070_01DA_Keyword",
        name="DICOM Standard Attribute (0070,01DA) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01E0)": DicomTagDefinition(
        tag="(0070,01E0)",
        group="0070",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_0070_01E0_Keyword",
        name="DICOM Standard Attribute (0070,01E0) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01E6)": DicomTagDefinition(
        tag="(0070,01E6)",
        group="0070",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_0070_01E6_Keyword",
        name="DICOM Standard Attribute (0070,01E6) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01EC)": DicomTagDefinition(
        tag="(0070,01EC)",
        group="0070",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_0070_01EC_Keyword",
        name="DICOM Standard Attribute (0070,01EC) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01F2)": DicomTagDefinition(
        tag="(0070,01F2)",
        group="0070",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_0070_01F2_Keyword",
        name="DICOM Standard Attribute (0070,01F2) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01F8)": DicomTagDefinition(
        tag="(0070,01F8)",
        group="0070",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_0070_01F8_Keyword",
        name="DICOM Standard Attribute (0070,01F8) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,01FE)": DicomTagDefinition(
        tag="(0070,01FE)",
        group="0070",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_0070_01FE_Keyword",
        name="DICOM Standard Attribute (0070,01FE) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0204)": DicomTagDefinition(
        tag="(0070,0204)",
        group="0070",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0070_0204_Keyword",
        name="DICOM Standard Attribute (0070,0204) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,020A)": DicomTagDefinition(
        tag="(0070,020A)",
        group="0070",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_0070_020A_Keyword",
        name="DICOM Standard Attribute (0070,020A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0210)": DicomTagDefinition(
        tag="(0070,0210)",
        group="0070",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_0070_0210_Keyword",
        name="DICOM Standard Attribute (0070,0210) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0216)": DicomTagDefinition(
        tag="(0070,0216)",
        group="0070",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_0070_0216_Keyword",
        name="DICOM Standard Attribute (0070,0216) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,021C)": DicomTagDefinition(
        tag="(0070,021C)",
        group="0070",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_0070_021C_Keyword",
        name="DICOM Standard Attribute (0070,021C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0222)": DicomTagDefinition(
        tag="(0070,0222)",
        group="0070",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_0070_0222_Keyword",
        name="DICOM Standard Attribute (0070,0222) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0228)": DicomTagDefinition(
        tag="(0070,0228)",
        group="0070",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_0070_0228_Keyword",
        name="DICOM Standard Attribute (0070,0228) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,022E)": DicomTagDefinition(
        tag="(0070,022E)",
        group="0070",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_0070_022E_Keyword",
        name="DICOM Standard Attribute (0070,022E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0234)": DicomTagDefinition(
        tag="(0070,0234)",
        group="0070",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_0070_0234_Keyword",
        name="DICOM Standard Attribute (0070,0234) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,023A)": DicomTagDefinition(
        tag="(0070,023A)",
        group="0070",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_0070_023A_Keyword",
        name="DICOM Standard Attribute (0070,023A) for Softcopy Presentation States Specification",
        retired=True
    ),
    "(0070,0240)": DicomTagDefinition(
        tag="(0070,0240)",
        group="0070",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_0070_0240_Keyword",
        name="DICOM Standard Attribute (0070,0240) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0246)": DicomTagDefinition(
        tag="(0070,0246)",
        group="0070",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_0070_0246_Keyword",
        name="DICOM Standard Attribute (0070,0246) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,024C)": DicomTagDefinition(
        tag="(0070,024C)",
        group="0070",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_0070_024C_Keyword",
        name="DICOM Standard Attribute (0070,024C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0252)": DicomTagDefinition(
        tag="(0070,0252)",
        group="0070",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_0070_0252_Keyword",
        name="DICOM Standard Attribute (0070,0252) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0258)": DicomTagDefinition(
        tag="(0070,0258)",
        group="0070",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_0070_0258_Keyword",
        name="DICOM Standard Attribute (0070,0258) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,025E)": DicomTagDefinition(
        tag="(0070,025E)",
        group="0070",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_0070_025E_Keyword",
        name="DICOM Standard Attribute (0070,025E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0264)": DicomTagDefinition(
        tag="(0070,0264)",
        group="0070",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_0070_0264_Keyword",
        name="DICOM Standard Attribute (0070,0264) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,026A)": DicomTagDefinition(
        tag="(0070,026A)",
        group="0070",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_0070_026A_Keyword",
        name="DICOM Standard Attribute (0070,026A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0270)": DicomTagDefinition(
        tag="(0070,0270)",
        group="0070",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_0070_0270_Keyword",
        name="DICOM Standard Attribute (0070,0270) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0276)": DicomTagDefinition(
        tag="(0070,0276)",
        group="0070",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_0070_0276_Keyword",
        name="DICOM Standard Attribute (0070,0276) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,027C)": DicomTagDefinition(
        tag="(0070,027C)",
        group="0070",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_0070_027C_Keyword",
        name="DICOM Standard Attribute (0070,027C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0282)": DicomTagDefinition(
        tag="(0070,0282)",
        group="0070",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_0070_0282_Keyword",
        name="DICOM Standard Attribute (0070,0282) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0288)": DicomTagDefinition(
        tag="(0070,0288)",
        group="0070",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_0070_0288_Keyword",
        name="DICOM Standard Attribute (0070,0288) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,028E)": DicomTagDefinition(
        tag="(0070,028E)",
        group="0070",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_0070_028E_Keyword",
        name="DICOM Standard Attribute (0070,028E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0294)": DicomTagDefinition(
        tag="(0070,0294)",
        group="0070",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_0070_0294_Keyword",
        name="DICOM Standard Attribute (0070,0294) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,029A)": DicomTagDefinition(
        tag="(0070,029A)",
        group="0070",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_0070_029A_Keyword",
        name="DICOM Standard Attribute (0070,029A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02A0)": DicomTagDefinition(
        tag="(0070,02A0)",
        group="0070",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_0070_02A0_Keyword",
        name="DICOM Standard Attribute (0070,02A0) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02A6)": DicomTagDefinition(
        tag="(0070,02A6)",
        group="0070",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_0070_02A6_Keyword",
        name="DICOM Standard Attribute (0070,02A6) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02AC)": DicomTagDefinition(
        tag="(0070,02AC)",
        group="0070",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_0070_02AC_Keyword",
        name="DICOM Standard Attribute (0070,02AC) for Softcopy Presentation States Specification",
        retired=True
    ),
    "(0070,02B2)": DicomTagDefinition(
        tag="(0070,02B2)",
        group="0070",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_0070_02B2_Keyword",
        name="DICOM Standard Attribute (0070,02B2) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02B8)": DicomTagDefinition(
        tag="(0070,02B8)",
        group="0070",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_0070_02B8_Keyword",
        name="DICOM Standard Attribute (0070,02B8) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02BE)": DicomTagDefinition(
        tag="(0070,02BE)",
        group="0070",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_0070_02BE_Keyword",
        name="DICOM Standard Attribute (0070,02BE) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02C4)": DicomTagDefinition(
        tag="(0070,02C4)",
        group="0070",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_0070_02C4_Keyword",
        name="DICOM Standard Attribute (0070,02C4) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02CA)": DicomTagDefinition(
        tag="(0070,02CA)",
        group="0070",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_0070_02CA_Keyword",
        name="DICOM Standard Attribute (0070,02CA) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02D0)": DicomTagDefinition(
        tag="(0070,02D0)",
        group="0070",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_0070_02D0_Keyword",
        name="DICOM Standard Attribute (0070,02D0) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02D6)": DicomTagDefinition(
        tag="(0070,02D6)",
        group="0070",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_0070_02D6_Keyword",
        name="DICOM Standard Attribute (0070,02D6) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02DC)": DicomTagDefinition(
        tag="(0070,02DC)",
        group="0070",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_0070_02DC_Keyword",
        name="DICOM Standard Attribute (0070,02DC) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02E2)": DicomTagDefinition(
        tag="(0070,02E2)",
        group="0070",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_0070_02E2_Keyword",
        name="DICOM Standard Attribute (0070,02E2) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02E8)": DicomTagDefinition(
        tag="(0070,02E8)",
        group="0070",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_0070_02E8_Keyword",
        name="DICOM Standard Attribute (0070,02E8) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02EE)": DicomTagDefinition(
        tag="(0070,02EE)",
        group="0070",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_0070_02EE_Keyword",
        name="DICOM Standard Attribute (0070,02EE) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02F4)": DicomTagDefinition(
        tag="(0070,02F4)",
        group="0070",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_0070_02F4_Keyword",
        name="DICOM Standard Attribute (0070,02F4) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,02FA)": DicomTagDefinition(
        tag="(0070,02FA)",
        group="0070",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_0070_02FA_Keyword",
        name="DICOM Standard Attribute (0070,02FA) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0300)": DicomTagDefinition(
        tag="(0070,0300)",
        group="0070",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_0070_0300_Keyword",
        name="DICOM Standard Attribute (0070,0300) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0306)": DicomTagDefinition(
        tag="(0070,0306)",
        group="0070",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_0070_0306_Keyword",
        name="DICOM Standard Attribute (0070,0306) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,030C)": DicomTagDefinition(
        tag="(0070,030C)",
        group="0070",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_0070_030C_Keyword",
        name="DICOM Standard Attribute (0070,030C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0312)": DicomTagDefinition(
        tag="(0070,0312)",
        group="0070",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_0070_0312_Keyword",
        name="DICOM Standard Attribute (0070,0312) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0318)": DicomTagDefinition(
        tag="(0070,0318)",
        group="0070",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_0070_0318_Keyword",
        name="DICOM Standard Attribute (0070,0318) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,031E)": DicomTagDefinition(
        tag="(0070,031E)",
        group="0070",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_0070_031E_Keyword",
        name="DICOM Standard Attribute (0070,031E) for Softcopy Presentation States Specification",
        retired=True
    ),
    "(0070,0324)": DicomTagDefinition(
        tag="(0070,0324)",
        group="0070",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_0070_0324_Keyword",
        name="DICOM Standard Attribute (0070,0324) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,032A)": DicomTagDefinition(
        tag="(0070,032A)",
        group="0070",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_0070_032A_Keyword",
        name="DICOM Standard Attribute (0070,032A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0330)": DicomTagDefinition(
        tag="(0070,0330)",
        group="0070",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_0070_0330_Keyword",
        name="DICOM Standard Attribute (0070,0330) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0336)": DicomTagDefinition(
        tag="(0070,0336)",
        group="0070",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_0070_0336_Keyword",
        name="DICOM Standard Attribute (0070,0336) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,033C)": DicomTagDefinition(
        tag="(0070,033C)",
        group="0070",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_0070_033C_Keyword",
        name="DICOM Standard Attribute (0070,033C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0342)": DicomTagDefinition(
        tag="(0070,0342)",
        group="0070",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_0070_0342_Keyword",
        name="DICOM Standard Attribute (0070,0342) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0348)": DicomTagDefinition(
        tag="(0070,0348)",
        group="0070",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_0070_0348_Keyword",
        name="DICOM Standard Attribute (0070,0348) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,034E)": DicomTagDefinition(
        tag="(0070,034E)",
        group="0070",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_0070_034E_Keyword",
        name="DICOM Standard Attribute (0070,034E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0354)": DicomTagDefinition(
        tag="(0070,0354)",
        group="0070",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_0070_0354_Keyword",
        name="DICOM Standard Attribute (0070,0354) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,035A)": DicomTagDefinition(
        tag="(0070,035A)",
        group="0070",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_0070_035A_Keyword",
        name="DICOM Standard Attribute (0070,035A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0360)": DicomTagDefinition(
        tag="(0070,0360)",
        group="0070",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_0070_0360_Keyword",
        name="DICOM Standard Attribute (0070,0360) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0366)": DicomTagDefinition(
        tag="(0070,0366)",
        group="0070",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_0070_0366_Keyword",
        name="DICOM Standard Attribute (0070,0366) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,036C)": DicomTagDefinition(
        tag="(0070,036C)",
        group="0070",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_0070_036C_Keyword",
        name="DICOM Standard Attribute (0070,036C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0372)": DicomTagDefinition(
        tag="(0070,0372)",
        group="0070",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_0070_0372_Keyword",
        name="DICOM Standard Attribute (0070,0372) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0378)": DicomTagDefinition(
        tag="(0070,0378)",
        group="0070",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_0070_0378_Keyword",
        name="DICOM Standard Attribute (0070,0378) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,037E)": DicomTagDefinition(
        tag="(0070,037E)",
        group="0070",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_0070_037E_Keyword",
        name="DICOM Standard Attribute (0070,037E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0384)": DicomTagDefinition(
        tag="(0070,0384)",
        group="0070",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_0070_0384_Keyword",
        name="DICOM Standard Attribute (0070,0384) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,038A)": DicomTagDefinition(
        tag="(0070,038A)",
        group="0070",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_0070_038A_Keyword",
        name="DICOM Standard Attribute (0070,038A) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0390)": DicomTagDefinition(
        tag="(0070,0390)",
        group="0070",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_0070_0390_Keyword",
        name="DICOM Standard Attribute (0070,0390) for Softcopy Presentation States Specification",
        retired=True
    ),
    "(0070,0396)": DicomTagDefinition(
        tag="(0070,0396)",
        group="0070",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_0070_0396_Keyword",
        name="DICOM Standard Attribute (0070,0396) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,039C)": DicomTagDefinition(
        tag="(0070,039C)",
        group="0070",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_0070_039C_Keyword",
        name="DICOM Standard Attribute (0070,039C) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03A2)": DicomTagDefinition(
        tag="(0070,03A2)",
        group="0070",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_0070_03A2_Keyword",
        name="DICOM Standard Attribute (0070,03A2) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03A8)": DicomTagDefinition(
        tag="(0070,03A8)",
        group="0070",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_0070_03A8_Keyword",
        name="DICOM Standard Attribute (0070,03A8) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03AE)": DicomTagDefinition(
        tag="(0070,03AE)",
        group="0070",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_0070_03AE_Keyword",
        name="DICOM Standard Attribute (0070,03AE) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03B4)": DicomTagDefinition(
        tag="(0070,03B4)",
        group="0070",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_0070_03B4_Keyword",
        name="DICOM Standard Attribute (0070,03B4) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03BA)": DicomTagDefinition(
        tag="(0070,03BA)",
        group="0070",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_0070_03BA_Keyword",
        name="DICOM Standard Attribute (0070,03BA) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03C0)": DicomTagDefinition(
        tag="(0070,03C0)",
        group="0070",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_0070_03C0_Keyword",
        name="DICOM Standard Attribute (0070,03C0) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03C6)": DicomTagDefinition(
        tag="(0070,03C6)",
        group="0070",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_0070_03C6_Keyword",
        name="DICOM Standard Attribute (0070,03C6) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03CC)": DicomTagDefinition(
        tag="(0070,03CC)",
        group="0070",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_0070_03CC_Keyword",
        name="DICOM Standard Attribute (0070,03CC) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03D2)": DicomTagDefinition(
        tag="(0070,03D2)",
        group="0070",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_0070_03D2_Keyword",
        name="DICOM Standard Attribute (0070,03D2) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03D8)": DicomTagDefinition(
        tag="(0070,03D8)",
        group="0070",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_0070_03D8_Keyword",
        name="DICOM Standard Attribute (0070,03D8) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03DE)": DicomTagDefinition(
        tag="(0070,03DE)",
        group="0070",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_0070_03DE_Keyword",
        name="DICOM Standard Attribute (0070,03DE) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03E4)": DicomTagDefinition(
        tag="(0070,03E4)",
        group="0070",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_0070_03E4_Keyword",
        name="DICOM Standard Attribute (0070,03E4) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03EA)": DicomTagDefinition(
        tag="(0070,03EA)",
        group="0070",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_0070_03EA_Keyword",
        name="DICOM Standard Attribute (0070,03EA) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03F0)": DicomTagDefinition(
        tag="(0070,03F0)",
        group="0070",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_0070_03F0_Keyword",
        name="DICOM Standard Attribute (0070,03F0) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03F6)": DicomTagDefinition(
        tag="(0070,03F6)",
        group="0070",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_0070_03F6_Keyword",
        name="DICOM Standard Attribute (0070,03F6) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,03FC)": DicomTagDefinition(
        tag="(0070,03FC)",
        group="0070",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_0070_03FC_Keyword",
        name="DICOM Standard Attribute (0070,03FC) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0402)": DicomTagDefinition(
        tag="(0070,0402)",
        group="0070",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_0070_0402_Keyword",
        name="DICOM Standard Attribute (0070,0402) for Softcopy Presentation States Specification",
        retired=True
    ),
    "(0070,0408)": DicomTagDefinition(
        tag="(0070,0408)",
        group="0070",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_0070_0408_Keyword",
        name="DICOM Standard Attribute (0070,0408) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,040E)": DicomTagDefinition(
        tag="(0070,040E)",
        group="0070",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_0070_040E_Keyword",
        name="DICOM Standard Attribute (0070,040E) for Softcopy Presentation States Specification",
        retired=False
    ),
    "(0070,0414)": DicomTagDefinition(
        tag="(0070,0414)",
        group="0070",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_0070_0414_Keyword",
        name="DICOM Standard Attribute (0070,0414) for Softcopy Presentation States Specification",
        retired=False
    ),
    # ========================================================
    # Section Group (3006): Radiotherapy Structure Set
    # ========================================================
    "(3006,0006)": DicomTagDefinition(
        tag="(3006,0006)",
        group="3006",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_3006_0006_Keyword",
        name="DICOM Standard Attribute (3006,0006) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,000C)": DicomTagDefinition(
        tag="(3006,000C)",
        group="3006",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_3006_000C_Keyword",
        name="DICOM Standard Attribute (3006,000C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0012)": DicomTagDefinition(
        tag="(3006,0012)",
        group="3006",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_3006_0012_Keyword",
        name="DICOM Standard Attribute (3006,0012) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0018)": DicomTagDefinition(
        tag="(3006,0018)",
        group="3006",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_3006_0018_Keyword",
        name="DICOM Standard Attribute (3006,0018) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,001E)": DicomTagDefinition(
        tag="(3006,001E)",
        group="3006",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_3006_001E_Keyword",
        name="DICOM Standard Attribute (3006,001E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0024)": DicomTagDefinition(
        tag="(3006,0024)",
        group="3006",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_3006_0024_Keyword",
        name="DICOM Standard Attribute (3006,0024) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,002A)": DicomTagDefinition(
        tag="(3006,002A)",
        group="3006",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_3006_002A_Keyword",
        name="DICOM Standard Attribute (3006,002A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0030)": DicomTagDefinition(
        tag="(3006,0030)",
        group="3006",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_3006_0030_Keyword",
        name="DICOM Standard Attribute (3006,0030) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0036)": DicomTagDefinition(
        tag="(3006,0036)",
        group="3006",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_3006_0036_Keyword",
        name="DICOM Standard Attribute (3006,0036) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,003C)": DicomTagDefinition(
        tag="(3006,003C)",
        group="3006",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_3006_003C_Keyword",
        name="DICOM Standard Attribute (3006,003C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0042)": DicomTagDefinition(
        tag="(3006,0042)",
        group="3006",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_3006_0042_Keyword",
        name="DICOM Standard Attribute (3006,0042) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0048)": DicomTagDefinition(
        tag="(3006,0048)",
        group="3006",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_3006_0048_Keyword",
        name="DICOM Standard Attribute (3006,0048) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,004E)": DicomTagDefinition(
        tag="(3006,004E)",
        group="3006",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_3006_004E_Keyword",
        name="DICOM Standard Attribute (3006,004E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0054)": DicomTagDefinition(
        tag="(3006,0054)",
        group="3006",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_3006_0054_Keyword",
        name="DICOM Standard Attribute (3006,0054) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,005A)": DicomTagDefinition(
        tag="(3006,005A)",
        group="3006",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_3006_005A_Keyword",
        name="DICOM Standard Attribute (3006,005A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0060)": DicomTagDefinition(
        tag="(3006,0060)",
        group="3006",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_3006_0060_Keyword",
        name="DICOM Standard Attribute (3006,0060) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0066)": DicomTagDefinition(
        tag="(3006,0066)",
        group="3006",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_3006_0066_Keyword",
        name="DICOM Standard Attribute (3006,0066) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,006C)": DicomTagDefinition(
        tag="(3006,006C)",
        group="3006",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_3006_006C_Keyword",
        name="DICOM Standard Attribute (3006,006C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0072)": DicomTagDefinition(
        tag="(3006,0072)",
        group="3006",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_3006_0072_Keyword",
        name="DICOM Standard Attribute (3006,0072) for Radiotherapy Structure Set Specification",
        retired=True
    ),
    "(3006,0078)": DicomTagDefinition(
        tag="(3006,0078)",
        group="3006",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_3006_0078_Keyword",
        name="DICOM Standard Attribute (3006,0078) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,007E)": DicomTagDefinition(
        tag="(3006,007E)",
        group="3006",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_3006_007E_Keyword",
        name="DICOM Standard Attribute (3006,007E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0084)": DicomTagDefinition(
        tag="(3006,0084)",
        group="3006",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_3006_0084_Keyword",
        name="DICOM Standard Attribute (3006,0084) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,008A)": DicomTagDefinition(
        tag="(3006,008A)",
        group="3006",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_3006_008A_Keyword",
        name="DICOM Standard Attribute (3006,008A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0090)": DicomTagDefinition(
        tag="(3006,0090)",
        group="3006",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_3006_0090_Keyword",
        name="DICOM Standard Attribute (3006,0090) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0096)": DicomTagDefinition(
        tag="(3006,0096)",
        group="3006",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_3006_0096_Keyword",
        name="DICOM Standard Attribute (3006,0096) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,009C)": DicomTagDefinition(
        tag="(3006,009C)",
        group="3006",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_3006_009C_Keyword",
        name="DICOM Standard Attribute (3006,009C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00A2)": DicomTagDefinition(
        tag="(3006,00A2)",
        group="3006",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_3006_00A2_Keyword",
        name="DICOM Standard Attribute (3006,00A2) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00A8)": DicomTagDefinition(
        tag="(3006,00A8)",
        group="3006",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_3006_00A8_Keyword",
        name="DICOM Standard Attribute (3006,00A8) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00AE)": DicomTagDefinition(
        tag="(3006,00AE)",
        group="3006",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_3006_00AE_Keyword",
        name="DICOM Standard Attribute (3006,00AE) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00B4)": DicomTagDefinition(
        tag="(3006,00B4)",
        group="3006",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_3006_00B4_Keyword",
        name="DICOM Standard Attribute (3006,00B4) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00BA)": DicomTagDefinition(
        tag="(3006,00BA)",
        group="3006",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_3006_00BA_Keyword",
        name="DICOM Standard Attribute (3006,00BA) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00C0)": DicomTagDefinition(
        tag="(3006,00C0)",
        group="3006",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_3006_00C0_Keyword",
        name="DICOM Standard Attribute (3006,00C0) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00C6)": DicomTagDefinition(
        tag="(3006,00C6)",
        group="3006",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_3006_00C6_Keyword",
        name="DICOM Standard Attribute (3006,00C6) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00CC)": DicomTagDefinition(
        tag="(3006,00CC)",
        group="3006",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_3006_00CC_Keyword",
        name="DICOM Standard Attribute (3006,00CC) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00D2)": DicomTagDefinition(
        tag="(3006,00D2)",
        group="3006",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_3006_00D2_Keyword",
        name="DICOM Standard Attribute (3006,00D2) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00D8)": DicomTagDefinition(
        tag="(3006,00D8)",
        group="3006",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_3006_00D8_Keyword",
        name="DICOM Standard Attribute (3006,00D8) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00DE)": DicomTagDefinition(
        tag="(3006,00DE)",
        group="3006",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_3006_00DE_Keyword",
        name="DICOM Standard Attribute (3006,00DE) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00E4)": DicomTagDefinition(
        tag="(3006,00E4)",
        group="3006",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_3006_00E4_Keyword",
        name="DICOM Standard Attribute (3006,00E4) for Radiotherapy Structure Set Specification",
        retired=True
    ),
    "(3006,00EA)": DicomTagDefinition(
        tag="(3006,00EA)",
        group="3006",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_3006_00EA_Keyword",
        name="DICOM Standard Attribute (3006,00EA) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00F0)": DicomTagDefinition(
        tag="(3006,00F0)",
        group="3006",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_3006_00F0_Keyword",
        name="DICOM Standard Attribute (3006,00F0) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00F6)": DicomTagDefinition(
        tag="(3006,00F6)",
        group="3006",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_3006_00F6_Keyword",
        name="DICOM Standard Attribute (3006,00F6) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,00FC)": DicomTagDefinition(
        tag="(3006,00FC)",
        group="3006",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_3006_00FC_Keyword",
        name="DICOM Standard Attribute (3006,00FC) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0102)": DicomTagDefinition(
        tag="(3006,0102)",
        group="3006",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_3006_0102_Keyword",
        name="DICOM Standard Attribute (3006,0102) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0108)": DicomTagDefinition(
        tag="(3006,0108)",
        group="3006",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_3006_0108_Keyword",
        name="DICOM Standard Attribute (3006,0108) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,010E)": DicomTagDefinition(
        tag="(3006,010E)",
        group="3006",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_3006_010E_Keyword",
        name="DICOM Standard Attribute (3006,010E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0114)": DicomTagDefinition(
        tag="(3006,0114)",
        group="3006",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_3006_0114_Keyword",
        name="DICOM Standard Attribute (3006,0114) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,011A)": DicomTagDefinition(
        tag="(3006,011A)",
        group="3006",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_3006_011A_Keyword",
        name="DICOM Standard Attribute (3006,011A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0120)": DicomTagDefinition(
        tag="(3006,0120)",
        group="3006",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_3006_0120_Keyword",
        name="DICOM Standard Attribute (3006,0120) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0126)": DicomTagDefinition(
        tag="(3006,0126)",
        group="3006",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_3006_0126_Keyword",
        name="DICOM Standard Attribute (3006,0126) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,012C)": DicomTagDefinition(
        tag="(3006,012C)",
        group="3006",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_3006_012C_Keyword",
        name="DICOM Standard Attribute (3006,012C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0132)": DicomTagDefinition(
        tag="(3006,0132)",
        group="3006",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_3006_0132_Keyword",
        name="DICOM Standard Attribute (3006,0132) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0138)": DicomTagDefinition(
        tag="(3006,0138)",
        group="3006",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_3006_0138_Keyword",
        name="DICOM Standard Attribute (3006,0138) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,013E)": DicomTagDefinition(
        tag="(3006,013E)",
        group="3006",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_3006_013E_Keyword",
        name="DICOM Standard Attribute (3006,013E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0144)": DicomTagDefinition(
        tag="(3006,0144)",
        group="3006",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_3006_0144_Keyword",
        name="DICOM Standard Attribute (3006,0144) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,014A)": DicomTagDefinition(
        tag="(3006,014A)",
        group="3006",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_3006_014A_Keyword",
        name="DICOM Standard Attribute (3006,014A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0150)": DicomTagDefinition(
        tag="(3006,0150)",
        group="3006",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_3006_0150_Keyword",
        name="DICOM Standard Attribute (3006,0150) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0156)": DicomTagDefinition(
        tag="(3006,0156)",
        group="3006",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_3006_0156_Keyword",
        name="DICOM Standard Attribute (3006,0156) for Radiotherapy Structure Set Specification",
        retired=True
    ),
    "(3006,015C)": DicomTagDefinition(
        tag="(3006,015C)",
        group="3006",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_3006_015C_Keyword",
        name="DICOM Standard Attribute (3006,015C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0162)": DicomTagDefinition(
        tag="(3006,0162)",
        group="3006",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_3006_0162_Keyword",
        name="DICOM Standard Attribute (3006,0162) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0168)": DicomTagDefinition(
        tag="(3006,0168)",
        group="3006",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_3006_0168_Keyword",
        name="DICOM Standard Attribute (3006,0168) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,016E)": DicomTagDefinition(
        tag="(3006,016E)",
        group="3006",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_3006_016E_Keyword",
        name="DICOM Standard Attribute (3006,016E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0174)": DicomTagDefinition(
        tag="(3006,0174)",
        group="3006",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_3006_0174_Keyword",
        name="DICOM Standard Attribute (3006,0174) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,017A)": DicomTagDefinition(
        tag="(3006,017A)",
        group="3006",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_3006_017A_Keyword",
        name="DICOM Standard Attribute (3006,017A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0180)": DicomTagDefinition(
        tag="(3006,0180)",
        group="3006",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_3006_0180_Keyword",
        name="DICOM Standard Attribute (3006,0180) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0186)": DicomTagDefinition(
        tag="(3006,0186)",
        group="3006",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_3006_0186_Keyword",
        name="DICOM Standard Attribute (3006,0186) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,018C)": DicomTagDefinition(
        tag="(3006,018C)",
        group="3006",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_3006_018C_Keyword",
        name="DICOM Standard Attribute (3006,018C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0192)": DicomTagDefinition(
        tag="(3006,0192)",
        group="3006",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_3006_0192_Keyword",
        name="DICOM Standard Attribute (3006,0192) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0198)": DicomTagDefinition(
        tag="(3006,0198)",
        group="3006",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_3006_0198_Keyword",
        name="DICOM Standard Attribute (3006,0198) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,019E)": DicomTagDefinition(
        tag="(3006,019E)",
        group="3006",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_3006_019E_Keyword",
        name="DICOM Standard Attribute (3006,019E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01A4)": DicomTagDefinition(
        tag="(3006,01A4)",
        group="3006",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_3006_01A4_Keyword",
        name="DICOM Standard Attribute (3006,01A4) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01AA)": DicomTagDefinition(
        tag="(3006,01AA)",
        group="3006",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_3006_01AA_Keyword",
        name="DICOM Standard Attribute (3006,01AA) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01B0)": DicomTagDefinition(
        tag="(3006,01B0)",
        group="3006",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_3006_01B0_Keyword",
        name="DICOM Standard Attribute (3006,01B0) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01B6)": DicomTagDefinition(
        tag="(3006,01B6)",
        group="3006",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_3006_01B6_Keyword",
        name="DICOM Standard Attribute (3006,01B6) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01BC)": DicomTagDefinition(
        tag="(3006,01BC)",
        group="3006",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_3006_01BC_Keyword",
        name="DICOM Standard Attribute (3006,01BC) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01C2)": DicomTagDefinition(
        tag="(3006,01C2)",
        group="3006",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_3006_01C2_Keyword",
        name="DICOM Standard Attribute (3006,01C2) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01C8)": DicomTagDefinition(
        tag="(3006,01C8)",
        group="3006",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_3006_01C8_Keyword",
        name="DICOM Standard Attribute (3006,01C8) for Radiotherapy Structure Set Specification",
        retired=True
    ),
    "(3006,01CE)": DicomTagDefinition(
        tag="(3006,01CE)",
        group="3006",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_3006_01CE_Keyword",
        name="DICOM Standard Attribute (3006,01CE) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01D4)": DicomTagDefinition(
        tag="(3006,01D4)",
        group="3006",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_3006_01D4_Keyword",
        name="DICOM Standard Attribute (3006,01D4) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01DA)": DicomTagDefinition(
        tag="(3006,01DA)",
        group="3006",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_3006_01DA_Keyword",
        name="DICOM Standard Attribute (3006,01DA) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01E0)": DicomTagDefinition(
        tag="(3006,01E0)",
        group="3006",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_3006_01E0_Keyword",
        name="DICOM Standard Attribute (3006,01E0) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01E6)": DicomTagDefinition(
        tag="(3006,01E6)",
        group="3006",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_3006_01E6_Keyword",
        name="DICOM Standard Attribute (3006,01E6) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01EC)": DicomTagDefinition(
        tag="(3006,01EC)",
        group="3006",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_3006_01EC_Keyword",
        name="DICOM Standard Attribute (3006,01EC) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01F2)": DicomTagDefinition(
        tag="(3006,01F2)",
        group="3006",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_3006_01F2_Keyword",
        name="DICOM Standard Attribute (3006,01F2) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01F8)": DicomTagDefinition(
        tag="(3006,01F8)",
        group="3006",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_3006_01F8_Keyword",
        name="DICOM Standard Attribute (3006,01F8) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,01FE)": DicomTagDefinition(
        tag="(3006,01FE)",
        group="3006",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_3006_01FE_Keyword",
        name="DICOM Standard Attribute (3006,01FE) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0204)": DicomTagDefinition(
        tag="(3006,0204)",
        group="3006",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_3006_0204_Keyword",
        name="DICOM Standard Attribute (3006,0204) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,020A)": DicomTagDefinition(
        tag="(3006,020A)",
        group="3006",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_3006_020A_Keyword",
        name="DICOM Standard Attribute (3006,020A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0210)": DicomTagDefinition(
        tag="(3006,0210)",
        group="3006",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_3006_0210_Keyword",
        name="DICOM Standard Attribute (3006,0210) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0216)": DicomTagDefinition(
        tag="(3006,0216)",
        group="3006",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_3006_0216_Keyword",
        name="DICOM Standard Attribute (3006,0216) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,021C)": DicomTagDefinition(
        tag="(3006,021C)",
        group="3006",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_3006_021C_Keyword",
        name="DICOM Standard Attribute (3006,021C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0222)": DicomTagDefinition(
        tag="(3006,0222)",
        group="3006",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_3006_0222_Keyword",
        name="DICOM Standard Attribute (3006,0222) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0228)": DicomTagDefinition(
        tag="(3006,0228)",
        group="3006",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_3006_0228_Keyword",
        name="DICOM Standard Attribute (3006,0228) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,022E)": DicomTagDefinition(
        tag="(3006,022E)",
        group="3006",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_3006_022E_Keyword",
        name="DICOM Standard Attribute (3006,022E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0234)": DicomTagDefinition(
        tag="(3006,0234)",
        group="3006",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_3006_0234_Keyword",
        name="DICOM Standard Attribute (3006,0234) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,023A)": DicomTagDefinition(
        tag="(3006,023A)",
        group="3006",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_3006_023A_Keyword",
        name="DICOM Standard Attribute (3006,023A) for Radiotherapy Structure Set Specification",
        retired=True
    ),
    "(3006,0240)": DicomTagDefinition(
        tag="(3006,0240)",
        group="3006",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_3006_0240_Keyword",
        name="DICOM Standard Attribute (3006,0240) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0246)": DicomTagDefinition(
        tag="(3006,0246)",
        group="3006",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_3006_0246_Keyword",
        name="DICOM Standard Attribute (3006,0246) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,024C)": DicomTagDefinition(
        tag="(3006,024C)",
        group="3006",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_3006_024C_Keyword",
        name="DICOM Standard Attribute (3006,024C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0252)": DicomTagDefinition(
        tag="(3006,0252)",
        group="3006",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_3006_0252_Keyword",
        name="DICOM Standard Attribute (3006,0252) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0258)": DicomTagDefinition(
        tag="(3006,0258)",
        group="3006",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_3006_0258_Keyword",
        name="DICOM Standard Attribute (3006,0258) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,025E)": DicomTagDefinition(
        tag="(3006,025E)",
        group="3006",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_3006_025E_Keyword",
        name="DICOM Standard Attribute (3006,025E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0264)": DicomTagDefinition(
        tag="(3006,0264)",
        group="3006",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_3006_0264_Keyword",
        name="DICOM Standard Attribute (3006,0264) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,026A)": DicomTagDefinition(
        tag="(3006,026A)",
        group="3006",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_3006_026A_Keyword",
        name="DICOM Standard Attribute (3006,026A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0270)": DicomTagDefinition(
        tag="(3006,0270)",
        group="3006",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_3006_0270_Keyword",
        name="DICOM Standard Attribute (3006,0270) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0276)": DicomTagDefinition(
        tag="(3006,0276)",
        group="3006",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_3006_0276_Keyword",
        name="DICOM Standard Attribute (3006,0276) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,027C)": DicomTagDefinition(
        tag="(3006,027C)",
        group="3006",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_3006_027C_Keyword",
        name="DICOM Standard Attribute (3006,027C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0282)": DicomTagDefinition(
        tag="(3006,0282)",
        group="3006",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_3006_0282_Keyword",
        name="DICOM Standard Attribute (3006,0282) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0288)": DicomTagDefinition(
        tag="(3006,0288)",
        group="3006",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_3006_0288_Keyword",
        name="DICOM Standard Attribute (3006,0288) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,028E)": DicomTagDefinition(
        tag="(3006,028E)",
        group="3006",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_3006_028E_Keyword",
        name="DICOM Standard Attribute (3006,028E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0294)": DicomTagDefinition(
        tag="(3006,0294)",
        group="3006",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_3006_0294_Keyword",
        name="DICOM Standard Attribute (3006,0294) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,029A)": DicomTagDefinition(
        tag="(3006,029A)",
        group="3006",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_3006_029A_Keyword",
        name="DICOM Standard Attribute (3006,029A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02A0)": DicomTagDefinition(
        tag="(3006,02A0)",
        group="3006",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_3006_02A0_Keyword",
        name="DICOM Standard Attribute (3006,02A0) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02A6)": DicomTagDefinition(
        tag="(3006,02A6)",
        group="3006",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_3006_02A6_Keyword",
        name="DICOM Standard Attribute (3006,02A6) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02AC)": DicomTagDefinition(
        tag="(3006,02AC)",
        group="3006",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_3006_02AC_Keyword",
        name="DICOM Standard Attribute (3006,02AC) for Radiotherapy Structure Set Specification",
        retired=True
    ),
    "(3006,02B2)": DicomTagDefinition(
        tag="(3006,02B2)",
        group="3006",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_3006_02B2_Keyword",
        name="DICOM Standard Attribute (3006,02B2) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02B8)": DicomTagDefinition(
        tag="(3006,02B8)",
        group="3006",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_3006_02B8_Keyword",
        name="DICOM Standard Attribute (3006,02B8) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02BE)": DicomTagDefinition(
        tag="(3006,02BE)",
        group="3006",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_3006_02BE_Keyword",
        name="DICOM Standard Attribute (3006,02BE) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02C4)": DicomTagDefinition(
        tag="(3006,02C4)",
        group="3006",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_3006_02C4_Keyword",
        name="DICOM Standard Attribute (3006,02C4) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02CA)": DicomTagDefinition(
        tag="(3006,02CA)",
        group="3006",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_3006_02CA_Keyword",
        name="DICOM Standard Attribute (3006,02CA) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02D0)": DicomTagDefinition(
        tag="(3006,02D0)",
        group="3006",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_3006_02D0_Keyword",
        name="DICOM Standard Attribute (3006,02D0) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02D6)": DicomTagDefinition(
        tag="(3006,02D6)",
        group="3006",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_3006_02D6_Keyword",
        name="DICOM Standard Attribute (3006,02D6) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02DC)": DicomTagDefinition(
        tag="(3006,02DC)",
        group="3006",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_3006_02DC_Keyword",
        name="DICOM Standard Attribute (3006,02DC) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02E2)": DicomTagDefinition(
        tag="(3006,02E2)",
        group="3006",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_3006_02E2_Keyword",
        name="DICOM Standard Attribute (3006,02E2) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02E8)": DicomTagDefinition(
        tag="(3006,02E8)",
        group="3006",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_3006_02E8_Keyword",
        name="DICOM Standard Attribute (3006,02E8) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02EE)": DicomTagDefinition(
        tag="(3006,02EE)",
        group="3006",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_3006_02EE_Keyword",
        name="DICOM Standard Attribute (3006,02EE) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02F4)": DicomTagDefinition(
        tag="(3006,02F4)",
        group="3006",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_3006_02F4_Keyword",
        name="DICOM Standard Attribute (3006,02F4) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,02FA)": DicomTagDefinition(
        tag="(3006,02FA)",
        group="3006",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_3006_02FA_Keyword",
        name="DICOM Standard Attribute (3006,02FA) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0300)": DicomTagDefinition(
        tag="(3006,0300)",
        group="3006",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_3006_0300_Keyword",
        name="DICOM Standard Attribute (3006,0300) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0306)": DicomTagDefinition(
        tag="(3006,0306)",
        group="3006",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_3006_0306_Keyword",
        name="DICOM Standard Attribute (3006,0306) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,030C)": DicomTagDefinition(
        tag="(3006,030C)",
        group="3006",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_3006_030C_Keyword",
        name="DICOM Standard Attribute (3006,030C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0312)": DicomTagDefinition(
        tag="(3006,0312)",
        group="3006",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_3006_0312_Keyword",
        name="DICOM Standard Attribute (3006,0312) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0318)": DicomTagDefinition(
        tag="(3006,0318)",
        group="3006",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_3006_0318_Keyword",
        name="DICOM Standard Attribute (3006,0318) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,031E)": DicomTagDefinition(
        tag="(3006,031E)",
        group="3006",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_3006_031E_Keyword",
        name="DICOM Standard Attribute (3006,031E) for Radiotherapy Structure Set Specification",
        retired=True
    ),
    "(3006,0324)": DicomTagDefinition(
        tag="(3006,0324)",
        group="3006",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_3006_0324_Keyword",
        name="DICOM Standard Attribute (3006,0324) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,032A)": DicomTagDefinition(
        tag="(3006,032A)",
        group="3006",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_3006_032A_Keyword",
        name="DICOM Standard Attribute (3006,032A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0330)": DicomTagDefinition(
        tag="(3006,0330)",
        group="3006",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_3006_0330_Keyword",
        name="DICOM Standard Attribute (3006,0330) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0336)": DicomTagDefinition(
        tag="(3006,0336)",
        group="3006",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_3006_0336_Keyword",
        name="DICOM Standard Attribute (3006,0336) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,033C)": DicomTagDefinition(
        tag="(3006,033C)",
        group="3006",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_3006_033C_Keyword",
        name="DICOM Standard Attribute (3006,033C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0342)": DicomTagDefinition(
        tag="(3006,0342)",
        group="3006",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_3006_0342_Keyword",
        name="DICOM Standard Attribute (3006,0342) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0348)": DicomTagDefinition(
        tag="(3006,0348)",
        group="3006",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_3006_0348_Keyword",
        name="DICOM Standard Attribute (3006,0348) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,034E)": DicomTagDefinition(
        tag="(3006,034E)",
        group="3006",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_3006_034E_Keyword",
        name="DICOM Standard Attribute (3006,034E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0354)": DicomTagDefinition(
        tag="(3006,0354)",
        group="3006",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_3006_0354_Keyword",
        name="DICOM Standard Attribute (3006,0354) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,035A)": DicomTagDefinition(
        tag="(3006,035A)",
        group="3006",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_3006_035A_Keyword",
        name="DICOM Standard Attribute (3006,035A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0360)": DicomTagDefinition(
        tag="(3006,0360)",
        group="3006",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_3006_0360_Keyword",
        name="DICOM Standard Attribute (3006,0360) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0366)": DicomTagDefinition(
        tag="(3006,0366)",
        group="3006",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_3006_0366_Keyword",
        name="DICOM Standard Attribute (3006,0366) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,036C)": DicomTagDefinition(
        tag="(3006,036C)",
        group="3006",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_3006_036C_Keyword",
        name="DICOM Standard Attribute (3006,036C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0372)": DicomTagDefinition(
        tag="(3006,0372)",
        group="3006",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_3006_0372_Keyword",
        name="DICOM Standard Attribute (3006,0372) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0378)": DicomTagDefinition(
        tag="(3006,0378)",
        group="3006",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_3006_0378_Keyword",
        name="DICOM Standard Attribute (3006,0378) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,037E)": DicomTagDefinition(
        tag="(3006,037E)",
        group="3006",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_3006_037E_Keyword",
        name="DICOM Standard Attribute (3006,037E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0384)": DicomTagDefinition(
        tag="(3006,0384)",
        group="3006",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_3006_0384_Keyword",
        name="DICOM Standard Attribute (3006,0384) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,038A)": DicomTagDefinition(
        tag="(3006,038A)",
        group="3006",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_3006_038A_Keyword",
        name="DICOM Standard Attribute (3006,038A) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0390)": DicomTagDefinition(
        tag="(3006,0390)",
        group="3006",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_3006_0390_Keyword",
        name="DICOM Standard Attribute (3006,0390) for Radiotherapy Structure Set Specification",
        retired=True
    ),
    "(3006,0396)": DicomTagDefinition(
        tag="(3006,0396)",
        group="3006",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_3006_0396_Keyword",
        name="DICOM Standard Attribute (3006,0396) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,039C)": DicomTagDefinition(
        tag="(3006,039C)",
        group="3006",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_3006_039C_Keyword",
        name="DICOM Standard Attribute (3006,039C) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03A2)": DicomTagDefinition(
        tag="(3006,03A2)",
        group="3006",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_3006_03A2_Keyword",
        name="DICOM Standard Attribute (3006,03A2) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03A8)": DicomTagDefinition(
        tag="(3006,03A8)",
        group="3006",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_3006_03A8_Keyword",
        name="DICOM Standard Attribute (3006,03A8) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03AE)": DicomTagDefinition(
        tag="(3006,03AE)",
        group="3006",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_3006_03AE_Keyword",
        name="DICOM Standard Attribute (3006,03AE) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03B4)": DicomTagDefinition(
        tag="(3006,03B4)",
        group="3006",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_3006_03B4_Keyword",
        name="DICOM Standard Attribute (3006,03B4) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03BA)": DicomTagDefinition(
        tag="(3006,03BA)",
        group="3006",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_3006_03BA_Keyword",
        name="DICOM Standard Attribute (3006,03BA) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03C0)": DicomTagDefinition(
        tag="(3006,03C0)",
        group="3006",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_3006_03C0_Keyword",
        name="DICOM Standard Attribute (3006,03C0) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03C6)": DicomTagDefinition(
        tag="(3006,03C6)",
        group="3006",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_3006_03C6_Keyword",
        name="DICOM Standard Attribute (3006,03C6) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03CC)": DicomTagDefinition(
        tag="(3006,03CC)",
        group="3006",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_3006_03CC_Keyword",
        name="DICOM Standard Attribute (3006,03CC) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03D2)": DicomTagDefinition(
        tag="(3006,03D2)",
        group="3006",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_3006_03D2_Keyword",
        name="DICOM Standard Attribute (3006,03D2) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03D8)": DicomTagDefinition(
        tag="(3006,03D8)",
        group="3006",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_3006_03D8_Keyword",
        name="DICOM Standard Attribute (3006,03D8) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03DE)": DicomTagDefinition(
        tag="(3006,03DE)",
        group="3006",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_3006_03DE_Keyword",
        name="DICOM Standard Attribute (3006,03DE) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03E4)": DicomTagDefinition(
        tag="(3006,03E4)",
        group="3006",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_3006_03E4_Keyword",
        name="DICOM Standard Attribute (3006,03E4) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03EA)": DicomTagDefinition(
        tag="(3006,03EA)",
        group="3006",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_3006_03EA_Keyword",
        name="DICOM Standard Attribute (3006,03EA) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03F0)": DicomTagDefinition(
        tag="(3006,03F0)",
        group="3006",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_3006_03F0_Keyword",
        name="DICOM Standard Attribute (3006,03F0) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03F6)": DicomTagDefinition(
        tag="(3006,03F6)",
        group="3006",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_3006_03F6_Keyword",
        name="DICOM Standard Attribute (3006,03F6) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,03FC)": DicomTagDefinition(
        tag="(3006,03FC)",
        group="3006",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_3006_03FC_Keyword",
        name="DICOM Standard Attribute (3006,03FC) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0402)": DicomTagDefinition(
        tag="(3006,0402)",
        group="3006",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_3006_0402_Keyword",
        name="DICOM Standard Attribute (3006,0402) for Radiotherapy Structure Set Specification",
        retired=True
    ),
    "(3006,0408)": DicomTagDefinition(
        tag="(3006,0408)",
        group="3006",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_3006_0408_Keyword",
        name="DICOM Standard Attribute (3006,0408) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,040E)": DicomTagDefinition(
        tag="(3006,040E)",
        group="3006",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_3006_040E_Keyword",
        name="DICOM Standard Attribute (3006,040E) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    "(3006,0414)": DicomTagDefinition(
        tag="(3006,0414)",
        group="3006",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_3006_0414_Keyword",
        name="DICOM Standard Attribute (3006,0414) for Radiotherapy Structure Set Specification",
        retired=False
    ),
    # ========================================================
    # Section Group (300A): Radiotherapy Plan Subsystem
    # ========================================================
    "(300A,0006)": DicomTagDefinition(
        tag="(300A,0006)",
        group="300A",
        element="0006",
        vr="SH",
        vm="1-N",
        keyword="Tag_300A_0006_Keyword",
        name="DICOM Standard Attribute (300A,0006) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,000C)": DicomTagDefinition(
        tag="(300A,000C)",
        group="300A",
        element="000C",
        vr="CS",
        vm="2",
        keyword="Tag_300A_000C_Keyword",
        name="DICOM Standard Attribute (300A,000C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0012)": DicomTagDefinition(
        tag="(300A,0012)",
        group="300A",
        element="0012",
        vr="UI",
        vm="3",
        keyword="Tag_300A_0012_Keyword",
        name="DICOM Standard Attribute (300A,0012) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0018)": DicomTagDefinition(
        tag="(300A,0018)",
        group="300A",
        element="0018",
        vr="PN",
        vm="6",
        keyword="Tag_300A_0018_Keyword",
        name="DICOM Standard Attribute (300A,0018) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,001E)": DicomTagDefinition(
        tag="(300A,001E)",
        group="300A",
        element="001E",
        vr="DA",
        vm="1",
        keyword="Tag_300A_001E_Keyword",
        name="DICOM Standard Attribute (300A,001E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0024)": DicomTagDefinition(
        tag="(300A,0024)",
        group="300A",
        element="0024",
        vr="TM",
        vm="1-N",
        keyword="Tag_300A_0024_Keyword",
        name="DICOM Standard Attribute (300A,0024) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,002A)": DicomTagDefinition(
        tag="(300A,002A)",
        group="300A",
        element="002A",
        vr="DS",
        vm="2",
        keyword="Tag_300A_002A_Keyword",
        name="DICOM Standard Attribute (300A,002A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0030)": DicomTagDefinition(
        tag="(300A,0030)",
        group="300A",
        element="0030",
        vr="IS",
        vm="3",
        keyword="Tag_300A_0030_Keyword",
        name="DICOM Standard Attribute (300A,0030) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0036)": DicomTagDefinition(
        tag="(300A,0036)",
        group="300A",
        element="0036",
        vr="SQ",
        vm="6",
        keyword="Tag_300A_0036_Keyword",
        name="DICOM Standard Attribute (300A,0036) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,003C)": DicomTagDefinition(
        tag="(300A,003C)",
        group="300A",
        element="003C",
        vr="US",
        vm="1",
        keyword="Tag_300A_003C_Keyword",
        name="DICOM Standard Attribute (300A,003C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0042)": DicomTagDefinition(
        tag="(300A,0042)",
        group="300A",
        element="0042",
        vr="LO",
        vm="1-N",
        keyword="Tag_300A_0042_Keyword",
        name="DICOM Standard Attribute (300A,0042) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0048)": DicomTagDefinition(
        tag="(300A,0048)",
        group="300A",
        element="0048",
        vr="SH",
        vm="2",
        keyword="Tag_300A_0048_Keyword",
        name="DICOM Standard Attribute (300A,0048) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,004E)": DicomTagDefinition(
        tag="(300A,004E)",
        group="300A",
        element="004E",
        vr="CS",
        vm="3",
        keyword="Tag_300A_004E_Keyword",
        name="DICOM Standard Attribute (300A,004E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0054)": DicomTagDefinition(
        tag="(300A,0054)",
        group="300A",
        element="0054",
        vr="UI",
        vm="6",
        keyword="Tag_300A_0054_Keyword",
        name="DICOM Standard Attribute (300A,0054) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,005A)": DicomTagDefinition(
        tag="(300A,005A)",
        group="300A",
        element="005A",
        vr="PN",
        vm="1",
        keyword="Tag_300A_005A_Keyword",
        name="DICOM Standard Attribute (300A,005A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0060)": DicomTagDefinition(
        tag="(300A,0060)",
        group="300A",
        element="0060",
        vr="DA",
        vm="1-N",
        keyword="Tag_300A_0060_Keyword",
        name="DICOM Standard Attribute (300A,0060) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0066)": DicomTagDefinition(
        tag="(300A,0066)",
        group="300A",
        element="0066",
        vr="TM",
        vm="2",
        keyword="Tag_300A_0066_Keyword",
        name="DICOM Standard Attribute (300A,0066) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,006C)": DicomTagDefinition(
        tag="(300A,006C)",
        group="300A",
        element="006C",
        vr="DS",
        vm="3",
        keyword="Tag_300A_006C_Keyword",
        name="DICOM Standard Attribute (300A,006C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0072)": DicomTagDefinition(
        tag="(300A,0072)",
        group="300A",
        element="0072",
        vr="IS",
        vm="6",
        keyword="Tag_300A_0072_Keyword",
        name="DICOM Standard Attribute (300A,0072) for Radiotherapy Plan Subsystem Specification",
        retired=True
    ),
    "(300A,0078)": DicomTagDefinition(
        tag="(300A,0078)",
        group="300A",
        element="0078",
        vr="SQ",
        vm="1",
        keyword="Tag_300A_0078_Keyword",
        name="DICOM Standard Attribute (300A,0078) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,007E)": DicomTagDefinition(
        tag="(300A,007E)",
        group="300A",
        element="007E",
        vr="US",
        vm="1-N",
        keyword="Tag_300A_007E_Keyword",
        name="DICOM Standard Attribute (300A,007E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0084)": DicomTagDefinition(
        tag="(300A,0084)",
        group="300A",
        element="0084",
        vr="LO",
        vm="2",
        keyword="Tag_300A_0084_Keyword",
        name="DICOM Standard Attribute (300A,0084) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,008A)": DicomTagDefinition(
        tag="(300A,008A)",
        group="300A",
        element="008A",
        vr="SH",
        vm="3",
        keyword="Tag_300A_008A_Keyword",
        name="DICOM Standard Attribute (300A,008A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0090)": DicomTagDefinition(
        tag="(300A,0090)",
        group="300A",
        element="0090",
        vr="CS",
        vm="6",
        keyword="Tag_300A_0090_Keyword",
        name="DICOM Standard Attribute (300A,0090) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0096)": DicomTagDefinition(
        tag="(300A,0096)",
        group="300A",
        element="0096",
        vr="UI",
        vm="1",
        keyword="Tag_300A_0096_Keyword",
        name="DICOM Standard Attribute (300A,0096) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,009C)": DicomTagDefinition(
        tag="(300A,009C)",
        group="300A",
        element="009C",
        vr="PN",
        vm="1-N",
        keyword="Tag_300A_009C_Keyword",
        name="DICOM Standard Attribute (300A,009C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00A2)": DicomTagDefinition(
        tag="(300A,00A2)",
        group="300A",
        element="00A2",
        vr="DA",
        vm="2",
        keyword="Tag_300A_00A2_Keyword",
        name="DICOM Standard Attribute (300A,00A2) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00A8)": DicomTagDefinition(
        tag="(300A,00A8)",
        group="300A",
        element="00A8",
        vr="TM",
        vm="3",
        keyword="Tag_300A_00A8_Keyword",
        name="DICOM Standard Attribute (300A,00A8) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00AE)": DicomTagDefinition(
        tag="(300A,00AE)",
        group="300A",
        element="00AE",
        vr="DS",
        vm="6",
        keyword="Tag_300A_00AE_Keyword",
        name="DICOM Standard Attribute (300A,00AE) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00B4)": DicomTagDefinition(
        tag="(300A,00B4)",
        group="300A",
        element="00B4",
        vr="IS",
        vm="1",
        keyword="Tag_300A_00B4_Keyword",
        name="DICOM Standard Attribute (300A,00B4) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00BA)": DicomTagDefinition(
        tag="(300A,00BA)",
        group="300A",
        element="00BA",
        vr="SQ",
        vm="1-N",
        keyword="Tag_300A_00BA_Keyword",
        name="DICOM Standard Attribute (300A,00BA) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00C0)": DicomTagDefinition(
        tag="(300A,00C0)",
        group="300A",
        element="00C0",
        vr="US",
        vm="2",
        keyword="Tag_300A_00C0_Keyword",
        name="DICOM Standard Attribute (300A,00C0) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00C6)": DicomTagDefinition(
        tag="(300A,00C6)",
        group="300A",
        element="00C6",
        vr="LO",
        vm="3",
        keyword="Tag_300A_00C6_Keyword",
        name="DICOM Standard Attribute (300A,00C6) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00CC)": DicomTagDefinition(
        tag="(300A,00CC)",
        group="300A",
        element="00CC",
        vr="SH",
        vm="6",
        keyword="Tag_300A_00CC_Keyword",
        name="DICOM Standard Attribute (300A,00CC) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00D2)": DicomTagDefinition(
        tag="(300A,00D2)",
        group="300A",
        element="00D2",
        vr="CS",
        vm="1",
        keyword="Tag_300A_00D2_Keyword",
        name="DICOM Standard Attribute (300A,00D2) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00D8)": DicomTagDefinition(
        tag="(300A,00D8)",
        group="300A",
        element="00D8",
        vr="UI",
        vm="1-N",
        keyword="Tag_300A_00D8_Keyword",
        name="DICOM Standard Attribute (300A,00D8) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00DE)": DicomTagDefinition(
        tag="(300A,00DE)",
        group="300A",
        element="00DE",
        vr="PN",
        vm="2",
        keyword="Tag_300A_00DE_Keyword",
        name="DICOM Standard Attribute (300A,00DE) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00E4)": DicomTagDefinition(
        tag="(300A,00E4)",
        group="300A",
        element="00E4",
        vr="DA",
        vm="3",
        keyword="Tag_300A_00E4_Keyword",
        name="DICOM Standard Attribute (300A,00E4) for Radiotherapy Plan Subsystem Specification",
        retired=True
    ),
    "(300A,00EA)": DicomTagDefinition(
        tag="(300A,00EA)",
        group="300A",
        element="00EA",
        vr="TM",
        vm="6",
        keyword="Tag_300A_00EA_Keyword",
        name="DICOM Standard Attribute (300A,00EA) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00F0)": DicomTagDefinition(
        tag="(300A,00F0)",
        group="300A",
        element="00F0",
        vr="DS",
        vm="1",
        keyword="Tag_300A_00F0_Keyword",
        name="DICOM Standard Attribute (300A,00F0) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00F6)": DicomTagDefinition(
        tag="(300A,00F6)",
        group="300A",
        element="00F6",
        vr="IS",
        vm="1-N",
        keyword="Tag_300A_00F6_Keyword",
        name="DICOM Standard Attribute (300A,00F6) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,00FC)": DicomTagDefinition(
        tag="(300A,00FC)",
        group="300A",
        element="00FC",
        vr="SQ",
        vm="2",
        keyword="Tag_300A_00FC_Keyword",
        name="DICOM Standard Attribute (300A,00FC) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0102)": DicomTagDefinition(
        tag="(300A,0102)",
        group="300A",
        element="0102",
        vr="US",
        vm="3",
        keyword="Tag_300A_0102_Keyword",
        name="DICOM Standard Attribute (300A,0102) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0108)": DicomTagDefinition(
        tag="(300A,0108)",
        group="300A",
        element="0108",
        vr="LO",
        vm="6",
        keyword="Tag_300A_0108_Keyword",
        name="DICOM Standard Attribute (300A,0108) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,010E)": DicomTagDefinition(
        tag="(300A,010E)",
        group="300A",
        element="010E",
        vr="SH",
        vm="1",
        keyword="Tag_300A_010E_Keyword",
        name="DICOM Standard Attribute (300A,010E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0114)": DicomTagDefinition(
        tag="(300A,0114)",
        group="300A",
        element="0114",
        vr="CS",
        vm="1-N",
        keyword="Tag_300A_0114_Keyword",
        name="DICOM Standard Attribute (300A,0114) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,011A)": DicomTagDefinition(
        tag="(300A,011A)",
        group="300A",
        element="011A",
        vr="UI",
        vm="2",
        keyword="Tag_300A_011A_Keyword",
        name="DICOM Standard Attribute (300A,011A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0120)": DicomTagDefinition(
        tag="(300A,0120)",
        group="300A",
        element="0120",
        vr="PN",
        vm="3",
        keyword="Tag_300A_0120_Keyword",
        name="DICOM Standard Attribute (300A,0120) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0126)": DicomTagDefinition(
        tag="(300A,0126)",
        group="300A",
        element="0126",
        vr="DA",
        vm="6",
        keyword="Tag_300A_0126_Keyword",
        name="DICOM Standard Attribute (300A,0126) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,012C)": DicomTagDefinition(
        tag="(300A,012C)",
        group="300A",
        element="012C",
        vr="TM",
        vm="1",
        keyword="Tag_300A_012C_Keyword",
        name="DICOM Standard Attribute (300A,012C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0132)": DicomTagDefinition(
        tag="(300A,0132)",
        group="300A",
        element="0132",
        vr="DS",
        vm="1-N",
        keyword="Tag_300A_0132_Keyword",
        name="DICOM Standard Attribute (300A,0132) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0138)": DicomTagDefinition(
        tag="(300A,0138)",
        group="300A",
        element="0138",
        vr="IS",
        vm="2",
        keyword="Tag_300A_0138_Keyword",
        name="DICOM Standard Attribute (300A,0138) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,013E)": DicomTagDefinition(
        tag="(300A,013E)",
        group="300A",
        element="013E",
        vr="SQ",
        vm="3",
        keyword="Tag_300A_013E_Keyword",
        name="DICOM Standard Attribute (300A,013E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0144)": DicomTagDefinition(
        tag="(300A,0144)",
        group="300A",
        element="0144",
        vr="US",
        vm="6",
        keyword="Tag_300A_0144_Keyword",
        name="DICOM Standard Attribute (300A,0144) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,014A)": DicomTagDefinition(
        tag="(300A,014A)",
        group="300A",
        element="014A",
        vr="LO",
        vm="1",
        keyword="Tag_300A_014A_Keyword",
        name="DICOM Standard Attribute (300A,014A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0150)": DicomTagDefinition(
        tag="(300A,0150)",
        group="300A",
        element="0150",
        vr="SH",
        vm="1-N",
        keyword="Tag_300A_0150_Keyword",
        name="DICOM Standard Attribute (300A,0150) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0156)": DicomTagDefinition(
        tag="(300A,0156)",
        group="300A",
        element="0156",
        vr="CS",
        vm="2",
        keyword="Tag_300A_0156_Keyword",
        name="DICOM Standard Attribute (300A,0156) for Radiotherapy Plan Subsystem Specification",
        retired=True
    ),
    "(300A,015C)": DicomTagDefinition(
        tag="(300A,015C)",
        group="300A",
        element="015C",
        vr="UI",
        vm="3",
        keyword="Tag_300A_015C_Keyword",
        name="DICOM Standard Attribute (300A,015C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0162)": DicomTagDefinition(
        tag="(300A,0162)",
        group="300A",
        element="0162",
        vr="PN",
        vm="6",
        keyword="Tag_300A_0162_Keyword",
        name="DICOM Standard Attribute (300A,0162) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0168)": DicomTagDefinition(
        tag="(300A,0168)",
        group="300A",
        element="0168",
        vr="DA",
        vm="1",
        keyword="Tag_300A_0168_Keyword",
        name="DICOM Standard Attribute (300A,0168) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,016E)": DicomTagDefinition(
        tag="(300A,016E)",
        group="300A",
        element="016E",
        vr="TM",
        vm="1-N",
        keyword="Tag_300A_016E_Keyword",
        name="DICOM Standard Attribute (300A,016E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0174)": DicomTagDefinition(
        tag="(300A,0174)",
        group="300A",
        element="0174",
        vr="DS",
        vm="2",
        keyword="Tag_300A_0174_Keyword",
        name="DICOM Standard Attribute (300A,0174) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,017A)": DicomTagDefinition(
        tag="(300A,017A)",
        group="300A",
        element="017A",
        vr="IS",
        vm="3",
        keyword="Tag_300A_017A_Keyword",
        name="DICOM Standard Attribute (300A,017A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0180)": DicomTagDefinition(
        tag="(300A,0180)",
        group="300A",
        element="0180",
        vr="SQ",
        vm="6",
        keyword="Tag_300A_0180_Keyword",
        name="DICOM Standard Attribute (300A,0180) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0186)": DicomTagDefinition(
        tag="(300A,0186)",
        group="300A",
        element="0186",
        vr="US",
        vm="1",
        keyword="Tag_300A_0186_Keyword",
        name="DICOM Standard Attribute (300A,0186) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,018C)": DicomTagDefinition(
        tag="(300A,018C)",
        group="300A",
        element="018C",
        vr="LO",
        vm="1-N",
        keyword="Tag_300A_018C_Keyword",
        name="DICOM Standard Attribute (300A,018C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0192)": DicomTagDefinition(
        tag="(300A,0192)",
        group="300A",
        element="0192",
        vr="SH",
        vm="2",
        keyword="Tag_300A_0192_Keyword",
        name="DICOM Standard Attribute (300A,0192) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0198)": DicomTagDefinition(
        tag="(300A,0198)",
        group="300A",
        element="0198",
        vr="CS",
        vm="3",
        keyword="Tag_300A_0198_Keyword",
        name="DICOM Standard Attribute (300A,0198) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,019E)": DicomTagDefinition(
        tag="(300A,019E)",
        group="300A",
        element="019E",
        vr="UI",
        vm="6",
        keyword="Tag_300A_019E_Keyword",
        name="DICOM Standard Attribute (300A,019E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01A4)": DicomTagDefinition(
        tag="(300A,01A4)",
        group="300A",
        element="01A4",
        vr="PN",
        vm="1",
        keyword="Tag_300A_01A4_Keyword",
        name="DICOM Standard Attribute (300A,01A4) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01AA)": DicomTagDefinition(
        tag="(300A,01AA)",
        group="300A",
        element="01AA",
        vr="DA",
        vm="1-N",
        keyword="Tag_300A_01AA_Keyword",
        name="DICOM Standard Attribute (300A,01AA) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01B0)": DicomTagDefinition(
        tag="(300A,01B0)",
        group="300A",
        element="01B0",
        vr="TM",
        vm="2",
        keyword="Tag_300A_01B0_Keyword",
        name="DICOM Standard Attribute (300A,01B0) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01B6)": DicomTagDefinition(
        tag="(300A,01B6)",
        group="300A",
        element="01B6",
        vr="DS",
        vm="3",
        keyword="Tag_300A_01B6_Keyword",
        name="DICOM Standard Attribute (300A,01B6) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01BC)": DicomTagDefinition(
        tag="(300A,01BC)",
        group="300A",
        element="01BC",
        vr="IS",
        vm="6",
        keyword="Tag_300A_01BC_Keyword",
        name="DICOM Standard Attribute (300A,01BC) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01C2)": DicomTagDefinition(
        tag="(300A,01C2)",
        group="300A",
        element="01C2",
        vr="SQ",
        vm="1",
        keyword="Tag_300A_01C2_Keyword",
        name="DICOM Standard Attribute (300A,01C2) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01C8)": DicomTagDefinition(
        tag="(300A,01C8)",
        group="300A",
        element="01C8",
        vr="US",
        vm="1-N",
        keyword="Tag_300A_01C8_Keyword",
        name="DICOM Standard Attribute (300A,01C8) for Radiotherapy Plan Subsystem Specification",
        retired=True
    ),
    "(300A,01CE)": DicomTagDefinition(
        tag="(300A,01CE)",
        group="300A",
        element="01CE",
        vr="LO",
        vm="2",
        keyword="Tag_300A_01CE_Keyword",
        name="DICOM Standard Attribute (300A,01CE) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01D4)": DicomTagDefinition(
        tag="(300A,01D4)",
        group="300A",
        element="01D4",
        vr="SH",
        vm="3",
        keyword="Tag_300A_01D4_Keyword",
        name="DICOM Standard Attribute (300A,01D4) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01DA)": DicomTagDefinition(
        tag="(300A,01DA)",
        group="300A",
        element="01DA",
        vr="CS",
        vm="6",
        keyword="Tag_300A_01DA_Keyword",
        name="DICOM Standard Attribute (300A,01DA) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01E0)": DicomTagDefinition(
        tag="(300A,01E0)",
        group="300A",
        element="01E0",
        vr="UI",
        vm="1",
        keyword="Tag_300A_01E0_Keyword",
        name="DICOM Standard Attribute (300A,01E0) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01E6)": DicomTagDefinition(
        tag="(300A,01E6)",
        group="300A",
        element="01E6",
        vr="PN",
        vm="1-N",
        keyword="Tag_300A_01E6_Keyword",
        name="DICOM Standard Attribute (300A,01E6) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01EC)": DicomTagDefinition(
        tag="(300A,01EC)",
        group="300A",
        element="01EC",
        vr="DA",
        vm="2",
        keyword="Tag_300A_01EC_Keyword",
        name="DICOM Standard Attribute (300A,01EC) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01F2)": DicomTagDefinition(
        tag="(300A,01F2)",
        group="300A",
        element="01F2",
        vr="TM",
        vm="3",
        keyword="Tag_300A_01F2_Keyword",
        name="DICOM Standard Attribute (300A,01F2) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01F8)": DicomTagDefinition(
        tag="(300A,01F8)",
        group="300A",
        element="01F8",
        vr="DS",
        vm="6",
        keyword="Tag_300A_01F8_Keyword",
        name="DICOM Standard Attribute (300A,01F8) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,01FE)": DicomTagDefinition(
        tag="(300A,01FE)",
        group="300A",
        element="01FE",
        vr="IS",
        vm="1",
        keyword="Tag_300A_01FE_Keyword",
        name="DICOM Standard Attribute (300A,01FE) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0204)": DicomTagDefinition(
        tag="(300A,0204)",
        group="300A",
        element="0204",
        vr="SQ",
        vm="1-N",
        keyword="Tag_300A_0204_Keyword",
        name="DICOM Standard Attribute (300A,0204) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,020A)": DicomTagDefinition(
        tag="(300A,020A)",
        group="300A",
        element="020A",
        vr="US",
        vm="2",
        keyword="Tag_300A_020A_Keyword",
        name="DICOM Standard Attribute (300A,020A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0210)": DicomTagDefinition(
        tag="(300A,0210)",
        group="300A",
        element="0210",
        vr="LO",
        vm="3",
        keyword="Tag_300A_0210_Keyword",
        name="DICOM Standard Attribute (300A,0210) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0216)": DicomTagDefinition(
        tag="(300A,0216)",
        group="300A",
        element="0216",
        vr="SH",
        vm="6",
        keyword="Tag_300A_0216_Keyword",
        name="DICOM Standard Attribute (300A,0216) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,021C)": DicomTagDefinition(
        tag="(300A,021C)",
        group="300A",
        element="021C",
        vr="CS",
        vm="1",
        keyword="Tag_300A_021C_Keyword",
        name="DICOM Standard Attribute (300A,021C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0222)": DicomTagDefinition(
        tag="(300A,0222)",
        group="300A",
        element="0222",
        vr="UI",
        vm="1-N",
        keyword="Tag_300A_0222_Keyword",
        name="DICOM Standard Attribute (300A,0222) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0228)": DicomTagDefinition(
        tag="(300A,0228)",
        group="300A",
        element="0228",
        vr="PN",
        vm="2",
        keyword="Tag_300A_0228_Keyword",
        name="DICOM Standard Attribute (300A,0228) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,022E)": DicomTagDefinition(
        tag="(300A,022E)",
        group="300A",
        element="022E",
        vr="DA",
        vm="3",
        keyword="Tag_300A_022E_Keyword",
        name="DICOM Standard Attribute (300A,022E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0234)": DicomTagDefinition(
        tag="(300A,0234)",
        group="300A",
        element="0234",
        vr="TM",
        vm="6",
        keyword="Tag_300A_0234_Keyword",
        name="DICOM Standard Attribute (300A,0234) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,023A)": DicomTagDefinition(
        tag="(300A,023A)",
        group="300A",
        element="023A",
        vr="DS",
        vm="1",
        keyword="Tag_300A_023A_Keyword",
        name="DICOM Standard Attribute (300A,023A) for Radiotherapy Plan Subsystem Specification",
        retired=True
    ),
    "(300A,0240)": DicomTagDefinition(
        tag="(300A,0240)",
        group="300A",
        element="0240",
        vr="IS",
        vm="1-N",
        keyword="Tag_300A_0240_Keyword",
        name="DICOM Standard Attribute (300A,0240) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0246)": DicomTagDefinition(
        tag="(300A,0246)",
        group="300A",
        element="0246",
        vr="SQ",
        vm="2",
        keyword="Tag_300A_0246_Keyword",
        name="DICOM Standard Attribute (300A,0246) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,024C)": DicomTagDefinition(
        tag="(300A,024C)",
        group="300A",
        element="024C",
        vr="US",
        vm="3",
        keyword="Tag_300A_024C_Keyword",
        name="DICOM Standard Attribute (300A,024C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0252)": DicomTagDefinition(
        tag="(300A,0252)",
        group="300A",
        element="0252",
        vr="LO",
        vm="6",
        keyword="Tag_300A_0252_Keyword",
        name="DICOM Standard Attribute (300A,0252) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0258)": DicomTagDefinition(
        tag="(300A,0258)",
        group="300A",
        element="0258",
        vr="SH",
        vm="1",
        keyword="Tag_300A_0258_Keyword",
        name="DICOM Standard Attribute (300A,0258) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,025E)": DicomTagDefinition(
        tag="(300A,025E)",
        group="300A",
        element="025E",
        vr="CS",
        vm="1-N",
        keyword="Tag_300A_025E_Keyword",
        name="DICOM Standard Attribute (300A,025E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0264)": DicomTagDefinition(
        tag="(300A,0264)",
        group="300A",
        element="0264",
        vr="UI",
        vm="2",
        keyword="Tag_300A_0264_Keyword",
        name="DICOM Standard Attribute (300A,0264) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,026A)": DicomTagDefinition(
        tag="(300A,026A)",
        group="300A",
        element="026A",
        vr="PN",
        vm="3",
        keyword="Tag_300A_026A_Keyword",
        name="DICOM Standard Attribute (300A,026A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0270)": DicomTagDefinition(
        tag="(300A,0270)",
        group="300A",
        element="0270",
        vr="DA",
        vm="6",
        keyword="Tag_300A_0270_Keyword",
        name="DICOM Standard Attribute (300A,0270) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0276)": DicomTagDefinition(
        tag="(300A,0276)",
        group="300A",
        element="0276",
        vr="TM",
        vm="1",
        keyword="Tag_300A_0276_Keyword",
        name="DICOM Standard Attribute (300A,0276) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,027C)": DicomTagDefinition(
        tag="(300A,027C)",
        group="300A",
        element="027C",
        vr="DS",
        vm="1-N",
        keyword="Tag_300A_027C_Keyword",
        name="DICOM Standard Attribute (300A,027C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0282)": DicomTagDefinition(
        tag="(300A,0282)",
        group="300A",
        element="0282",
        vr="IS",
        vm="2",
        keyword="Tag_300A_0282_Keyword",
        name="DICOM Standard Attribute (300A,0282) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0288)": DicomTagDefinition(
        tag="(300A,0288)",
        group="300A",
        element="0288",
        vr="SQ",
        vm="3",
        keyword="Tag_300A_0288_Keyword",
        name="DICOM Standard Attribute (300A,0288) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,028E)": DicomTagDefinition(
        tag="(300A,028E)",
        group="300A",
        element="028E",
        vr="US",
        vm="6",
        keyword="Tag_300A_028E_Keyword",
        name="DICOM Standard Attribute (300A,028E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0294)": DicomTagDefinition(
        tag="(300A,0294)",
        group="300A",
        element="0294",
        vr="LO",
        vm="1",
        keyword="Tag_300A_0294_Keyword",
        name="DICOM Standard Attribute (300A,0294) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,029A)": DicomTagDefinition(
        tag="(300A,029A)",
        group="300A",
        element="029A",
        vr="SH",
        vm="1-N",
        keyword="Tag_300A_029A_Keyword",
        name="DICOM Standard Attribute (300A,029A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02A0)": DicomTagDefinition(
        tag="(300A,02A0)",
        group="300A",
        element="02A0",
        vr="CS",
        vm="2",
        keyword="Tag_300A_02A0_Keyword",
        name="DICOM Standard Attribute (300A,02A0) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02A6)": DicomTagDefinition(
        tag="(300A,02A6)",
        group="300A",
        element="02A6",
        vr="UI",
        vm="3",
        keyword="Tag_300A_02A6_Keyword",
        name="DICOM Standard Attribute (300A,02A6) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02AC)": DicomTagDefinition(
        tag="(300A,02AC)",
        group="300A",
        element="02AC",
        vr="PN",
        vm="6",
        keyword="Tag_300A_02AC_Keyword",
        name="DICOM Standard Attribute (300A,02AC) for Radiotherapy Plan Subsystem Specification",
        retired=True
    ),
    "(300A,02B2)": DicomTagDefinition(
        tag="(300A,02B2)",
        group="300A",
        element="02B2",
        vr="DA",
        vm="1",
        keyword="Tag_300A_02B2_Keyword",
        name="DICOM Standard Attribute (300A,02B2) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02B8)": DicomTagDefinition(
        tag="(300A,02B8)",
        group="300A",
        element="02B8",
        vr="TM",
        vm="1-N",
        keyword="Tag_300A_02B8_Keyword",
        name="DICOM Standard Attribute (300A,02B8) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02BE)": DicomTagDefinition(
        tag="(300A,02BE)",
        group="300A",
        element="02BE",
        vr="DS",
        vm="2",
        keyword="Tag_300A_02BE_Keyword",
        name="DICOM Standard Attribute (300A,02BE) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02C4)": DicomTagDefinition(
        tag="(300A,02C4)",
        group="300A",
        element="02C4",
        vr="IS",
        vm="3",
        keyword="Tag_300A_02C4_Keyword",
        name="DICOM Standard Attribute (300A,02C4) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02CA)": DicomTagDefinition(
        tag="(300A,02CA)",
        group="300A",
        element="02CA",
        vr="SQ",
        vm="6",
        keyword="Tag_300A_02CA_Keyword",
        name="DICOM Standard Attribute (300A,02CA) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02D0)": DicomTagDefinition(
        tag="(300A,02D0)",
        group="300A",
        element="02D0",
        vr="US",
        vm="1",
        keyword="Tag_300A_02D0_Keyword",
        name="DICOM Standard Attribute (300A,02D0) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02D6)": DicomTagDefinition(
        tag="(300A,02D6)",
        group="300A",
        element="02D6",
        vr="LO",
        vm="1-N",
        keyword="Tag_300A_02D6_Keyword",
        name="DICOM Standard Attribute (300A,02D6) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02DC)": DicomTagDefinition(
        tag="(300A,02DC)",
        group="300A",
        element="02DC",
        vr="SH",
        vm="2",
        keyword="Tag_300A_02DC_Keyword",
        name="DICOM Standard Attribute (300A,02DC) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02E2)": DicomTagDefinition(
        tag="(300A,02E2)",
        group="300A",
        element="02E2",
        vr="CS",
        vm="3",
        keyword="Tag_300A_02E2_Keyword",
        name="DICOM Standard Attribute (300A,02E2) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02E8)": DicomTagDefinition(
        tag="(300A,02E8)",
        group="300A",
        element="02E8",
        vr="UI",
        vm="6",
        keyword="Tag_300A_02E8_Keyword",
        name="DICOM Standard Attribute (300A,02E8) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02EE)": DicomTagDefinition(
        tag="(300A,02EE)",
        group="300A",
        element="02EE",
        vr="PN",
        vm="1",
        keyword="Tag_300A_02EE_Keyword",
        name="DICOM Standard Attribute (300A,02EE) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02F4)": DicomTagDefinition(
        tag="(300A,02F4)",
        group="300A",
        element="02F4",
        vr="DA",
        vm="1-N",
        keyword="Tag_300A_02F4_Keyword",
        name="DICOM Standard Attribute (300A,02F4) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,02FA)": DicomTagDefinition(
        tag="(300A,02FA)",
        group="300A",
        element="02FA",
        vr="TM",
        vm="2",
        keyword="Tag_300A_02FA_Keyword",
        name="DICOM Standard Attribute (300A,02FA) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0300)": DicomTagDefinition(
        tag="(300A,0300)",
        group="300A",
        element="0300",
        vr="DS",
        vm="3",
        keyword="Tag_300A_0300_Keyword",
        name="DICOM Standard Attribute (300A,0300) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0306)": DicomTagDefinition(
        tag="(300A,0306)",
        group="300A",
        element="0306",
        vr="IS",
        vm="6",
        keyword="Tag_300A_0306_Keyword",
        name="DICOM Standard Attribute (300A,0306) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,030C)": DicomTagDefinition(
        tag="(300A,030C)",
        group="300A",
        element="030C",
        vr="SQ",
        vm="1",
        keyword="Tag_300A_030C_Keyword",
        name="DICOM Standard Attribute (300A,030C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0312)": DicomTagDefinition(
        tag="(300A,0312)",
        group="300A",
        element="0312",
        vr="US",
        vm="1-N",
        keyword="Tag_300A_0312_Keyword",
        name="DICOM Standard Attribute (300A,0312) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0318)": DicomTagDefinition(
        tag="(300A,0318)",
        group="300A",
        element="0318",
        vr="LO",
        vm="2",
        keyword="Tag_300A_0318_Keyword",
        name="DICOM Standard Attribute (300A,0318) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,031E)": DicomTagDefinition(
        tag="(300A,031E)",
        group="300A",
        element="031E",
        vr="SH",
        vm="3",
        keyword="Tag_300A_031E_Keyword",
        name="DICOM Standard Attribute (300A,031E) for Radiotherapy Plan Subsystem Specification",
        retired=True
    ),
    "(300A,0324)": DicomTagDefinition(
        tag="(300A,0324)",
        group="300A",
        element="0324",
        vr="CS",
        vm="6",
        keyword="Tag_300A_0324_Keyword",
        name="DICOM Standard Attribute (300A,0324) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,032A)": DicomTagDefinition(
        tag="(300A,032A)",
        group="300A",
        element="032A",
        vr="UI",
        vm="1",
        keyword="Tag_300A_032A_Keyword",
        name="DICOM Standard Attribute (300A,032A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0330)": DicomTagDefinition(
        tag="(300A,0330)",
        group="300A",
        element="0330",
        vr="PN",
        vm="1-N",
        keyword="Tag_300A_0330_Keyword",
        name="DICOM Standard Attribute (300A,0330) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0336)": DicomTagDefinition(
        tag="(300A,0336)",
        group="300A",
        element="0336",
        vr="DA",
        vm="2",
        keyword="Tag_300A_0336_Keyword",
        name="DICOM Standard Attribute (300A,0336) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,033C)": DicomTagDefinition(
        tag="(300A,033C)",
        group="300A",
        element="033C",
        vr="TM",
        vm="3",
        keyword="Tag_300A_033C_Keyword",
        name="DICOM Standard Attribute (300A,033C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0342)": DicomTagDefinition(
        tag="(300A,0342)",
        group="300A",
        element="0342",
        vr="DS",
        vm="6",
        keyword="Tag_300A_0342_Keyword",
        name="DICOM Standard Attribute (300A,0342) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0348)": DicomTagDefinition(
        tag="(300A,0348)",
        group="300A",
        element="0348",
        vr="IS",
        vm="1",
        keyword="Tag_300A_0348_Keyword",
        name="DICOM Standard Attribute (300A,0348) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,034E)": DicomTagDefinition(
        tag="(300A,034E)",
        group="300A",
        element="034E",
        vr="SQ",
        vm="1-N",
        keyword="Tag_300A_034E_Keyword",
        name="DICOM Standard Attribute (300A,034E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0354)": DicomTagDefinition(
        tag="(300A,0354)",
        group="300A",
        element="0354",
        vr="US",
        vm="2",
        keyword="Tag_300A_0354_Keyword",
        name="DICOM Standard Attribute (300A,0354) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,035A)": DicomTagDefinition(
        tag="(300A,035A)",
        group="300A",
        element="035A",
        vr="LO",
        vm="3",
        keyword="Tag_300A_035A_Keyword",
        name="DICOM Standard Attribute (300A,035A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0360)": DicomTagDefinition(
        tag="(300A,0360)",
        group="300A",
        element="0360",
        vr="SH",
        vm="6",
        keyword="Tag_300A_0360_Keyword",
        name="DICOM Standard Attribute (300A,0360) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0366)": DicomTagDefinition(
        tag="(300A,0366)",
        group="300A",
        element="0366",
        vr="CS",
        vm="1",
        keyword="Tag_300A_0366_Keyword",
        name="DICOM Standard Attribute (300A,0366) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,036C)": DicomTagDefinition(
        tag="(300A,036C)",
        group="300A",
        element="036C",
        vr="UI",
        vm="1-N",
        keyword="Tag_300A_036C_Keyword",
        name="DICOM Standard Attribute (300A,036C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0372)": DicomTagDefinition(
        tag="(300A,0372)",
        group="300A",
        element="0372",
        vr="PN",
        vm="2",
        keyword="Tag_300A_0372_Keyword",
        name="DICOM Standard Attribute (300A,0372) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0378)": DicomTagDefinition(
        tag="(300A,0378)",
        group="300A",
        element="0378",
        vr="DA",
        vm="3",
        keyword="Tag_300A_0378_Keyword",
        name="DICOM Standard Attribute (300A,0378) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,037E)": DicomTagDefinition(
        tag="(300A,037E)",
        group="300A",
        element="037E",
        vr="TM",
        vm="6",
        keyword="Tag_300A_037E_Keyword",
        name="DICOM Standard Attribute (300A,037E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0384)": DicomTagDefinition(
        tag="(300A,0384)",
        group="300A",
        element="0384",
        vr="DS",
        vm="1",
        keyword="Tag_300A_0384_Keyword",
        name="DICOM Standard Attribute (300A,0384) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,038A)": DicomTagDefinition(
        tag="(300A,038A)",
        group="300A",
        element="038A",
        vr="IS",
        vm="1-N",
        keyword="Tag_300A_038A_Keyword",
        name="DICOM Standard Attribute (300A,038A) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0390)": DicomTagDefinition(
        tag="(300A,0390)",
        group="300A",
        element="0390",
        vr="SQ",
        vm="2",
        keyword="Tag_300A_0390_Keyword",
        name="DICOM Standard Attribute (300A,0390) for Radiotherapy Plan Subsystem Specification",
        retired=True
    ),
    "(300A,0396)": DicomTagDefinition(
        tag="(300A,0396)",
        group="300A",
        element="0396",
        vr="US",
        vm="3",
        keyword="Tag_300A_0396_Keyword",
        name="DICOM Standard Attribute (300A,0396) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,039C)": DicomTagDefinition(
        tag="(300A,039C)",
        group="300A",
        element="039C",
        vr="LO",
        vm="6",
        keyword="Tag_300A_039C_Keyword",
        name="DICOM Standard Attribute (300A,039C) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03A2)": DicomTagDefinition(
        tag="(300A,03A2)",
        group="300A",
        element="03A2",
        vr="SH",
        vm="1",
        keyword="Tag_300A_03A2_Keyword",
        name="DICOM Standard Attribute (300A,03A2) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03A8)": DicomTagDefinition(
        tag="(300A,03A8)",
        group="300A",
        element="03A8",
        vr="CS",
        vm="1-N",
        keyword="Tag_300A_03A8_Keyword",
        name="DICOM Standard Attribute (300A,03A8) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03AE)": DicomTagDefinition(
        tag="(300A,03AE)",
        group="300A",
        element="03AE",
        vr="UI",
        vm="2",
        keyword="Tag_300A_03AE_Keyword",
        name="DICOM Standard Attribute (300A,03AE) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03B4)": DicomTagDefinition(
        tag="(300A,03B4)",
        group="300A",
        element="03B4",
        vr="PN",
        vm="3",
        keyword="Tag_300A_03B4_Keyword",
        name="DICOM Standard Attribute (300A,03B4) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03BA)": DicomTagDefinition(
        tag="(300A,03BA)",
        group="300A",
        element="03BA",
        vr="DA",
        vm="6",
        keyword="Tag_300A_03BA_Keyword",
        name="DICOM Standard Attribute (300A,03BA) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03C0)": DicomTagDefinition(
        tag="(300A,03C0)",
        group="300A",
        element="03C0",
        vr="TM",
        vm="1",
        keyword="Tag_300A_03C0_Keyword",
        name="DICOM Standard Attribute (300A,03C0) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03C6)": DicomTagDefinition(
        tag="(300A,03C6)",
        group="300A",
        element="03C6",
        vr="DS",
        vm="1-N",
        keyword="Tag_300A_03C6_Keyword",
        name="DICOM Standard Attribute (300A,03C6) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03CC)": DicomTagDefinition(
        tag="(300A,03CC)",
        group="300A",
        element="03CC",
        vr="IS",
        vm="2",
        keyword="Tag_300A_03CC_Keyword",
        name="DICOM Standard Attribute (300A,03CC) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03D2)": DicomTagDefinition(
        tag="(300A,03D2)",
        group="300A",
        element="03D2",
        vr="SQ",
        vm="3",
        keyword="Tag_300A_03D2_Keyword",
        name="DICOM Standard Attribute (300A,03D2) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03D8)": DicomTagDefinition(
        tag="(300A,03D8)",
        group="300A",
        element="03D8",
        vr="US",
        vm="6",
        keyword="Tag_300A_03D8_Keyword",
        name="DICOM Standard Attribute (300A,03D8) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03DE)": DicomTagDefinition(
        tag="(300A,03DE)",
        group="300A",
        element="03DE",
        vr="LO",
        vm="1",
        keyword="Tag_300A_03DE_Keyword",
        name="DICOM Standard Attribute (300A,03DE) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03E4)": DicomTagDefinition(
        tag="(300A,03E4)",
        group="300A",
        element="03E4",
        vr="SH",
        vm="1-N",
        keyword="Tag_300A_03E4_Keyword",
        name="DICOM Standard Attribute (300A,03E4) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03EA)": DicomTagDefinition(
        tag="(300A,03EA)",
        group="300A",
        element="03EA",
        vr="CS",
        vm="2",
        keyword="Tag_300A_03EA_Keyword",
        name="DICOM Standard Attribute (300A,03EA) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03F0)": DicomTagDefinition(
        tag="(300A,03F0)",
        group="300A",
        element="03F0",
        vr="UI",
        vm="3",
        keyword="Tag_300A_03F0_Keyword",
        name="DICOM Standard Attribute (300A,03F0) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03F6)": DicomTagDefinition(
        tag="(300A,03F6)",
        group="300A",
        element="03F6",
        vr="PN",
        vm="6",
        keyword="Tag_300A_03F6_Keyword",
        name="DICOM Standard Attribute (300A,03F6) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,03FC)": DicomTagDefinition(
        tag="(300A,03FC)",
        group="300A",
        element="03FC",
        vr="DA",
        vm="1",
        keyword="Tag_300A_03FC_Keyword",
        name="DICOM Standard Attribute (300A,03FC) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0402)": DicomTagDefinition(
        tag="(300A,0402)",
        group="300A",
        element="0402",
        vr="TM",
        vm="1-N",
        keyword="Tag_300A_0402_Keyword",
        name="DICOM Standard Attribute (300A,0402) for Radiotherapy Plan Subsystem Specification",
        retired=True
    ),
    "(300A,0408)": DicomTagDefinition(
        tag="(300A,0408)",
        group="300A",
        element="0408",
        vr="DS",
        vm="2",
        keyword="Tag_300A_0408_Keyword",
        name="DICOM Standard Attribute (300A,0408) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,040E)": DicomTagDefinition(
        tag="(300A,040E)",
        group="300A",
        element="040E",
        vr="IS",
        vm="3",
        keyword="Tag_300A_040E_Keyword",
        name="DICOM Standard Attribute (300A,040E) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
    "(300A,0414)": DicomTagDefinition(
        tag="(300A,0414)",
        group="300A",
        element="0414",
        vr="SQ",
        vm="6",
        keyword="Tag_300A_0414_Keyword",
        name="DICOM Standard Attribute (300A,0414) for Radiotherapy Plan Subsystem Specification",
        retired=False
    ),
}

def lookup_dicom_tag(tag_str: str) -> Optional[DicomTagDefinition]:
    """Looks up tag definition by (GGGG,EEEE) format or hex tag"""
    tag_formatted = tag_str.upper()
    if not tag_formatted.startswith("("):
        if len(tag_formatted) == 8:
            tag_formatted = f"({tag_formatted[:4]},{tag_formatted[4:]})"
    return STANDARD_DICOM_TAGS.get(tag_formatted)
