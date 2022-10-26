import csv

# *Correct: если 0, то данные достоверные, 9 - данные отсутствуют
header = ['Date', 'Min', 'MinCorrect', 'Average', 'AverageCorrect', 'Max', 'MaxCorrect']

if __name__ == "__main__":
    with open('26063.dat', 'r') as file:
        stripped = (line.strip() for line in file)
        lines = (line.split(" ") for line in stripped if line)
        with open('data.csv', 'w', newline='') as output_file:
            writer = csv.writer(output_file, delimiter=',')
            writer.writerow(header)

            for line in lines:
                l = list(filter(lambda a: a != '', line))

                # минимальная температура отсутствует заполняем пустым символом
                if l[5] == '9':
                    l.insert(5, '')

                # среднесуточная температура отсутствует, пропускаем данные
                if l[7] == '9':
                    continue

                # максимальная температура отсутствует заполняем пустым символом
                if l[9] == '9':
                    l.insert(9, '')

                # если день/месяц представлены одной цифрой, добавляем ноль и сливаем дату в одну ячейку
                if len(l[2]) < 2:
                    l[2] = "0" + l[2]

                if len(l[3]) < 2:
                    l[3] = "0" + l[3]

                l[3] = ''.join(l[1:4])
                for i in range(3):
                    l.pop(0)
                l.pop(1)

                writer.writerow(l[:7])
