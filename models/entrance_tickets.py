from pydantic import BaseModel
import time


class EntranceTicket(BaseModel):
    ticket_id: str
    gate_id: str
    timestamp: float
