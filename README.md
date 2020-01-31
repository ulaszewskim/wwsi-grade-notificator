# WWSI Grade Notificator
Intended to WWSI (Warsaw School of Computer Science) students. Checks for new grades and sends results by mail.

## General information:
This program checks your grades at *student.wwsi.edu.pl/oceny* and sends email message with detected changes.

## Example output
```
WWSI Grade Notificator has detected changes in your grades:
+-----+---------+------------------------------------------------+-------+------------+-------------------------+
|     | Semestr |                   Przedmiot                    | Ocena |    Data    |        Wykładowca       |
+-----+---------+------------------------------------------------+-------+------------+-------------------------+
| NEW |    3    |            Systemy mobilne (Wykład)            |  4.5  | 2020-01-25 |  dr inż. XXXX XXXXXXXX  |
| OLD |    3    |            Systemy mobilne (Wykład)            |       |            |                         |
|     |         |                                                |       |            |                         |
| NEW |    2    | Zaawansowane systemy baz danych (Laboratorium) |   5   | 2019-06-16 |    dr inż. YYY YYYYY    |
| OLD |    2    | Zaawansowane systemy baz danych (Laboratorium) |   4   | 2019-06-10 |    dr inż. YYY YYYYY    |
|     |         |                                                |       |            |                         |
+-----+---------+------------------------------------------------+-------+------------+-------------------------+
```


## How to use:
1.	Change variables in **grade_notificator.py**:<br>
    - `wwsi_login` - your WWSI login<br>
    - `wwsi_password` - your WWSI password<br>
    - `source_email` - email account that program will use to send mail. must be GMAIL<br>
    - `source_password` - password to this account<br>
    - `target_email` - email that program will send messages to<br>
     - `check_every_x_minutes` - how often program must refresh website for changes<br>
2.	Turn on [less secure apps access](https://support.google.com/accounts/answer/6010255?hl=en) for `source_email`.
3.	Run `grade_notificator.py`.
