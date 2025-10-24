"""Database models using SQLModel"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid
import json


class Scenario(SQLModel, table=True):
    """Saved tax calculation scenario"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    label: Optional[str] = Field(default=None, max_length=200)
    
    # Store as JSON strings
    inputs_json: str = Field(sa_column_kwargs={"name": "inputs"})
    outputs_json: str = Field(sa_column_kwargs={"name": "outputs"})
    
    @property
    def inputs(self) -> dict:
        """Parse inputs JSON"""
        return json.loads(self.inputs_json)
    
    @inputs.setter
    def inputs(self, value: dict):
        """Set inputs as JSON"""
        self.inputs_json = json.dumps(value)
    
    @property
    def outputs(self) -> dict:
        """Parse outputs JSON"""
        return json.loads(self.outputs_json)
    
    @outputs.setter
    def outputs(self, value: dict):
        """Set outputs as JSON"""
        self.outputs_json = json.dumps(value)
