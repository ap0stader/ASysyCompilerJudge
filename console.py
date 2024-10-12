from typing import List

from analyzer.common import Analyzer
from analyzer.statstatus import StatStatus
from util.termcolor import RESET, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, BRIGHT, ITALIC, UNDERLINE, INVERT


def java_detected_hook(jar_name: str):
    print("New " + INVERT + jar_name + RESET + " has been detected and copied.")


def started_observe_hook():
    print(">>> All Observers Started!")
    print(">>> Press Ctrl+C to exit.")


def executor_start_hook():
    print(">>> Starting Executor...")


def task_start_hook(task_name: str):
    print(">>> Task: " + task_name)


def summary_hook(analyzers: List[Analyzer]):
    for analyzer in analyzers:
        if isinstance(analyzer, StatStatus):
            print("===== " + analyzer.name() + " Statistics =====")
            for origin, stat in analyzer.status_data.items():
                print("Judge: " + origin)

                print(CYAN + "ALL: " + RESET + f"{stat['ALL']:<5}", end=" ")
                print(GREEN + "AC: " + RESET + f"{stat['AC']:<5}", end=" ")
                print(RED + "WA: " + RESET + f"{stat['WA']:<5}", end=" ")
                print(BLUE + "TLE: " + RESET + f"{stat['TLE']:<5}", end=" ")
                print(MAGENTA + "RE: " + RESET + f"{stat['RE']:<5}", end=" ")
                if stat["UNKNOWN"] != 0:
                    print("UNKNOWN: " + f"{stat['UNKNOWN']:<5}", flush=True)
                else:
                    print(flush=True)


def executor_finish_hook(result_subfolder_name: str):
    print("Results folder: results/" + GREEN + result_subfolder_name + RESET)
    print(">>> Judge finished! Continuing... ")
