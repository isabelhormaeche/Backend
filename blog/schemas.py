from pydantic import BaseModel


# Create  film location blog
class Blog (BaseModel):
    title: str
    desc: str
    cat: str
    