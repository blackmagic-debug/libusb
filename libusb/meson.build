# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 L. E. Segovia <amy@amyspark.me>

libusb_headers = files(
	'libusbi.h',
	'version.h',
	'version_nano.h',
)

libusb_srcs = files(
	'core.c',
	'descriptor.c',
	'hotplug.c',
	'io.c',
	'strerror.c',
	'sync.c'
) + [config_h]

if platform == 'posix'
	libusb_headers += files(
		'os/events_posix.h',
		'os/threads_posix.h',
	)
	libusb_srcs += files(
		'os/events_posix.c',
		'os/threads_posix.c',
	)
else
	libusb_headers += files(
		'os/events_windows.h',
		'os/threads_windows.h',
	)
	libusb_srcs += files(
		'os/events_windows.c',
		'os/threads_windows.c',
	)
endif

platform_libs = []

include_directories += include_directories('.')

if backend == 'darwin'
	libusb_headers += files(
		'os/darwin_usb.h',
	)
	libusb_srcs += files(
		'os/darwin_usb.c',
	)
elif backend == 'haiku'
	libusb_haiku_sources = files(
		'os/haiku_usb_backend.cpp',
		'os/haiku_pollfs.cpp',
		'os/haiku_usb_raw.cpp',
	)

	libusb_haiku_headers = files(
		'os/haiku_usb.h',
		'os/haiku_usb_raw.h',
	)

	libusb_haiku = static_library(
		'usb_haiku',
		libusb_haiku_sources,
		extra_files: libusb_haiku_headers,
		c_args: c_args,
		link_args: c_link_args,
		gnu_symbol_visibility: 'hidden',
		dependencies: dependencies,
		version: meson.project_version(),
		install: false,
	)

	platform_libs += libusb_haiku
elif backend == 'linux'
	libusb_headers += files(
		'os/linux_usbfs.h',
	)
	libusb_srcs += files(
		'os/linux_usbfs.c',
	)
	if use_udev
		libusb_srcs += files(
			'os/linux_udev.c',
		)
	else
		libusb_srcs += files(
			'os/linux_netlink.c',
		)
	endif
elif backend == 'emscripten'
	libusb_emscripten_sources = files(
		'os/emscripten_webusb.cpp',
	)

	libusb_emscripten_headers = []

	libusb_emscripten = static_library(
		'usb_emscripten',
		libusb_emscripten_sources,
		extra_files: libusb_emscripten_headers,
		c_args: c_args,
		link_args: c_link_args,
		gnu_symbol_visibility: 'hidden',
		dependencies: dependencies,
		version: meson.project_version(),
		install: false,
	)

	platform_libs += libusb_emscripten
elif backend == 'netbsd'
	libusb_headers += []
	libusb_srcs += files(
		'os/netbsd_usb.c',
	)
elif backend == 'null'
	libusb_headers += []
	libusb_srcs += files(
		'os/null_usb.c',
	)
elif backend == 'openbsd'
	libusb_headers += []
	libusb_srcs += files(
		'os/openbsd_usb.c',
	)
elif backend == 'sunos'
	libusb_headers += files(
		'os/sunos_usb.h',
	)
	libusb_srcs += files(
		'os/sunos_usb.c',
	)
elif backend == 'windows'
	libusb_headers += files(
		'libusb-1.0.def',
		'os/windows_common.h',
		'os/windows_usbdk.h',
		'os/windows_winusb.h',
	)
	libusb_srcs += files(
		'os/windows_common.c',
		'os/windows_usbdk.c',
		'os/windows_winusb.c',
	)

	libusb_srcs += windows.compile_resources(
		'libusb-1.0.rc',
		include_directories: include_directories,
	)
endif

if needs_getopt
	dependencies += [getopt_dep]
endif

libusb_def = configure_file(
	command: [fix_def, '@INPUT@', '@OUTPUT@'],
	input: meson.current_source_dir() / 'libusb-1.0.def',
	output: 'libusb-1.0-patched.def'
)

libusb = library(
	'usb-1.0',
	libusb_srcs,
	extra_files: libusb_headers,
	c_args: c_args,
	link_args: c_link_args,
	gnu_symbol_visibility: 'hidden',
	dependencies: dependencies,
	include_directories: include_directories,
	vs_module_defs: libusb_def,
	version: lt_version,
	install: true,
)

pkginclude_headers = files(
	'libusb.h',
)

install_headers(
	pkginclude_headers,
	subdir: meson.project_name()
)

libusb_dep = declare_dependency(
	link_with: libusb,
	include_directories: include_directories,
)
