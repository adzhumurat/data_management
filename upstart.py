import os
from argparse import ArgumentParser
from subprocess import call

PROJECT_NAME = 'data-mng'
MAIN_SERVICE_NAME = 'service-app'
# переменная среды SOURCE_DATA используется в docker-compose
os.environ['SOURCE_DATA'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_store')
os.environ['JUPYTER_NOTEBOOKS'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jupyter_notebooks')
SPARK_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'spark_example')

docker_compose = f"""docker-compose --project-name {PROJECT_NAME} -f docker_compose/docker-compose.yml \
"""
docker_compose_postfix = f" --rm --name {PROJECT_NAME} {MAIN_SERVICE_NAME} "
simple_run = f'{docker_compose} run {docker_compose_postfix}'

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--scenario', dest='scenario', required=True, help='Сценарий работы')
    args = parser.parse_args()
    if args.scenario in ('bash', ):
        sh_command = f'{simple_run} {args.scenario}'
    elif args.scenario == 'mongo':
        sh_command = f'{docker_compose} run {docker_compose_postfix} "/usr/bin/mongo" mongo_host:27017'
    elif args.scenario == 'mongoimport':
        sh_command = f'{docker_compose} run {docker_compose_postfix} "/usr/bin/mongoimport" --host mongo_host --port 27017 --db movie --collection tags --file /usr/share/data_store/raw_data/tags.json'
    elif args.scenario == 'load':
        sh_command = f'{docker_compose} run {docker_compose_postfix} "pipenv" run python3 scripts/load_data.py -s load'
    elif args.scenario == 'psql':
        sh_command = f'{docker_compose} run {docker_compose_postfix} "psql" -h postgres_host -U postgres'
    elif args.scenario == 'test':
        sh_command = f'{docker_compose} run {docker_compose_postfix} "pipenv" run python3 scripts/load_data.py -s row_count'
    elif args.scenario == 'down':
        sh_command = f'{docker_compose} {args.scenario}'
    elif args.scenario == 'service':
        sh_command = f'{docker_compose} run -d -p 5001:5000 {docker_compose_postfix} "pipenv" run python3 app/simple_service.py'
    elif args.scenario == 'jupyter':
        sh_command = f'{docker_compose} run -p 8889:8888 --rm --name {PROJECT_NAME}_jupyter jupyter-app {args.scenario}'
    elif args.scenario == 'spark-jupyter':
        sh_command = f'docker run -p 8890:8888 -v "{SPARK_DIR}:/home/jovyan/work" jupyter/pyspark-notebook:45bfe5a474fa'
    else:
        raise ValueError('Ошибочный сценарий: %s' % args.scenario)
    print(sh_command)
    call(sh_command, shell=True)
