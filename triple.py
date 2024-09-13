from analyzer.stat import SingleStat
from judge.line import Line


def get(mode: str):
    match mode:
        case "lexical_analysis":
            return (["output.txt"],
                    [Line("Lexical Analysis")],
                    SingleStat("Lexical Analysis")),

        case "syntax_analysis":
            return (["output.txt"],
                    [Line("Syntax Analysis")],
                    SingleStat("Syntax Analysis"))

        case _:
            print("When triple get(), got wrong mode.")
