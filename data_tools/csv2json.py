import os
import csv
import json

source_dir = os.getenv('SOURCE_DATA')
INPUT_FILE = f'{source_dir}/raw_data/movies_metadata.csv'
OUTPUT_FILE = f'{source_dir}/raw_data/tags.json'

fields = (
    'adult', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id',
    'imdb_id', 'original_language', 'original_title', 'overview',
    'popularity', 'poster_path', 'production_companies',
    'production_countries', 'release_date', 'revenue', 'runtime',
    'spoken_languages', 'status', 'tagline', 'title', 'video',
    'vote_average', 'vote_count'
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
print('Данные в выходной файл записаны %d строк' % cnt)
