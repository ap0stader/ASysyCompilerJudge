from analyzer.common import Analyzer
from util.statuscode import StatusCode


class StatStatus(Analyzer):
    status_data = {}

    @staticmethod
    def get_empty_stat() -> dict:
        return {"ALL": 0, "AC": 0, "WA": 0, "TLE": 0, "RE": 0, "UNKNOWN": 0}

    def register_origin(self, origin: str):
        self.status_data[origin] = self.get_empty_stat()

    def prepare(self):
        for key in self.status_data:
            self.status_data[key] = self.get_empty_stat()

    def update_data(self, status: StatusCode, origin: str):
        self.status_data[origin]["ALL"] += 1
        match status:
            case StatusCode.JUDGE_AC:
                self.status_data[origin]["AC"] += 1
            case StatusCode.JUDGE_WA:
                self.status_data[origin]["WA"] += 1
            case StatusCode.JUDGE_TLE, StatusCode.EXECUTE_TLE:
                self.status_data[origin]["TLE"] += 1
            case StatusCode.JUDGE_RE, StatusCode.EXECUTE_RE:
                self.status_data[origin]["RE"] += 1
            case _:
                self.status_data[origin]["UNKNOWN"] += 1

    def analyze(self, status: StatusCode, origin: str, info_dict: dict):
        if origin is None:
            for key in self.status_data:
                self.update_data(status, key)
        else:
            self.update_data(status, origin)

    def summary(self) -> str:
        strbuilder = "===== " + self.name() + " Statistics =====\n"
        for origin, stat in self.status_data.items():
            strbuilder += "Judge: " + origin + "\n"

            strbuilder += f"ALL: {stat['ALL']:<5} "
            strbuilder += f"AC: {stat['AC']:<5} "
            strbuilder += f"WA: {stat['WA']:<5} "
            strbuilder += f"TLE: {stat['TLE']:<5} "
            strbuilder += f"RE: {stat['RE']:<5} "

            if stat["UNKNOWN"] != 0:
                strbuilder += f"UNKNOWN: {stat['UNKNOWN']:<5}"
        return strbuilder + "\n"
    