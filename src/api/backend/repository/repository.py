from typing import List, Optional
from pydantic import BaseModel


class Operator(BaseModel):
    registro_ans: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    score: float = 0.0


class SearchResponse(BaseModel):
    results: List[Operator]
