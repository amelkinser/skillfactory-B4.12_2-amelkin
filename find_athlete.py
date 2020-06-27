
##---------- B4.12 Домашнее задание № 2 --------------------------------------
##    Написать модуль find_athlete.py поиска ближайшего к пользователю атлета
##    27.06.2020 г.
##    Группа: PWS-21.
##    Амелькин С.Б.
##----------------------------------------------------------------------------

# испортируем модули стандартной библиотеки datetime
import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

# Описывает структуру таблицы athelete 
class Athelete(Base):
    # задаем название таблицы
    __tablename__ = 'athelete'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)             # возраст
    birthdate = sa.Column(sa.Text)          # День Рождения
    gender = sa.Column(sa.Text)             # пол
    height = sa.Column(sa.Float)            # рост
    name = sa.Column(sa.Text)               # имя
    weight = sa.Column(sa.INTEGER)          # вес
    gold_medals = sa.Column(sa.INTEGER)     # золотые медали
    silver_medals = sa.Column(sa.INTEGER)   # серебряные медали
    bronze_medals = sa.Column(sa.INTEGER)   # бронзовые медали
    total_medals = sa.Column(sa.INTEGER)    # общее число медалей
    sport = sa.Column(sa.Text)              # спорт
    country = sa.Column(sa.Text)            # страна

# Описывает структуру таблицы user 
class User(Base):
    
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.INTEGER, primary_key=True)
    # имя 
    first_name = sa.Column(sa.Text)
    # фамилия 
    last_name = sa.Column(sa.Text)
    # пол
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # День Рождения
    birthdate = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.Float)



# Устанавливает соединение к базе данных,
# создает таблицы, если их еще нет и возвращает объект сессии 
def connect_db():
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()



# Производит поиск пользователей в таблице Athelete по введенному идентификатору number
def find(number, session):
    all_athelete_list = session.query(Athelete).all()
    all_users_list = session.query(User).all()

    # ПОИСК ПО РОСТУ
    user1=""
    for user in all_users_list: # В таблице "user" по id=number определяем,
                                # какие ему соответствуют рост и дата,
                                # а также указываем начальные значения минимальных "дельт" роста и даты
                                # для последующей работы с ними
        if user.id==number:
            height_sel=user.height
            delta_min=user.height
            data_birthdate=user.birthdate
            if data_birthdate!="": # Если в таблице "user" по id=number указана дата
                data_sel=datetime.datetime.strptime(data_birthdate, '%Y-%m-%d')
                data_min=datetime.datetime.strptime("0001-01-01", '%Y-%m-%d')
                delta_data_min=abs(data_sel-data_min)
            

    if height_sel!=None: # Если в таблице "user" по id=number указан рост
        for user in all_athelete_list:  # Пробегаемся по таблице атлетов
            curr_height=user.height     # Рост в текущей строке таблицы "athelete"
            if curr_height==None: continue # Пропускаем эту строку, если там нет роста

            curr_delta=abs(height_sel-curr_height) # Разница в росте

            if curr_delta<delta_min:        # Поиск минимальной разницы в росте
                    delta_min=curr_delta    # Как только находим очередной минимум-> переписываем ответ
                    user1 = """\nБлижайший по РОСТУ атлет: 
    - ИДЕНТИФИКАТОР: {}
    - возраст: {}
    - День Рождения: {}
    - пол: {}
    - РОСТ: {}
    - имя: {}
    - вес: {}
    - золотые медали: {}
    - серебряные медали: {}
    - бронзовые медали: {}
    - общее число медалей: {}
    - спорт: {}
    - страна: {}""".format(user.id, user.age, user.birthdate,user.gender,user.height,
                           user.name,user.weight,user.gold_medals,user.silver_medals,
                           user.bronze_medals,user.total_medals,user.sport,user.country)
    else:
        print("Рост не указан")

    # ПОИСК ПО ДАТЕ (выполняется аналогично поиску по росту)
    user2=""
    if data_birthdate!="": # Если в таблице "user" по id=number указана дата
        for user in all_athelete_list: # Пробегаемся по таблице атлетов
            if user.birthdate=="": continue # Пропускаем эту строку, если там нет даты
            curr_data_sel=datetime.datetime.strptime(user.birthdate, '%Y-%m-%d')
            curr_data_delta=abs(curr_data_sel-data_sel) # Разница в дате
            if curr_data_delta<delta_data_min: # Поиск минимальной разницы
                delta_data_min=curr_data_delta # Как только находим очередной минимум-> переписываем ответ
                user2 = """\nБлижайший по ДАТЕ (День Рождения) атлет: 
    - ИДЕНТИФИКАТОР: {}
    - возраст: {}
    - ДЕНЬ РОЖДЕНИЯ: {}
    - пол: {}
    - рост: {}
    - имя: {}
    - вес: {}
    - золотые медали: {}
    - серебряные медали: {}
    - бронзовые медали: {}
    - общее число медалей: {}
    - спорт: {}
    - страна: {}""".format(user.id, user.age, user.birthdate,user.gender,user.height,
                           user.name,user.weight,user.gold_medals,user.silver_medals,
                           user.bronze_medals,user.total_medals,user.sport,user.country)
    else:
        print("\nДаты нет в таблице \"user\"")
        
    return user1, user2



# Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
# и выводит результат
def main():
    session = connect_db()
    query = session.query(User)
    
    max_id = query.count()
    if max_id==0:
        print("\nОшибка! Нет записей в таблице User")
        return
    number = int(input("""\nПожалуйста, введите идентификатор пользователя из таблицы \"user\" \nв диапазоне от 1 до {}:""".format(max_id)))
    if number<1 or number>max_id:
        print("Ошибка! Неверный идентификатор")
        return
    
    user1,user2 = find(number, session) # результат работы
    print(user2)
    print(user1)
    


if __name__ == "__main__":
    main()

















    
