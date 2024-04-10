from fastapi import FastAPI, HTTPException
import requests
import zipfile
import os
from typing import Union


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/download_address_csv/{da_date}")
async def download_and_extract(da_date: str):
    url = f"https://business.juso.go.kr/addrlink/download.do?reqType=ALLRNADR_KOR&regYmd={da_date[:4]}&ctprvnCd=00&stdde={da_date}&fileName={da_date}_%EB%8F%84%EB%A1%9C%EB%AA%85%EC%A3%BC%EC%86%8C%20%ED%95%9C%EA%B8%80_%EC%A0%84%EC%B2%B4%EB%B6%84.zip&intNum=undefined&intFileNo=undefined&realFileName=RNADDR_KOR_2403.zip"

    try:
        # 파일 다운로드
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to download file")

        with open("data.zip", "wb") as f:
            f.write(response.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")

    try:
        # 압축 해제
        with zipfile.ZipFile("data.zip", "r") as zip_ref:
            zip_ref.extractall(f"extracted_data_{da_date}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract zip file: {str(e)}")

    try:
        # 한개의 CSV 파일로 변환
        with open("merged_data.csv", "w", encoding="UTF-8") as output_file:
            # kor_header = "도로명주소관리번호|법정동코드|시도명|시군구명|법정읍면동명|법정리명|산여부|지번본번(번지)|지번부번(호)|도로명코드|도로명|지하여부|건물본번|건물부번|행정동코드|행정동명|기초구역번호|이전도로명주소|효력발생일|공동주택구분|이동사유코드|건축물대장건물명|시군구용건물명|비고\n"
            header = "add_no|cd_bubjung|add_sido|add_sigun|add_bubjungdong|add_bubjunglee|is_mountain|add_jibunbon|add_jibunbu|cd_doro|add_doro|add_is_underground|add_building_bon|add_building_bu|cd_haeng_code|add_haengjungdong|zip_code|add_doro_before|da_date_enrolled|add_is_apartment_house|add_is_changed|add_building_name|add_sigungu_building_name|bigo\n"
            # new_header = "산여부,이전도로명주소,효력발생일,비고" "is_mountain,add_doro_before,da_date_enrolled,bigo"
            
            output_file.write(header)

            # 각 파일을 순회하며 데이터 읽기
            for file_name in os.listdir(f"extracted_data_{da_date}"):
                file_path = os.path.join(f"extracted_data_{da_date}", file_name)
                with open(file_path, "r", encoding="CP949") as input_file:
                    for line in input_file:
                        output_file.write(line)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert to CSV: {str(e)}")

    # 모든 작업이 성공했을 때
    return {"status": "success", "status_code": 200, "status_msg": "Download, extraction, and CSV conversion successful"}
    