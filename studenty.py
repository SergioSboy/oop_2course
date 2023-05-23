# открываем файл на чтение
import csv


def getFile(filename):
    f = open(filename, 'r')
    return csv.DictReader(f, delimiter=';')

def getGeneralStatement(filename):
    """Общая ведомость"""

    reader = getFile(filename)
    result = ''
    if reader:
        result = f"{'№':5} ФИО\n_________________________________________________________\n"  # заголовок данных

        for row in reader:
            result += f"{row['ID']:5}" + row['Name'] + '\n'

    return result


def getStudentById(filename, id):
    """Справка о студенте по номеру зачетки"""
    reader = getFile(filename)
    result = ''
    if (id and reader):
        for row in filter(lambda d: int(d['ID']) == (id), reader):
            result = 'Номер зачетки:                  {0}\n' \
                     'ФИО:                            {1}\n' \
                     'Номер варианта:                 {2}\n' \
                     'Отметка о выполнении задания 1: {3}\n' \
                     'Отметка о выполнении задания 2: {4}\n' \
                     'Отметка о выполнении задания 3: {5}\n'.format(row['ID'], row['Name'], row['Variant'], row['R1'],
                                                                    row['R2'], row['R3'])

    return result


def getTaskByNumber(filename, task_number):
    """Ведомость о выполнении студентами задания с указанным номером """
    reader = getFile(filename)
    result = ''
    if reader and task_number:
        result = f"{'Номер':5} {'ФИО':30} {'Оценка':5}\n"  # заголовок данных
        for row in filter(lambda d: int(d['T' + str(task_number)]) == 1, reader):
            result += f'{row["ID"]:5} {row["Name"]:30} {row["R" + str(task_number)]}\n'

    return result


def getStudentListBySum(filename, variant:int, sum:int):
    """Список студентов с заданным номером варианта, имеющих заданную сумму баллов по всем 3 задачам """
    reader = getFile(filename)
    result = ''
    # print(variant)
    # print(sum)
    if reader and variant and sum:
        result = f"{'Номер':5} {'ФИО':50} {'Задание1':8} {'Задание2':8} {'Задание3':8}\n"  # заголовок данных
        for row in filter(lambda d: (int(d['Variant']) == variant and (int(d['R1']) + int(d['R2']) + int(d['R3'])) >= sum), reader):
            # print(row["ID"])
            result += f'{row["ID"]:5} {row["Name"]:50} {int(row["R1"]):8} {int(row["R2"]):8} {int(row["R3"]):8}\n'
    # print(result)
    return result


def getStudentListNotTaskByNumber(filename, task_number: str):
    """Список студентов, не получивших задание с указанным номером """
    reader = getFile(filename)
    result = ''

    # print(task_number)
    # print(reader)
    if reader and task_number:
        result += f"{'Номер':5} {'ФИО':50}\n"  # заголовок данных
        for row in filter(lambda d: int(d[f'T{task_number}']) == 0, reader):
            result += f'{row["ID"]:5} {row["Name"]:50}\n'
    # print(result)
    return result

# with open('C:\\repos\\test\\study.dat', 'r') as f:
#     reader = csv.DictReader(f, delimiter=';')
#     getStudentListNotTaskByNumber(reader, str(1))
