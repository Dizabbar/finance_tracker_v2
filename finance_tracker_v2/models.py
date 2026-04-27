from abc import ABC, abstractmethod
import json
import datetime


class Record(ABC):
    """
    Абстрактный базовый класс для всех видов финансовых записей.

    Определяет интерфейс, который должны реализовать все конкретные типы записей:
        - Сериализация в словарь для сохранения в JSON.
        - Десериализация из словаря при загрузке данных.
    """
    
    @abstractmethod
    def to_dict(self) -> dict:
        """
        Преобразует объект записи в словарь для последующего сохранения в JSON.
        """
       
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'Record':
        """
        Создаёт объект записи из словаря загруженного из JSON
        """
        pass


class BaseStorage():  
    """
    Базовый класс для хранилищ записей, реализующий общую логику работы с JSON-файлами.

    Атрибуты:
        filename (str): путь к JSON-файлу хранилища.
        record_class (type): класс записей, которые хранятся в этом хранилище (например, FinanceRecord).
        records (list): список загруженных объектов записей.
    """
    
    def __init__(self, filename:str, record_class:type[Record]) -> None:
        self.filename = filename
        self.record_class = record_class
        self.records = self._load()
    
    def _load(self) -> list[Record]:
        """
        Загружает записи из JSON-файла. Если файл отсутствует или повреждён, возвращает пустой список.
        """
       
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

                return [self.record_class.from_dict(item) for item in data]

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self) -> None:
        """Сохраняет текущий список записей в JSON-файл."""

        data = [r.to_dict() for r in self.records]

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add(self, record: Record) -> str:
        """
        Добавляет новую запись в хранилище и сохраняет изменения в файл.
        """

        self.records.append(record)

        self._save()

    def remove(self, index: int) -> str:
        """
        Удаляет запись по её индексу в списке records.
        """

        if 0 <= index < len(self.records):
            del self.records[index]
            self._save()
        
            return f'Транзакция с ID - {index} успешно удалена'  
        
        return 'Не коректное значение или не существуюший ID'

    def search_transactions_date(self, date_left: str, date_right: str) -> str:
        """
        Выводит записи, даты которых попадают в заданный диапазон (включительно).

        Аргументы:
            date_left (str): начальная дата диапазона.
            date_right (str): конечная дата диапазона.
        """

        for trans in range(len(self.records)):
            if self.records[trans].date == date_left:
                print(self.records[trans])
           
            elif trans.date == date_right and trans == len(self.records) - 1:
                break
            
            else:
                return 'Вы ввели не коректную дату'
            
    def all_trans(self) -> str:
        """Возвращает строковое представление всех записей."""
        if len(self.records) != 0: 
            return '\n'.join(str(record) for record in self.records)
        
        else:
            return 'Транзакций не найдено'

