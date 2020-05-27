import os

from subprocess import call
from argparse import ArgumentParser

PROJECT_NAME = 'spark_etl'
VESRION = 'ubuntu_18_spark_2.4'
DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

docker_run = f"""
    docker run -v "{DATA_DIR}:/tmp/data" \
    --env-file env.list \
    --network data-mng_aviation_network \
"""
docker_run_postfix = f" -it --rm {PROJECT_NAME}:{VESRION} "

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--scenario', dest='scenario', required=True, help='Сценарий работы')
    args = parser.parse_args()
    sh_command = None
    if args.scenario in ('bash', 'setup_spark', 'pyspark', 'extract_data', 'extract', 'transform'):
        sh_command = f'{docker_run} {docker_run_postfix} {args.scenario}'
    elif args.scenario == 'build':
        sh_command = f'docker build -t {PROJECT_NAME}:{VESRION} .'
    else:
        raise ValueError('Ошибочный сценарий: %s' % args.scenario)
    print(sh_command)
    call(sh_command, shell=True)