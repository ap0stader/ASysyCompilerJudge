from analyzer.common import Analyzer
from util.statuscode import StatusCode


def get_empty_stat() -> dict:
    return {"ALL": 0, "AC": 0, "WA": 0, "TLE": 0, "RE": 0, "UNKNOWN": 0}


class StatStatus(Analyzer):
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
            case StatusCode.JUDGE_WA:
                self.__data[origin]["WA"] += 1
            case StatusCode.JUDGE_TLE, StatusCode.EXECUTE_TLE:
                self.__data[origin]["TLE"] += 1
            case StatusCode.JUDGE_RE, StatusCode.EXECUTE_RE:
                self.__data[origin]["RE"] += 1
            case _:
                self.__data[origin]["UNKNOWN"] += 1

    def analyze(self, status: StatusCode, origin: str, info_dict: dict):
        if origin is None:
            for key in self.__data:
                self.update_data(status, key)
        else:
            self.update_data(status, origin)

    def summary(self) -> str:
        strbuilder = "===== " + self.name() + " Statistics =====\n"
        for origin, stat in self.__data.items():
            strbuilder += "Judge: " + origin + "\n"

            strbuilder += f"ALL: {stat['ALL']:<5} "
            strbuilder += f"AC: {stat['AC']:<5} "
            strbuilder += f"WA: {stat['WA']:<5} "
            strbuilder += f"TLE: {stat['TLE']:<5} "
            strbuilder += f"RE: {stat['RE']:<5} "

            if stat["UNKNOWN"] != 0:
                strbuilder += f"UNKNOWN: {stat['UNKNOWN']:<5}"
        return strbuilder + "\n"
