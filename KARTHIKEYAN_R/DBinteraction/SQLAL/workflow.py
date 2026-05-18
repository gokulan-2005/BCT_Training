from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

#Create connection (SQLite database file)
engine = create_engine("sqlite:///mydb.db")

#Base class for models
Base = declarative_base()

# Define table as Python class
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# Create table in DB (if not exists)
Base.metadata.create_all(engine)

# Create session (to interact with DB)
Session = sessionmaker(bind=engine)
session = Session()

student1 = Student(name="Karthikeyan", age=21)
session.add(student1)
session.commit()
print("Single data inserted!")
students = [
    Student(name="Alice", age=20),
    Student(name="Bob", age=23),
    Student(name="Charlie", age=22),
    Student(name="David", age=24)
]

session.add_all(students)
session.commit()
print("Multiple records inserted!")
print("\nAll Students:")
for s in session.query(Student).all():
    print(s.id, s.name, s.age)
print("\nStudents with age > 21:")
result = session.query(Student).filter(Student.age > 21).all()

for s in result:
    print(s.name, s.age)
student = session.query(Student).filter_by(name="Alice").first()

if student:
    student.age = 25
    session.commit()
    print("\nAlice's age updated!")
student = session.query(Student).filter_by(name="Bob").first()

if student:
    session.delete(student)
    session.commit()
    print("Bob deleted!")
count = session.query(Student).count()
print("\nTotal students:", count)
print("\nStudents sorted by age (DESC):")
sorted_students = session.query(Student).order_by(Student.age.desc()).all()

for s in sorted_students:
    print(s.name, s.age)

session.close()
print("\nSession closed!")