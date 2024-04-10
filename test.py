import pandas as pd 
def open_csv_file(file_path):
    try:
        # CSV 파일을 읽어서 DataFrame으로 변환
        df = pd.read_csv(file_path, encoding='utf-8', sep='|')
        return df

    except Exception as e:
        print(f"Failed to open CSV file: {str(e)}")

# 테스트
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
file_path = 'merged_data.csv'
data_frame = open_csv_file(file_path)
print(data_frame.head())