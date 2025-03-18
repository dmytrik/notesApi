from fastapi.exceptions import ValidationException
from profanityfilter import ProfanityFilter


pf = ProfanityFilter()

def validate_note(note: str) -> str:
    if pf.is_profane(note):
        raise ValidationException("Note contains inappropriate language")
    return note
