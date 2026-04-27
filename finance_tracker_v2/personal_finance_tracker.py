import datetime
from models import (
    FinanceTracker, SavingsTracker, Statistics,
    RegularPayments, FinanceRecord, SavingsRecord, RegularRecord
)


def get_valid_date(*args:str) -> None:
    """
    Проверяет, соответствует ли строка заданному формату даты.
    При несовпадении запрашивает повторный ввод до тех пор, пока не будет введена корректная дата или команда 'exit'.

    Аргументы:
        *args: строки с датами для проверки.
        **kwargs: дополнительные параметры.
            date_format (str): ожидаемый формат даты (по умолчанию "%Y-%m-%d").

    Возвращает:
        bool: True, если все переданные строки соответствуют формату даты.
        str: 'Вы вышли', если пользователь ввёл 'exit'.
    """
    
    results = []
    count = 0
   
    while len(results) != len(args):
        try:
            datetime.datetime.strptime(args[count], "%Y-%m-%d")
            results.append(True)
            count += 1

        except ValueError:
            print('\nВведите коректную дату в формате ГГГГ-ММ-ДД\n')
            break
    

def show_stats(stats: Statistics) -> str:
    date = input('Введите дату в формате ГГГГ-ММ-ДД: ')
    get_valid_date(date)
    return stats.stats_procent(date)

 
def transaction_menu(tracker: FinanceRecord) -> None:
    """
    Консольное меню управления финансовыми транзакциями.
    """
    
    today = str(datetime.date.today())
    
    while True:
        print("\n" + "=" * 40)
        print("УПРАВЛЕНИЕ ТРАНЗАКЦИЯМИ".center(40))
        print("=" * 40)
        print('1.Добавление доходной транзакции')
        print('2.Добавление расходной транзакции')
        print('3.Просмотр транзакций')
        print('4.Удаление транзакций по ID')
        print('0.Выход')
    
        choise= input('Выберите пункт из меню 0-4: ')

        if choise == '0':
            break

        elif choise == '1':
            try: 
                amount = int(input('Введите сумму транзакции: '))
            except ValueError:
                print('Ошибка: Сумма транзакции должна быть целым числом')
                continue
            
            description = input('Можете ввести описание данной операции. Напишите "Другое" если не хотите вводить описание: ')
            idx = len(tracker.records)
            tracker.add(FinanceRecord(amount, today, FinanceRecord.INCOME, 
                                      description, idx))

            print('\nВЫПОЛНЕНО')

        elif choise == '2':
            try:
                amount = int(input('Наберите сумму транзакции: '))
            except ValueError:
                print('Ошибка: Сумма транзакции должна быть целым числом')
                continue


            description = input('Можете ввести описание данной операции. Напишите "Другое" если не хотите вводить описание: ')
            idx = len(tracker.records)
            tracker.add(FinanceRecord(amount, today, FinanceRecord.EXPENSE, 
                                      description, idx))

            print('\nВЫПОЛНЕНО')

        elif choise == '3':
            while True:
                print('1:Просмотр всех транзакций')
                print('2:Просмотр транзакций по датам')
                print('0.Выход')
                
                choice = input('Выберите пунк из меню 0-2: ')
            
                if choice == '0':
                    break

                elif choice  == '1':
                    print(tracker.all_trans())
                
                elif choice == '2':
                    date_left = input('Введите дату с которой хотите вывести транзакциив формате ГГГГ-ММ-ДД: ')
                    date_right = input('Введите дату до которой хотите вывести транзакции в формате ГГГГ-ММ-ДД: ')
                    get_valid_date(date_left,date_right)

                    tracker.search_transactions_date(date_left, date_right)
                
                else:
                    print('Вы вели не коректное значение.')
                    continue


        elif choise == '4':
            try:
                idx = int(input('Введите ID транзакции которую хотите удалить: '))
            except ValueError:
                print('Ошибка: ID транзакции должна быть целым числом')
                continue
            
            tracker.remove(idx)

            print('\nВЫПОЛНЕНО')

        else: 
            print('Вы вели не коректное значение.')
            continue
 

