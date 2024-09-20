from pathlib import Path
from typing import Tuple, Dict, Any, List

from analyzer.common import Analyzer
from executor import ExecutorObserver
from judge.common import Judge


def get() -> Tuple[Dict[str, Any], List[ExecutorObserver]]:
    raise Exception("Custom configuration was not set")


def example_multiple():
    return {
        "judge_type": "multiple",  # DO NOT MODIFY
        "judge_configs": [
            {
                "args": "-args",
                "compiler_output_file": "output.txt",
                "judge": Judge("name"),
                "testfile_path": Path("testfile_path"),
                "sourcecode_filename": "sourcecode_filename",
                "input_filename": "input_filename",
                "answer_filename": "answer_filename"
            }
        ],
        "analyzer": Analyzer("name"),
    }, []


def example_single():
    return {
        "judge_type": "single",  # DO NOT MODIFY
        "args": "-args",
        "judge_pairs": [
            ("compiler_output_file", Judge("name")),
        ],
        "testfile_path": Path("testfile_path"),
        "sourcecode_filename": "sourcecode_filename",
        "input_filename": "input_filename",
        "answer_filename": "answer_filename",
        "analyzer": Analyzer("name"),
    }, []
