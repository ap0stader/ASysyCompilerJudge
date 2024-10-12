from typing import List

from analyzer.common import Analyzer
from analyzer.statstatus import StatStatus
from judge.common import Judge
from util.statuscode import StatusCode
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


def testcase_start_hook(test_index: int, testcase_relative_path: str):
    print(f"No. {test_index:<4} Testcase: {str(testcase_relative_path):<16}", end=" ", flush=True)


def execute_status_hook(test_index: int, testcase_relative_path: str, statuscode: StatusCode):
    match statuscode:
        case StatusCode.EXECUTE_TLE:
            print(BLUE + "TLE" + RESET, flush=True)
        case StatusCode.EXECUTE_RE:
            print(MAGENTA + "RE" + RESET, flush=True)
        case StatusCode.EXECUTE_UNKNOWN:
            print("UNKNOWN", flush=True)


def judge_start_hook(test_index: int, testcase_relative_path: str, judge: Judge):
    print(f"{judge.name():>20}=>", end="", flush=True)


def judge_status_hook(test_index: int, testcase_relative_path: str, judge: Judge,
                      judge_status: StatusCode, judge_info_object: dict):
    match judge_status:
        case StatusCode.JUDGE_AC:
            print(GREEN + "AC" + RESET, end="")
            if judge_info_object["info"] != "":
                print("(" + judge_info_object["info"] + ")", end=" ")
            else:
                print("", end=" ")
        case StatusCode.JUDGE_WA:
            print(RED + "WA" + RESET, end=" ")
        case StatusCode.JUDGE_TLE:
            print(BLUE + "TLE" + RESET, end=" ")
        case StatusCode.JUDGE_RE:
            print(MAGENTA + "RE" + RESET, end=" ")
        case StatusCode.JUDGE_UNKNOWN:
            print("UNKNOWN", end=" ")


def judge_end_hook(test_index: int, testcase_relative_path: str, judge: Judge):
    print(flush=True)


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
