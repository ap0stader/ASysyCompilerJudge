from pathlib import Path
from typing import Tuple

from judge.common import Judge
from util.statuscode import StatusCode


class LineCompare(Judge):
    def init(self):
        pass

    def judge(self, compiler_output_path: Path, input_path: Path, answer_path: Path) -> Tuple[StatusCode, dict]:
        if not compiler_output_path.is_file():
            return StatusCode.JUDGE_UNKNOWN, {"info": ("File " + compiler_output_path.name) + " not found!"}

        with (open(compiler_output_path, "r", encoding="utf-8") as output_file,
              open(answer_path, "r", encoding="utf-8") as answer_file):
            output_lines = [line.strip() for line in output_file if line.strip()]
            answer_lines = [line.strip() for line in answer_file if line.strip()]

            output_length = output_lines.__len__()
            answer_length = answer_lines.__len__()

            for i in range(min(output_length, answer_length)):
                if output_lines[i] != answer_lines[i]:
                    return StatusCode.JUDGE_WA, {"info": ("Wrong answer at line " + str(i + 1) +
                                                          "!\nGot: " + output_lines[i] +
                                                          "\nExpected: " + answer_lines[i])}

            if output_lines < answer_lines:
                return StatusCode.JUDGE_WA, {"info": ("Output is fewer than answer!\nTotal Lines: "
                                                      + str(output_length) + "\nExpected: " + str(answer_length))}
            elif output_lines > answer_lines:
                return StatusCode.JUDGE_WA, {"info": ("Output is more than answer!\nTotal Lines: "
                                                      + str(output_length) + "\nExpected: " + str(answer_length))}

            return StatusCode.JUDGE_AC, {"info": ""}
