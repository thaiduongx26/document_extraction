import logging

import utils
from preprocess.document_structuring.node import Node
from preprocess.utils.color_utils import generate_random_bright_color

logger = logging.getLogger(__name__)


class Exporter:
    def __init__(self, root: Node):
        """Export the SE output tree to different formats such as json, xlsx.
        :param root: root of the SE output tree.
        """
        self._root = root

    def flatten_tree(self):
        """Flatten the tree. (express the tree in list format)
        :return: the flattened tree as a list.
        """
        result_list = []

        def append_result_list(node: Node):
            nonlocal result_list
            result_list.append(
                dict(index=node.paragraph.index, parent_index=node.parent_index,
                     text=node.paragraph.text, is_table=node.paragraph.is_table(),
                     bullet=node.paragraph.bullet.text,
                     numbering=node.paragraph.numbering.text,
                     is_title=(node.paragraph.is_title()
                               or node.paragraph.has_bullet()
                               or node.paragraph.has_numbering())
                              and len(node.children) > 0,
                     has_child=len(node.children) > 0,
                     page_number=node.paragraph.page_number,
                     parser=node.parser_name))

        self._travel_tree(self._root, append_result_list)

        return result_list

    def to_json_flattened(self, outfile):
        logger.info('OUTPUT-FLATTENED-JSON: ' + outfile)
        with open(outfile, 'w+', encoding='utf-8') as f:
            import json
            json.dump(self.flatten_tree(), f, ensure_ascii=False, indent=2)

    def to_xlsx(self, outfile: str):
        import xlsxwriter
        if utils.enable_debug:
            logger.info('OUTPUT-XLSX:      ' + outfile)

        # TODO: implement an util to fit the data
        def col_counter(counter=100):
            for i in range(counter):
                yield i

        ctr1 = col_counter()
        ctr2 = col_counter()
        workbook = xlsxwriter.Workbook(outfile)
        worksheet = workbook.add_worksheet('Sheet1')
        worksheet.set_default_row(30)
        worksheet.set_column(next(ctr2), next(ctr1), width=7)  # Page number
        if utils.enable_debug:
            worksheet.set_column(next(ctr2), next(ctr1), width=5)  # Bullet
            worksheet.set_column(next(ctr2), next(ctr1), width=9)  # Numbering
        worksheet.set_column(next(ctr2), next(ctr1), width=100)  # Text
        # worksheet.set_column(next(ctr2), next(ctr1), width=50)  # Title
        worksheet.set_column(next(ctr2), next(ctr1), width=7)  # Index
        worksheet.set_column(next(ctr2), next(ctr1), width=12)  # Parent Index
        worksheet.set_column(next(ctr2), next(ctr1), width=12)  # Is Title
        worksheet.set_column(next(ctr2), next(ctr1), width=12)  # Is Table
        if utils.enable_debug:
            worksheet.set_column(next(ctr2), next(ctr1), width=25)  # Parser
        ctr1 = col_counter()
        cell_header_format = workbook.add_format({'align': 'center',
                                                  'valign': 'vcenter',
                                                  'border': 1,
                                                  'bold': True,
                                                  'font_name': 'Times New Roman',
                                                  'font_size': 12})
        worksheet.write_string(0, next(ctr1), 'Page No', cell_header_format)
        if utils.enable_debug:
            worksheet.write_string(0, next(ctr1), 'Bullet', cell_header_format)
            worksheet.write_string(0, next(ctr1), 'Numbering', cell_header_format)
        worksheet.write_string(0, next(ctr1), 'Text', cell_header_format)
        # worksheet.write_string(0, next(ctr1), 'Title', cell_header_format)
        worksheet.write_string(0, next(ctr1), 'Index', cell_header_format)
        worksheet.write_string(0, next(ctr1), 'Parent Index', cell_header_format)
        worksheet.write_string(0, next(ctr1), 'Is Title', cell_header_format)
        worksheet.write_string(0, next(ctr1), 'Is Table', cell_header_format)
        if utils.enable_debug:
            worksheet.write_string(0, next(ctr1), 'Parser', cell_header_format)
        row_index = 0
        colors = dict()
        default_fmt = workbook.add_format()
        title_fmt = workbook.add_format({'bg_color': 'yellow'})
        for row in self.flatten_tree():
            row_index += 1
            ctr1 = col_counter()
            row_index_format = workbook.add_format()
            cell_format = default_fmt
            if row['has_child']:
                cell_format = title_fmt
                row_index_format = workbook.add_format({'bg_color': generate_random_bright_color()})
                colors[row['index']] = row_index_format
            worksheet.write_number(row_index, next(ctr1), row['page_number'], cell_format)
            if utils.enable_debug:
                worksheet.write_string(row_index, next(ctr1), row['bullet'], cell_format)
                worksheet.write_string(row_index, next(ctr1), row['numbering'], cell_format)
            worksheet.write_string(row_index, next(ctr1), row['text'], cell_format)
            # worksheet.write_string(row_index, next(ctr1),
            #                        row['title'] if row['title'] is not None else '', cell_format)
            worksheet.write_number(row_index, next(ctr1), row['index'], row_index_format)
            if row['parent_index'] is not None:
                worksheet.write_number(row_index, next(ctr1), row['parent_index'],
                                       colors[row['parent_index']])
            else:
                worksheet.write_string(row_index, next(ctr1), '')
            worksheet.write_string(row_index, next(ctr1), 'x' if row['is_title'] else '', cell_format)
            worksheet.write_string(row_index, next(ctr1), 'x' if row['is_table'] else '', cell_format)
            if utils.enable_debug:
                worksheet.write_string(row_index, next(ctr1), row['parser'], cell_format)
        workbook.close()
        return outfile


    def to_json(self, outfile: str):
        """Export SE output tree to json.
        :param outfile: path of the output JSON file.
        """
        logger.info('OUTPUT-TREE-JSON:      ' + outfile)

        with open(outfile, 'w+', encoding="utf-8") as f:
            print(self._root, file=f)

    def _travel_tree(self, node: Node, exporter):
        if not node.is_root():
            exporter(node)

        for child in node.children:
            self._travel_tree(child, exporter)
