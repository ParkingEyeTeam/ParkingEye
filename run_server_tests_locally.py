import os
import argparse
os.environ["MONGO_DB"] = 'test_server_db'
IGOR = True

if IGOR:
    os.environ["MONGO_HOST"] = 'localhost:27020'

parser = argparse.ArgumentParser()
parser.add_argument('--test_group', required=False, default=None,
                    help='группа тестов, например tests/server_tests/test_crud_cam_park.py::test_read_all')

args = parser.parse_args()


if args.test_group is None:
    os.system("pytest -vs")
else:
    os.system("pytest -vs " + args.test_group)
