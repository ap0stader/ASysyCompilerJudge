from judge.common import Judge
from util.statuscode import StatusCode


class Line(Judge):
    name = "UNKNOWN NAME LINE COMPARE"

    def __init__(self, name):
        self.name = name

    def init(self):
        pass

    def judge(self, compiler_output_path: str, input_path: str, answer_path: str):
        with open(compiler_output_path, 'r') as output_file, open(answer_path, 'r') as answer_file:
            output_lines = [line.strip() for line in output_file if line.strip()]
            answer_lines = [line.strip() for line in answer_file if line.strip()]

            output_length = output_lines.__len__()
            answer_length = answer_lines.__len__()

            for i in range(min(output_length, answer_length)):
                if output_lines[i] != answer_lines[i]:
                    return StatusCode.JUDGE_WA, ("Wrong answer at line " + str(i + 1)
                                                 + "!\nGot: " + output_lines[i] + "\nExpected: " + answer_lines[i])

            if output_lines < answer_lines:
                return StatusCode.JUDGE_WA, ("Output is fewer than answer!\nTotal Lines: "
                                             + str(output_length) + "\nExpected: " + str(answer_length))
            elif output_lines > answer_lines:
                return StatusCode.JUDGE_WA, ("Output is more than answer!\nTotal Lines: "
                                             + str(output_length) + "\nExpected: " + str(answer_length))

            return StatusCode.JUDGE_AC, ""
