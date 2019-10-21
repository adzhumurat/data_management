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
        z.extract(file_name, os.path.join(data_dir, 'raw_data', file_name))
print(f'Файлы распакованы в {data_dir}/raw_data')
