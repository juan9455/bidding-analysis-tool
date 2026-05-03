"""
Database Models using SQLAlchemy
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()


class Project(Base):
    """招标项目"""
    __tablename__ = "projects"

    project_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    project_name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class BiddingFile(Base):
    """招标文件"""
    __tablename__ = "bidding_files"

    file_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    project_id = Column(String(36), ForeignKey("projects.project_id"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, docx, xlsx, txt, image
    file_size = Column(Integer, nullable=False)  # bytes
    status = Column(String(20), default="pending")  # pending, extracting, completed, failed
    error_message = Column(Text, nullable=True)
    raw_content = Column(Text, nullable=True)  # 提取的原始文本
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class BiddingParameter(Base):
    """招标参数"""
    __tablename__ = "bidding_parameters"

    param_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    file_id = Column(String(36), ForeignKey("bidding_files.file_id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.project_id"), nullable=False, index=True)
    
    # 参数类型: scoring_criteria, technical_param, commercial_param, basic_info
    param_type = Column(String(50), nullable=False, index=True)
    
    # 参数内容（JSON格式）
    param_content = Column(JSON, nullable=False)
    
    # 置信度 (0-100)
    confidence = Column(Integer, default=100)
    
    # 是否由用户验证
    verified = Column(Integer, default=0)  # 0: 未验证, 1: 已验证
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class ExtractionLog(Base):
    """提取日志"""
    __tablename__ = "extraction_logs"

    log_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    file_id = Column(String(36), ForeignKey("bidding_files.file_id"), nullable=False, index=True)
    action = Column(String(100), nullable=False)  # uploaded, parsing, extracting, completed
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
