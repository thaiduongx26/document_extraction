import os
import numpy as np
import pandas as pd
import re, glob
from tqdm import tqdm
import unicodedata


def lcs_not_recognition(a, b):
    # generate matrix of length of longest common subsequence for substrings of both words
    lengths = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if (x == y) or ((x in y or y in x) and (abs(len(x) - len(y)) <= 3)):
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])

    # read a substring from the matrix
    result = []
    j = len(b)
    for i in range(1, len(a) + 1):
        if lengths[i][j] != lengths[i - 1][j]:
            pass
        else:
            result.append(a[i - 1])
    return len(result)


def lcs(a, b):
    # generate matrix of length of longest common subsequence for substrings of both words
    lengths = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if (x == y) or ((x in y or y in x) and (abs(len(x) - len(y)) <= 3)):
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])

    # read a substring from the matrix
    result = []
    j = len(b)
    for i in range(1, len(a) + 1):
        if lengths[i][j] != lengths[i - 1][j]:
            result.append(a[i - 1])
    #     print(len(result))
    return len(result)


def lcs_get_list(a, b):
    # generate matrix of length of longest common subsequence for substrings of both words
    lengths = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if (x == y) or ((x in y or y in x) and (abs(len(x) - len(y)) < 3)):
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])

    # read a substring from the matrix
    result = []
    j = len(b)
    for i in range(1, len(a) + 1):
        if lengths[i][j] != lengths[i - 1][j]:
            result.append(a[i - 1])
    #     print(len(result))
    return result


def text_process(text):
    text = str(text)
    text = unicodedata.normalize('NFKC', text)
    text = re.sub('\s+', '', text)
    return text


def read_excel(excel_path, extract_sent_ca=False):
    xl = pd.ExcelFile(excel_path)
    df = xl.parse("Sheet1")
    df.dropna(subset=["Text"], inplace=True)
    # get sentences_no_table
    df_no_table = df[df["Is Table"] != 'x']
    sentences_no_table = df_no_table["Text"].values
    sentences_no_table = [text_process(sent) for sent in sentences_no_table]

    # get number of table
    number_table = 0
    is_table = df["Is Table"]
    i = 0
    while i < len(is_table):
        if is_table[i] == 'x':
            while is_table[i] == 'x':
                i += 1
                if i >= len(is_table):
                    break
            number_table += 1
        else:
            i += 1
    # get title
    df_title = df[df["Is Title"] == 'x']
    title_sentences = df_title["Text"].values
    title_sentences = [text_process(sent) for sent in title_sentences]

    # get sentences have CA
    if extract_sent_ca:
        df_no_table = df[df["Is Table"] != 'x']
        sentences_have_CA_no_table = df_no_table["Text"].values
        sentences_have_CA_no_table = [text_process(sentences_have_CA_no_table[j]) for j in
                                      range(len(sentences_have_CA_no_table))]
    else:
        sentences_have_CA_no_table = []
    return sentences_no_table, number_table, title_sentences, sentences_have_CA_no_table, df


def get_tables(dataframe):
    tables = []
    is_table = dataframe["Is Table"]
    texts = dataframe["Text"]
    texts = [text_process(t) for t in texts]
    i = 0
    while i < len(is_table):
        if is_table[i] == 'x':
            table = []
            while is_table[i] == 'x':
                table.append(texts[i])
                i += 1
                if i >= len(is_table):
                    break
            tables.append(table)
        else:
            i += 1
    return tables


def get_table_index(table, list_table):
    acc = []
    for t in list_table:
        acc.append(lcs(table, t) / len(t))
    if max(acc) == 0:
        return -1, 0

    return acc.index(max(acc)), max(acc)


def check_table_extract(df_CA, df_SE):
    tables_CA = get_tables(df_CA)
    tables_SE = get_tables(df_SE)
    #     print(tables_CA)
    #     print(tables_SE)
    num = 0
    for table in tables_SE:
        index, acc = get_table_index(table, tables_CA)
        if index != -1 and acc != 1.0:
            num += 1
    if num > len(tables_CA):
        return 100.0
    return num / len(tables_CA)


