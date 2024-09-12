from enum import Enum, unique


@unique
class StatusCode(Enum):
    EXECUTE_OK = 100
    EXECUTE_TLE = 101
    EXECUTE_RE = 102
    EXECUTE_UNKNOWN = 199

    JUDGE_AC = 200
    JUDGE_PART = 201
    JUDGE_WA = 202
    JUDGE_UNKNOWN = 299
