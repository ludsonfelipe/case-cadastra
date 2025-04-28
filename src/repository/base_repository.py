from typing import List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository:
    """Base repository class for all database operations."""

    def __init__(self, session: Session, model_class: Type[T]):
        """Initialize the repository with a database session and model class."""
        self.session = session
        self.model_class = model_class

    def create(self, obj: T) -> T:
        """Create a new object in the database."""
        self.session.add(obj)
        self.session.commit()
        return obj

    def create_many(self, objs: List[T]) -> List[T]:
        """Create multiple objects in the database."""
        self.session.add_all(objs)
        self.session.commit()
        return objs

    def get_all(self) -> List[T]:
        """Get all objects from the database."""
        return self.session.query(self.model_class).all()

    def get_by_id(self, id: str) -> Optional[T]:
        """Get an object by its ID."""
        return self.session.query(self.model_class).filter_by(id=id).first()

    def update(self, obj: T) -> T:
        """Update an object in the database."""
        self.session.commit()
        return obj

    def delete(self, obj: T) -> None:
        """Delete an object from the database."""
        self.session.delete(obj)
        self.session.commit()
