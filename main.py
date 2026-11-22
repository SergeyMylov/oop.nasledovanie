# main.py
from classes.users import Customer, Admin
from classes.auth_service import AuthenticationService

def main():
    # Инициализация сервиса
    auth_service = AuthenticationService()

    print("="*50)
    print("1. РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЕЙ")
    print("="*50)

    # Регистрация обычного клиента (Customer)
    # Аргументы: username, email, password, address (доп. аргумент для Customer)
    res_customer = auth_service.register(
        user_class=Customer,
        username="mikhail_dev",
        email="mikhail@python.ru",
        password="secret123",
        address="Москва, ул. Программистов, д. 1"
    )
    print(res_customer["message"])

    # Регистрация администратора (Admin)
    # Аргументы: username, email, password, admin_level (доп. аргумент для Admin)
    res_admin = auth_service.register(
        user_class=Admin,
        username="root",
        email="admin@system.ru",
        password="adminPass456",
        admin_level=5
    )
    print(res_admin["message"])

    # Проверка уникальности: попытка зарегистрировать михаила снова
    res_dup = auth_service.register(
        user_class=Customer,
        username="mikhail_dev",
        email="another@email.com",
        password="wrong",
        address="SPb"
    )
    print(res_dup["message"])

    print("\n" + "="*50)
    print("2. АДМИНИСТРИРОВАНИЕ (Управление пользователями)")
    print("="*50)
    
    # Только Админ может видеть список (в реальной системе нужно бы проверять права)
    # Здесь мы просто вызываем статический метод класса Admin
    print(Admin.list_users())

    print("\n" + "="*50)
    print("3. АВТОРИЗАЦИЯ (LOGIN)")
    print("="*50)

    # Успешный вход клиента
    res_login = auth_service.login("mikhail_dev", "secret123")
    print(res_login["message"])
    
    # Проверка текущей сессии
    current = auth_service.get_current_user()
    if current["success"]:
        print(f"Текущий пользователь в сессии: {current['data'].get_details()}")

    # Неправильный пароль
    res_bad_pass = auth_service.login("mikhail_dev", "wrong_password")
    print(res_bad_pass["message"])

    # Выход
    res_logout = auth_service.logout()
    print(res_logout["message"])

    # Повторный вход, чтобы удалить пользователя
    auth_service.login("root", "adminPass456")
    
    print("\n" + "="*50)
    print("4. УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ")
    print("="*50)
    
    # Удаляем клиента
    res_delete = Admin.delete_user("mikhail_dev")
    print(res_delete)
    
    # Проверяем список снова
    print("\nПосле удаления:")
    print(Admin.list_users())

if __name__ == "__main__":
    main()
