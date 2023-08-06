from inventorpy.http_api.app import create_app
from inventorpy.storage import MemoryDB
from inventorpy.entities import Item, User
from inventorpy.utils import import_from_csv

from inventorpy.entities import Item

db = MemoryDB()

def items_list():
    s = list()
    for i in range(20):
        name = f'dummy_name_{i}'
        description = f'description {i}'
        s.append(Item(name=name, description=description))
    return s

items_list = items_list()
for each in items_list:
    db.create(each)

user_list = db.retrieve(entity_class='User')
if len(user_list) == 0:
    admin_user = User('admin', 'admin', 'admin@admin.com', 'admin')
    db.create(admin_user)

app = create_app(db)
app.run(debug=True)
