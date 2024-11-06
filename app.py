import tkinter as tk
from tkinter import ttk, messagebox
from database import session, GasStation, Employee, Product


class GasStationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("АЗС Управление")
        self.root.geometry("600x400")  # Фиксированный размер окна

        # Кнопки для открытия окон по категориям
        tk.Button(root, text="АЗС", command=self.open_gas_station_window).pack(fill=tk.X, pady=5)
        tk.Button(root, text="Сотрудники", command=self.open_employees_window).pack(fill=tk.X, pady=5)
        tk.Button(root, text="Товары", command=self.open_products_window).pack(fill=tk.X, pady=5)

    def open_gas_station_window(self):
        GasStationWindow(self.root)

    def open_employees_window(self):
        EmployeesWindow(self.root)

    def open_products_window(self):
        ProductsWindow(self.root)


class GasStationWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("АЗС")
        self.window.geometry("500x400")

        # Интерфейс для добавления АЗС
        tk.Label(self.window, text="Название").grid(row=0, column=0)
        tk.Label(self.window, text="Адрес").grid(row=1, column=0)
        tk.Label(self.window, text="Телефон").grid(row=2, column=0)

        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=0, column=1)
        self.address_entry = tk.Entry(self.window)
        self.address_entry.grid(row=1, column=1)
        self.phone_entry = tk.Entry(self.window)
        self.phone_entry.grid(row=2, column=1)

        tk.Button(self.window, text="Добавить", command=self.add_gas_station).grid(row=3, column=0, columnspan=2,
                                                                                   pady=10)

        # Интерфейс таблицы
        self.data_frame = tk.Frame(self.window)
        self.data_frame.grid(row=4, column=0, columnspan=3, sticky="nsew")

        self.tree = ttk.Treeview(self.data_frame, columns=("Name", "Address", "Phone"), show='headings')
        self.tree.heading("Name", text="Название")
        self.tree.heading("Address", text="Адрес")
        self.tree.heading("Phone", text="Телефон")
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.tree.bind("<Double-1>", self.on_item_double_click)  # Обработка двойного клика для редактирования
        self.list_stations()

        # Кнопка для удаления АЗС
        tk.Button(self.window, text="Удалить", command=self.delete_gas_station).grid(row=3, column=2)

    def list_stations(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        stations = session.query(GasStation).all()
        for station in stations:
            self.tree.insert("", "end", values=(station.name, station.address, station.phone))

    def add_gas_station(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()

        if name and address:
            try:
                station = GasStation(name=name, address=address, phone=phone)
                session.add(station)
                session.commit()
                messagebox.showinfo("Успех", "АЗС добавлена!")
                self.list_stations()  # Обновляем список станций
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", f"Не удалось добавить АЗС: {e}")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item, "values")

        self.name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        self.name_entry.insert(0, item_values[0])
        self.address_entry.insert(0, item_values[1])
        self.phone_entry.insert(0, item_values[2])

        # Кнопка для редактирования АЗС
        tk.Button(self.window, text="Редактировать", command=lambda: self.edit_gas_station(selected_item)).grid(row=3,
                                                                                                                column=3)

    def edit_gas_station(self, selected_item):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()

        if name and address:
            try:
                station_name = self.tree.item(selected_item, "values")[0]
                station = session.query(GasStation).filter_by(name=station_name).first()
                if station:
                    station.name = name
                    station.address = address
                    station.phone = phone
                    session.commit()
                    messagebox.showinfo("Успех", "АЗС обновлена!")
                    self.list_stations()  # Обновляем список станций
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", f"Не удалось обновить АЗС: {e}")

    def delete_gas_station(self):
        selected_item = self.tree.selection()[0]
        station_name = self.tree.item(selected_item, "values")[0]
        station = session.query(GasStation).filter_by(name=station_name).first()
        if station:
            try:
                session.delete(station)
                session.commit()
                messagebox.showinfo("Успех", "АЗС удалена!")
                self.list_stations()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", f"Не удалось удалить АЗС: {e}")


class EmployeesWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Сотрудники")
        self.window.geometry("600x400")

        # Интерфейс для добавления сотрудников
        tk.Label(self.window, text="Имя").grid(row=0, column=0)
        tk.Label(self.window, text="Фамилия").grid(row=1, column=0)
        tk.Label(self.window, text="Отчество").grid(row=2, column=0)
        tk.Label(self.window, text="Должность").grid(row=3, column=0)
        tk.Label(self.window, text="Телефон").grid(row=4, column=0)

        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=0, column=1)
        self.surname_entry = tk.Entry(self.window)
        self.surname_entry.grid(row=1, column=1)
        self.patronymic_entry = tk.Entry(self.window)
        self.patronymic_entry.grid(row=2, column=1)
        self.position_entry = tk.Entry(self.window)
        self.position_entry.grid(row=3, column=1)
        self.phone_entry = tk.Entry(self.window)
        self.phone_entry.grid(row=4, column=1)

        tk.Button(self.window, text="Добавить", command=self.add_employee).grid(row=5, column=0, columnspan=2, pady=10)

        # Интерфейс таблицы
        self.data_frame = tk.Frame(self.window)
        self.data_frame.grid(row=6, column=0, columnspan=3, sticky="nsew")

        self.tree = ttk.Treeview(self.data_frame, columns=("Name", "Surname", "Patronymic", "Position", "Phone"),
                                 show='headings')
        self.tree.heading("Name", text="Имя")
        self.tree.heading("Surname", text="Фамилия")
        self.tree.heading("Patronymic", text="Отчество")
        self.tree.heading("Position", text="Должность")
        self.tree.heading("Phone", text="Телефон")
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.tree.bind("<Double-1>", self.on_item_double_click)  # Обработка двойного клика для редактирования
        self.list_employees()

        # Кнопка для удаления сотрудника
        tk.Button(self.window, text="Удалить", command=self.delete_employee).grid(row=5, column=2)

    def list_employees(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        employees = session.query(Employee).all()
        for employee in employees:
            self.tree.insert("", "end", values=(
            employee.name, employee.surname, employee.patronymic, employee.position, employee.phone))

    def add_employee(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        patronymic = self.patronymic_entry.get()
        position = self.position_entry.get()
        phone = self.phone_entry.get()

        if name and surname and position:
            try:
                employee = Employee(name=name, surname=surname, patronymic=patronymic, position=position, phone=phone)
                session.add(employee)
                session.commit()
                messagebox.showinfo("Успех", "Сотрудник добавлен!")
                self.list_employees()  # Обновляем список сотрудников
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", f"Не удалось добавить сотрудника: {e}")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item, "values")

        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.patronymic_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        self.name_entry.insert(0, item_values[0])
        self.surname_entry.insert(0, item_values[1])
        self.patronymic_entry.insert(0, item_values[2])
        self.position_entry.insert(0, item_values[3])
        self.phone_entry.insert(0, item_values[4])

        # Кнопка для редактирования сотрудника
        tk.Button(self.window, text="Редактировать", command=lambda: self.edit_employee(selected_item)).grid(row=5,
                                                                                                             column=3)

    def edit_employee(self, selected_item):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        patronymic = self.patronymic_entry.get()
        position = self.position_entry.get()
        phone = self.phone_entry.get()

        if name and surname and position:
            try:
                employee_name = self.tree.item(selected_item, "values")[0]
                employee = session.query(Employee).filter_by(name=employee_name,
                                                             surname=self.tree.item(selected_item, "values")[1]).first()
                if employee:
                    employee.name = name
                    employee.surname = surname
                    employee.patronymic = patronymic
                    employee.position = position
                    employee.phone = phone
                    session.commit()
                    messagebox.showinfo("Успех", "Сотрудник обновлен!")
                    self.list_employees()  # Обновляем список сотрудников
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", f"Не удалось обновить сотрудника: {e}")

    def delete_employee(self):
        selected_item = self.tree.selection()[0]
        employee_name = self.tree.item(selected_item, "values")[0]
        employee_surname = self.tree.item(selected_item, "values")[1]
        employee = session.query(Employee).filter_by(name=employee_name, surname=employee_surname).first()
        if employee:
            try:
                session.delete(employee)
                session.commit()
                messagebox.showinfo("Успех", "Сотрудник удален!")
                self.list_employees()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", f"Не удалось удалить сотрудника: {e}")


class ProductsWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Товары")
        self.window.geometry("600x400")

        # Интерфейс для добавления товаров
        tk.Label(self.window, text="Название").grid(row=0, column=0)
        tk.Label(self.window, text="Количество").grid(row=1, column=0)
        tk.Label(self.window, text="Цена").grid(row=2, column=0)

        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=0, column=1)
        self.quantity_entry = tk.Entry(self.window)
        self.quantity_entry.grid(row=1, column=1)
        self.price_entry = tk.Entry(self.window)
        self.price_entry.grid(row=2, column=1)

        tk.Button(self.window, text="Добавить", command=self.add_product).grid(row=3, column=0, columnspan=2, pady=10)

        # Интерфейс таблицы
        self.data_frame = tk.Frame(self.window)
        self.data_frame.grid(row=4, column=0, columnspan=3, sticky="nsew")

        self.tree = ttk.Treeview(self.data_frame, columns=("Name", "Quantity", "Price"), show='headings')
        self.tree.heading("Name", text="Название")
        self.tree.heading("Quantity", text="Количество")
        self.tree.heading("Price", text="Цена")
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.tree.bind("<Double-1>", self.on_item_double_click)  # Обработка двойного клика для редактирования
        self.list_products()

        # Кнопка для удаления товара
        tk.Button(self.window, text="Удалить", command=self.delete_product).grid(row=3, column=2)

    def list_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        products = session.query(Product).all()
        for product in products:
            self.tree.insert("", "end", values=(product.name, product.quantity, product.price))

    def add_product(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
            try:
                product = Product(name=name, quantity=int(quantity), price=float(price))
                session.add(product)
                session.commit()
                messagebox.showinfo("Успех", "Товар добавлен!")
                self.list_products()  # Обновляем список товаров
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", f"Не удалось добавить товар: {e}")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля корректно.")

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item, "values")

        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

        self.name_entry.insert(0, item_values[0])
        self.quantity_entry.insert(0, item_values[1])
        self.price_entry.insert(0, item_values[2])

        # Кнопка для редактирования товара
        tk.Button(self.window, text="Редактировать", command=lambda: self.edit_product(selected_item)).grid(row=3,
                                                                                                            column=3)

    def edit_product(self, selected_item):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
            try:
                product_name = self.tree.item(selected_item, "values")[0]
                product = session.query(Product).filter_by(name=product_name).first()
                if product:
                    product.name = name
                    product.quantity = int(quantity)
                    product.price = float(price)
                    session.commit()
                    messagebox.showinfo("Успех", "Товар обновлен!")
                    self.list_products()  # Обновляем список товаров
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", f"Не удалось обновить товар: {e}")

    def delete_product(self):
        selected_item = self.tree.selection()[0]
        product_name = self.tree.item(selected_item, "values")[0]
        product = session.query(Product).filter_by(name=product_name).first()
        if product:
            try:
                session.delete(product)
                session.commit()
                messagebox.showinfo("Успех", "Товар удален!")
                self.list_products()
            except Exception as e:
                session.rollback()
                messagebox.showerror("Ошибка", f"Не удалось удалить товар: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GasStationApp(root)
    root.mainloop()
