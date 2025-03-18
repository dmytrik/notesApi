from fastapi import HTTPException, status
from profanityfilter import ProfanityFilter


pf = ProfanityFilter()

def validate_note(note: str) -> str:
    if pf.is_profane(note):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Note contains inappropriate language"
        )
    return note
