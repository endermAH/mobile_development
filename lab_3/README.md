# Использование
```bash
$ sudo pip install pdfkit
$ sudo apt-get install wkhtmltopdf
$ cd lab_1
$ ./main.py
```

# Параметры тарификатора

| Название переменной  | Тип данных | Дефолтное значение | Описание |
| ------------- | :-------------: | :-------------: | ------------- |
|outcome_limit | float | 0 | Количество минут по сниженной цене на исходящие звонки |
|income_limit | float | 50 | Количество минут по сниженной цене на входящие звонки |
|k_income_prelimit | float | 0 | Стоимость входящей минуты по сниженной цене |
|k_outcome_prelimit | float | 2 | Стоимость исходящей минуты по сниженной цене |
|k_income_postlimit | float | 1 | Стоимость входящей минуты |
|k_outcome_postlimit | float | 2 | Стоимость исходящей минуты |
|free_sms_count | int | 0 | Количество бесплатных минут |
|sms_cost | float | 1 | Стоимость sms |
|data_file_path | string | './data.csv' | Путь до файла csv |
|factor | float | 1 | Стоимость 1 Мегабайта |
|data_file_path | string | './nf_decoded' | Путь до расшифрованного файла NetFlow |

# Методы тарификатора

| Название метода  | Параметры | Описание |
| ------------- | -------------  | ------------- |
| tarificate_tel | target (string) - *тарифицируемый номер* | Тарифицировать звонки с определенного номера |
| tarificate_sms | target (string) - *тарифицируемый номер* | Тарифицировать sms с определенного номера |
| tarificate_net | target (string) - *тарифицируемый ip* | Тарифицировать трафик с определенного ip |
| generate_pdf | output(string) - *путь до результирующего pdf*, bik(string) - *БИК*, src_num(string) - *номер счета списания* ,inn(string) - *ИНН* ,kpp(string) - *КПП*, dst(string) - *номер счета для перевода*, number(string) - *номер выставленного счета*, date(string) - *дата*, customer(string) - *ФИО клиента*, tel(float) - *стоимость телефоонных звонков*, sms(float) - *стоимость смс*, net(float) - *стоимость интернет услуг* | Сгенерировать pdf счет за все услуги |

## Контакты
1. Skype: live:.cid.fc863756509c8a3d
2. Telegram: @endermah
3. Email: evg.kuryatov@gmail.com
