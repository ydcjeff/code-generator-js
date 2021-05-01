###
from logging import Logger
from pathlib import Path
from typing import Any, Mapping, Optional, Tuple, Union

import ignite.distributed as idist
import torch
from ignite.contrib.handlers import PiecewiseLinear
from ignite.contrib.handlers.param_scheduler import ParamScheduler
from ignite.engine import Engine
from ignite.engine.engine import Engine
from ignite.handlers import Checkpoint
from ignite.handlers.checkpoint import Checkpoint
from ignite.utils import setup_logger
from models import get_model
from torch.nn import CrossEntropyLoss, Module
from torch.optim import SGD, Optimizer
from torch.optim.lr_scheduler import _LRScheduler
from torch.optim.optimizer import Optimizer


### initialize
def initialize(
    config: Optional[Any],
) -> Tuple[Module, Optimizer, Module, Union[_LRScheduler, ParamScheduler]]:
    """Initializing model, optimizer, loss function, and lr scheduler
    with correct settings.

    Parameters
    ----------
    config:
        config object

    Returns
    -------
    model, optimizer, loss_fn, lr_scheduler
    """
    model = get_model(config.model)
    optimizer = SGD(
        model.parameters(),
        lr=config.lr,
        momentum=config.momentum,
        weight_decay=config.weight_decay,
        nesterov=True,
    )
    loss_fn = CrossEntropyLoss().to(idist.device())
    le = config.num_iters_per_epoch
    milestones_values = [
        (0, 0.0),
        (le * config.num_warmup_epochs, config.lr),
        (le * config.max_epochs, 0.0),
    ]
    lr_scheduler = PiecewiseLinear(
        optimizer, param_name="lr", milestones_values=milestones_values
    )
    model = idist.auto_model(model)
    optimizer = idist.auto_optim(optimizer)
    loss_fn = loss_fn.to(idist.device())

    return model, optimizer, loss_fn, lr_scheduler


### log_metrics
def log_metrics(engine: Engine, tag: str) -> None:
    """Log `engine.state.metrics` with given `engine` and `tag`.

    Parameters
    ----------
    engine
        instance of `Engine` which metrics to log.
    tag
        a string to add at the start of output.
    """
    metrics_format = "{0} [{1}/{2}]: {3}".format(
        tag, engine.state.epoch, engine.state.iteration, engine.state.metrics
    )
    engine.logger.info(metrics_format)


### resume_from
def resume_from(
    to_load: Mapping,
    checkpoint_fp: Union[str, Path],
    logger: Logger,
    strict: bool = True,
    model_dir: Optional[str] = None,
) -> None:
    """Loads state dict from a checkpoint file to resume the training.

    Parameters
    ----------
    to_load
        a dictionary with objects, e.g. {“model”: model, “optimizer”: optimizer, ...}
    checkpoint_fp
        path to the checkpoint file
    logger
        to log info about resuming from a checkpoint
    strict
        whether to strictly enforce that the keys in `state_dict` match the keys
        returned by this module’s `state_dict()` function. Default: True
    model_dir
        directory in which to save the object
    """
    if isinstance(checkpoint_fp, str) and checkpoint_fp.startswith("https://"):
        checkpoint = torch.hub.load_state_dict_from_url(
            checkpoint_fp, model_dir=model_dir, map_location="cpu", check_hash=True
        )
    else:
        if isinstance(checkpoint_fp, str):
            checkpoint_fp = Path(checkpoint_fp)

        if not checkpoint_fp.exists():
            raise FileNotFoundError(f"Given {str(checkpoint_fp)} does not exist.")
        checkpoint = torch.load(checkpoint_fp, map_location="cpu")

    Checkpoint.load_objects(to_load=to_load, checkpoint=checkpoint, strict=strict)
    logger.info("Successfully resumed from a checkpoint: %s", checkpoint_fp)


### setup_logging
def setup_logging(config: Any) -> Logger:
    """Setup logger with `ignite.utils.setup_logger()`.

    Parameters
    ----------
    config
        config object. config has to contain `output_dir` attribute.

    Returns
    -------
    logger
        an instance of `Logger`
    """
    green = "\033[32m"
    reset = "\033[0m"
    logger = setup_logger(
        name=f"{green}[ignite]{reset}",
        format="%(name)s: %(message)s",
        filepath=config.output_dir / "training-info.log",
    )
    return logger
