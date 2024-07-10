from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String

# Database setup
engine = create_engine('sqlite:///contactBook.db')
Base = declarative_base()

class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    group = Column(String, default='Anonymous')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
mySession = Session()

#########################################
# Custom Logic for my Contact Book

def createContact ():
    print('\nEnter the Contact Name:')
    name = input()

    print('\nEnter the Phone Number:')
    phone = input()

    print('\nDefine contacts group (Optional):')
    group = input()

    print('\nEnter user\'s email address:')
    email = input()

    # Create a new contact
    new_contact = Contacts(name=name, email=email, phone=phone, group=group)
    mySession.add(new_contact)
    mySession.commit()

    print('Contact created successfully!')

def showAllContacts():
    # Query the table
    all_contacts = mySession.query(Contacts).all()
    print('\n')

    # Print column names
    column_names = Contacts.__table__.columns.keys()
    print("| " + f"{' | '.join(column_names)}")

    # Print the results row by row
    for contact in all_contacts:
        print(f"| {contact.id} | {contact.name} | {contact.email} | {contact.phone} | {contact.group}")

def editContact():
    print('\nEnter the contact_id:')
    try:
        contact_id = int(input())
    except ValueError:
        print('Invalid Entry! Please try again...')
        return

    _contact = mySession.query(Contacts).filter_by(id=contact_id).first()
    
    if not _contact:
        print('Contact not found!')
        return

    print('''\nEnter the data in the following order (leave empty for no change):
    _________________
    1.  contact_name
    2.  contact_email
    3.  contact_phone
    4.  contact_group
    _________________''')

    new_name = input().strip()
    new_email = input().strip()
    new_phone = input().strip()
    new_group = input().strip()

    # Only update fields if new values are provided
    if new_name:
        _contact.name = new_name # type: ignore
    if new_email:
        _contact.email = new_email # type: ignore
    if new_phone:
            _contact.phone = new_phone # type: ignore
    if new_group:
        _contact.group = new_group # type: ignore

    mySession.commit()
    print('Contact updated successfully!')

def clearAll():
    mySession.query(Contacts).delete()
    mySession.commit()
    print("Deleted all Contacts !")

def deleteContact():
    print('\nEnter the contact id:')
    try:
        target_id = int(input())
    except ValueError:
        print('Invalid input! Please enter a valid number only.')
        return  # Exit the function if the input is invalid

    target = mySession.query(Contacts).filter_by(id=target_id).first()
    if target is None:
        print(f'No contact found with id {target_id}.')
    else:
        mySession.delete(target)
        mySession.commit()  # Commit the changes to the database
        print(f'Contact with id ({target_id}) has been deleted.')


def showOnly():
    print('\nEnter the contact name:')
    try:
        target_id = int(input())
    except ValueError:
        print('Invalid input! Please enter a valid number only.')

    target = mySession.query(Contacts).filter_by(id=target_id).first()
    column_names = Contacts.__table__.columns.keys()

    print("| " + f"{' | '.join(column_names)}")
    print(f"| {target.id} | {target.name} | {target.email} | {target.phone} | {target.group}") # type: ignore

def Help():
    print('''\n##############################################################################
--------------------------
WELOCME TO THE USER GUIDE!
--------------------------

Following are the commands with description:

[1]  .create: "Use this command to create a new contact."

[2]  .edit: "Use this command to edit an existing contact."

[3]  .delete: "Use this command to delete a specific contact (by id)."

[4]  .showOnly: "Use this command to show a contact (by name)."

[5]  .showAll: "Use this command to show all contacts from your book."

[6]  .clearAll: "Use this command to clear all contacts from your book."

[7]  .help: "Use this command to display this guide."

[8]  .quit: "Use this command to exit the Contact Book."
_____________________________________________________________________________
          
Have fun using this Contact Book 😀
##############################################################################''')

#########################################
flag = False

def checkResponse(respond):
    match respond:
        case '.create':
            # Create a new contact
            createContact()
            return
        case '.edit':
            # Edit a contact
            editContact()
            return
        case '.delete':
            # Delete a contact
            deleteContact()
            return
        case '.showonly':
            # Show a specific contact
            showOnly()
            return
        case '.showall':
            # Show all contacts
            showAllContacts()
            return
        case '.clearall':
            # Clear all contacts
            clearAll()
            return
        case '.help':
            # Show User-Manual
            Help()
            return
        case '.quit':
            global flag
            flag = True
        case _:
            print("Invalid Syntax! Type '.help' for user guidance.")

#########################################
print("Welcome to this Contact Book!")

while flag is False:
    print('\nType from the following commands:')
    print('.create  .edit  .delete  .showOnly  .showAll  .clearAll  .help  .quit')

    response = input().lower()
    checkResponse(respond=response)
