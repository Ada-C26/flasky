from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Caretaker(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    cats: Mapped[list["Cat"]] = relationship(back_populates="caretaker")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    @classmethod
    def from_dict(cls, caretaker_data):
        new_caretaker = cls(name=caretaker_data["name"])
        return new_caretaker