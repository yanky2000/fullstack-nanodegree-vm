from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()

def fetchRestaurants():
    q = session.query(Restaurant)

    print "RESTAURANTS fetched"
    rests = q.all()
    for rest in rests:
        print rest.id, rest.name
        print "\n"

#
#
#
# m = session.query(MenuItem)
# items = m.all()
# print "MENU ITEMS"
# for item in items:
#     print item.name
# print
# print "ITEMS: ", items

# finding veggieBurgers

# one = session.query(MenuItem).filter_by(id=1).one()
# one.price = 2.99
# session.add(one)
# session.commit()
#

session = DBSession()

veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
#


for veggieBurger in veggieBurgers:
    # if veggieBurger.price != 2.99:
    #     veggieBurger.price = 2.99
    #     session.add(veggieBurger)
    #     session.commit()
    print veggieBurger.id
    print veggieBurger.name

    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"
#
# for rest in rests:
#     print rest.name
#     # print rest.column_descriptions

# # Menu for UrbanBurger
# restaurant1 = Restaurant(name="Urban Burger")
#
# session.add(restaurant1)
# session.commit()
#
# menuItem2 = MenuItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                      price="$7.50", course="Entree", restaurant=restaurant1)
#
# session.add(menuItem2)
# session.commit()

