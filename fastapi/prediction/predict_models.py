from pydantic import BaseModel

class PredictRequest(BaseModel):
  job_type: str
  quantity: int
  size: str
  material: str
  isColored: bool
  model: str