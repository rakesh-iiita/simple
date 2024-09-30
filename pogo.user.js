
;(function () {	// eslint-disable-line no-extra-semi
	'use strict';

	const plugin_info = {};
	if (typeof GM_info !== 'undefined' && GM_info && GM_info.script) {
		plugin_info.script = {
			version: GM_info.script.version,
			name: GM_info.script.name,
			description: GM_info.script.description
		};
	}


	const setup = function () {

		alert('The iitc-plugin-pogo, "pogo for portals" plugin is outdated and its features are included in "s2Check".\r\n' +
			'Please, uninstall this plugin to avoid conflicts');

	};


	setup.info = plugin_info; //add the script info data to the function as a property
	if (!window.bootPlugins) {
		window.bootPlugins = [];
	}
	window.bootPlugins.push(setup);
	// if IITC has already booted, immediately run the 'setup' function
	if (window.iitcLoaded && typeof setup === 'function') {
		setup();
	}
})();
