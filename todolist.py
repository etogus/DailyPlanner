from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker


# The menu options
MENU = {1: "Today's tasks", 2: "Week's tasks", 3: "All tasks", 4: "Missed tasks",
        5: "Add a task", 6: "Delete a task", 0: "Exit"}


# Display the menu options
def show_menu():
    for key, value in MENU.items():
        print(f"{key}) {value}")


# Set up the SQLite database
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


# Class to map to the 'task' table in the database
class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# Create the 'task' table in the database
Base.metadata.create_all(engine)

# Create a new session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Main loop to interact with the user
while True:
    show_menu()
    user_input = int(input())
    if user_input == 0:
        # Exit the program
        print("Bye!")
        break
    elif user_input == 1:
        # Display today's tasks
        rows = session.query(Task).filter(Task.deadline == datetime.date(datetime.today())).all()
        print(F"Today {datetime.today().day} {datetime.today().strftime('%b')}:")
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for row in rows:
                print(f"{row.id}. {row}")
    elif user_input == 2:
        # Display tasks for the week
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        for i in range(0, 7):
            day = today+timedelta(days=i)
            rows = session.query(Task).filter(Task.deadline == day).all()
            if len(rows) == 0:
                print(f"{day.strftime('%A %d %b')}:")
                print("Nothing to do!")
            else:
                print(f"{day.strftime('%A %d %b')}:")
                for j, row in enumerate(rows):
                    print(f"{j+1}. {row}")
            print("")
    elif user_input == 3:
        # Display all tasks ordered by deadline
        rows = session.query(Task).order_by(Task.deadline).all()
        for i, row in enumerate(rows):
            print(f"{i}. {row}. {row.deadline.day} {row.deadline.strftime('%b')}")
    elif user_input == 4:
        # Display missed tasks (tasks with deadlines before today)
        rows = session.query(Task).filter(Task.deadline < datetime.today()).all()
        print("Missed tasks:")
        if len(rows) == 0:
            print("All tasks have been completed!")
        else:
            for i, row in enumerate(rows):
                print(f"{i+1}. {row}. {row.deadline.strftime('%d %b')}")
        print("")
    elif user_input == 5:
        # Add a new task
        print("Enter a task")
        new_task = input()
        print("Enter a deadline")
        new_task_deadline = datetime.strptime(input(), '%Y-%m-%d')
        new_row = Task(task=new_task, deadline=new_task_deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif user_input == 6:
        # Delete a task
        print("Choose the number of the task you want to delete:")
        rows = session.query(Task).order_by(Task.deadline).all()
        for i, row in enumerate(rows):
            print(f"{i+1}. {row}. {row.deadline.day} {row.deadline.strftime('%b')}")
        task_to_delete = int(input())-1
        session.delete(rows[task_to_delete])
        session.commit()
        print("The task has been deleted!")
    else:
        print("Incorrect input!")
