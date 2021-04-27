"""utility functions which can be used in training."""

import hashlib
import logging
import shutil
from logging import Logger
from pathlib import Path
from pprint import pformat
from typing import Any, Mapping, Optional, Tuple, Union

import ignite.distributed as idist
import torch
from ignite.contrib.handlers import PiecewiseLinear
from ignite.contrib.handlers.param_scheduler import ParamScheduler
from ignite.engine import Engine
from ignite.handlers.checkpoint import Checkpoint
from ignite.utils import setup_logger
from models import get_model
from torch.nn import CrossEntropyLoss, Module
from torch.optim import SGD, Optimizer
from torch.optim.lr_scheduler import _LRScheduler
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, Union

from ignite.contrib.engines import common
from ignite.contrib.handlers.base_logger import BaseLogger
from ignite.contrib.handlers.param_scheduler import LRScheduler
from ignite.engine.engine import Engine
from ignite.engine.events import Events
from ignite.handlers import Checkpoint, EarlyStopping, TimeLimit, Timer
from torch.nn import Module
from torch.optim.optimizer import Optimizer
from torch.utils.data.distributed import DistributedSampler

#%%

def get_handlers(
    config: Any,
    model: Module,
    trainer: Engine,
    evaluator: Engine,
    metric_name: str,
    es_metric_name: str,
    train_sampler: Optional[DistributedSampler] = None,
    to_save: Optional[Mapping] = None,
    lr_scheduler: Optional[LRScheduler] = None,
    output_names: Optional[Iterable[str]] = None,
    **kwargs: Any,
) -> Union[Tuple[Checkpoint, EarlyStopping, Timer], Tuple[None, None, None]]:
    """Get best model, earlystopping, timer handlers.

    Parameters
    ----------
    config
        Config object for setting up handlers

    `config` has to contain
    - `output_dir`: output path to indicate where to_save objects are stored
    - `save_every_iters`: saving iteration interval
    - `n_saved`: number of best models to store
    - `log_every_iters`: logging interval for iteration progress bar and `GpuInfo` if true
    - `with_pbars`: show two progress bars
    - `with_pbar_on_iters`: show iteration-wise progress bar
    - `stop_on_nan`: Stop the training if engine output contains NaN/inf values
    - `clear_cuda_cache`: clear cuda cache every end of epoch
    - `with_gpu_stats`: show GPU information: used memory percentage, gpu utilization percentage values
    - `patience`: number of events to wait if no improvement and then stop the training
    - `limit_sec`: maximum time before training terminates in seconds

    model
        best model to save
    trainer
        the engine used for training
    evaluator
        the engine used for evaluation
    metric_name
        evaluation metric to save the best model
    es_metric_name
        evaluation metric to early stop the model
    train_sampler
        distributed training sampler to call `set_epoch`
    to_save
        objects to save during training
    lr_scheduler
        learning rate scheduler as native torch LRScheduler or ignite’s parameter scheduler
    output_names
        list of names associated with `trainer`'s process_function output dictionary
    kwargs
        keyword arguments passed to Checkpoint handler

    Returns
    -------
    best_model_handler, es_handler, timer_handler
    """

    best_model_handler, es_handler, timer_handler = None, None, None

    # https://pytorch.org/ignite/contrib/engines.html#ignite.contrib.engines.common.setup_common_training_handlers
    # kwargs can be passed to save the model based on training stats
    # like score_name, score_function
    common.setup_common_training_handlers(
        trainer=trainer,
        train_sampler=train_sampler,
        to_save=to_save,
        lr_scheduler=lr_scheduler,
        output_names=output_names,
        output_path=config.output_dir / 'checkpoints',
        save_every_iters=config.save_every_iters,
        n_saved=config.n_saved,
        log_every_iters=config.log_every_iters,
        with_pbars=config.with_pbars,
        with_pbar_on_iters=config.with_pbar_on_iters,
        stop_on_nan=config.stop_on_nan,
        clear_cuda_cache=config.clear_cuda_cache,
        with_gpu_stats=config.with_gpu_stats,
        **kwargs,
    )
    return best_model_handler, es_handler, timer_handler

#%%

def get_logger(
    config: Any,
    trainer: Engine,
    evaluator: Optional[Union[Engine, Dict[str, Engine]]] = None,
    optimizers: Optional[Union[Optimizer, Dict[str, Optimizer]]] = None,
    **kwargs: Any,
) -> Optional[BaseLogger]:
    """Get Ignite provided logger.

    Parameters
    ----------
    config
        Config object for setting up loggers

    `config` has to contain
    - `filepath`: logging path to output file
    - `logger_log_every_iters`: logging iteration interval for loggers

    trainer
        trainer engine
    evaluator
        evaluator engine
    optimizers
        optimizers to log optimizer parameters
    kwargs
        optional keyword arguments passed to the logger

    Returns
    -------
    logger_handler
        Ignite provided logger instance
    """

    logger_handler = common.setup_tb_logging(
        output_path=config.output_dir,
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluator,
        log_every_iters=config.logger_log_every_iters,
        **kwargs,
    )
    return logger_handler

