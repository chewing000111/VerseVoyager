import json
import yaml
from munch import DefaultMunch


def load_yaml(path, encoding="utf-8-sig"):
    with open(path, "r", encoding=encoding) as f:
        return DefaultMunch.fromDict(yaml.load(f.read(), yaml.Loader))


def load_json(path, encoding="utf-8-sig"):
    with open(path, "r", encoding=encoding) as f:
        return json.load(f)

def save_json(data, path, encoding="utf-8-sig", ensure_ascii=False):
    with open(path, "w", encoding=encoding) as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=ensure_ascii))