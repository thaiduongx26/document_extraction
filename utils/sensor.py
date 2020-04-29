import glob
from pathlib import Path
from typing import List

import logging

logger = logging.getLogger(__name__)

is_first_run_ = True
enable_sensor_log = True


def collect_document(folder: str) -> List[Path]:
    pdf_files = []
    for file in glob.glob(f'{folder}/**/*.pdf', recursive=True):
        pdf_files.append(Path(file))

    if enable_sensor_log and pdf_files:
        logger.info(f'Found {len(pdf_files)} PDF files under {folder}')

    return pdf_files


def scan() -> List[Path]:
    """ Scan for pdf file within `input` and `working` folder
    :return:
    """
    global enable_sensor_log
    if enable_sensor_log:
        logger.info('Scanning for new document')

    pdf_files = []
    global is_first_run_
    if is_first_run_:
        is_first_run_ = False
        pdf_files.extend(collect_document('data/working'))

    pdf_files.extend(collect_document('data/input'))

    enable_sensor_log = len(pdf_files) > 0
    return pdf_files
