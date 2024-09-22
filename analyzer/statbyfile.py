from analyzer.common import Analyzer
from util.statuscode import StatusCode
from util.termcolor import RESET, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN


def get_empty_stat() -> dict:
    return {"ALL": 0, "AC": 0, "PART": 0, "WA": 0, "TLE": 0, "RE": 0, "UNKNOWN": 0}


class StatByFile(Analyzer):
    __data = {}

    def register_origin(self, origin: str):
        self.__data[origin] = get_empty_stat()

    def prepare(self):
        for key in self.__data:
            self.__data[key] = get_empty_stat()

    def update_data(self, status: StatusCode, origin: str):
        self.__data[origin]["ALL"] += 1
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

            print(CYAN + "ALL: " + RESET + f"{stat['ALL']:<5}", end=" ")
            print(GREEN + "AC: " + RESET + f"{stat['AC']:<5}", end=" ")
            if stat["PART"] != 0:
                print(YELLOW + "PART: " + RESET + f"{stat['PART']:<5}", end=" ")
            print(RED + "WA: " + RESET + f"{stat['WA']:<5}", end=" ")
            print(BLUE + "TLE: " + RESET + f"{stat['TLE']:<5}", end=" ")
            print(MAGENTA + "RE: " + RESET + f"{stat['RE']:<5}", end=" ")
            if stat["UNKNOWN"] != 0:
                print("UNKNOWN: " + f"{stat['UNKNOWN']:<5}", flush=True)
            else:
                print(flush=True)

    def summary_save(self) -> str:
        strbuilder = "===== " + self.name() + " Statistics =====\n"
        for origin, stat in self.__data.items():
            strbuilder += "Judge: " + origin + "\n"

            strbuilder += "ALL: " + f"{stat['ALL']:<5} "
            strbuilder += "AC: " + f"{stat['AC']:<5} "
            if stat["PART"] != 0:
                strbuilder += "PART: " + f"{stat['PART']:<5} "
            strbuilder += "WA: " + f"{stat['WA']:<5} "
            strbuilder += "TLE: " + f"{stat['TLE']:<5} "
            strbuilder += "RE: " + f"{stat['RE']:<5} "
            if stat["UNKNOWN"] != 0:
                strbuilder += "UNKNOWN: " + f"{stat['UNKNOWN']:<5}"
        return strbuilder + "\n"
