# data_management

Перед началом работы

```shell
python3 upstart.py -s prepare_dirs
```

## Курс "Управление данными"

Узнаём про различные форматы хранения и СУБД. Пишем много SQL

* [Введение в курс]
    * [Видео](https://youtu.be/XIclsB6sui0?t=539)
    * [Слайды](https://docs.google.com/presentation/d/1dA8uWlMzBoTOqQCDNzTsKszZt1UgmeGdQYnlSSenV4w/edit?usp=sharing)
* [Подготовка машины к работе](./slides/env_start_up.md)
    * [Видео](https://youtu.be/1iwA1_Ss7jA)
    * [Туториал по технологии docker](https://github.com/aleksandr-dzhumurat/workshop_docker_beginner)
* [Ведение в базы данных](./slides/database_intro.md)
    * [Видео](https://youtu.be/jAhI5ZawKxI)
* [Язык запросов SQL](./slides/sql_language.md)
    * [Видео ч.1: Реляционная алгебра](https://youtu.be/9SjVtiT4kgg)
    * [Видео ч.2: Простые операторы SQL + Pandas](https://youtu.be/qdrkKnDURP8)
    * [Домашняя работа: создание и модификация таблиц](./slides/hw/hw1.md)
    * [Домашняя работа: SQL запросы](./slides/hw/hw2.md)
* [Работа с Postgres](./slides/postgres_db.md)
    * [Слайды](https://docs.google.com/presentation/d/1328oFuAQfOWH8EWC4MGwfzxc0XUfdXN6Ne1cn9Ry4tY/edit?usp=sharing)
* [Нереляционные СУБД: MongoDB](./slides/mongo_db.md)
    * [Домашняя работа: работа с MongoDB](./slides/hw/hw2.md)
* [Данные для рекомендательных систем](https://github.com/aleksandr-dzhumurat/recsys_workshop/blob/main/recsys_demo_workshop.ipynb)
    * [Видео](https://www.youtube.com/watch?v=P7sgVvkpK7A&t=71s)
    * [Слайды](https://docs.google.com/presentation/d/1VjRdKM_pnROd83Obeav2mHnAWQMl9THooxbGfIWDP30/edit?usp=sharing)


## Курс "Анализ данных"

Учимся извлекать из данных пользу

![slides/img/ivi_logo.png](slides/img/ivi_logo.png)


* [Вспоминаем тервер и матстат](./jupyter_notebooks/I_probability.ipynb)
    * [Домашняя работа: задачки по терверу](./jupyter_notebooks/I_probability_hw_1_proba.ipynb)
    * [Домашняя работа: наивный байесовский классификатор](./jupyter_notebooks/I_probability_hw_2_naive_bayes.ipynb)
    * [Домашняя работа: проверка статистических гипотез](./jupyter_notebooks/I_probability_hw_3_stat.ipynb)
    * [Видео: введение в теорию вероятностей](https://www.youtube.com/watch?v=KPdBdblatC4)
    * [Видео: как считать retention](https://www.youtube.com/watch?v=Nds_9ZTihIY)
    * [Видео: домашка по Naive bayes. Метод fit](https://youtu.be/OYmha7NDsuA)
    * [Видео: домашка по Naive bayes. Метод predict](https://youtu.be/imhuUiodhL4)
* [Введение в ML](./jupyter_notebooks/II_machine_learning_intro.ipynb)
    * [Домашняя работа: обучаем линейную регрессию](./jupyter_notebooks/II_machine_learning_intro_hw.ipynb)
    * [Видео: основные понятия ML](https://youtu.be/mrI-k8ItnOY)
    * [Видео: жизненный цикл ML проекта, CRISP-DM](https://youtu.be/DnGtiUzn-9k)
* [Машинное обучение с учителем](./jupyter_notebooks/III_machine_learning_supervised.ipynb)
    * [Домашняя работа: выбираем лучший классификатор](./jupyter_notebooks/III_machine_learning_supervised_hw.ipynb)
    * [Видео: машинное обучение с учителем](https://youtu.be/05KpKpAKOus)
* [Машинное обучение без учителя](./jupyter_notebooks/IV_machine_learning_unsupervised.ipynb)
    * [Домашняя работа: выбираем применяем снижение размерности](./jupyter_notebooks/IV_machine_learning_unsupervised_hw.ipynb)
	* [Видео: машинное обучение без учителя](https://youtu.be/COcSkDuVU1g)
* [Методы обучения моделей: регуляризация, градиентный спуск](./jupyter_notebooks/V_machine_learning_tuning.ipynb)
    * [Домашняя работа: реализуем градиентный спуск с регуляризацией](./jupyter_notebooks/V_machine_learning_tuning.ipynb)
    * [Видео: регуляризация](https://youtu.be/cIa3ogbF9TY)
    * [Видео: градиентный спуск](https://youtu.be/9f1B_D5K_9o)
    * [Видео: инжениринг фичей](https://youtu.be/d5TjzF_MNWo)
* [Машинное обучение в продакшн. Рекомендательные системы](./jupyter_notebooks/VI_machine_learning_production.ipynb)
    * [Домашняя работа: изучаем пакет implicit в задаче построения рекомендательных систем](./jupyter_notebooks/VI_machine_learning_production.ipynb)
    * [Видео: метрики ML сервиса](https://youtu.be/XYiC9tgnebk)
    * [Видео: Docker для ML сервиса](https://youtu.be/K37RlsZhH8s)
    * [Видео: рекомендательные системы]( https://youtu.be/PwIYGIfwvWo)
