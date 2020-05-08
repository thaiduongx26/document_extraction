import logging
import shutil

from preprocess import process_folder, process_file
from utils.ai import initialize_ai_model

logging.getLogger('pdfminer').setLevel(level=logging.ERROR)
logging.getLogger('PIL').setLevel(level=logging.ERROR)
logger = logging.getLogger()


def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn


# def test_entry_point():
#     try:
#         shutil.rmtree('data/working', ignore_errors=True)
#         shutil.rmtree('data/input/*', ignore_errors=True)
#         shutil.rmtree('E:\\document_dataset\\kepco_output', ignore_errors=True)
#         shutil.copy('data/0001_no19-270.pdf', 'data/input/0001_no19-270.pdf')
#     except BaseException as e:
#         logging.exception(e)
#         pass
#
#     from entrypoint import main_loop
#     main_loop()


def full_flow(input_file: str):
    model = initialize_ai_model()

    _, excel_file = process_file(input_file)
    ai_output = model.predict_excel(excel_file)
    return ai_output


def se_flow():
    # process_folder('E:\\document_dataset\\kepco_data_pdf')
    process_folder('E:\\document_dataset\\pdf_files\\working', output_folder = 'E:\\document_dataset\\pdf_files\\debug')
    # process_folder('E:\\document_dataset\\pdf_files', output_folder = 'E:\\document_dataset\\yoko_table_output')

    # process_file('data/original_pdf/0257_SN15-296.pdf')

    # from preprocess.utils.utils import launch
    from preprocess.utils.utils import launch
    # launch('data/original_pdf/.cache/0001_no19-270.pdf.xlsx')
    # launch('data/se/.cache/.cache/a.html.xlsx')


# Entry point
def main():
    se_flow()


if __name__ == '__main__':
    main()