class FinanceRecord(Record):
    """Запись об финансовой транзакции."""

    INCOME = 'income'   
    EXPENSE = 'expense' 
    TRANSFER_TO_SAVINGS = 'transfer_to_savings' 
    TRANSFER_FROM_SAVINGS = 'transfer_from_savings'

    def __init__(self, amount: int, date: str, operation_type: str, 
                 description: str, idx: int) -> None:
        self.amount = amount
        self.date = date
        self.operation_type = operation_type   
        self.description = description
        self.idx = idx

    def to_dict(self) -> dict:
        return {
            'amount': self.amount,                           
            'date': self.date,
            'operation_type': self.operation_type,
            'description': self.description,
            'idx': self.idx
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'FinanceRecord':
        return cls(
            amount=data['amount'],
            date=data['date'],
            operation_type=data['operation_type'],
            description=data['description'],
            idx = data['idx']
        )

    def __str__(self):
        
        return ( 
            f'\nТип операции: {self.operation_type}  Сумма операции {self.amount} руб'
            f'-Дата:{self.date} - Описание {self.description} - ID {self.idx}'
        )

    def __repr__(self):

        return self.__str__()
  

class SavingsRecord(Record): 
    """Запись об операции с накоплениями."""
    
    DEPOSIT = "deposit"    
    WITHDRAWAL = "withdrawal" 
    TRANSFER_TO_FINANCE = 'transfer_to_finance'
    TRANSFER_FROM_FINANCE = 'transfer_from_finance'
    
    def __init__(self, amount: int, date: str, operation_type: str,
                description: str, idx: int) -> None:
        self.amount = amount
        self.date = date
        self.operation_type = operation_type   
        self.description = description
        self.idx = idx    

    def to_dict(self) -> dict:
        return {
            'amount': self.amount,
            'date': self.date,
            'operation_type': self.operation_type,
            'description': self.description,
            'idx': self.idx
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SavingsRecord':
        return cls(
            amount=data['amount'],
            date=data['date'],
            operation_type=data['operation_type'],
            description=data['description'],
            idx = data['idx']
        )

    def __str__(self):
        
        return ( 
            f'\nТип операции: {self.operation_type}  Сумма операции {self.amount} руб'
            f'-Дата:{self.date} - Описание {self.description} - ID {self.idx}'
        )

    def __repr__(self):

        return self.__str__()


class RegularRecord(Record):
    """Регулярная (повторяющаяся) операция."""

    EXPENSE_REGULAR = 'regular_expense'             
    INCOME_REGULAR = 'regular_income'       

    def __init__(self, amount: int, month_day: str, operation_type: str, 
                 description: str, idx: int, last_processed='None') -> None:
        self.amount = amount
        self.month_day = month_day
        self.operation_type = operation_type
        self.description = description
        self.idx = idx
        self.last_processed = last_processed

    def to_dict(self) -> dict:
        return {
            'amount': self.amount,
            'month_day': self.month_day,
            'operation_type': self.operation_type,
            'description': self.description ,
            'idx': self.idx,
            'last_processed': self.last_processed
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RegularRecord':
        return cls(
            amount = data['amount'],
            month_day = data['month_day'],
            operation_type = data['operation_type'],
            description = data['description'],
            idx = data['idx'],
            last_processed = data['last_processed'] 
        )

    def __str__(self):
        
        return ( 
            f'\nТип операции: {self.operation_type}  Сумма операции {self.amount} руб'
            f'-Дата:{self.month_day} - Описание {self.description} - ID {self.idx}'
        )

    def __repr__(self):

        return self.__str__()


class FinanceTracker(BaseStorage):
    """Хранилище для финансовых транзакций"""
    
    def __init__(self, filename='finance_transactions.json') -> None:
        super().__init__(filename, FinanceRecord)
    
    def get_balance(self) -> str:  
        """Рассчитывает текущий баланс на основе всех транзакций"""

        balance = 0
        # Операции, увеличивающие баланс (доходы, регулярные доходы, переводы из накоплений)
        profitable_operations = ['income', 'regular_income', 'transfer_from_savings' ] 

        for t in self.records:
            if t.operation_type in profitable_operations:
                balance += t.amount

            else:
                balance -= t.amount
    
        return f'На вашем счету {balance} руб'



class SavingsTracker(BaseStorage):
    """Хранилище для записей о сбережениях"""

    def __init__(self, filename='savings_transactions.json'):
        super().__init__(filename, SavingsRecord)

    def transfer_to_finance_tracker(self, amount: int, date: str, 
                                    description: str, finance_tracker: FinanceTracker, idx: int) -> None:
        """
           Переводит средства из накоплений в основной баланс.

           Создаёт:
               - Доходную транзакцию в FinanceTracker (использует переданный idx).
               - Расходную запись в SavingsTracker.

           Почему для SavingsRecord используется idx = len(self.records), а не переданный idx?
               - Параметр idx, переданный из меню, вычисляется как len(tracker.records)
                 и предназначен для обеспечения уникальности ID в FinanceTracker.
               - У SavingsTracker свой собственный список записей (self.records),
                 и нумерация в нём не зависит от FinanceTracker.
               - Использование len(self.records) гарантирует, что новая запись в SavingsTracker
                 получит следующий по порядку ID внутри этого хранилища, без пропусков и дубликатов.
               - Если бы мы передали сюда тот же idx, что и в FinanceTracker, то:
                  * при несовпадении длин списков могли бы возникнуть дубликаты ID в SavingsTracker;
                  * нарушилась бы логика последовательной нумерации в каждом хранилище.
        """
        
        income = SavingsRecord(amount, date, FinanceRecord.TRANSFER_FROM_SAVINGS,
                               description, idx)
        finance_tracker.add(income)
        
        withdral = SavingsRecord(amount, date, SavingsRecord.TRANSFER_TO_FINANCE,
                                 description, idx=len(self.records))
        self.add(withdral)

    def transfer_from_finance_tracker(self,amount: int, date: str, description: str, 
                                      finance_tracker: FinanceTracker, idx: int) -> None:
        """
          Переводит средства из основного баланса в накопления.

          Создаёт:
              - Расходную транзакцию в FinanceTracker (использует переданный idx).
              - Доходную запись в SavingsTracker.

          Почему idx для SavingsRecord вычисляется как len(self.records) — см. пояснение в методе
          transfer_to_finance_tracker (причины те же: независимая нумерация в разных хранилищах,
          избежание коллизий и сохранение последовательности ID).
        """
    
        expense = SavingsRecord(amount, date, FinanceRecord.TRANSFER_TO_SAVINGS,
                                description, idx)
        finance_tracker.add(expense)
        
        deposit = SavingsRecord(amount, date, SavingsRecord.TRANSFER_FROM_FINANCE, 
                                description, idx=len(self.records))
        self.add(deposit)

    def balance_savings(self) -> str:
        """
        Рассчитывает текущий баланс сбережений.
        """
        
        balance = 0
        # Операции, увеличивающие баланс (доходы, регулярные доходы, переводы из накоплений)
        profitable_operations = ['deposit', 'transfer_from_finance']
        
        for r in self.records:
            if r.operation_type in profitable_operations:
                balance += r.amount

            else:
                balance -= r.amount    
        
        return f'Ваш баланс сбережений: {balance} руб'


class RegularPayments(BaseStorage):
    """
    Хранилище регулярных платежей.
    """

    def __init__(self, filename='regular_payments.json') -> None:
        super().__init__(filename, RegularRecord)

        self.check_today = str(datetime.date.today())

    def сheck_regular_trans(self, tracker: FinanceTracker) -> str: 
        """
        Проверяет все регулярные записи и при необходимости добавляет соответствующие транзакции.

        Транзакция добавляется, если:
            - Сегодняшняя дата совпадает с датой регулярной записи (rec.today).
            - Эта запись ещё не была обработана сегодня (last_processed != today).

        После добавления поле last_processed обновляется, и изменения сохраняются в файл.
        """
        today_md = datetime.date.today().strftime("%d")
        today = str(datetime.date.today())
        print(today,today_md)
        

        for rec in self.records:
            if (rec.month_day == today_md 
                and rec.last_processed != today
                and rec.operation_type == 'regular_expense'):
     
                tracker.add(FinanceRecord(rec.amount, today,
                                          RegularRecord.EXPENSE_REGULAR, rec.description,idx=len(self.records)))
                rec.last_processed = today

                print(f'Зачисленна регулярная операция. Описание: {rec.description}')     

            elif (rec.month_day == today_md 
                  and rec.last_processed != today 
                  and rec.operation_type == 'regular_income'):

                tracker.add(FinanceRecord(rec.amount, today,
                                          RegularRecord.INCOME_REGULAR, rec.description,idx=len(self.records)))
                rec.last_processed = today                                               

                print(f'Зачисленна регулярная операция. Описание: {rec.description}')

            self._save()


class Statistics:
    """Класс для получения статистики по финансовым транзакциям за определённый месяц."""

    def __init__(self, finance_tracker: FinanceTracker) -> None:
        self.tracker = finance_tracker   

    def filter_by_month(self, year_month: str) -> list:
        """
        Возвращает список транзакций, относящихся к заданному месяцу."""

        result = []

        for t in self.tracker.records:
            if t.date.startswith(year_month):
                result.append(t)
        return result

    def stats_procent(self, year_month) -> str:
        """
        Выводит процентное распределение расходов по категориям (типам операций) за месяц.

        Для каждой категории рассчитывается доля от общей суммы расходов и отображается
        текстовой полосой из символов '|'
        """

        transactions = self.filter_by_month(year_month)
        total = sum(t.amount for t in transactions)

        if total == 0:
            return f'Транзакций за дату {year_month} не было'

        categories = {}

        for t in transactions:
            cat = t.operation_type
            categories[cat] = categories.get(cat, 0) + t.amount

        sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)

        for cat, amount in sorted_cats:
            procent = (amount / total) * 100
            bar = '|' * int(procent // 5)

            print(f'{cat:15} {amount:7} руб {bar} {procent:.1f}%')





    