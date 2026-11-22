# classes/users.py
import hashlib
import uuid

class User:
    """
    Базовый класс, представляющий пользователя.
    """
    # Классовый атрибут для хранения всех зарегистрированных пользователей
    # В реальном приложении это была бы база данных, но для ДЗ используем список
    users = [] 

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        # Сохраняем захешированный пароль
        self.password_hash = self.hash_password(password)
        self.user_id = str(uuid.uuid4()) # Уникальный ID пользователя

    @staticmethod
    def hash_password(password):
        """
        Хеширование пароля с использованием sha256.
        Для большей безопасности в реальных приложениях добавляют 'salt', 
        но для учебных задач это достаточно.
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def check_password(stored_password, provided_password):
        """
        Проверка пароля.
        """
        return stored_password == User.hash_password(provided_password)

    def get_details(self):
        return f"Пользователь: {self.username}, Email: {self.email}"

class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """
    def __init__(self, username, email, password, address):
        # Вызываем конструктор родительского класса User
        super().__init__(username, email, password)
        self.address = address

    def get_details(self):
        return f"Клиент: {self.username}, Email: {self.email}, Адрес: {self.address}"

class Admin(User):
    """
    Класс, представляющий администратора, наследующий класс User.
    """
    def __init__(self, username, email, password, admin_level):
        # Вызываем конструктор родительского класса User
        super().__init__(username, email, password)
        self.admin_level = admin_level

    def get_details(self):
        return f"Администратор: {self.username}, Email: {self.email}, Уровень: {self.admin_level}"

    @staticmethod
    def list_users():
        """
        Выводит список всех пользователей.
        """
        if not User.users:
            return "Список пользователей пуст."
        
        user_list = "Список всех пользователей:\n"
        for user in User.users:
            user_list += f"  - ID: {user.user_id}, {user.get_details()}\n"
        return user_list

    @staticmethod
    def delete_user(username):
        """
        Удаляет пользователя по имени пользователя.
        """
        # Ищем пользователя в статическом списке
        user_to_delete = None
        for user in User.users:
            if user.username == username:
                user_to_delete = user
                break
        
        if user_to_delete:
            User.users.remove(user_to_delete)
            return f"Пользователь '{username}' успешно удален."
        else:
            return f"Пользователь с именем '{username}' не найден."
