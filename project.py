
1. Создание базы данных

```python
import sqlite3

# Создаем подключение к базе данных
conn = sqlite3.connect('employees.db')

# Создаем таблицу для хранения данных о сотрудниках
cursor = conn.cursor()
cursor.execute('''CREATE TABLE employees
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   phone TEXT,
                   email TEXT,
                   salary REAL)''')
conn.commit()

# Закрываем подключение к базе данных
conn.close()
```

2. Добавление нового сотрудника


```python
from tkinter import *
import sqlite3

class AddEmployeeForm:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent)
        self.frame.pack()

        self.name_label = Label(self.frame, text='Name')
        self.name_label.grid(row=0, column=0)
        self.name_entry = Entry(self.frame)
        self.name_entry.grid(row=0, column=1)

        self.phone_label = Label(self.frame, text='Phone')
        self.phone_label.grid(row=1, column=0)
        self.phone_entry = Entry(self.frame)
        self.phone_entry.grid(row=1, column=1)

        self.email_label = Label(self.frame, text='Email')
        self.email_label.grid(row=2, column=0)
        self.email_entry = Entry(self.frame)
        self.email_entry.grid(row=2, column=1)

        self.salary_label = Label(self.frame, text='Salary')
        self.salary_label.grid(row=3, column=0)
        self.salary_entry = Entry(self.frame)
        self.salary_entry.grid(row=3, column=1)

        self.submit_button = Button(self.frame, text='Submit', command=self.submit)
        self.submit_button.grid(row=4, column=0, columnspan=2)

    def submit(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        salary = float(self.salary_entry.get())

        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)',
                       (name, phone, email, salary))
        conn.commit()
        conn.close()

        self.parent.destroy()

root = Tk()
form = AddEmployeeForm(root)
root.mainloop()
```

3. Изменение текущего сотрудника

```python
from tkinter import *
import sqlite3

class EditEmployeeForm:
    def __init__(self, parent, employee_id):
        self.parent = parent
        self.employee_id = employee_id

        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, phone, email, salary FROM employees WHERE id=?', (employee_id,))
        row = cursor.fetchone()
        conn.close()

        self.frame = Frame(parent)
        self.frame.pack()

        self.name_label = Label(self.frame, text='Name')
        self.name_label.grid(row=0, column=0)
        self.name_entry = Entry(self.frame, value=row[0])
        self.name_entry.grid(row=0, column=1)

        self.phone_label = Label(self.frame, text='Phone')
        self.phone_label.grid(row=1, column=0)
        self.phone_entry = Entry(self.frame, value=row[1])
        self.phone_entry.grid(row=1, column=1)

        self.email_label = Label(self.frame, text='Email')
        self.email_label.grid(row=2, column=0)
        self.email_entry = Entry(self.frame, value=row[2])
        self.email_entry.grid(row=2, column=1)

        self.salary_label = Label(self.frame, text='Salary')
        self.salary_label.grid(row=3, column=0)
        self.salary_entry = Entry(self.frame, value=row[3])
        self.salary_entry.grid(row=3, column=1)

        self.submit_button = Button(self.frame, text='Submit', command=self.submit)
        self.submit_button.grid(row=4, column=0, columnspan=2)

    def submit(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        salary = float(self.salary_entry.get())

        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?',
                       (name, phone, email, salary, self.employee_id))
        conn.commit()
        conn.close()

        self.parent.destroy()

root = Tk()
form = EditEmployeeForm(root, 1) # Изменяем сотрудника с id=1
root.mainloop()
```

4. Удаление сотрудника

```python
import sqlite3

def delete_employee(employee_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id=?', (employee_id,))
    conn.commit()
    conn.close()
```

5. Поиск по ФИО

```python
from tkinter import *
from tkinter.ttk import *
import sqlite3

class SearchEmployeeForm:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent)
        self.frame.pack()

        self.name_label = Label(self.frame, text='Name')
        self.name_label.grid(row=0, column=0)
        self.name_entry = Entry(self.frame)
        self.name_entry.grid(row=0, column=1)

        self.search_button = Button(self.frame, text='Search', command=self.search)
        self.search_button.grid(row=1, column=0, columnspan=2)

        self.treeview = Treeview(self.frame, columns=('phone', 'email', 'salary'))
        self.treeview.heading('#0', text='Name')
        self.treeview.heading('phone', text='Phone')
        self.treeview.heading('email', text='Email')
        self.treeview.heading('salary', text='Salary')
        self.treeview.grid(row=2, column=0, columnspan=2)

    def search(self):
        name = self.name_entry.get()

        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, phone, email, salary FROM employees WHERE name LIKE ?', ('%'+name+'%',))
        rows = cursor.fetchall()
        conn.close()

        self.treeview.delete(*self.treeview.get_children())

        for row in rows:
            self.treeview.insert('', 'end', text=row[1], values=(row[2], row[3]))

root = Tk()
form = SearchEmployeeForm(root)
root.mainloop()
```

6. Обновление записей из БД в виджете Treeview

```python
from tkinter import *
from tkinter.ttk import *
import sqlite3

class EmployeeList:
    def __init__(self, parent):
        self.parent = parent

        self.treeview = Treeview(parent, columns=('phone', 'email', 'salary'))
        self.treeview.heading('#0', text='Name')
        self.treeview.heading('phone', text='Phone')
        self.treeview.heading('email', text='Email')
        self.treeview.heading('salary', text='Salary')
        self.treeview.pack()

        self.update()

    def update(self):
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, phone, email, salary FROM employees')
        rows = cursor.fetchall()
        conn.close()

        self.treeview.delete(*self.treeview.get_children())

        for row in rows:
            self.treeview.insert('', 'end', text=row[1], values=(row[2], row[3], row[4]))

root = Tk()
form = EmployeeList(root)
root.mainloop()
```

