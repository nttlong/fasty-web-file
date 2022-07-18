from pydantic import BaseModel
from pydantic.fields import Field
from typing import Union
from .errors import Error as ret_error

class UploadChunkResult(BaseModel):
    SizeInHumanReadable: Union[str, None] = Field(description="Dung lương format dưới dạng text")
    SizeUploadedInHumanReadable: Union[str, None] = Field(description="Dung lương đã upload format dưới dạng text")
    Percent: Union[float, None] = Field(description="Phần trăm hoàn tất")
    NumOfChunksCompleted: Union[int, None]

class UploadFilesChunkInfoResult(BaseModel):
    Data: Union[UploadChunkResult, None] = Field(description="Kết quả nếu không lỗi")
    Error: Union[ret_error, None] = Field(description="Lỗi")