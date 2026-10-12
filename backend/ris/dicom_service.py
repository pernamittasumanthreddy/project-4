import os
import io
import math
import numpy as np
from pathlib import Path
from django.conf import settings
from django.utils import timezone
import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, SecondaryCaptureImageStorage, generate_uid
from PIL import Image

def generate_synthetic_dicom_file(patient, procedure, study_uid, accession_no, modality='DX', slice_index=1, total_slices=1):
    """
    Generates a genuine standard-compliant DICOM file (.dcm) with:
    - Standard DICOM Part 10 header
    - File Meta Information (Transfer Syntax: Explicit VR Little Endian)
    - Full patient demographics and clinical tags
    - Anatomical synthetic pixel data with appropriate Hounsfield Units / Grayscale
    """
    storage_dir = Path(settings.DICOM_STORAGE_ROOT) / study_uid
    storage_dir.mkdir(parents=True, exist_ok=True)
    file_path = storage_dir / f"slice_{slice_index:03d}.dcm"

    # 1. Create File Meta Information
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
    sop_instance_uid = f"{study_uid}.1.{slice_index}"
    file_meta.MediaStorageSOPInstanceUID = sop_instance_uid
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    # 2. Main DICOM Dataset
    ds = Dataset()
    ds.file_meta = file_meta
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    # Patient Module
    ds.PatientName = f"{patient.last_name}^{patient.first_name}"
    ds.PatientID = patient.uhid
    ds.PatientBirthDate = patient.dob.strftime('%Y%m%d') if patient.dob else '19850101'
    ds.PatientSex = patient.gender

    # Study Module
    ds.StudyInstanceUID = study_uid
    ds.StudyDate = timezone.now().strftime('%Y%m%d')
    ds.StudyTime = timezone.now().strftime('%H%M%S')
    ds.AccessionNumber = accession_no
    ds.StudyID = accession_no
    ds.StudyDescription = procedure.name

    # Series Module
    series_uid = f"{study_uid}.1"
    ds.SeriesInstanceUID = series_uid
    ds.SeriesNumber = 1
    ds.Modality = modality
    ds.SeriesDescription = f"{procedure.body_part} {modality} Series"

    # Instance Module
    ds.SOPClassUID = SecondaryCaptureImageStorage
    ds.SOPInstanceUID = sop_instance_uid
    ds.InstanceNumber = slice_index

    # Image Pixel Module
    width, height = 512, 512
    ds.Rows = height
    ds.Columns = width
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.BitsAllocated = 16
    ds.BitsStored = 12
    ds.HighBit = 11
    ds.PixelRepresentation = 0 # unsigned 12-bit
    ds.RescaleIntercept = "0"
    ds.RescaleSlope = "1"

    # Window / Level defaults according to modality
    if modality == 'CT':
        ds.WindowCenter = "40"
        ds.WindowWidth = "400"
    elif modality == 'MR':
        ds.WindowCenter = "500"
        ds.WindowWidth = "1000"
    else: # DX / X-Ray
        ds.WindowCenter = "2048"
        ds.WindowWidth = "4096"

    # Generate synthetic anatomical slice
    # Grid coordinates
    y, x = np.ogrid[:height, :width]
    center_y, center_x = height // 2, width // 2

    if modality == 'CT':
        # Thorax CT simulation: Outer body contour, lung fields, spine, heart
        body_mask = ((x - center_x) ** 2 / (200 ** 2) + (y - center_y) ** 2 / (160 ** 2)) < 1.0
        # Lungs (dark/low attenuation, air ~ -800 to -500 HU -> scaled to 200..400)
        left_lung = ((x - (center_x - 85)) ** 2 / (55 ** 2) + (y - (center_y - 10)) ** 2 / (80 ** 2)) < 1.0
        right_lung = ((x - (center_x + 85)) ** 2 / (55 ** 2) + (y - (center_y - 10)) ** 2 / (80 ** 2)) < 1.0
        # Spine bone (dense, high HU ~ 1500)
        spine = ((x - center_x) ** 2 / (25 ** 2) + (y - (center_y + 110)) ** 2 / (25 ** 2)) < 1.0
        # Sternum
        sternum = ((x - center_x) ** 2 / (20 ** 2) + (y - (center_y - 140)) ** 2 / (15 ** 2)) < 1.0
        # Heart / Mediastinum (soft tissue ~ 1000)
        heart = ((x - (center_x - 20)) ** 2 / (45 ** 2) + (y - (center_y + 10)) ** 2 / (50 ** 2)) < 1.0

        pixel_data = np.zeros((height, width), dtype=np.uint16)
        pixel_data[body_mask] = 1000 # Soft tissue
        pixel_data[left_lung] = 200 # Air
        pixel_data[right_lung] = 200
        pixel_data[heart] = 1050
        pixel_data[spine] = 2800 # Bone
        pixel_data[sternum] = 2600

        # Add simulated pulmonary vascular markings
        noise = np.random.RandomState(42 + slice_index).randint(0, 150, size=(height, width)).astype(np.uint16)
        pixel_data[left_lung | right_lung] += (noise[left_lung | right_lung] // 2)

    elif modality == 'MR':
        # Brain MRI simulation (Skull, CSF, White matter, Gray matter)
        head_mask = ((x - center_x) ** 2 / (170 ** 2) + (y - center_y) ** 2 / (190 ** 2)) < 1.0
        skull = head_mask & ~(((x - center_x) ** 2 / (155 ** 2) + (y - center_y) ** 2 / (175 ** 2)) < 1.0)
        brain = ((x - center_x) ** 2 / (150 ** 2) + (y - center_y) ** 2 / (170 ** 2)) < 1.0
        ventricle_left = ((x - (center_x - 25)) ** 2 / (15 ** 2) + (y - center_y) ** 2 / (40 ** 2)) < 1.0
        ventricle_right = ((x - (center_x + 25)) ** 2 / (15 ** 2) + (y - center_y) ** 2 / (40 ** 2)) < 1.0

        pixel_data = np.zeros((height, width), dtype=np.uint16)
        pixel_data[skull] = 400
        pixel_data[brain] = 1400
        # Cortex modulation
        r = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        theta = np.arctan2(y - center_y, x - center_x)
        gyri = (np.sin(theta * 12 + slice_index) * 200).astype(np.int16)
        pixel_data[brain] = np.clip(pixel_data[brain].astype(np.int32) + gyri[brain], 800, 1800).astype(np.uint16)
        pixel_data[ventricle_left | ventricle_right] = 300 # CSF (dark on T1)

    else: # Digital Radiography / X-Ray
        # Chest PA Radiograph projection
        body_outline = ((x - center_x) ** 2 / (210 ** 2) + (y - center_y) ** 2 / (230 ** 2)) < 1.0
        lungs_l = ((x - (center_x - 90)) ** 2 / (65 ** 2) + (y - (center_y - 20)) ** 2 / (110 ** 2)) < 1.0
        lungs_r = ((x - (center_x + 90)) ** 2 / (65 ** 2) + (y - (center_y - 20)) ** 2 / (110 ** 2)) < 1.0
        heart_shadow = ((x - (center_x - 30)) ** 2 / (70 ** 2) + (y - (center_y + 40)) ** 2 / (70 ** 2)) < 1.0
        spine_strip = (np.abs(x - center_x) < 25) & (y > 40) & (y < 460)
        clavicle_l = (y > 100) & (y < 125) & (x > 80) & (x < 240)
        clavicle_r = (y > 100) & (y < 125) & (x > 272) & (x < 432)

        pixel_data = np.full((height, width), 400, dtype=np.uint16) # Air surrounding
        pixel_data[body_outline] = 1200 # Soft tissue
        pixel_data[lungs_l | lungs_r] = 600 # Radiolucent lungs
        pixel_data[heart_shadow] = 2200 # Radiopaque cardiac density
        pixel_data[spine_strip] = 2600 # Dense vertebral column
        pixel_data[clavicle_l | clavicle_r] = 2400 # Clavicles

        # Simulated rib cages
        for rib_y in range(160, 420, 45):
            rib_mask = (y >= rib_y) & (y <= rib_y + 16) & (body_outline)
            pixel_data[rib_mask] = np.clip(pixel_data[rib_mask].astype(np.int32) + 600, 0, 4095).astype(np.uint16)

    ds.PixelData = pixel_data.tobytes()
    pydicom.filewriter.dcmwrite(str(file_path), ds, write_like_original=False)
    return str(file_path)

def render_dicom_to_png_bytes(dcm_path):
    """Parses a real DICOM file and returns high-resolution PNG bytes for preview/fallback"""
    ds = pydicom.dcmread(dcm_path)
    arr = ds.pixel_array.astype(float)
    # Rescale slope / intercept
    slope = getattr(ds, 'RescaleSlope', 1)
    intercept = getattr(ds, 'RescaleIntercept', 0)
    arr = arr * float(slope) + float(intercept)

    # Window / Level
    wc = float(getattr(ds, 'WindowCenter', np.mean(arr)))
    ww = float(getattr(ds, 'WindowWidth', np.ptp(arr) or 1))
    
    val_min = wc - ww / 2.0
    val_max = wc + ww / 2.0
    arr_clipped = np.clip((arr - val_min) / (val_max - val_min), 0.0, 1.0)
    img_8bit = (arr_clipped * 255.0).astype(np.uint8)

    img = Image.fromarray(img_8bit)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()
