import csv
import json
import os
import zipfile

# путь до директории с zip-архивом
current_script_dir = os.path.dirname(os.path.realpath(__file__))
# ищем путь до "соседней" директории, где будем хранить данные для работы
data_dir = os.path.join(current_script_dir, '..', 'data_store')
# список файлов, которые будем извлекать из архива
filenames = (
    'dogs.json',
    'links.csv',
    'ratings.csv',
    'movies_metadata.csv',
)
child_dirs = ('pg_data', 'raw_data')

# создание дочерних директорий
for child_dir in child_dirs:
    child_dir_path = os.path.join(data_dir, child_dir)
    if not os.path.exists(child_dir_path):
        os.mkdir(child_dir_path)
    else:
        print(f'Директория {child_dir_path} уже существует')

# распаковываем файлы
zip_file_name = 'movies_data.zip'
zipped_data_path = os.path.join(data_dir, zip_file_name)
with zipfile.ZipFile(zipped_data_path, mode='r', compression=zipfile.ZIP_DEFLATED) as z:
    for file_name in filenames:
        z.extract(file_name, os.path.join(data_dir, 'raw_data'))
print(f'Файлы распакованы в {data_dir}/raw_data')

# выполняем препроцессинг csv->json
source_dir = os.path.join(data_dir, 'raw_data')
INPUT_FILE = os.path.join(source_dir, 'movies_metadata.csv')
OUTPUT_FILE = os.path.join(source_dir, 'tags.json')

fields = (
    'adult', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id', 'imdb_id', 'original_language',
    'original_title', 'overview','popularity', 'poster_path', 'production_companies', 'production_countries',
    'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title', 'video', 'vote_average', 'vote_count'
)

with open(OUTPUT_FILE, 'w') as f:
    with open(INPUT_FILE) as csvfile:
        cnt = 0
        reader = csv.DictReader(csvfile, fieldnames=fields, delimiter=',')
        next(reader, None)
        for row in reader:
            content_item = {'movie_id': row['id']}
            for genre in eval(row['genres']):
                content_item.update({'tag_id': genre['id'], 'tag_name': genre['name']})
                f.write(json.dumps(content_item)+'\n')
                cnt += 1
print(f'Данные из {INPUT_FILE} записаны в выходной файл {OUTPUT_FILE} в количестве {cnt} строк')
