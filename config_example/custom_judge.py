from pathlib import Path
from typing import Tuple, Dict, Any, List

from analyzer.common import Analyzer
from analyzer.statstatus import StatStatus
from executor import ExecutorObserver
from judge.common import Judge
from judge.linecompare import LineCompare


def get() -> Tuple[List[Dict[str, Any]], List[ExecutorObserver]]:
    raise Exception("Custom configuration was not set.")


def example():
    public_analyzer_example = Analyzer("public")
    return [{
        "name": "Task1",
        "args": "-args1",
        "testfile_path": "testfile_path1",
        "config_filename": "config_filename1",
        "sourcecode_filename": Path("sourcecode_filename1"),
        "input_filename": "input_filename1",
        "answer_filename": "answer_filename1",
        "judge_dict": {
            "type1": [{
                "compiler_output_filename": "type1.txt",
                "judge": Judge("1"),
                "analyzers": [public_analyzer_example]
            }],
            "type2": [{
                "compiler_output_filename": "type2.txt",
                "judge": Judge("2"),
                "analyzers": [public_analyzer_example]
            }],
        },
    }, {
        "name": "Task2",
        "args": "-args2",
        "testfile_path": "testfile_path2",
        "config_filename": "config_filename2",
        "sourcecode_filename": Path("sourcecode_filename2"),
        "input_filename": "input_filename2",
        "answer_filename": "answer_filename2",
        "judge_dict": {
            "typea": [{
                "compiler_output_filename": "typea.txt",
                "judge": Judge("a"),
                "analyzers": [Analyzer("a"), Analyzer("b")]
            }],
            "typeb": [{
                "compiler_output_filename": "typeb.txt",
                "judge": Judge("b"),
                "analyzers": [Analyzer("b"), Analyzer("b")]
            }],
        },
    }], []
