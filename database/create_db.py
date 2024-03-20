from sqlalchemy import create_engine
from models import Base

# This creates the database
engine = create_engine('sqlite:///clippr.sqlite', echo=True)
Base.metadata.create_all(engine)