def savings_menu(savings: SavingsTracker) -> None:
    """
      Консольное меню управления сбережениями.

    Особенности:

        - Для операций перевода между основным балансом и накоплениями
          (пункты меню 3 и 4) используются методы `transfer_from_finance_tracker`
          и `transfer_to_finance_tracker` класса `SavingsTracker`.
        - Эти методы добавляют новые записи в `FinanceTracker` (основной баланс).

        - ID для новых записей в `FinanceTracker` вычисляется как `len(tracker.records)`,
          где `tracker` —  экземпляр `FinanceTracker`. Это гарантирует
          уникальность ID внутри основного хранилища.
        - Если бы для ID использовалась длина `savings.records`, возникли бы коллизии,
          так как нумерация в `SavingsTracker` независима от `FinanceTracker`.
    """
    today = str(datetime.date.today())

    while True:
        print("\n" + "=" * 40)
        print("УПРАВЛЕНИЕ СБЕРЕЖЕНИЯМИ".center(40))
        print("=" * 40)
        print('1.Просмотр баланса сбережений')
        print('2.Пополнить накопления без изменения основного баланса')
        print('3.Пополнить накопления из основного баланс')
        print('4.Снять с накоплений в основной баланс')
        print('5.Просмотр истории транзакций сбережений')
        print('0.Выход')

        choice = input('Выберите пункт из меню 0-4: ')

        if choice == '0':
            break                                                         

        elif choice == '1':
            print(savings.balance_savings())

        elif choice == '2':
            try: 
                amount = int(input('Введите сумму транзакции: '))
            except ValueError:
                print('Ошибка: Сумма транзакции должна быть целым числом')
                continue
           
            description = input('Можете ввести описание данной операции. Напишите "Другое" если не хотите вводить описание: ')
            idx = len(savings.records)
            savings.add(SavingsRecord(amount, today, SavingsRecord.DEPOSIT, 
                                      description, idx))
            
            print('\nВЫПОЛНЕНО')

        elif choice == '3':
            try: 
                amount = int(input('Введите сумму транзакции: '))
            except ValueError:
                print('Ошибка: Сумма транзакции должна быть целым числом')
                continue

            description = input('Можете ввести описание данной операции. Напишите "Другое" если не хотите вводить описание: ')
            today = str(datetime.date.today())
            idx = len(tracker.records)
            savings.transfer_from_finance_tracker(amount,today,description,tracker,idx)
            
            print('\nВЫПОЛНЕНО')

    
        elif choice == '4':
            try:
                amount = int(input('Введите сумму транзакции: '))
            except ValueError:
                print('Ошибка: Сумма сберегательной должна быть целым числом')
                continue                                                    
            
            description = input('Можете ввести описание данной операции. Напишите "Другое" если не хотите вводить описание: ')
            idx = len(tracker.records)         
            savings.transfer_to_finance_tracker(amount,today,description,tracker,idx)
            
            print('\nВЫПОЛНЕНО')
        
        elif choice == '5':
            while True:
                print('1:Просмотр всех транзакций')
                print('2:Просмотр транзакций по датам')
                print('0.Выход')
                
                choice = input('Выберите пунк из меню 0-2: ')
            
                if choice == '0':
                    break

                elif choice  == '1':
                    print(savings.all_trans())
                
                elif choice == '2':
                    date_left = input('Введите дату с которой хотите вывести транзакции в формате ГГГГ-ММ-ДД: ')
                    date_right = input('Введите дату до которой хотите вывести транзакции в формате ГГГГ-ММ-ДД: ')
                    get_valid_date(date_left,date_right)

                    savings.search_transactions_date(date_left, date_right)
                
                else:
                    print('Вы вели не коректное значение.')
                    continue

        else: 
            print('Вы вели не коректное значение.')
            continue


