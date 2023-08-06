import argparse

from util import load_yaml
from resource import ResourceManager
from writer import *


def run(document_file_path, resources):
    document = Document(load_yaml(document_file_path))

    writer = DocumentWriter(resources, "%s.pdf" % document.number, document)
    writer.write()

    print "Document %s PDF created" % document.number


def main(debug=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--doc', nargs=1, metavar='PATH', required=True,
                        help="Document yaml file path")
    args = parser.parse_args()
    run(args.doc[0], ResourceManager(debug))


if __name__ == "__main__":
    main(debug=True)
