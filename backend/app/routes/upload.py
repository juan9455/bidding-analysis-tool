"""
File Upload Routes
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, BiddingFile, BiddingParameter
from app.services.file_parser import FileParser
from app.services.parameter_extractor import ParameterExtractor
from app.config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from pathlib import Path
from datetime import datetime
import os
from uuid import uuid4

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    project_name: str = "Default Project",
    db: Session = Depends(get_db)
):
    """
    Upload and parse a bidding file
    
    Supported formats: PDF, DOCX, DOC, XLSX, XLS, TXT, PNG, JPG, JPEG, BMP, GIF
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower().lstrip(".")
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File format not supported. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Create uploads directory if not exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_id = str(uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Check or create project
        project = db.query(Project).filter(
            Project.project_name == project_name
        ).first()
        
        if not project:
            project = Project(
                project_id=str(uuid4()),
                project_name=project_name,
                description=f"Created on {datetime.utcnow()}"
            )
            db.add(project)
            db.commit()
        
        # Create BiddingFile record
        bidding_file = BiddingFile(
            file_id=file_id,
            project_id=project.project_id,
            file_name=file.filename,
            file_path=file_path,
            file_type=file_ext,
            file_size=len(content),
            status="extracting"
        )
        db.add(bidding_file)
        db.commit()
        
        # Parse file
        text_content, parse_error = FileParser.parse(file_path)
        
        if parse_error:
            bidding_file.status = "failed"
            bidding_file.error_message = parse_error
            db.commit()
            raise HTTPException(
                status_code=400,
                detail=f"Error parsing file: {parse_error}"
            )
        
        # Save raw content
        bidding_file.raw_content = text_content[:100000]  # Limit size
        
        # Extract parameters
        extracted_params = ParameterExtractor.extract_all(text_content)
        
        # Save extracted parameters to database
        for basic_info_key, basic_info_value in (extracted_params.get("basic_info") or {}).items():
            param = BiddingParameter(
                param_id=str(uuid4()),
                file_id=file_id,
                project_id=project.project_id,
                param_type="basic_info",
                param_content={"key": basic_info_key, "value": basic_info_value},
                confidence=100,
                verified=0
            )
            db.add(param)
        
        # Save scoring criteria
        for criteria in extracted_params.get("scoring_criteria", []):
            param = BiddingParameter(
                param_id=str(uuid4()),
                file_id=file_id,
                project_id=project.project_id,
                param_type="scoring_criteria",
                param_content=criteria,
                confidence=85,
                verified=0
            )
            db.add(param)
        
        # Save technical parameters
        for tech_param in extracted_params.get("technical_params", []):
            param = BiddingParameter(
                param_id=str(uuid4()),
                file_id=file_id,
                project_id=project.project_id,
                param_type="technical_param",
                param_content=tech_param,
                confidence=80,
                verified=0
            )
            db.add(param)
        
        # Save commercial parameters
        for comm_param in extracted_params.get("commercial_params", []):
            param = BiddingParameter(
                param_id=str(uuid4()),
                file_id=file_id,
                project_id=project.project_id,
                param_type="commercial_param",
                param_content=comm_param,
                confidence=80,
                verified=0
            )
            db.add(param)
        
        bidding_file.status = "completed"
        db.commit()
        db.refresh(bidding_file)
        
        return {
            "success": True,
            "file_id": file_id,
            "project_id": project.project_id,
            "project_name": project.project_name,
            "file_name": file.filename,
            "status": "completed",
            "extracted_parameters": extracted_params,
            "message": "File uploaded and parsed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
