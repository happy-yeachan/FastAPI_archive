from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, Table, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.hybrid import hybrid_property

from middleware_ex import read_root

# 데이터베이스 설정 및 세션 생성
DATABASE_URL = "sqlite:///:memory:" # In-memory 데이터베이스 사용
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# 모델 정의
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    addresses = relationship("Address", back_populates="user")
    roles = relationship("Role", secondary="association", back_populates="users")

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", secondary="association", back_populates="roles")

association_table = Table('association', Base.metadata,
                          Column('user_id', Integer, ForeignKey('user_id')),
                          Column('role_id', Integer, ForeignKey('roles.id')))