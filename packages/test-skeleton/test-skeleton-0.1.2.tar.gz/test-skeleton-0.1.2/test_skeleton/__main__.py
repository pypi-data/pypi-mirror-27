from test_skeleton.cli import cli
from test_skeleton.parse import parse
from test_skeleton.skeleton import create
import os

if __name__ == "__main__":
    args = cli()
    parsed = parse(args.input)
    skeleton = create(parsed)
    print(skeleton)
    if args.save:
        fname = 'test_{}'.format(os.path.basename(args.input))
        fpath = os.path.join(os.getcwd(), fname)
        with open(fpath, 'w') as f:
            f.write(skeleton)
