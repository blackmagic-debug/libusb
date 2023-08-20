# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 L. E. Segovia <amy@amyspark.me>

project(
	'libusb-1.0',
	'c', 'cpp',
	version: '1.0.27',
	meson_version: '>= 0.58',
	license: 'LGPL-2.1-or-later',
	default_options: [
		'c_std=gnu11',
		'warning_level=1',
		'b_pie=true',
		'b_lto=true',
		'cpp_eh=s',
	]
)

lt_version = '0.4.0'

cfg = configuration_data()

create_import_lib = false
is_android_linux = false

host = target_machine.system()

cc = meson.get_compiler('c')

c_args = []
c_link_args = []

if ['darwin', 'haiku', 'emscripten', 'linux', 'netbsd', 'openbsd', 'sunos'].contains(host)
	backend = host
	platform = 'posix'
elif host == 'android'
	# on Android Linux, some functions are in different places
	is_android_linux = true
	backend = 'linux'
	platform = 'posix'
elif host == 'cygwin'
	backend = 'windows'
	platform = 'windows'
	c_args += cc.get_supported_arguments('-mwin32')
elif host == 'windows'
	backend = 'windows'
	platform = 'windows'
	create_import_lib = get_option('default_library') != 'static'
	c_args += cc.get_supported_arguments('-fno-omit-frame-pointer')
	c_link_args += cc.get_supported_arguments('-static-libgcc')
else
	warning('The host being compiled for is not supported.')
	warning('The library may compile but will not function in any useful manner.')
	backend = 'null'
	platform = 'posix'
endif

message('Checking operating system... @0@'.format(backend))

thread_dep = dependency('threads')

dependencies = [thread_dep]

if platform == 'posix'
	cfg.set10('PLATFORM_POSIX', true, description: 'Define to 1 if compiling for a POSIX platform.')
	cfg.set('HAVE_NFDS_T', cc.has_type('nfds_t', prefix: '#include <poll.h>'))

	if backend != 'emscripten'
		# pipe2 is detected as present on Emscripten, but it isn't actually ported and always
		# returns an error. https://github.com/emscripten-core/emscripten/issues/14824
		cfg.set('HAVE_PIPE2', cc.has_function('pipe2'))
	endif

	# No special checks are needed for pthread. See thread_dep.

	# Check for new-style atomic builtins. We first check without linking to -latomic.
	gcc_atomic_builtins = '''
		#include <stdint.h>
		int main() {
			struct {
				uint64_t *v;
			} x;
			return (int)__atomic_load_n(x.v, __ATOMIC_ACQUIRE) &
				(int)__atomic_add_fetch(x.v, (uint64_t)1, __ATOMIC_ACQ_REL);
		}
	'''
	cfg.set('GCC_ATOMIC_BUILTINS_SUPPORTED', cc.links(gcc_atomic_builtins))
	if not cfg.get('GCC_ATOMIC_BUILTINS_SUPPORTED')
		atomic_dep = cc.find_library('atomic', required: false)
		if cc.has_function('__atomic_fetch_add_4', dependencies: atomic_dep)
			cfg.set('GCC_ATOMIC_BUILTINS_SUPPORTED', true)
			ac_result = 'yes'
			dependencies += [atomic_dep]
		else
			ac_result = 'no'
		endif
	else
		ac_result = 'yes'
	endif
	message('whether __atomic_load_n is supported... @0@'.format(ac_result))
elif platform == 'windows'
	cfg.set10('PLATFORM_WINDOWS', true, description: 'Define to 1 if compiling for a Windows platform.')
else
	error('Unknown platform')
endif

if backend == 'darwin'
	cfg.set('HAVE_PTHREAD_THREADID_NP', cc.has_function('pthread_threadid_np', dependencies: dependencies))
	add_languages('objc', required: true)
	dependencies += [
		cc.find_library('objc', required: true),
		dependency('IOKit', required: true, method: 'extraframework'),
		dependency('CoreFoundation', required: true, method: 'extraframework'),
		dependency('Security', required: true, method: 'extraframework'),
	]
	cfg.set('HAVE_IOKIT_USB_IOUSBHOSTFAMILYDEFINITIONS_H', cc.has_header('IOKit/usb/IOUSBHostFamilyDefinitions.h', dependencies: dependencies))
elif backend == 'haiku'
	dependencies += [
		cc.find_library('be', required: true),
	]