def regular_operations(regular: RegularPayments) -> None:
    """
    Консольное меню управления регулярными платежами.
    """                                     

    while True:
        print("\n" + "=" * 40)
        print("РЕГУЛЯРНЫЕ ПЛАТЕЖИ".center(40))
        print("=" * 40)
        print('1.Добавить доходную регулярную операцию')
        print('2.Добавить расходную регулярную операцию')
        print('3.Просмотр регулярный операций')
        print('4.Удаление регулярной операции по ID')
        print('0.Выход')

        choice = input('Выберите пункт из меню 0-4: ')

        if choice == '0':
            break

        elif choice == '1':
            try:
                amount = int(input('Наберите сумму регулярной операции: '))
            except ValueError:
                print('Ошибка: Сумма регулярной операции должна быть целым числом')
                continue
            
            description = input('Введите описание регулярной операции: ')
           
            date = input('Введите дату срабатывания регуляной операции в формате ГГГГ-ММ-ДД: ')
            get_valid_date(date)
            parts = date.split('-')
            month_day = f"{parts[2]}"
     
            
            idx = len(regular.records) 
            
            regular.add(RegularRecord(amount, month_day, RegularRecord.INCOME_REGULAR, 
                                      description, idx, last_processed=None))
            
            print('\nРегулярное начисление активировано!')
            print(f'Теперь каждый месяц {month_day}-го числа на ваш счёт будут прибавляться деньги. ')
        
        elif choice == '2':
            try:
                amount = int(input('Наберите сумму регулярной операции: '))
            except ValueError:
                print('Ошибка: Сумма регулярной операции должна быть целым число')
                continue
            
            description = input('Введите описание регулярной операции: ')
            
            date = input('Введите дату срабатывания регулряной операции в формате ГГГГ-ММ-ДД: ')
            get_valid_date(date)
            parts = date.split('-')
            month_day = f"{parts[2]}"

            idx = len(regular.records)
            
            regular.add(RegularRecord(amount, month_day, RegularRecord.EXPENSE_REGULAR, description, idx))
            
            print('\nРегулярное начисление активировано!')
            print(f'Теперь каждый месяц {month_day}-го числа на ваш счёт будут прибавляться деньги. ')

        elif choice == '3':
                print(regular.all_trans())

        elif choice == '4':
            try:
                idx = int(input('Введите ID регулярного платежа которую хотите удалить: '))
            except ValueError:
                print('Ошибка: ID должна быть целым число')
          
            regular.remove(idx)
            
            print('\nВЫПОЛНЕНО')

        else:
            print('Введите коректное значение') 
            
tracker = FinanceTracker()
savings = SavingsTracker()
stats = Statistics(tracker)
regular = RegularPayments()
            

def user_balance(tracker: FinanceTracker, savings: SavingsTracker, stats: Statistics, regular: RegularPayments) -> None:
    """
    Главное консольное меню приложения.

    Координирует работу всех подсистем:
        - Управление транзакциями.
        - Управление сбережениями.
        - Управление регулярными платежами.
        - Управление статистикой
    """

    while True:
        regular.сheck_regular_trans(tracker)

        print("\n" + "=" * 40)
        print("ГЛАВНОЕ МЕНЮ".center(40))
        print("=" * 40)
        print('1.Управление транзакциями')
        print('2.Управление сбережениями')
        print('3.Управление регулярными платежами')
        print('4.Просмотреть статистику')
        print('5.Баланс')
        print('0:Выход')

        choice = input('Выберите пункт из меню 0-3: ')

        if choice == '0': 
            break

        elif choice == '1':
            transaction_menu(tracker)

        elif choice == '2':
            savings_menu(savings)

        elif choice == '3':
            regular_operations(regular)

        elif choice == '4':
            print(show_stats(stats))

        elif choice == '5':
            print(tracker.get_balance())
        else:
            print('Введите коректное значение')  
        
    
if __name__ == "__main__":
    tracker = FinanceTracker()
    savings = SavingsTracker()
    stats = Statistics(tracker)
    regular = RegularPayments()
    user_balance(tracker, savings, stats, regular)