def analyst(excel_save_name, data_path, se_path):
    paragraph_acc = []
    table_detection_acc = []
    title_detection_acc = []
    paragraph_have_CA_not_recognized = []
    table_extract_not_completed = []
    folder = os.listdir(data_path)

    folder_se = os.listdir(se_path)
    # print("folder: ", folder)
    # print("folder_se: ", folder_se)
    files_final = []
    # for folder_name in tqdm(folder):
    #     #         print(file_name)
    #     if folder_name not in folder_se:
    #         continue
    #     files = glob.glob(data_path + '/' + folder_name + '/*.xlsx')
    #     se_files = glob.glob(se_path + '/' + folder_name + '/*.xlsx')
    #     se_file_names = [os.path.basename(file) for file in se_files]
    files = glob.glob((data_path+'/*.xlsx'))
    file_names = [os.path.basename(file) for file in files]
    se_files = glob.glob(se_path + '/*.xlsx')
    for file in se_files:
        file_name = os.path.basename(file)
        sentences_no_table_SE, number_table_SE, title_sentences_SE, sentences_have_CA_no_table_SE, df_SE = read_excel(
            os.path.join(se_path, file_name))

        file_name_wo_pdf = file_name.split('.')[0]+'.xlsx'
        if file_name not in file_names and file_name_wo_pdf not in file_names:
            continue
        elif file_name_wo_pdf in file_names:
            file_name = file_name_wo_pdf
        files_final.append( file_name)
        # print("file_name: ", file_name)
        # print("os.path.join(data_path, folder_name, file_name): ", os.path.join(data_path, file_name))
        sentences_no_table_CA, number_table_CA, title_sentences_CA, sentences_have_CA_no_table_CA, df_CA = read_excel(
            os.path.join(data_path, file_name), extract_sent_ca=True)
        paragraph_acc.append(lcs(sentences_no_table_CA, sentences_no_table_SE) / len(sentences_no_table_CA))
        #         print(sentences_no_table_CA)
        #         print(lcs(sentences_no_table_CA, sentences_no_table_SE))
        if number_table_CA == 0:
            number_table_acc = -1
        else:
            number_table_acc = number_table_SE / number_table_CA
        if number_table_SE > number_table_CA:
            number_table_acc = 1.0
        table_detection_acc.append(number_table_acc)
        title_detection_acc.append(lcs(title_sentences_CA, title_sentences_SE) / len(title_sentences_CA) if len(
            title_sentences_CA) != 0 else 0)
        if len(sentences_have_CA_no_table_CA) == 0:
            paragraph_have_CA_not_recognized.append(-1)
        else:
            paragraph_common = lcs_get_list(sentences_no_table_CA, sentences_no_table_SE)
            paragraph_have_CA_not_recognized.append(
                lcs_not_recognition(sentences_have_CA_no_table_CA, paragraph_common) / len(
                    sentences_have_CA_no_table_CA))
        if number_table_CA == 0:
            table_extract_not_completed.append(-1)
        else:
            table_extract_not_completed.append(check_table_extract(df_CA, df_SE))

    # save to excel file
    df_excel = pd.DataFrame(
        data={'file name': files_final, 'paragraph_acc': paragraph_acc, 'table_detection_acc': table_detection_acc,
              'title_detection_acc': title_detection_acc,
              'paragraph_have_CA_not_recognized': paragraph_have_CA_not_recognized,
              'table_extract_not_completed': table_extract_not_completed})
    df_excel.to_excel(excel_save_name)


if __name__ == '__main__':
    folder = "C:\\Users\\cinnamon\\Desktop\\excel_output"
    # data_path = "E:\\document_dataset\\kepco_dataset_excel_converted"
    # se_path = "E:\\document_dataset\\kepco_document_reading_output"
    data_path = "E:\\document_dataset\\all_data"
    se_path = "E:\\document_dataset\\yoko_table_output"
    analyst("report_table.xlsx", data_path, se_path)
    pass