elif backend == 'linux'
	rt_dep = cc.find_library('rt', required: false)
	if cc.has_function('clock_gettime', dependencies: rt_dep)
		cfg.set('HAVE_CLOCK_GETTIME', true)
		dependencies += [rt_dep]
	endif
	use_udev = not get_option('udev').disabled()

	if use_udev
		udev_dep = dependency('libudev', required: true)
		cc.has_header('libudev.h', dependencies: udev_dep, required: true)
		if not cc.has_function('udev_new', dependencies: udev_dep)
			error('udev support requested but libudev not installed')
		else
			dependencies += [udev_dep]
			cfg.set('HAVE_LIBUDEV', true)
		endif

		# We can build umockdev tests (if available)
		umockdev_dep = dependency('umockdev-1.0', version: '>=0.16.0', disabler: true, required: false)
		if umockdev_dep.found()
			cfg.set10('UMOCKDEV_HOTPLUG', umockdev_dep.version().version_compare('>=0.17.7'))
		endif
	else
		umockdev_dep = disabler()

		cfg.set('HAVE_ASM_TYPES_H', cc.has_header('asm/types.h'))
		if not cc.has_header('linux/netlink.h')
			error('Linux netlink header not found')
		endif
		if not cc.has_header('sys/socket.h')
			error('Linux socket header not found')
		endif
	endif
elif backend == 'sunos'
	dependencies += [
		cc.find_library('devinfo', required: true),
	]
elif backend == 'windows'
	cfg.set('HAVE_STRUCT_TIMESPEC', cc.has_type('struct timespec', prefix: '#include <time.h>'))
	cfg.set('_WIN32_WINNT', '_WIN32_WINNT_VISTA', description: 'Define to the oldest supported Windows version.')
elif backend == 'emscripten'
	EXEEXT = '.html'
	c_link_args += [
		'--bind',
		'-s', 'ASYNCIFY',
		'-s', 'ASSERTIONS',
		'-s', 'ALLOW_MEMORY_GROWTH',
		'-s', 'INVOKE_RUN=0',
		'-s', 'EXPORTED_RUNTIME_METHODS=[\'callMain\']'
	]
else
	# no special handling required
endif

# headers not available on all platforms but required on others
cfg.set('HAVE_SYS_TIME_H', cc.has_header('sys/time.h'))

# check availability of clock_gettime(), except don't bother on Darwin, because the result is not used.
if platform == 'posix' and backend != 'darwin'
	if not cc.has_function('clock_gettime', dependencies: dependencies)
		error('clock_gettime() is required on this platform')
	endif

	# the clock_gettime() function needs certain clock IDs defined
	cc.has_header_symbol('time.h', 'CLOCK_MONOTONIC', required: true)
	# use the monotonic clock for condition variable timed waits if possible
	if not cc.has_function('pthread_condattr_setclock', dependencies: dependencies)
		cc.has_header_symbol('time.h', 'CLOCK_REALTIME', required: true)
	endif
endif

# eventfd support
if ['linux', 'sunos'].contains(backend)
	use_eventfd = get_option('eventfd')
	if not use_eventfd.disabled()
		if cc.has_header('sys/eventfd.h')
			if cc.has_header_symbol('sys/eventfd.h', 'EFD_NONBLOCK') and cc.has_header_symbol('sys/eventfd.h', 'EFD_CLOEXEC')
				if cc.has_function('eventfd')
					cfg.set('HAVE_EVENTFD', true, description: 'Define to 1 if the system has eventfd functionality.')
					ac_result = 'yes'
				elif use_eventfd.enabled()
					error('eventfd() function not found; glibc 2.9+ required')
				else
					ac_result = 'no (functions not available)'
				endif
			elif use_eventfd.enabled()
				error('eventfd header not usable; glibc 2.9+ required')
			else
				ac_result = 'no (header not usable)'
			endif
		elif use_eventfd.enabled()
			error('eventfd header not available; glibc 2.9+ required')
		else
			ac_result = 'no (header not available)'
		endif
	else
		ac_result = 'no (disabled by user)'
	endif
	message('whether to use eventfd for signalling... @0@'.format(ac_result))
endif

# timerfd support
if backend == 'linux' or backend == 'sunos'
	use_timerfd = get_option('timerfd')
	if not use_timerfd.disabled()
		if cc.has_header('sys/timerfd.h')
			if cc.has_header_symbol('sys/timerfd.h', 'TFD_NONBLOCK') and cc.has_header_symbol('sys/timerfd.h', 'TFD_CLOEXEC')
				if cc.has_function('timerfd_create')
					cfg.set('HAVE_TIMERFD', true, description: 'Define to 1 if the system has timerfd functionality.')
					ac_result = 'yes'
				elif use_timerfd.enabled()
					error('timerfd_create() function not found; glibc 2.9+ required')
					ac_result = 'no (functions not available)'
				endif
			elif use_timerfd.enabled()
				error('timerfd header not usable; glibc 2.9+ required')
				ac_result = 'no (header not usable)'
			endif
		elif use_timerfd.enabled()
			error('timerfd header not available; glibc 2.9+ required')
			ac_result = 'no (header not available)'
		endif
	else
		ac_result = 'no (disabled by user)'
	endif
	message('whether to use timerfd for timing... @0@'.format(ac_result))
endif

