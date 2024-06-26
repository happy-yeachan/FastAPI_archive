from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, Table, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.hybrid import hybrid_property

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
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship("User", secondary="association", back_populates="roles")

association_table = Table('association', Base.metadata,
                          Column('user_id', Integer, ForeignKey('users.id')),
                          Column('role_id', Integer, ForeignKey('roles.id')))

# 하이브리드 속성 예제
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    # 파이썬 코드에서 동작 할 때 사용됨
    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    # slq express에서 해당 객체가 생성됐을 때 사용
    @full_name.expression
    def full_name(cls):
        return cls.first_name + " " + cls.last_name # SQLite에서는 || 대신 + 사용
    
# 모델 생성
Base.metadata.create_all(engine)

# 데이터 추가 및 쿼리
user = User(name="Yea Chan")
address1 = Address(email="yea@naver.com", user=user)
address2 = Address(email='chan@naver.com', user = user)
session.add_all([user, address1, address2])
session.commit()

for address in session.query(Address).join(User).filter(User.name == "Yea Chan"):
    print(address.email)

users = session.query(User).options(joinedload(User.addresses)).all()
for user in users:
    print(user.name)
    for address in user.addresses:
        print(address.email)

#이벤트 리스너 등록
@event.listens_for(User, 'after_insert')
def my_listener(mapper, connection, target):
    print(f'New user created: {target.name}')

# 새 사용자 추가
new_user = User(name="Alice Wonderland")
session.add(new_user)
session.commit()

try:
    session.add(User(name="Alice Wonderland"))
    session.commit()
except SQLAlchemyError as e:
    session.rollback()
    print(f"Transaction failed: {e}")
finally:
    session.close()

# joinedload와 selectionload의 사용 예
user_with_addresses_joined = session.query(User).options(joinedload(User.addresses)).all()
user_with_addresses_selection = session.query(User).options(selectinload(User.addresses)).all()
for user in user_with_addresses_joined:
    print(user.name, [address.email for address in user.addresses])
for user in user_with_addresses_selection:
    print(user.name, [address.email for address in user.addresses])

# 쿼리 예제 
session.add_all([Employee(first_name="Yea", last_name="Chan"),
                 Employee(first_name="John", last_name="Doe")])
session.commit()

for employee in session.query(Employee).filter(Employee.full_name == 'Yea Chan'):
    print(employee.first_name, employee.last_name)