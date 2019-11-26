import datetime
import sys

from peewee import *
from collections import OrderedDict

db = SqliteDatabase('diary.db')

class Entry(Model):
    # content
    # timestamp
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def create_and_connect():
    """Connects to the database and creates the tables"""
    db.connect()
    db.create_tables([Entry],safe=True)

def menu_loop():
    """Show menu"""
    choice = None
    while choice != 'q':
        print("Press 'q' to quit")

        for key,value in menu.items():
            print("{}) {}".format(key,value.__doc__))
        choice = input("Action: ").lower().strip()

        if choice in menu:
            menu[choice]()

def add_entry():
    """Add Entry"""
    print("Enter your thoughts. Press Ctrl + D to finish")
    data = sys.stdin.read().strip()

    if data:
        if input("Do you want to save your entry? [Yn]").lower().strip() != 'n':
            Entry.create(content=data)
            print("Your entry was saved succesfully.")

def view_entries():
    """View All Entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print("*"*len(timestamp))
        print(entry.content)
        print("n) next entry")
        print("q) return to menu")

        next_action = input("Action: ").lower().strip()

        if next_action == 'q':
            break

def search_entries():
    """Search an entry"""
    

def delete_entry():
    """Delete an Entry"""

menu = OrderedDict([
    ('a',add_entry),
    ('v',view_entries),
    ('s',search_entries),
    ('d',delete_entry)
])

if __name__ == '__main__':
    create_and_connect()
    menu_loop()
