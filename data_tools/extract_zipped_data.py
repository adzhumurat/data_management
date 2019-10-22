from argparse import ArgumentParser
import csv
import json
import os
import zipfile


class Constant:
    # путь до директории с zip-архивом
    current_script_dir = os.path.dirname(os.path.realpath(__file__))
    # ищем путь до "соседней" директории, где будем хранить данные для работы
    data_dir = os.path.join(current_script_dir, '..', 'data_store')
    # сценариии обработки данных
    extract = 'extract'
    transfom = 'transform'
    # список файлов, которые будем извлекать из архива - чтобы не извлекать ничего лишнего
    filenames = ('dogs.json', 'links.csv', 'ratings.csv', 'movies_metadata.csv', 'tags.json', )
    # директории, которые будут созданы
    raw_data_dir = 'raw_data'
    postgres_data_dir = 'pg_data'
    child_dirs = (postgres_data_dir, raw_data_dir)
    # Архив для распаковки
    zipped_data_path = os.path.join(data_dir, 'movies_data.zip')
    # отдельные константы для удобства обработки csv->json
    source_dir = os.path.join(data_dir, raw_data_dir)
    INPUT_FILE = os.path.join(source_dir, 'movies_metadata.csv')
    OUTPUT_FILE = os.path.join(source_dir, 'tags.json')
    # директория, куда распаковывать
    destination_dir = os.path.join(data_dir, raw_data_dir)
    # набор полей в csv файле
    csv_fields = (
        'adult', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id', 'imdb_id', 'original_language',
        'original_title', 'overview', 'popularity', 'poster_path', 'production_companies', 'production_countries',
        'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title', 'video', 'vote_average',
        'vote_count'
    )


def extract():
    """Функция для извлечения файлов из архива movies_data.zip

    Создаём дочерние директории и извлекаем туда файлы

    :return:
    """
    # создание дочерних директорий
    for child_dir in Constant.child_dirs:
        child_dir_path = os.path.join(Constant.data_dir, child_dir)
        if not os.path.exists(child_dir_path):
            os.mkdir(child_dir_path)
        else:
            print(f'Директория {child_dir_path} уже существует')

    # распаковываем файлы
    with zipfile.ZipFile(Constant.zipped_data_path, mode='r', compression=zipfile.ZIP_DEFLATED) as z:
        for file_name in Constant.filenames:
            z.extract(file_name, Constant.destination_dir)
    print(f'Файлы распакованы в {Constant.data_dir}/{Constant.raw_data_dir}')


def transform():
    """Трансформируем csv-файл в single-line JSON

    :return:
    """
    with open(Constant.OUTPUT_FILE, 'w') as f:
        with open(Constant.INPUT_FILE) as csvfile:
            cnt = 0
            reader = csv.DictReader(csvfile, fieldnames=Constant.csv_fields, delimiter=',')
            next(reader, None)
            for row in reader:
                content_item = {'movie_id': row['id']}
                for genre in eval(row['genres']):
                    content_item.update({'tag_id': genre['id'], 'tag_name': genre['name']})
                    f.write(json.dumps(content_item) + '\n')
                    cnt += 1
    print(f'Данные из {Constant.INPUT_FILE} записаны в выходной файл {Constant.OUTPUT_FILE} в количестве {cnt} строк')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--scenario', dest='scenario', required=True, help='Сценарий: extract, transform')
    args = parser.parse_args()
    if args.scenario == Constant.extract:
        extract()
    elif args.scenario == Constant.transfom:
        transform()
