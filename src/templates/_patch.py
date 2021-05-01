###
from typing import Any
from ignite.handlers import Checkpoint, DiskSaver

###
def checkpoint_training(to_save: dict, config: Any):
    ckpt_handler_train = Checkpoint(
        to_save,
        DiskSaver(dirname=config.dirname, require_empty=False),
        filename_prefix=config.filename_prefix,
        n_saved=config.n_saved,
    )
    return ckpt_handler_train
