from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./blog.db"

Base = declarative_base()


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)


# Creating database engine
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Creating session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)