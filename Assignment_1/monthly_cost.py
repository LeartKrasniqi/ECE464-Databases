# Problem 3 -- Expanding DB to include monthly cost report system
from sqlalchemy import create_engine, Integer, String, Column, Date, ForeignKey, PrimaryKeyConstraint, func, desc, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship

# Create engine and connect to new database
engine = create_engine('mysql+pymysql://root:root1234@localhost/monthly_cost', echo = True)
connection = engine.connect()

# Make session and metadata so we can commit changes
session = sessionmaker(bind = engine)
s = session()
metadata = MetaData(engine)


# Create new schema to hold the data:
sailors = Table('sailors', metadata, 
		Column('sid', Integer, primary_key = True),
        	Column('sname', String(30)),
        	Column('rating', Integer),
        	Column('age', Integer))

boats = Table('boats', metadata,
        	Column('bid', Integer, primary_key = True),
        	Column('bname', String(20)),
        	Column('color', String(10)),
        	Column('length', Integer),
        	Column('flat_cost', Integer), 		# Cost including the fuel, cleaning, and any other fixed costs for the month
        	Column('daily_price', Integer)) 	# Price to reserve the boat for a day

reserves = Table('reserves', metadata,
        	Column('sid', Integer, primary_key = True),
        	Column('bid', Integer, primary_key = True),
        	Column('day_res', Date, primary_key = True), 	# Day reserved
        	Column('day_ret', Date, primary_key = True)) 	# Day returned

# Store employees and their hourly wage
employees = Table('employees', metadata,
                Column('eid', Integer, primary_key = True),
                Column('ename', String(30)),
                Column('wage', Integer))

# Store the number of hours each employee has worked 
weekly_hours = Table('weekly_hours', metadata,
                Column('week', Date, primary_key = True),
                Column('eid', Integer, ForeignKey("employees.eid"), primary_key = True),
                Column('hours', Integer))

# Delete all data first and then create
metadata.drop_all()
metadata.create_all()

# Populate the tables (the sailors, boats, and reserves are populated using the new_sailors_mysql.sql file):
sql_file = open("./new_sailors_mysql.sql", "r")
for line in sql_file:
        line = line.strip("\n")
        connection.execute(line)

employees_arr = [ {"eid": 1, "ename": "Lay Ree", "wage": 13}, 
                  {"eid": 2, "ename": "Heff Jakner", "wage": 18},
                  {"eid": 3, "ename": "Kam Seene", "wage": 10},
                  {"eid": 4, "ename": "Sarl Cable", "wage": 25},         
                  {"eid": 5, "ename": "Fred Fontaine", "wage": 22}, 
                ]

hours_arr = [ {"week": "1998/11/1", "eid": 1, "hours": 8},
              {"week": "1998/11/8", "eid": 1, "hours": 8},
              {"week": "1998/11/15", "eid": 1, "hours": 8},
              {"week": "1998/11/22", "eid": 1, "hours": 8},
              {"week": "1998/11/29", "eid": 1, "hours": 8},
              {"week": "1998/11/1", "eid": 2, "hours": 4},
              {"week": "1998/11/8", "eid": 2, "hours": 3},
              {"week": "1998/11/15", "eid": 2, "hours": 10},
              {"week": "1998/11/22", "eid": 2, "hours": 11},
              {"week": "1998/11/29", "eid": 2, "hours": 0},
              {"week": "1998/11/1", "eid": 3, "hours": 0},
              {"week": "1998/11/8", "eid": 3, "hours": 0},
              {"week": "1998/11/15", "eid": 3, "hours": 0},
              {"week": "1998/11/22", "eid": 3, "hours": 10},
              {"week": "1998/11/29", "eid": 3, "hours": 10},
              {"week": "1998/11/1", "eid": 4, "hours": 8},
              {"week": "1998/11/8", "eid": 4, "hours": 9},
              {"week": "1998/11/15", "eid": 4, "hours": 7},
              {"week": "1998/11/22", "eid": 4, "hours": 1},
              {"week": "1998/11/29", "eid": 4, "hours": 1},
              {"week": "1998/11/1", "eid": 5, "hours": 10},
              {"week": "1998/11/8", "eid": 5, "hours": 10},
              {"week": "1998/11/15", "eid": 5, "hours": 10},
              {"week": "1998/11/22", "eid": 5, "hours": 10},
              {"week": "1998/11/29", "eid": 5, "hours": 11},
            ]


connection.execute(employees.insert(), employees_arr)
connection.execute(weekly_hours.insert(), hours_arr)



# Functions to get profits for the month

def get_employee_pay(month_start):
        # Get the wage and hours for each employee
        hours_tuple = connection.execute("SELECT e.eid, e.wage, wh.hours FROM employees e, weekly_hours wh WHERE e.eid = wh.eid AND MONTH(wh.week) = %s ORDER BY e.eid" % (month_start)).fetchall()

        # Get amount we must pay each employee
        pay = 0
        for h in hours_tuple:
                pay += h[1]*h[2]

        return pay

def get_boat_profits(month_start):
        # Gets bid, flat cost, daily price, and num of days reserved
        boats_tuple = connection.execute("SELECT b.bid, b.flat_cost, b.daily_price, (r.day_ret - r.day_res + 1) FROM boats b, reserves r WHERE r.bid = b.bid AND MONTH(r.day_res) = %s ORDER BY b.bid" % (month_start)).fetchall()

        # Get profit from each boat
        profit = 0
        for boats in boats_tuple:
                profit += boats[2]*boats[3] - boats[1]

        return profit

def get_monthly_profit(month_start):
        # date_string = split('/', week_start)
        # month_start = date_string[1]

        # Get total payment for employees
        pay = get_employee_pay(month_start)

        # Get total revenue from boats
        rev = get_boat_profits(month_start)

        # Get the total profit
        profit = rev - pay

        print("The profit for month %s is %d" % (month_start, profit))
        return profit

import pytest
# Test functions -- Assume month = 11 (i.e. November)
test_month = 11
def test_get_employee_pay():
        assert get_employee_pay(test_month) == 2996

def test_get_boat_profits():
        assert get_boat_profits(test_month) == 4060

def test_get_monthly_profit():
        assert get_monthly_profit(test_month) == 1064














