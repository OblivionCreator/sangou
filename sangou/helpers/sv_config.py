import yaml
import shutil
import copy
import json
import os

server_data = "data/servers"
with open("assets/config.example.yml", "r") as f:
    stock_config = yaml.safe_load(f)

model_config = {
    "logging": {
        "modlog": "channelid",
        "serverlog": "channelid",
        "userlog": "channelid",
    },
    "staff": {
        "adminrole": "roleid",
        "modrole": "roleid",
        "exstaffrole": "roleid",
        "botrole": "roleid",
        "raidrole": "roleid",
        "staffchannel": "channelid",
        "rulesurl": str,
        "appealurl": str,
        "watchchannel": "channelid",
        "noreplythreshold": int,
    },
    "toss": {
        "tossrole": "channelid",
        "tosscategory": "catid",
        "tosschannels": list,
        "tosstopic": str,
    },
    "surveyr": {
        "surveychannel": "channelid",
        "startingcase": int,
        "loggingtypes": list,
        "loggingroles": "listroleid",
    },
    "cotd": {
        "cotdrole": "roleid",
        "cotdname": str,
    },
    "reaction": {
        "embedenable": bool,
        "translateenable": bool,
        "burstreactsenable": bool,
        "autoreadableenable": bool,
        "paidforprofileeffectsenable": bool,
    },
    "metadata": {
        "version": int,
    },
}


def make_config(sid):
    if not os.path.exists(f"{server_data}/{sid}"):
        os.makedirs(f"{server_data}/{sid}")
    shutil.copyfile("assets/config.example.yml", f"{server_data}/{sid}/config.yml")
    return stock_config


def get_config(sid, part, key):
    configs = fill_config(sid)

    return configs[part][key]


def fill_config(sid):
    configs = (
        get_raw_config(sid)
        if os.path.exists(f"{server_data}/{sid}/config.yml")
        else make_config(sid)
    )

    if configs["metadata"]["version"] < stock_config["metadata"]["version"]:
        # Version update code.

        # * to 3.
        if configs["metadata"]["version"] < 3:
            configs["staff"]["adminrole"] = None
            configs["staff"]["modrole"] = configs["staff"]["staffrole"]
            del configs["staff"]["staffrole"]

        # * to 4.
        if configs["metadata"]["version"] < 4:
            del configs["toss"]["drivefolder"]
            configs["toss"]["tosstopic"] = None
        set_raw_config(sid, configs)

    return configs


def get_raw_config(sid):
    with open(f"{server_data}/{sid}/config.yml", "r") as f:
        config = yaml.safe_load(f)
    return config


def set_raw_config(sid, contents):
    contents["metadata"]["version"] = stock_config["metadata"]["version"]
    with open(f"{server_data}/{sid}/config.yml", "w") as f:
        yaml.dump(contents, f, sort_keys=False)
