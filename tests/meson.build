# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 L. E. Segovia <amy@amyspark.me>

testlib_sources = files(
	'testlib.c',
)

testlib_headers = files(
	'libusb_testlib.h',
)

testlib_lib = static_library(
	'testlib',
	testlib_sources,
	include_directories: include_directories,
	extra_files: testlib_headers,
	dependencies: libusb_dep,
)

testlib = declare_dependency(
	link_with: testlib_lib,
	include_directories: include_directories,
)

stress_sources = files(
	'stress.c',
)

stress_exe = executable(
	'stress',
	stress_sources,
	dependencies: testlib,
	install: false,
)

stress_mt_sources = files(
	'stress_mt.c',
)

if backend == 'emscripten'
	stress_mt_link_args = [
		'-s', 'PROXY_TO_PTHREAD',
		'-s', 'EXIT_RUNTIME'
	]
else
	stress_mt_link_args = []
endif

stress_mt_exe = executable(
	'stress_mt',
	stress_mt_sources,
	link_args: stress_mt_link_args,
	dependencies: [testlib, thread_dep],
	override_options: ['prefer_static=true'],
	install: false,
)

set_option_sources = files(
	'set_option.c',
)

set_option_exe = executable(
	'set_option',
	set_option_sources,
	dependencies: testlib,
	install: false,
)

init_context_sources = files(
	'init_context.c',
)

init_context_exe = executable(
	'init_context',
	init_context_sources,
	dependencies: testlib,
	install: false,
)

test('stress', stress_exe)
test('stress_mt', stress_mt_exe)
test('set_option', set_option_exe)
test('init_context', init_context_exe)

if backend == 'linux'
	# NOTE: We add libumockdev-preload.so so that we can run tests in-process
	#       We also use -Wl,-lxxx as the compiler doesn't need it and libtool
	#       would reorder the flags otherwise.

	# NOTE (Meson): Meson has full access to the build system logic, so
	# instead of using tons of AM_DEFINE, let's access use_udev and then
	# rely on dependency(disabler: true) to yank this test if incompatible.

	umockdev_sources = files(
		'umockdev.c',
	)

	libumockdev_preload = cc.find_library('umockdev-preload', required: true)

	libumockdev_preload_dep = declare_dependency(
		dependencies: [umockdev_dep, libumockdev_preload],
		link_args: ['-Wl,--push-state,--no-as-needed', '-Wl,-lumockdev-preload', '-Wl,--pop-state']
	)

	umockdev_exe = executable(
		'umockdev',
		umockdev_sources,
		dependencies: [testlib, libumockdev_preload_dep],
		install: false,
	)

	test('umockdev', umockdev_exe)
endif
