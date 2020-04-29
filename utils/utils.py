import json
import logging
import shutil
from collections import namedtuple
from pathlib import Path
from typing import List

import logging

from utils import Folder

logger = logging.getLogger(__name__)
import utils

Output = namedtuple('Output', 'filename, status, message, AI_output, SE_output')


def ignore(folder: Path):
    """Mark a contract/consortium folder as skipped by placing a `skipped.end` file.
    :param folder: path to consortium/contract folder.
    """
    logger.warning(f'Ignoring "{folder}" by renaming lock file to "skipped.end"')
    try:
        lock_file = folder.joinpath('end')
        skipped_lock_file = folder.joinpath('skipped.end')
        if lock_file.exists():
            shutil.move(str(lock_file), str(skipped_lock_file))
        else:
            skipped_lock_file.touch(exist_ok=True)
    except BaseException as e:
        logger.exception(f'Unable mark "{folder}" as skipped due to "{e}"')
        logger.fatal(f'Unable to process or remove lock for "{folder}"')


def move_to_working_folder(pdf_files: List[Path]) -> List[Path]:
    """ Move pdf files to a working folder.
    """
    files = []
    for pdf_file in pdf_files:
        try:
            working_pdf_file = Path(str(pdf_file.absolute()).replace('/input/', '/working/', 1))
            if working_pdf_file != pdf_file:
                working_pdf_file.parent.mkdir(exist_ok=True, parents=True)
                shutil.move(str(pdf_file), str(working_pdf_file))

            files.append(working_pdf_file)
        except BaseException as e:
            logger.exception(f'Unable to move "{pdf_file}" to working folder due to "{e}"')

    return files


def move_to_output_folder(batch_id, working_file: Path) -> Path:
    dest = Path(str(working_file.absolute()).replace(Folder.working, f'{Folder.output}/{batch_id}'))
    try:
        dest.parent.mkdir(exist_ok=True, parents=True)
        shutil.move(str(working_file), str(dest))

        return dest
    except BaseException as e:
        logger.exception(f'Unable to move "{working_file}" to "{dest}" due to "{e}"')
        raise


def write_output(output_pdf_file: Path, output: dict) -> None:
    if utils.enable_debug:
        output_json_file = str(output_pdf_file)[:-3] + 'ai.json'
        with open(output_json_file, 'w', encoding='utf8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

    output_excel_file = str(output_pdf_file)[:-3] + 'xlsx'

    import xlsxwriter
    def col_counter(counter=100):
        for i in range(counter):
            yield i

    ctr1 = col_counter()
    ctr2 = col_counter()
    workbook = xlsxwriter.Workbook(output_excel_file)
    worksheet = workbook.add_worksheet('Sheet1')
    worksheet.set_default_row(30)
    worksheet.set_column(next(ctr2), next(ctr1), width=30)  # Filename
    worksheet.set_column(next(ctr2), next(ctr1), width=50)  # Item ID
    worksheet.set_column(next(ctr2), next(ctr1), width=100)  # Result

    ctr1 = col_counter()
    cell_header_format = workbook.add_format({'align': 'center',
                                              'valign': 'vcenter',
                                              'border': 1,
                                              'bold': True,
                                              'font_name': 'Times New Roman',
                                              'font_size': 12})
    worksheet.write_string(0, next(ctr1), 'File Name', cell_header_format)
    worksheet.write_string(0, next(ctr1), 'Item ID', cell_header_format)
    worksheet.write_string(0, next(ctr1), 'result', cell_header_format)

    row_index = 0
    for tag, results in output['AI_output'].items():
        for result in results:
            for extracted_text in result['texts_extracted']:
                row_index += 1
                ctr1 = col_counter()
                worksheet.write_string(row_index, next(ctr1), output['file_name'])
                worksheet.write_string(row_index, next(ctr1), tag)
                worksheet.write_string(row_index, next(ctr1), extracted_text)

    workbook.close()


def log_master_record(filename, page_count):
    logging.getLogger('charge_log').info(f'{filename},{page_count}')


def delete_cache():
    shutil.rmtree(Folder.working + '/.cache', ignore_errors=True)
