getopt_headers = files(
	'getopt.h',
)

getopt_srcs = files(
	'getopt.c',
	'getopt1.c',
)

getopt_c_args = c_args + [
	'-DHAVE_CONFIG_H'
] + cc.get_supported_arguments('/wd4100', '/wd4131')

getopt_lib = static_library(
	'getopt',
	getopt_srcs,
	extra_files: getopt_headers,
	c_args: getopt_c_args,
	include_directories: include_directories,
	install: false,
)

getopt_dep = declare_dependency(
	link_with: getopt_lib,
	include_directories: include_directories('.')
)
