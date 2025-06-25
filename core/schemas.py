# core/schemas.py (V3.0 - Final MVP Schemas)
from pydantic import BaseModel, Field
from typing import List, Optional

class FreeNoteCard(BaseModel):
    """The universal fallback for any note that cannot be categorized."""
    title: Optional[str] = Field(default=None, description="A best-guess title for the note.")
    content: str = Field(description="The user's original, unmodified input text.")
    tags: Optional[List[str]] = Field(default=None, description="User-defined labels for organization.")

class ArtEvent(BaseModel):
    """A data model for logging art-related events."""
    title: str = Field(description="The official title of the exhibit or artwork.")
    creators: Optional[List[str]] = Field(default=None, description="The artists or creators.")
    location: Optional[str] = Field(default=None, description="The museum or location.")
    notes: Optional[str] = Field(default=None, description="Personal notes or reflections.")
    category: Optional[str] = Field(default=None, description="e.g., 'Exhibit', 'Mural', 'Performance Art'.")

class DJMix(BaseModel):
    """A data model for capturing a DJ mix or track transition idea."""
    title: Optional[str] = Field(default="Untitled Mix", description="A creative name for this mix idea.")
    tracks: str = Field(description="The songs in the mix, ideally one per line.")
    vibe: Optional[str] = Field(default=None, description="Keywords describing the feel of the mix.")

class Recipe(BaseModel):
    """A data model for saving a recipe."""
    title: str = Field(description="The name of the dish.")
    ingredients: str = Field(description="A list of the ingredients required, one per line.")
    instructions: str = Field(description="The step-by-step instructions.")
    source: Optional[str] = Field(default=None, description="The URL or cookbook name.")

class VehicleLog(BaseModel):
    """A data model for logging vehicle maintenance."""
    title: str = Field(description="The type of service or issue, e.g., 'Oil Change', 'Brake Noise'.")
    vehicle: Optional[str] = Field(default=None, description="The specific vehicle this note pertains to.")
    date: Optional[str] = Field(default=None, description="The date of the service.")
    details: str = Field(description="Details about the service, parts used, or observations.")

class PersonNote(BaseModel):
    """A data model for remembering key information about a person."""
    title: str = Field(description="The full name of the person this note is about.")
    context: str = Field(description="How you know this person or where you met.")
    key_info: str = Field(description="The important information to remember.")

class GeneralQuery(BaseModel):
    """A tool for when the user is asking a question, not logging data."""
    query: str = Field(description="The user's specific question.")