# Message logging
cfg.set('ENABLE_LOGGING', not get_option('log').disabled(), description: 'Define to 1 to enable message logging.')

cfg.set('ENABLE_DEBUG_LOGGING', get_option('debug_log').enabled(), description: 'Define to 1 to start with debug message logging enabled.')

if not get_option('system_log').disabled()
	cfg.set('USE_SYSTEM_LOGGING_FACILITY', true, description: 'Define to 1 to output logging messages to the systemwide log.')
	if backend != 'windows' and not is_android_linux
		# Check if syslog is available in standard C library
		if cc.has_header('syslog.h')
			cfg.set('HAVE_SYSLOG', cc.has_function('syslog'))
		endif
	endif
endif

# Examples build
build_examples = get_option('examples').enabled()

# Tests build
build_tests = get_option('tests').enabled()

# The -Wcast-function-type warning causes a flurry of warnings when compiling
# Windows with GCC 8 or later because of dynamically loaded functions
if backend == 'windows'
	c_args += cc.get_supported_arguments('-Wno-cast-function-type')
endif

# Some linkers do not support the '--add-stdcall-alias' option so check for it here
if backend == 'windows'
	c_link_args += cc.get_supported_link_arguments('-Wl,--add-stdcall-alias')
endif

c_args += cc.get_supported_arguments(
	'-Wshadow',
	'-Wunused',
	'-Wwrite-strings',
	'-Werror=format-security',
	'-Werror=implicit-function-declaration',
	'-Werror=implicit-int',
	'-Werror=init-self',
	'-Werror=missing-prototypes',
	'-Werror=strict-prototypes',
	'-Werror=undef',
	'-Werror=uninitialized'
)

# Meson: set properly some defines up and check pragma warnings up.

cfg.set('_GNU_SOURCE', backend == 'linux' or backend == 'darwin', description: 'Enable GNU extensions.')
if cc.has_function_attribute('visibility:default')
	default_visibility = '__attribute__ ((visibility ("default")))'
else
	default_visibility = ''
endif
cfg.set('DEFAULT_VISIBILITY', default_visibility, description: 'Define to the attribute for default visibility.')
if cc.get_id() != 'msvc'
	printf_format = '__attribute__ ((__format__ (__printf__, a, b)))'
else
	printf_format = ''
endif
cfg.set('PRINTF_FORMAT(a, b)', printf_format, description: 'Define to the attribute for enabling parameter checks on printf-like functions.')

# Meson: clang-cl in both modes defines _MSC_VER, rendering
# cc.get_argument_syntax useless to detect MSVC ABI compilers.
msc_ver = cc.get_define('_MSC_VER')

if msc_ver != ''
	if msc_ver.version_compare('<1800')
		error('Visual Studio 2013 or later is required.')
	elif msc_ver.version_compare('<=1900')
		# Visual Studio 2013 and 2015 do not support __func__
		cfg.set('__func__', '__FUNCTION__')
	elif msc_ver.version_compare('>=1900')
		# Visual Studio 2015 and later defines timespec
		cfg.set('_TIMESPEC_DEFINED', true)
	endif

	c_args += cc.get_supported_arguments(
		# Disable: warning C4127: conditional expression is constant
		'/wd4127',
		# Disable: warning C4200: nonstandard extension used : zero-sized array in struct/union
		'/wd4200',
		# Disable: warning C4201: nonstandard extension used : nameless struct/union
		'/wd4201',
		# Disable: warning C4324: structure was padded due to __declspec(align())
		'/wd4324',
		# Disable: warning C4996: 'GetVersionExA': was declared deprecated
		'/wd4996',
	)

	if cc.get_define('_PREFAST_') != ''
			c_args += cc.get_supported_arguments(
			# Disable "Banned API" errors when using the MS's WDK OACR/Prefast
			'/wd28719',
			# Disable "The function 'InitializeCriticalSection' must be called from within a try/except block"
			'/wd28125',
		)

	endif
endif

# Meson: check for getopt.c components.
# These are hardcoded in the MSVC config file.
cfg.set10('HAVE_STRING_H', cc.has_header('string.h'))

config_h = configure_file(
	output: 'config.h',
	configuration: cfg
)

fix_def = find_program('meson/fix_def.py', required: true)
windows = import('windows')

include_directories = [include_directories('.')]

# Meson: set getopt_dep separately.
needs_getopt = not cc.has_function('getopt')

if needs_getopt
	subdir('msvc')
endif
subdir('libusb')
if build_examples
	subdir('examples')
endif
if build_tests
	subdir('tests')
endif
subdir('doc')

pkg = import('pkgconfig')

pkg.generate(
	libusb,
	name: meson.project_name(),
	url: 'https://libusb.info',
	description: 'C API for USB device access from Linux, Mac OS X, Windows, OpenBSD/NetBSD and Solaris userspace'
)

meson.override_dependency(meson.project_name(), libusb_dep)
