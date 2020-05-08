import pandas as pd
import glob, json, os
import unicodedata
import tqdm


def read_original_file(excel_path, output_folder):
    df = pd.read_excel(excel_path, sheet_name='SE result')
    sentences = df['Sentence'].values
    title = df['Titles'].values
    try:
        title = [json.loads(str(x))[0] if len(json.loads(str(x)))>0 else '' for x in title]
    except:
        print("error file: ", excel_path)
        return None
    is_titles = df['Is_title'].values
    is_tables = df['Is_table'].values
    data = [{'Index': i, 'Text': sentences[i], 'Is Title': is_titles[i], 'Is Table': is_tables[i], 'Parent Index': 0}
            for i in range(len(sentences))]
    for i in range(len(data)):
        for j in range(i):
            # print("unicodedata.normalize('NFKC', title[i]): ", unicodedata.normalize('NFKC', title[i]))
            if unicodedata.normalize('NFKC', title[i])== unicodedata.normalize('NFKC', data[j]['Text']):
                data[i]['Parent Index'] = j
    name = os.path.basename(excel_path)
    output_df = pd.DataFrame(data)
    output_df.to_excel(output_folder+'/'+name)


if __name__ == '__main__':
    excel_folder = "E:\\kepco_data_excel"
    excel_files = glob.glob(excel_folder + '/*/*/*.xlsx')
    output_folder = "E:\\document_dataset\\kepco_dataset_excel_converted"
    for i in tqdm.tqdm(range(len(excel_files))):
        dir_path = os.path.basename( os.path.dirname(excel_files[i]))
        try:
            os.mkdir(output_folder+'/'+dir_path)
        except:
            a = 0
        read_original_file(excel_files[i], output_folder+'/'+dir_path)
