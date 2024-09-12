from analyzer.common import Analyzer
from util.statuscode import StatusCode
from util.termcolor import RESET, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN


class Stat(Analyzer):
    name = "UNKNOWN NAME STATISTICS"
    All: int
    AC: int
    PART: int
    WA: int
    TLE: int
    RE: int
    UNKNOWN: int

    def __init__(self, name: str):
        self.name = name

    def prepare(self):
        self.All = 0
        self.AC = 0
        self.PART = 0
        self.WA = 0
        self.TLE = 0
        self.RE = 0
        self.UNKNOWN = 0

    def info(self, status: StatusCode, info):
        self.All += 1
        match status:
            case StatusCode.JUDGE_AC:
                self.AC += 1
            case StatusCode.JUDGE_PART:
                self.PART += 1
            case StatusCode.JUDGE_WA:
                self.WA += 1
            case StatusCode.EXECUTE_TLE:
                self.TLE += 1
            case StatusCode.EXECUTE_RE:
                self.RE += 1
            case _:
                self.UNKNOWN += 1

    def summary_print(self):
        print("===== " + self.name + " Statistics =====")
        print(CYAN + "All: " + RESET + str(self.All), end="\t")
        print(GREEN + "AC: " + RESET + str(self.AC), end="\t")
        if self.PART != 0:
            print(YELLOW + "PART: " + RESET + str(self.PART), end="\t")
        print(RED + "WA: " + RESET + str(self.WA), end="\t")
        print(BLUE + "TLE: " + RESET + str(self.TLE), end="\t")
        print(PURPLE + "RE: " + RESET + str(self.RE), end="\t")
        if self.UNKNOWN != 0:
            print("UNKNOWN: " + str(self.UNKNOWN))
        else:
            print()

    def summary_save(self) -> str:
        return ("===== " + self.name + " Statistics =====\n" +
                "All: " + str(self.All) + "\t" +
                "AC: " + str(self.AC) + "\t" +
                "PART: " + str(self.PART) + "\t" +
                "WA: " + str(self.WA) + "\t" +
                "TLE: " + str(self.TLE) + "\t" +
                "RE: " + str(self.RE) + "\t" +
                "UNKNOWN: " + str(self.UNKNOWN))
