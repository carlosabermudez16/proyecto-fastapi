from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.session import base


class Item(base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, index=True)
    description = Column(Text)

    # foreignkey
    user_id = Column(Integer, ForeignKey("user.id"))

    # relations with table user
    user = relationship("User", back_populates="items")