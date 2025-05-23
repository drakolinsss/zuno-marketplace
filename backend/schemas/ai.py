from pydantic import BaseModel
from typing import Dict, List, Optional

class ProductAnalysis(BaseModel):
    categories: Dict[str, float]
    is_filtered: bool
    similar_products: List[str]
    fraud_risk: Optional[Dict[str, float]]

class UserActivityData(BaseModel):
    user_id: int
    ip_address: str
    activity_type: str
    timestamp: str
    metadata: Optional[Dict] = {}
