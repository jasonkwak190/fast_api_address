from pydantic import BaseModel, Field

# post 경우만
# class download_schema(BaseModel):
#     da_date: str = Field(default= '202403', title='다운로드 받을 날짜', description = '오늘 날짜 기준 한달 전 값을 넣으시오')
    # class Config:
    #     json_schema_extra = {
    #         "example": {
    #             "da_date":"202403"
    #         }
    #     }