import datetime
import sys

from collections import OrderedDict
from peewee import *

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
    db.create_tables([Entry], safe=True)


def menu_loop():
    """Show menu"""
    choice = None
    while choice != 'q':
        print("Press 'q' to quit")

        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Action: ").lower().strip()

        if choice in menu:
            menu[choice]()


def add_entry():
    """Add Entry"""
    print("Enter your thoughts.")
    print("Press Ctrl+z (Windows) or Ctrl+D (MacOS/Unix) to finish.")
    data = sys.stdin.read().strip()

    if data:
        if input("Do you want to save your entry?[Yn]").lower().strip() != 'n':
            Entry.create(content=data)
            print("Your entry was saved succesfully.")


def view_entries(search_query=None):
    """View All Entries"""

    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print("*"*len(timestamp))
        print("\n")
        print(entry.content)
        print("\n")
        print("*"*len(timestamp))
        print("n) next entry")
        print("d) delete entry")
        print("q) return to menu")

        next_action = input("Action:[Ndq] ").lower().strip()

        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entries():
    """Search an entry"""
    search_query = input("Search query: ").strip()
    view_entries(search_query)


def delete_entry(entry):
    """Delete an Entry"""
    action = input("Are you sure?[Yn] ").lower().strip()

    if action == 'y':
        entry.delete_instance()

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])

if __name__ == '__main__':
    create_and_connect()
    menu_loop()
