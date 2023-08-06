import os
import json
import click
import requests

def read_config(config_file):
    config = json.loads(config_file.read())

    # Rudimentary support for pulling config from env vars
    for key, value in config.items():
        if value.startswith("${"):
            var_name = value[2:-1]
            config[key] = os.environ.get(var_name, None)
            print("Replaced %s with %s" % (key, config[key]))
    return config

@click.command()
@click.argument('code_file', type=click.File('rb'))
@click.argument('inputs_file', type=click.File('rb'))
@click.argument('config_file', type=click.File('rb'))
def cli(code_file, inputs_file, config_file):
    config = read_config(config_file)

    submit_url = os.path.join(config['base_url'], "submit_job_token/")

    payload = {
        'ghap_credentials': {
            'username': config['ghap_username'],
            'password': config['ghap_password'],
            'ip': config['ghap_ip']
        },
        'inputs': json.loads(inputs_file.read()),
        'backend': 'ghap',
        'code': code_file.read().decode('utf-8')
    }

    response = requests.post(submit_url, json=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': config['token'],
    })

    print(response)