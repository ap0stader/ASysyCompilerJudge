from pathlib import Path

from analyzer.common import Analyzer
from judge.common import Judge


def get_different():
    return {
        "args": "-args",
        "judge_type": "different",  # DO NOT MODIFY
        "judge_configs": [
            {
                "compiler_output_file": "output.txt",
                "judge": Judge("name"),
                "testfile_path": Path("testfile_path"),
                "sourcecode_prefix": "sourcecode_prefix",
                "input_prefix": "input_prefix",
                "answer_prefix": "answer_prefix"
            }
        ],
        "analyzer": Analyzer("name"),
    }, []


def get_same():
    return {
        "args": "-args",
        "judge_type": "same",  # DO NOT MODIFY
        "judge_configs": {
            "judge_pairs": [
                ("compiler_output_file", Judge("name")),
            ],
            "testfile_path": Path("testfile_path"),
            "sourcecode_prefix": "sourcecode_prefix",
            "input_prefix": "input_prefix",
            "answer_prefix": "answer_prefix"
        },
        "analyzer": Analyzer("name"),
    }, []