#%%


def initialize(config: Optional[Any]) -> Tuple[Module, Optimizer, Module, Union[_LRScheduler, ParamScheduler]]:
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
    lr_scheduler = PiecewiseLinear(optimizer, param_name="lr", milestones_values=milestones_values)
    model = idist.auto_model(model)
    optimizer = idist.auto_optim(optimizer)
    loss_fn = loss_fn.to(idist.device())

    return model, optimizer, loss_fn, lr_scheduler

#%%

def log_basic_info(logger: Logger, config: Any) -> None:
    """Logging about pytorch, ignite, configurations, gpu system
    distributed settings.

    Parameters
    ----------
    logger
        Logger instance for logging
    config
        config object to log
    """
    import ignite

    logger.info("PyTorch version: %s", torch.__version__)
    logger.info("Ignite version: %s", ignite.__version__)
    if torch.cuda.is_available():
        # explicitly import cudnn as
        # torch.backends.cudnn can not be pickled with hvd spawning procs
        from torch.backends import cudnn

        logger.info("GPU device: %s", torch.cuda.get_device_name(idist.get_local_rank()))
        logger.info("CUDA version: %s", torch.version.cuda)
        logger.info("CUDNN version: %s", cudnn.version())

    logger.info("Configuration: %s", pformat(vars(config)))

    if idist.get_world_size() > 1:
        logger.info("distributed configuration: %s", idist.model_name())
        logger.info("backend: %s", idist.backend())
        logger.info("device: %s", idist.device().type)
        logger.info("hostname: %s", idist.hostname())
        logger.info("world size: %s", idist.get_world_size())
        logger.info("rank: %s", idist.get_rank())
        logger.info("local rank: %s", idist.get_local_rank())
        logger.info("num processes per node: %s", idist.get_nproc_per_node())
        logger.info("num nodes: %s", idist.get_nnodes())
        logger.info("node rank: %s", idist.get_node_rank())

#%%


def log_metrics(engine: Engine, tag: str) -> None:
    """Log `engine.state.metrics` with given `engine` and `tag`.

    Parameters
    ----------
    engine
        instance of `Engine` which metrics to log.
    tag
        a string to add at the start of output.
    """
    metrics_format = "{0} [{1}/{2}]: {3}".format(tag, engine.state.epoch, engine.state.iteration, engine.state.metrics)
    engine.logger.info(metrics_format)

#%%

def setup_logging(config: Any) -> Logger:
    """Setup logger with `ignite.utils.setup_logger()`.

    Parameters
    ----------
    config
        config object. config has to contain
        `verbose` and `output_dir` attributes.

    Returns
    -------
    logger
        an instance of `Logger`
    """
    green = "\033[32m"
    reset = "\033[0m"
    logger = setup_logger(
        name=f"{green}[ignite]{reset}",
        level=logging.INFO if config.verbose else logging.WARNING,
        format="%(name)s: %(message)s",
        filepath=config.output_dir / "training-info.log",
    )
    return logger

#%%


def hash_checkpoint(
    checkpoint_fp: Union[str, Path],
    jitted: bool,
    output_path: Union[str, Path],
) -> Tuple[Path, str]:
    """Hash the checkpoint file to be used with `check_hash` of
    `torch.hub.load_state_dict_from_url`.

    Parameters
    ----------
    checkpoint_fp
        path to the checkpoint file.
    jitted
        indicate the checkpoint is already applied torch.jit or not.
    output_path
        path to store the hashed checkpoint file.

    Returns
    -------
    hashed_fp and sha_hash
        path to the hashed file and SHA hash
    """
    if isinstance(checkpoint_fp, str):
        checkpoint_fp = Path(checkpoint_fp)

    sha_hash = hashlib.sha256(checkpoint_fp.read_bytes()).hexdigest()
    ckpt_file_name = checkpoint_fp.stem

    if jitted:
        hashed_fp = "-".join((ckpt_file_name, sha_hash[:8])) + ".ptc"
    else:
        hashed_fp = "-".join((ckpt_file_name, sha_hash[:8])) + ".pt"

    if isinstance(output_path, str):
        output_path = Path(output_path)

    hashed_fp = output_path / hashed_fp
    shutil.move(checkpoint_fp, hashed_fp)
    print(f"Saved state dict into {hashed_fp} | SHA256: {sha_hash}")

    return hashed_fp, sha_hash

#%%

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
