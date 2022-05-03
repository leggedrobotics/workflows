from pytorch_lightning.loggers.neptune import NeptuneLogger
from pytorch_lightning.loggers import TensorBoardLogger
import os

from template_project_name.utils import flatten_dict
from template_project_name import ROOT_DIR

__all__ = ["get_neptune_logger", "get_tensorboard_logger"]


def log_important_params(exp):
    dic = {}
    dic = flatten_dict(exp)
    return dic


def get_neptune_logger(exp, env, exp_p, env_p, project_name="jonasfrey96/asl"):
    params = log_important_params(exp)

    name_full = exp["general"]["name"]
    name_short = "__".join(name_full.split("/")[-2:])

    if os.environ["ENV_WORKSTATION_NAME"] == "euler":
        proxies = {"http": "http://proxy.ethz.ch:3128", "https": "http://proxy.ethz.ch:3128"}
        return NeptuneLogger(
            api_key=os.environ["NEPTUNE_API_TOKEN"],
            project=project_name,
            name=name_short,
            tags=[os.environ["ENV_WORKSTATION_NAME"], name_full.split("/")[-2], name_full.split("/")[-1]],
            proxies=proxies,
        )

    return NeptuneLogger(
        api_key=os.environ["NEPTUNE_API_TOKEN"],
        project=project_name,
        name=name_short,
        tags=[os.environ["ENV_WORKSTATION_NAME"], name_full.split("/")[-2], name_full.split("/")[-1]],
    )


def get_tensorboard_logger(exp, env, exp_p, env_p):
    params = log_important_params(exp)
    return TensorBoardLogger(save_dir=exp["name"], name="tensorboard", default_hp_metric=params)
