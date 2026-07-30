import enum
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Time,
    ForeignKey, Enum, CheckConstraint, UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography

from app.database import Base


class Gender(enum.Enum):
    male = "male"
    female = "female"


class MatchStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"
    cancelled = "cancelled"


class MatchResult(enum.Enum):
    win = "win"
    lose = "lose"
    draw = "draw"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    photo_url = Column(String(512), nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    username = Column(String(64), nullable=False)
    age = Column(Integer, nullable=True)
    rating = Column(Integer, nullable=False, default=100)
    has_weapon_license = Column(Boolean, nullable=False, default=False)

    about = Column(String(512), nullable=True)
    criminal_record = Column(String(512), nullable=True)
    martial_arts_skills = Column(String(512), nullable=True)

    height_cm = Column(Integer, nullable=True)
    weight_kg = Column(Integer, nullable=True)

    available_from = Column(Time, nullable=True)
    available_to = Column(Time, nullable=True)

    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=True)
    favorite_place_description = Column(String(512), nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


class Wish(Base):
    __tablename__ = "wishes"

    id = Column(Integer, primary_key=True)
    
    rating = Column(Integer, nullable=False, default=0)

    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_by_user = relationship("User")


class UserWish(Base):
    __tablename__ = "user_wishes"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wish_id = Column(Integer, ForeignKey("wishes.id"), nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User")
    wish = relationship("Wish")

    __table_args__ = (
        UniqueConstraint("user_id", "wish_id", name="uq_user_wish"),
    )


class UserMatch(Base):
    __tablename__ = "user_matches"

    id = Column(Integer, primary_key=True)

    initiator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    responder_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(Enum(MatchStatus), nullable=False, default=MatchStatus.pending)

    initiator_travel_time_minutes = Column(Integer, nullable=True)
    responder_travel_time_minutes = Column(Integer, nullable=True)

    winner_by_initiator = Column(Enum(MatchResult), nullable=True)
    winner_by_responder = Column(Enum(MatchResult), nullable=True)
    final_result = Column(Enum(MatchResult), nullable=True)

    initiator_accepted = Column(Boolean, nullable=False, default=False)
    responder_accepted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    initiator = relationship("User", foreign_keys=[initiator_id])
    responder = relationship("User", foreign_keys=[responder_id])

    __table_args__ = (
        CheckConstraint("initiator_id <> responder_id", name="check_not_self_match"),
    )