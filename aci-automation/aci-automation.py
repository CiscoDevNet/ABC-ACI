import os
import sys
import yaml
import argparse
import logging
import logging.handlers as handlers
import os
import argparse
import json
import glob
import subprocess

class CustomFormatter(logging.Formatter):
    def __init__(self, patterns=[], fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.patterns = patterns

    def format(self, record: logging.LogRecord):
        res = super(CustomFormatter, self).format(record)
        for pattern in self.patterns:
            res = res.replace(pattern, "*******")
        return res

def default(name, level="INFO", patterns=[], logfile=None):
    ch = logging.StreamHandler()
    custom_formatter = CustomFormatter(patterns=patterns, fmt="[%(asctime)s] [%(levelname)8s] (%(filename)s:%(lineno)s) --- %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    ch.setLevel(level)
    logger = logging.getLogger(name)
    logger.handlers = []
    ch.setFormatter(custom_formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    if not logfile == None:
        # 100 MB Log Files
        rfh = handlers.RotatingFileHandler(logfile, mode='a+',maxBytes=104857600, backupCount=2)
        rfh.setLevel(logging.DEBUG)
        rfh.setFormatter(custom_formatter)
        logger.addHandler(rfh)
    return logger

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='aci-automation')
    parser.add_argument('--log', default="DEBUG")
    parser.add_argument('--tenants_dir', default="tenants")
    parser.add_argument('--actions_dir', default="actions")
    parser.add_argument('--env_file', default="env.yml")
    parser.add_argument('--inventory_file', default="inventory")
    parser.add_argument('--path', default='./')
    args = parser.parse_args()
    logger = default("aci-basics", level=args.log)

    path = os.path.abspath(args.path)
    env_file = os.path.abspath(args.env_file)
    inventory_file = os.path.abspath(args.inventory_file)
    
    tenant_info = dict()
    # action =  None

    for filename in glob.iglob(path + f'/{args.tenants_dir}/**', recursive=True):
        environments = []
        # action_key = None
        if not os.path.isdir(filename):
            logger.debug("processing file " + filename)
            with open(filename) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                for item in data["items"]:
                    env_data = dict()
                    for key in item.keys():
                        env_data.setdefault(f'apic_{key}', item[key])
                    environments.append(env_data)
                
                action = data["action"]
                logger.debug("environments action=%s json=%s", action, environments)
                if action not in tenant_info:
                    tenant_info[action] = environments
                else:
                    tenant_info[action] = tenant_info[action] + environments
    with open(env_file, 'w') as f:
        logger.debug("writing env_file=%s", env_file)
        f.write(yaml.dump(tenant_info))

    for filename in glob.iglob(path + f'/{args.actions_dir}/**', recursive=True):
        if not os.path.isdir(filename):
            normalize_action_name = os.path.basename(filename).replace(".yml", "").replace("-", "_")
        
            logger.debug("processing action=%s file=%s", normalize_action_name, filename)
            cmd = ['ansible-playbook', '-i', f'{inventory_file}', f'{filename}', "--extra-vars", f'@{env_file}']
        
            logger.debug("running cmd='%s'", ' '.join(cmd))
            for path in execute(cmd):
                print(path, end="")
