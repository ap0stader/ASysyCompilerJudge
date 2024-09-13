from analyzer.common import Analyzer
from util.statuscode import StatusCode
from util.termcolor import RESET, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN


def get_empty_stat() -> dict:
    return {"All": 0, "AC": 0, "PART": 0, "WA": 0, "TLE": 0, "RE": 0, "UNKNOWN": 0}


class StatByFile(Analyzer):
    __data = {}

    def register_origin(self, origin: str, **kwargs):
        self.__data[origin] = get_empty_stat()

    def prepare(self):
        for key in self.__data:
            self.__data[key] = get_empty_stat()

    def update_data(self, status: StatusCode, origin: str):
        self.__data[origin]["All"] += 1
        match status:
            case StatusCode.JUDGE_AC:
                self.__data[origin]["AC"] += 1
            case StatusCode.JUDGE_PART:
                self.__data[origin]["PART"] += 1
            case StatusCode.JUDGE_WA:
                self.__data[origin]["WA"] += 1
            case StatusCode.EXECUTE_TLE:
                self.__data[origin]["TLE"] += 1
            case StatusCode.EXECUTE_RE:
                self.__data[origin]["RE"] += 1
            case _:
                self.__data[origin]["UNKNOWN"] += 1

    def analyze(self, status: StatusCode, origin: str, info_dict: dict):
        if origin is None:
            for key in self.__data:
                self.update_data(status, key)
        else:
            self.update_data(status, origin)

    def summary_print(self):
        print("===== " + self.name() + " Statistics =====")
        for origin, stat in self.__data.items():
            print("Judge: " + origin)
            print(CYAN + "All: " + RESET + str(stat["All"]), end="\t")
            print(GREEN + "AC: " + RESET + str(stat["AC"]), end="\t")
            if stat["PART"] != 0:
                print(YELLOW + "PART: " + RESET + str(stat["PART"]), end="\t")
            print(RED + "WA: " + RESET + str(stat["WA"]), end="\t")
            print(BLUE + "TLE: " + RESET + str(stat["TLE"]), end="\t")
            print(PURPLE + "RE: " + RESET + str(stat["RE"]), end="\t")
            if stat["UNKNOWN"] != 0:
                print("UNKNOWN: " + str(stat["UNKNOWN"]))
            else:
                print()

    def summary_save(self) -> str:
        strbuilder = "===== " + self.name() + " Statistics =====\n"
        for origin, stat in self.__data.items():
            strbuilder += "Judge: " + origin + "\n"
            strbuilder += "All: " + str(stat["All"]) + "\t"
            strbuilder += "AC: " + str(stat["AC"]) + "\t"
            strbuilder += "PART: " + str(stat["PART"]) + "\t"
            strbuilder += "WA: " + str(stat["WA"]) + "\t"
            strbuilder += "TLE: " + str(stat["TLE"]) + "\t"
            strbuilder += "RE: " + str(stat["RE"]) + "\t"
            strbuilder += "UNKNOWN: " + str(stat["UNKNOWN"]) + "\n"
        return strbuilder
