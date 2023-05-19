doxygen_exe = find_program('doxygen', required: false)

if doxygen_exe.found()
	doxygen_conf = configuration_data()

	doxygen_conf.set('PACKAGE_VERSION', meson.project_version())
	doxygen_conf.set('DOXYGEN_HTMLDIR', 'api-1.0')
	doxygen_conf.set('top_srcdir', meson.project_source_root())

	doxyfile = configure_file(
		input: 'doxygen.cfg.in',
		output: 'Doxyfile',
		configuration: doxygen_conf,
	)

	custom_target(
		'docs',
		input: doxyfile,
		output: 'api-1.0',
		command: [doxygen_exe, doxyfile],
		depend_files: files(
			'libusb.png',
		),
		console: true,
		install: true,
		install_dir: get_option('datadir') / 'doc' / meson.project_name(),
	)
endif

