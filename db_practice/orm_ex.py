from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

# 데이터베이스 엔진 설정
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()

# 모델 베이스 클래스
Base = declarative_base()

def print_all_data(session):
    # 모든 사용자 출력
    all_users = session.query(User).all()
    print("All Users: ")
    for user in all_users:
        print(user)
    # 모든 게시글 출력
    all_posts = session.query(Post).all()
    print("All Posts: ")
    for post in all_posts:
        print(post)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    name = Column(String)
    age = Column(Integer)
    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"<User(name={self.name}, age={self.age})>"
    
# 게시글 테이블을 정의하는 모델
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    author = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(title={self.title}, content={self.content})>"