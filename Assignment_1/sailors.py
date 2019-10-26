# Problem 2 -- Using ORM to add more functionality 
from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship


# Create engine and connect
engine = create_engine('mysql+pymysql://root:root1234@localhost/sailors', echo = True)
connection = engine.connect()

# Make session so we can commit changes
session = sessionmaker(bind = engine)
s = session()

# Create Base and then use it for each of the classes
Base = declarative_base()

# Define each of the classes and their mapping to the MySQL DB
class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key = True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    def __repr__(self):
        return "<Sailor(id = %s, name = '%s', rating = %s)>" % (self.sid, self.sname, self.age)

class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key = True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

    reservations = relationship('Reservation', backref = backref('boat', cascade = 'delete'))

    def __repr__(self):
        return "<Boat(id = %s, name = '%s', color = %s)>" % (self.bid, self.bname, self.color)

class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    sailor = relationship('Sailor')

    def __repr__(self):
        return "<Reservation(sid = %s, bid = %s, day = %s)>" % (self.sid, self.bid, self.day)


# Quick test functions
# for i in s.query(Sailor):
# 	print(i)

# for i in s.query(Boat):
# 	print(i)

# for i in s.query(Reservation):
# 	print(i)        


#########################################
#			     TESTS			   		#			
#########################################
#import pytest

# Function to test the MySQL query with the ORM query
def assert_function(sql_query, orm_query):
	# Lists to hold the results from both queries
	sql_list = []
	orm_list = []

	# Get result from straight up SQL query
	sql_results = connection.execute(sql_query)

	for result in sql_results:
		sql_list.append(result)

	for result in orm_query:
		orm_list.append(result)

	# Assert that the two lists are the same
	assert sql_list == orm_list
	#return (sql_list == orm_list)

# Simple test to make sure we can query all the data
def test_simple():
	sql_query1 = "SELECT * FROM sailors"
	orm_query1 = s.query(Sailor.sid, Sailor.sname, Sailor.rating, Sailor.age)

	sql_query2 = "SELECT * FROM boats"
	orm_query2 = s.query(Boat.bid, Boat.bname, Boat.color, Boat.length)

	sql_query3 = "SELECT * FROM reserves"
	orm_query3 = s.query(Reservation.sid, Reservation.bid, Reservation.day)

	assert_function(sql_query1, orm_query1)
	assert_function(sql_query2, orm_query2)
	assert_function(sql_query3, orm_query3)

# The following functions test out the ORM using some of the queries from Problem 1
# Q2: List, for every boat, the number of times it has been reserved, excluding those boats that have never been reserved.
def test_q2():
	sql_query = "SELECT B.bid, COUNT(*) as Num_Res FROM boats B, reserves R WHERE B.bid = R.bid GROUP BY B.bid HAVING Num_Res > 0;"
	orm_query = s.query(Reservation.bid, func.count("*")).group_by(Reservation.bid).having(func.count("*") > 0)
	assert_function(sql_query, orm_query)  

# Q5: For which boat are there the most reservations?
def test_q5():
	sql_query = "SELECT B.bid, COUNT(*) as Num_Res FROM boats B, reserves R WHERE B.bid = R.bid GROUP BY B.bid ORDER BY Num_Res DESC LIMIT 1;"
	orm_query = s.query(Reservation.bid, func.count("*")).group_by(Reservation.bid).group_by(Reservation.bid).order_by(desc(func.count("*"))).limit(1)
	assert_function(sql_query, orm_query)

# Q7: Find the average age of sailors with a rating of 10.
def test_q7():
	sql_query = "SELECT AVG(S.age) FROM sailors S WHERE S.rating = 10;"
	orm_query = s.query(func.avg(Sailor.age)).filter(Sailor.rating == 10).all()
	assert_function(sql_query, orm_query)






















