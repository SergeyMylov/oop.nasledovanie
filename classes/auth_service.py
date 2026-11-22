# classes/auth_service.py
from .users import User, Customer, Admin

class AuthenticationService:
    """
    Сервис для управления регистрацией и аутентификацией пользователей.
    """
    def __init__(self):
        # Храним активную сессию (в реальной системе это был бы токен в HTTP-заголовках)
        self.current_user = None

    def register(self, user_class, username, email, password, **kwargs):
        """
        Регистрация нового пользователя.
        :param user_class: Класс пользователя (Customer или Admin)
        :param username: Имя пользователя
        :param email: Email
        :param password: Пароль
        :param args: Дополнительные аргументы (address для Customer, admin_level для Admin)
        """
        # 1. Проверка уникальности имени пользователя
        for user in User.users:
            if user.username == username:
                return {"success": False, "message": f"Пользователь с именем '{username}' уже существует."}

        try:
            # 2. Создание объекта пользователя
            user_instance = user_class(username, email, password, **kwargs)
            
            # 3. Добавление в глобальный список пользователей
            User.users.append(user_instance)
            
            return {"success": True, "message": f"Регистрация успешна! Добро пожаловать, {username}!"}
        except TypeError as e:
            return {"success": False, "message": f"Ошибка создания объекта: {str(e)}"}

    def login(self, username, password):
        """
        Аутентификация пользователя.
        """
        # 1. Поиск пользователя
        found_user = None
        for user in User.users:
            if user.username == username:
                found_user = user
                break
        
        if not found_user:
            return {"success": False, "message": "Пользователь не найден."}

        # 2. Проверка пароля
        if not User.check_password(found_user.password_hash, password):
            return {"success": False, "message": "Неверный пароль."}

        # 3. Успешный вход - устанавливаем текущую сессию
        self.current_user = found_user
        return {"success": True, "message": f"Вход выполнен успешно. Вы вошли как: {found_user.get_details()}"}

    def logout(self):
        """
        Выход пользователя из системы.
        """
        if self.current_user:
            user_name = self.current_user.username
            self.current_user = None
            return {"success": True, "message": f"Выход выполнен. Пока, {user_name}!"}
        else:
            return {"success": False, "message": "Вы не вошли в систему."}

    def get_current_user(self):
        """
        Возвращает текущего вошедшего пользователя.
        """
        if self.current_user:
            return {"success": True, "data": self.current_user}
        else:
            return {"success": False, "message": "Пользователь не вошел в систему."}
