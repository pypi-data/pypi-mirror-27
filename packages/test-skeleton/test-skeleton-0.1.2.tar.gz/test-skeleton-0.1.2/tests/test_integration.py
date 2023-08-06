from os import path as osp
import os
import pytest
from test_skeleton.parse import parse
from test_skeleton.skeleton import create

INPUT_DIR = osp.join(osp.dirname(osp.abspath(__file__)), 'data', 'input')
OUTPUT_DIR = osp.join(osp.dirname(osp.abspath(__file__)), 'data', 'output')


def case_files():
    assert len(os.listdir(INPUT_DIR)) == len(os.listdir(OUTPUT_DIR))

    for i in range(len(os.listdir(INPUT_DIR))):
        input = osp.join(INPUT_DIR, '{}.py').format(i + 1)
        output = osp.join(OUTPUT_DIR, '{}.txt').format(i + 1)
        yield input, output


@pytest.mark.parametrize('input_path,output_path', case_files())
def test_input_to_output(input_path, output_path):
    with open(output_path, 'r') as f:
        expected = f.read()
        res = create(parse(input_path))
        assert res == expected
