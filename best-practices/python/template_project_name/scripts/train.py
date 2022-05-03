from template_project_name import ROOT_DIR
from template_project_name.lightning import LightningNet, CityscapesDataModule
from template_project_name.utils import get_neptune_logger, get_tensorboard_logger, load_yaml, flatten_dict

from pytorch_lightning import seed_everything, Trainer
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint, LearningRateMonitor
from pytorch_lightning.profiler import AdvancedProfiler

import torch 
import argparse
import os
from pathlib import Path
import datetime
import shutil
import coloredlogs

coloredlogs.install()

def train(exp) -> float:
    seed_everything(42)

    ##################################################  LOAD CONFIG  ###################################################
    # ROOT_DIR is defined int template_project_name/__init__.py
    env_cfg_path = os.path.join(ROOT_DIR, "cfg/env", os.environ["ENV_WORKSTATION_NAME"] + ".yml")
    env = load_yaml(env_cfg_path)
    ####################################################################################################################

    ############################################  CREAT EXPERIMENT FOLDER  #############################################
    if exp["general"]["timestamp"]:
        timestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
        model_path = os.path.join(env["results"], exp["general"]["name"])
        p = model_path.rfind("/")+1
        model_path = model_path[:p] + str(timestamp) + "_" + model_path[p:]
    else:
        model_path = os.path.join(env["results"], exp["general"]["name"])
        if exp["general"]["clean_up_folder_if_exists"]:
            shutil.rmtree(model_path, ignore_errors=True)

    # Create the directory
    Path(model_path).mkdir(parents=True, exist_ok=True)

    # Copy config files
    exp_cfg_fn = os.path.split(exp_cfg_path)[-1]
    env_cfg_fn = os.path.split(env_cfg_path)[-1]
    print(f"Copy {env_cfg_path} to {model_path}/{exp_cfg_fn}")
    shutil.copy(exp_cfg_path, f"{model_path}/{exp_cfg_fn}")
    shutil.copy(env_cfg_path, f"{model_path}/{env_cfg_fn}")
    exp["general"]["name"] = model_path
    ####################################################################################################################

    #################################################  CREATE LOGGER  ##################################################
    if exp["logger"]["type"] == "neptune":
        logger = get_neptune_logger(
            exp=exp,
            env=env,
            exp_p=exp_cfg_path,
            env_p=env_cfg_path,
            project_name=exp["logger"]["neptune_project_name"],
        )
        exp["experiment_id"] = logger.experiment._short_id
        print("Created Experiment ID: " + str(exp["experiment_id"]))

        ex = flatten_dict(exp)
        logger.log_hyperparams(ex)
        logger._run_instance["code"].upload_files(
            [str(s) for s in Path(os.getcwd()).rglob("*.py") if str(p).find("vscode") == -1]
        )
        logger._run_instance["cfg"].upload_files([exp_cfg_path, env_cfg_path])

    elif exp["logger"]["type"] == "tensorboard":
        logger = get_tensorboard_logger(exp=exp, env=env, exp_p=exp_cfg_path, env_p=env_cfg_path)
    else:
        raise ValueError("Not defined logger type")
    
    ####################################################################################################################

    ###########################################  CREAET NETWORK AND DATASET  ###########################################
    model = LightningNet(exp, env)
    datamodule = CityscapesDataModule(env, exp["data_module"])
    ####################################################################################################################

    #################################################  TRAINER SETUP  ##################################################
    # Callbacks
    lr_monitor = LearningRateMonitor(logging_interval="step")
    cb_ls = [lr_monitor]

    if exp["cb_checkpoint"]["active"]:
        m = "/".join([a for a in model_path.split("/")])
        checkpoint_callback = ModelCheckpoint(
            dirpath=m,
            filename="Checkpoint-{epoch:02d}--{step:06d}",
            **exp["cb_checkpoint"]["cfg"],
        )
        cb_ls.append(checkpoint_callback)
    # ... add further callbacks to list

    # set gpus
    if (exp["trainer"]).get("gpus", -1) == -1:
        nr = torch.cuda.device_count()
        print(f"Set GPU Count for Trainer to {nr}!")
        for i in range(nr):
            print(f"Device {i}: ", torch.cuda.get_device_name(i))
        exp["trainer"]["gpus"] = nr

    # profiler
    if exp["trainer"].get("profiler", False):
        exp["trainer"]["profiler"] = AdvancedProfiler(output_filename=os.path.join(model_path, "profile.out"))
    else:
        exp["trainer"]["profiler"] = False

    # check if restore checkpoint
    if exp["trainer"]["resume_from_checkpoint"] is True:
        exp["trainer"]["resume_from_checkpoint"] = os.path.join(env["results_root"], exp["generatl"]["checkpoint_load"])
    else:
        del exp["trainer"]["resume_from_checkpoint"]

    trainer = Trainer(
        **exp["trainer"],
        default_root_dir=model_path,
        callbacks=cb_ls,
        logger=logger,
    )
    ####################################################################################################################

    res = trainer.fit(model, datamodule=datamodule)

    return res

if __name__ == "__main__":
    os.chdir(ROOT_DIR)
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exp",
        default="exp.yml",
        help="Experiment yaml file path relative to template_project_name/cfg/exp directory.",
    )
    args = parser.parse_args()
    exp_cfg_path = os.path.join(ROOT_DIR, "cfg/exp", args.exp)
    exp = load_yaml(exp_cfg_path)

    train(exp)
