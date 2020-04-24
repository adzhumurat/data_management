import os
from argparse import ArgumentParser
from subprocess import call

PROJECT_NAME = 'data-mng'
MAIN_SERVICE_NAME = 'service-app'
# переменная среды SOURCE_DATA используется в docker-compose
os.environ['SOURCE_DATA'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data_store')
os.environ['JUPYTER_NOTEBOOKS'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jupyter_notebooks')

docker_compose = f"""docker-compose --project-name {PROJECT_NAME} -f docker_compose/docker-compose.yml \
"""
docker_compose_postfix = f" --rm --name {PROJECT_NAME} {MAIN_SERVICE_NAME} "
simple_run = f'{docker_compose} run {docker_compose_postfix}'

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--scenario', dest='scenario', required=True, help='Сценарий работы')
    args = parser.parse_args()
    if args.scenario in ('pipenv', 'bash', 'psql', 'load', 'test', 'mongo', 'mongoimport'):
        sh_command = f'{simple_run} {args.scenario}'
    elif args.scenario == 'down':
        sh_command = f'{docker_compose} {args.scenario}'
    elif args.scenario == 'jupyter-full':
        sh_command = f'{docker_compose} run -d -p 8889:8888 {docker_compose_postfix} {args.scenario}'
    elif args.scenario == 'jupyter':
        sh_command = f'{docker_compose} run -d -p 8889:8888 --rm --name {PROJECT_NAME}_jupyter jupyter-app {args.scenario}'
    elif args.scenario == 'service':
        sh_command = f'{docker_compose} run -d -p 5001:5000 {docker_compose_postfix} {args.scenario}'
    elif args.scenario == 'docker':
        sh_command = f'{docker_compose} build {MAIN_SERVICE_NAME}'
    elif args.scenario == 'docker-jupyter':
        sh_command = f'{docker_compose} build jupyter-app'
    else:
        raise ValueError('Ошибочный сценарий: %s' % args.scenario)
    print(sh_command)
    call(sh_command, shell=True)
