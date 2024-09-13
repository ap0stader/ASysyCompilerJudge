from analyzer.statbyfile import StatByFile
from judge.linecompare import LineCompare


def get(mode: str):
    match mode:
        case "lexical_analysis":
            return (["output.txt"],
                    [LineCompare("Lexical Analysis")],
                    StatByFile("Lexical Analysis")),

        case "syntax_analysis":
            return (["output.txt"],
                    [LineCompare("Syntax Analysis")],
                    StatByFile("Syntax Analysis"))

        case _:
            print("When triple get(), got wrong mode.")
