import logging
import os
import time
import warnings
from datetime import datetime
from pathlib import Path
from typing import Union

import utils
from preprocess import process_file
from utils.ai import initialize_ai_model

logger = logging.getLogger(__name__)
logging.getLogger('pdfminer').setLevel(logging.ERROR)


def dummy(*args, **kwargs):
    pass


warnings.warn = dummy


def run_pipeline(model, file: Union[Path, str]) -> dict:
    se_output, excel_file = process_file(str(file))
    logger.info(f'Predicting "{Path(file).name}"')
    ai_output = model.predict_excel(excel_file)
    return dict(file_name=Path(file).name,
                AI_output=ai_output,
                SE_output=se_output)


def main_loop():
    model = initialize_ai_model()

    while True:
        begin = time.time()
        try:
            input_pdf_files = utils.sensor.scan()
            if input_pdf_files:
                batch_id = f'{datetime.now().strftime("%Y%m%d%H%M%S")}'
                logger.info(
                    f'Starting batch "{batch_id}" with '
                    f'{len(input_pdf_files)} files: "{", ".join([file.name for file in input_pdf_files])}"')

                working_pdf_files = utils.move_to_working_folder(input_pdf_files)
                for file in working_pdf_files:
                    logger.info(f'Reading "{file.name}"')
                    try:
                        result = run_pipeline(model, file)
                        output_file = utils.move_to_output_folder(batch_id, file)
                        utils.write_output(output_file, result)
                        utils.log_master_record(file.name, result['SE_output'][-1]['page_number'])
                    except BaseException as e:
                        logger.exception(f'Error while processing file "{file}" due to \n{e}')

                if not utils.enable_debug:
                    utils.delete_cache()
                os.system(f'chmod -R a+rw {utils.Folder.output}')
                logger.info(f'Batch "{batch_id}" finished.')

        except BaseException as e:
            logger.exception(e)
            if utils.enable_debug:
                raise
        finally:
            sleep_time = int(utils.settings['sensor']['schedule']) - (time.time() - begin)
            time.sleep(sleep_time if sleep_time > 0 else 0)


if __name__ == '__main__':
    main_loop()
