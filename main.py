import csv
from typing import Any
import click


@click.group()
def cli():
    pass


def read_data(file_name: Any) -> list:
    """
    Функция для чтения данных файла и внесения их в список
    """
    try:
        with open(file_name, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
            return data
    except FileNotFoundError:
        print('Файл не найден')
        return []


wallet_file = 'wallet.csv'
wallet_data = read_data(wallet_file)


def write_data(file_name: Any, data: list, writing_type: str) -> None:
    """
    Функция для добавления данных в файл
    """
    with open(file_name, writing_type, newline='', encoding='utf-8') as file:
        fieldnames = ['Дата', 'Категория', 'Сумма', 'Описание']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if writing_type == 'w':
            writer.writeheader()
            for record in data:
                writer.writerow(record)
        elif writing_type == 'a':
            writer.writerow(data[-1])


@click.argument('data', default=wallet_data, type=list)
@cli.command()
def display_balance(data: list) -> None:
    """
    Функция возвращающая баланс, расходы и доходы
    """
    total_income = 0
    total_expense = 0
    for record in data:
        if record['Категория'] == 'Доход':
            total_income += int(record['Сумма'])
        elif record['Категория'] == 'Расход':
            total_expense += int(record['Сумма'])
    balance = total_income - total_expense
    click.echo('Текущий баланс: {}.\n'
               'Доходы: {}\n'
               'Расходы: {}'.format(
                balance, total_income, total_expense))


@click.argument('file_name', default=wallet_file)
@click.argument('data', default=wallet_data, type=list)
@cli.command()
def add_record(file_name: Any, data: list) -> None:
    """
    Функция для добавления записей
    """
    date = input('Введите дату (гггг-мм-дд): ')
    category = input('Введите категорию (Доход/Расход): ').title()
    amount = int(input('Введите сумму: '))
    description = input('Введите описание: ')
    data.append({'Дата': date, 'Категория': category, 'Сумма': amount, 'Описание': description})
    write_data(file_name=file_name, data=data, writing_type='a')
    click.echo('Запись добавлена!')


@click.argument('file_name', default=wallet_file)
@click.argument('data', default=wallet_data, type=list)
@cli.command()
def edit_record(file_name: Any, data: list) -> None:
    """
    Функция для изменения данных в data[list]
    """
    index = int(input('Введите индекс записи для редактирования: '))
    if 0 <= index < len(data):
        print('Текущая запись: {}'.format(data[index]))
        field = input('Введите поле для редактирования ('
                      'Дата/Категория/Сумма/Описание'
                      '): ').title()
        if field in data[index]:
            value = input('Введите новое значение для {}: '.format(field))
            data[index][field] = value
            write_data(file_name=file_name, data=data, writing_type='w')
            click.echo('Запись успешно изменена.')
        else:
            click.echo('Некорректное поле.')
    else:
        click.echo('Некоректный индекс.')


@click.argument('data', default=wallet_data, type=list)
@cli.command()
def search_record(data: list) -> None:
    """
    Функция для поиска записей
    """
    criterion = input('Введите критерий для поиска ('
                      'Дата/Категория/Сумма/Описание'
                      '): ').title()
    category = input('Введите что искать по критерию {}: '
                     .format(criterion))
    found_records = [record for record in data
                     if record[criterion] == category]
    if found_records:
        click.echo("Найденные записи:")
        for record in found_records:
            click.echo(record)
    else:
        click.echo("Записи не найдены.")


test = click.CommandCollection(sources=[cli])

if __name__ == '__main__':
    test()
