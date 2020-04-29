import logging
from pathlib import Path

from preprocess.document_reader import Document
from preprocess.utils import utils

logger = logging.getLogger(__name__)


def export_to_json(document: Document, out_file: str) -> str:
    with open(out_file, 'w', encoding='utf8') as f:
        print(document, file=f)

    return out_file


def export_to_txt(document: Document, out_file: str) -> str:
    with open(out_file, 'w', encoding='utf8') as f:
        for paragraph in document:
            f.write(str(paragraph) + '\n')

    return out_file


def export_to_csv(document: Document, out_file: str) -> str:
    with open(out_file, 'w', encoding='utf8') as f:
        import csv
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['bullet_text', 'numbering_text', 'paragraph_text'])
        for paragraph in document:
            writer.writerow(paragraph)

    return out_file


def export_to_xlsx(document: Document, out_file: str) -> str:
    import xlsxwriter
    with xlsxwriter.Workbook(out_file) as workbook:
        worksheet = utils.setup_worksheet(
            workbook,
            ['#', 'paragraph_text', 'indentation', 'is_title', 'is_table', 'layout'],
            [5, 100, 15, 15, 15, 100])

        for row_index, paragraph in enumerate(document, 1):
            col_index = iter(range(100))
            worksheet.write_number(row_index, next(col_index), paragraph.index)
            # worksheet.write_string(row_index, next(col_index), paragraph.bullet.text)
            # worksheet.write_string(row_index, next(col_index), paragraph.numbering.text)
            worksheet.write_string(row_index, next(col_index), paragraph.text)
            worksheet.write_number(row_index, next(col_index), paragraph.indentation)
            worksheet.write_string(row_index, next(col_index), 'x' if paragraph.is_title() else '')
            worksheet.write_string(row_index, next(col_index), 'x' if paragraph.is_table() else '')
            worksheet.write_string(row_index, next(col_index), str(paragraph.layout))

    return out_file


def export(document: Document, extension: str = '.json', out_dir: str = '.cache') -> str:
    """ Export the paragraphs in `document` to `fmt` format in `out_dir` folder.
    :param document: a Document object, typically, output from the document_reader module.
    :param extension: string, supported format: .json, .csv, .txt, .xlsx
    :param out_dir: folder to place the exported file.
    """
    out_path = Path(out_dir)
    out_path.mkdir(exist_ok=True)

    out_file = str(out_path.joinpath(Path(document.file_name).name + extension))

    logger.info(f'Exporting {document.file_name} to {out_file}')

    try:
        extension = extension.lower()
        if extension == '.json': return export_to_json(document, out_file)
        if extension == '.csv': return export_to_csv(document, out_file)
        if extension == '.txt': return export_to_txt(document, out_file)
        if extension == '.xlsx': return export_to_xlsx(document, out_file)

        raise Exception(f'{extension} format does not support. No file will be exported!')
    except Exception as e:
        logging.error(
            f'{e} \n'
            f'Context: {__name__}(document={document.file_name},fmt={extension},out_dir={out_dir})')
        raise
