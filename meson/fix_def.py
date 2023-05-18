#!/usr/bin/env python3

from argparse import ArgumentParser, FileType

if __name__ == '__main__':
	parser = ArgumentParser(description='Remove LIBRARY clause from module definition files')
	parser.add_argument('input', type=FileType('r', encoding='utf-8'), help='Source module definition file')
	parser.add_argument('output', type=FileType('w', encoding='utf-8'), help='Destination module definition file')

	args = parser.parse_args()

	lines = [line for line in args.input.readlines() if not line.startswith('LIBRARY')]

	args.output.writelines(lines)
