"""
Parameter Extraction Service

Extracts scoring criteria, technical parameters, and commercial parameters
from bidding document text using keyword matching and regex patterns.
"""
import re
from typing import List, Dict, Any, Optional


class ParameterExtractor:
    """招标参数提取器"""

    # 关键词配置
    SCORING_KEYWORDS = [
        "评分标准", "评分项", "权重", "分数", "得分", "评价标准",
        "scoring criteria", "evaluation criteria", "score"
    ]

    TECHNICAL_KEYWORDS = [
        "技术", "参数", "规格", "性能", "配置", "功能", "要求",
        "技术指标", "技术要求", "性能指标", "配置要求",
        "technical", "parameter", "specification", "performance", "feature",
        "requirement", "config"
    ]

    COMMERCIAL_KEYWORDS = [
        "商务", "价格", "付款", "交货", "保修", "服务", "条件",
        "商务条款", "付款条件", "交货期", "保修期", "售后",
        "commercial", "price", "payment", "delivery", "warranty",
        "condition", "term"
    ]

    BASIC_INFO_KEYWORDS = {
        "bidding_unit": ["招标单位", "招标人", "bidding unit", "bidding organization"],
        "agency": ["招标代理", "代理机构", "代理", "agency", "bidding agent"],
        "project_name": ["项目名称", "项目", "project name", "project"],
        "budget": ["预算", "投资额", "项目投资", "budget", "investment"],
    }

    @staticmethod
    def extract_all(text: str) -> Dict[str, Any]:
        """
        Extract all parameters from text
        
        Args:
            text: Extracted text from bidding document
            
        Returns:
            Dictionary containing all extracted parameters
        """
        result = {
            "basic_info": ParameterExtractor.extract_basic_info(text),
            "scoring_criteria": ParameterExtractor.extract_scoring_criteria(text),
            "technical_params": ParameterExtractor.extract_technical_params(text),
            "commercial_params": ParameterExtractor.extract_commercial_params(text),
        }
        return result

    @staticmethod
    def extract_basic_info(text: str) -> Dict[str, Optional[str]]:
        """
        Extract basic information
        
        Returns dict with: bidding_unit, agency, project_name, budget, etc.
        """
        info = {
            "bidding_unit": None,
            "agency": None,
            "project_name": None,
            "budget": None,
            "bidding_date": None,
            "opening_date": None,
        }

        # Extract bidding unit
        for keyword in ParameterExtractor.BASIC_INFO_KEYWORDS["bidding_unit"]:
            match = re.search(rf"{keyword}[：:]*([^\n\r,，。]*)", text, re.IGNORECASE)
            if match:
                info["bidding_unit"] = match.group(1).strip()
                break

        # Extract agency
        for keyword in ParameterExtractor.BASIC_INFO_KEYWORDS["agency"]:
            match = re.search(rf"{keyword}[：:]*([^\n\r,，。]*)", text, re.IGNORECASE)
            if match:
                info["agency"] = match.group(1).strip()
                break

        # Extract project name
        for keyword in ParameterExtractor.BASIC_INFO_KEYWORDS["project_name"]:
            match = re.search(rf"{keyword}[：:]*([^\n\r,，。]*)", text, re.IGNORECASE)
            if match:
                info["project_name"] = match.group(1).strip()
                break

        # Extract budget
        for keyword in ParameterExtractor.BASIC_INFO_KEYWORDS["budget"]:
            match = re.search(rf"{keyword}[：:]*([^\n\r,，。]*)", text, re.IGNORECASE)
            if match:
                info["budget"] = match.group(1).strip()
                break

        # Extract dates
        date_pattern = r"\d{4}[-/]\d{1,2}[-/]\d{1,2}"
        dates = re.findall(date_pattern, text)
        if dates:
            info["bidding_date"] = dates[0]
            if len(dates) > 1:
                info["opening_date"] = dates[1]

        return {k: v for k, v in info.items() if v is not None}

    @staticmethod
    def extract_scoring_criteria(text: str) -> List[Dict[str, Any]]:
        """
        Extract scoring criteria from text
        
        Returns list of scoring criteria with: item_name, weight, full_score
        """
        criteria_list = []
        
        # Find scoring criteria section
        # Look for lines with keywords like "评分标准"
        for keyword in ParameterExtractor.SCORING_KEYWORDS:
            if keyword.lower() in text.lower():
                # Extract lines after the keyword
                pattern = rf"{keyword}[^]*?(?=(?:技术|商务|第|Chapter|Section|\n\n)|$)"
                matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    section = match.group(0)
                    
                    # Extract scoring items
                    # Look for patterns like "项目名 权重% 满分分"
                    lines = section.split("\n")
                    for line in lines:
                        line = line.strip()
                        if not line or len(line) < 3:
                            continue
                        
                        # Try to find percentages
                        percent_match = re.search(r"(\d+(?:\.\d+)?)%", line)
                        score_match = re.search(r"(?:满分|分值|满分值)[：:]*([\d.]+)", line, re.IGNORECASE)
                        
                        if percent_match or score_match:
                            criteria = {
                                "item_name": line[:50],  # First 50 chars as name
                                "weight": float(percent_match.group(1)) if percent_match else None,
                                "full_score": float(score_match.group(1)) if score_match else None,
                            }
                            criteria_list.append({k: v for k, v in criteria.items() if v is not None})
        
        return criteria_list

    @staticmethod
    def extract_technical_params(text: str) -> List[Dict[str, str]]:
        """
        Extract technical parameters
        
        Returns list of technical parameters
        """
        params_list = []
        
        # Look for technical parameter section
        for keyword in ParameterExtractor.TECHNICAL_KEYWORDS:
            if keyword in text:
                # Find all lines in technical section
                pattern = rf"{keyword}[^]*?(?=(?:商务|第|Chapter|Section|\n\n)|$)"
                matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    section = match.group(0)
                    lines = section.split("\n")
                    
                    for line in lines:
                        line = line.strip()
                        # Skip empty lines and keywords
                        if not line or len(line) < 2 or any(kw in line for kw in ParameterExtractor.TECHNICAL_KEYWORDS):
                            continue
                        
                        # Extract parameter and value
                        if "：" in line or ":" in line:
                            parts = re.split("[：:]", line, maxsplit=1)
                            if len(parts) == 2:
                                param = {
                                    "param_name": parts[0].strip()[:100],
                                    "param_value": parts[1].strip()[:200],
                                }
                                params_list.append(param)
        
        return params_list

    @staticmethod
    def extract_commercial_params(text: str) -> List[Dict[str, str]]:
        """
        Extract commercial parameters
        
        Returns list of commercial parameters
        """
        params_list = []
        
        # Look for commercial parameter section
        for keyword in ParameterExtractor.COMMERCIAL_KEYWORDS:
            if keyword in text:
                pattern = rf"{keyword}[^]*?(?=(?:附件|第|Chapter|Section|\n\n)|$)"
                matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    section = match.group(0)
                    lines = section.split("\n")
                    
                    for line in lines:
                        line = line.strip()
                        # Skip empty lines
                        if not line or len(line) < 2:
                            continue
                        
                        # Extract parameter
                        if "：" in line or ":" in line:
                            parts = re.split("[：:]", line, maxsplit=1)
                            if len(parts) == 2:
                                param = {
                                    "param_name": parts[0].strip()[:100],
                                    "param_value": parts[1].strip()[:200],
                                }
                                params_list.append(param)
        
        return params_list
