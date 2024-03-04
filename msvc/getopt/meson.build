# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 L. E. Segovia <amy@amyspark.me>

getopt_headers = files(
	'getopt.h',
)

getopt_srcs = files(
	'getopt.c',
	'getopt1.c',
)

getopt_c_args = c_args + [
	'-DHAVE_CONFIG_H',
	'-DHAVE_LIBINTL_H=0'
] + cc.get_supported_arguments(
	'/wd4100',
	'/wd4131',
	'-Wno-error=strict-prototypes',
	'-Wno-error=missing-prototypes'
)

getopt_lib = static_library(
	'getopt',
	getopt_srcs,
	extra_files: getopt_headers,
	c_args: getopt_c_args,
	include_directories: include_directories,
	install: false,
	native: native
)

getopt_dep = declare_dependency(
	link_with: getopt_lib,
	include_directories: include_directories('.')
)
