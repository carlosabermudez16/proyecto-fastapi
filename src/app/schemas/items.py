from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    user_id:int

class ItemScheme(ItemBase):
    id: int
    user_id: int

    # permite que fastapi pueda serializar los objetos de la db como json de forma automática
    class Config:
        from_attributes = True
