import pandas as pd
import glob


def read_original_file(excel_path):
    df = pd.read_excel(excel_path, sheet_name='SE result')
    sentences = df['Sentence'].values
    titles = df['Titles']
    is_titles = df['Is_title']
    is_tables = df['Is_table']
    data = []


if __name__=='__main__':
    excel_folder = "E:\\kepco_data_excel\\1012_No2_update1029\\九州0049"
    excel_files = glob.glob(excel_folder+'/*.xlsx')
    read_original_file(excel_files[0])