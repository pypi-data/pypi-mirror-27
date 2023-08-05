# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import io
import json
import platform
import time
import traceback
from typing import Any, Callable, Dict, Iterator

from logzero import logger

from chaoslib import __version__
from chaoslib.action import ensure_action_is_valid, run_action
from chaoslib.exceptions import FailedAction, FailedActivity, FailedProbe,\
    InvalidExperiment
from chaoslib.probe import ensure_probe_is_valid, run_probe
from chaoslib.secret import load_secrets
from chaoslib.types import Activity, Experiment, Journal, Run, Secrets, Step


__all__ = ["ensure_experiment_is_valid", "run_experiment"]


def load_experiment(path: str) -> Experiment:
    """
    Parse the given experiment from `path` and return it.
    """
    with io.open(path) as f:
        return json.load(f)


def ensure_experiment_is_valid(experiment: Experiment):
    """
    A chaos experiment consists of a method made of activities to carry
    sequentially.

    There are two kinds of activities:

    * probe: detecting the state of a resource in your system or external to it
      There are two kinds of probes: `steady` and `close`
    * action: an operation to apply against your system

    Usually, an experiment is made of a set of `steady` probes that ensure the
    system is sound to carry further the experiment. Then, an action before
    another set of of  ̀close` probes to sense the state of the system
    post-action.

    This function raises :exc:`InvalidExperiment`, :exc:`InvalidProbe` or
    :exc:`InvalidAction` depending on where it fails.
    """
    if not experiment:
        raise InvalidExperiment("an empty experiment is not an experiment")

    if not experiment.get("title"):
        raise InvalidExperiment("experiment requires a title")

    if not experiment.get("description"):
        raise InvalidExperiment("experiment requires a description")

    method = experiment.get("method")
    if not method:
        raise InvalidExperiment("an experiment requires a method with "
                                "at least one activity")

    for step in method:
        if "title" not in step:
            raise InvalidExperiment("an activity step must have a title")

        action = step.get("action")
        if action:
            ensure_action_is_valid(action)

        probes = step.get("probes")
        if probes:
            steady = probes.get("steady")
            if steady:
                ensure_probe_is_valid(steady)

            close = probes.get("close")
            if close:
                ensure_probe_is_valid(close)


def initialize_run_journal(experiment: Experiment) -> Dict[str, Any]:
    return {
        "chaoslib-version": __version__,
        "platform": platform.platform(),
        "node": platform.node(),
        "experiment": experiment.copy(),
        "start": datetime.utcnow().isoformat(),
        "run": []
    }


def get_background_pool(experiment: Experiment) -> ThreadPoolExecutor:
    """
    Create a pool for background activities. The pool is as big as the number
    of declared background activities. If none are declared, returned `None`.
    """
    method = experiment.get("method")

    background_count = 0
    for step in method:
        action = step.get("action")
        if action and action.get("background"):
            background_count = background_count + 1

    if background_count:
        logger.debug(
            "{c} activities will be run in the background".format(
                c=background_count))
        return ThreadPoolExecutor(background_count)


def run_experiment(experiment: Experiment) -> Journal:
    """
    Run the given `experiment` method step by step, in the following sequence:
    steady probe, action, close probe.

    Activities can be executed in background when they have the
    `"background"` property set to `true`. In that case, the activity is run in
    a thread. By the end of runs, those threads block until they are all
    complete.

    If the experiment has the `"dry"` property set to `False`, the experiment
    runs without actually executing the activities.
    """
    logger.info("Experiment: {t}".format(t=experiment["title"]))

    dry = experiment.get("dry", False)
    if dry:
        logger.warning("Dry mode enabled")

    started_at = time.time()
    secrets = load_secrets(experiment.get("secrets", {}))
    pool = get_background_pool(experiment)

    journal = initialize_run_journal(experiment)

    runs = list(run_steps(experiment, secrets, pool, dry))

    journal["end"] = datetime.utcnow().isoformat()
    journal["duration"] = time.time() - started_at

    if pool:
        logger.debug("Waiting for background actions to complete...")
        pool.shutdown(wait=True)

    for run in runs:
        if not run:
            continue
        if isinstance(run, dict):
            journal["run"].append(run)
        else:
            journal["run"].append(run.result())

    logger.info("Experiment is now complete")

    return journal


def run_steps(experiment: Experiment, secrets: Secrets,
              pool: ThreadPoolExecutor, dry: bool = False) -> Iterator[Run]:
    method = experiment.get("method")
    for step in method:
        logger.info("Step: {t}".format(t=step.get("title")))

        yield run_steady_probe(step, secrets, pool, dry)
        yield apply_action(step, secrets, pool, dry)
        yield run_close_probe(step, secrets, pool, dry)


def run_steady_probe(step: Step, secrets: Secrets = None,
                     pool: ThreadPoolExecutor = None,
                     dry: bool = False) -> Run:
    probes = step.get("probes", {})
    steady = probes.get("steady")
    if steady:
        if steady.get("background"):
            logger.debug("steady probe will run in the background")
            run = pool.submit(run_activity, steady, "steady state",
                              func=run_probe, secrets=secrets, dry=dry)
        else:
            run = run_activity(steady, "steady state", func=run_probe,
                               secrets=secrets, dry=dry)
        return run


def apply_action(step: Step, secrets: Secrets = None,
                 pool: ThreadPoolExecutor = None,
                 dry: bool = False) -> Run:
    action = step.get("action")
    if action:
        if action.get("background"):
            logger.debug("action will run in the background")
            run = pool.submit(run_activity, action, "action",
                              func=run_action, secrets=secrets, dry=dry)
        else:
            run = run_activity(action, "action", func=run_action,
                               secrets=secrets, dry=dry)
        return run


def run_close_probe(step: Step, secrets: Secrets = None,
                    pool: ThreadPoolExecutor = None,
                    dry: bool = False) -> Run:
    probes = step.get("probes", {})
    close = probes.get("close")
    if close:
        if close.get("background"):
            logger.debug("close probe will run in the background")
            run = pool.submit(run_activity, close, "close state",
                              func=run_probe, secrets=secrets, dry=dry)
        else:
            run = run_activity(close, "close state", func=run_probe,
                               secrets=secrets, dry=dry)
        return run


def run_activity(activity: Activity, kind: str,
                 func: Callable[[Activity], Any],
                 secrets: Secrets, dry: bool = False) -> Run:
    logger.info("  {n}: {t}".format(n=kind.title(), t=activity["title"]))
    start = datetime.utcnow()

    run = {
        "activity": activity,
        "kind": kind,
        "output": None
    }

    try:
        if not dry:
            result = func(activity, secrets)
            run["output"] = result
        run["status"] = "succeeded"
        logger.info("  => succeeded with '{r}'".format(r=result))
    except FailedActivity as x:
        error_msg = str(x)
        run["status"] = "failed"
        run["output"] = str(x)
        run["exception"] = traceback.format_exception(type(x), x, None)
        logger.error("   => failed: {x}".format(x=error_msg))

    end = datetime.utcnow()
    run["start"] = start.isoformat()
    run["end"] = end.isoformat()
    run["duration"] = (end - start).total_seconds()

    return run
