"""
Pydantic Data Validation Schemas
"""
from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel


# ============ File Upload ============
class FileUploadResponse(BaseModel):
    """文件上传响应"""
    file_id: str
    project_id: str
    file_name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Projects ============
class ProjectBase(BaseModel):
    """项目基础信息"""
    project_name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """创建项目"""
    pass


class ProjectResponse(ProjectBase):
    """项目响应"""
    project_id: str
    created_at: datetime
    updated_at: datetime
    file_count: Optional[int] = 0

    class Config:
        from_attributes = True


# ============ Bidding Parameters ============
class ScoringCriteria(BaseModel):
    """评分标准"""
    item_name: str
    weight: Optional[float] = None
    full_score: Optional[float] = None
    description: Optional[str] = None


class TechnicalParameter(BaseModel):
    """技术参数"""
    param_name: str
    param_value: str
    unit: Optional[str] = None
    description: Optional[str] = None


class CommercialParameter(BaseModel):
    """商务参数"""
    param_name: str
    param_value: str
    description: Optional[str] = None


class BasicInfo(BaseModel):
    """基本信息"""
    bidding_unit: Optional[str] = None
    agency: Optional[str] = None
    project_name: Optional[str] = None
    bidding_date: Optional[str] = None
    opening_date: Optional[str] = None
    budget: Optional[str] = None


class ExtractedParameters(BaseModel):
    """提取的所有参数"""
    basic_info: Optional[BasicInfo] = None
    scoring_criteria: List[ScoringCriteria] = []
    technical_params: List[TechnicalParameter] = []
    commercial_params: List[CommercialParameter] = []


class BiddingFileResponse(BaseModel):
    """招标文件响应"""
    file_id: str
    project_id: str
    file_name: str
    file_type: str
    file_size: int
    status: str
    created_at: datetime
    extracted_parameters: Optional[ExtractedParameters] = None

    class Config:
        from_attributes = True


class ProjectDetailResponse(BaseModel):
    """项目详情响应"""
    project_id: str
    project_name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    files: List[BiddingFileResponse] = []
    parameters: Optional[ExtractedParameters] = None

    class Config:
        from_attributes = True
