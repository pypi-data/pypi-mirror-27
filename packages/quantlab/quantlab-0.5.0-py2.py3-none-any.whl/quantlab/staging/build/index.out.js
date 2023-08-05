require('es6-promise/auto');  // polyfill Promise on IE

var PageConfig = require('@quantlab/coreutils').PageConfig;
__webpack_public_path__ = PageConfig.getOption('publicUrl');

// This needs to come after __webpack_public_path__ is set.
require('font-awesome/css/font-awesome.min.css');
var app = require('@quantlab/application').QuantLab;


function main() {
    // Get the disabled extensions.
    var disabled = { patterns: [], matches: [] };
    var disabledExtensions = [];
    try {
        var option = PageConfig.getOption('disabledExtensions');
        if (option) {
            disabledExtensions = JSON.parse(option).map(function(pattern) {
                disabled.patterns.push(pattern);
                return { raw: pattern, rule: new RegExp(pattern) };
            });
        }
    } catch (error) {
        console.warn('Unable to parse disabled extensions.', error);
    }

    // Get the deferred extensions.
    var deferred = { patterns: [], matches: [] };
    var deferredExtensions = [];
    var ignorePlugins = [];
    try {
        var option = PageConfig.getOption('deferredExtensions');
        if (option) {
            deferredExtensions = JSON.parse(option).map(function(pattern) {
                deferred.patterns.push(pattern);
                return { raw: pattern, rule: new RegExp(pattern) };
            });
        }
    } catch (error) {
        console.warn('Unable to parse deferred extensions.', error);
    }

    function isDeferred(value) {
        return deferredExtensions.some(function(pattern) {
            return pattern.raw === value || pattern.rule.test(value)
        })
    }

    function isDisabled(value) {
        return disabledExtensions.some(function(pattern) {
            return pattern.raw === value || pattern.rule.test(value)
        });
    }

    var version = PageConfig.getOption('appVersion') || 'unknown';
    var name = PageConfig.getOption('appName') || 'QuantLab';
    var namespace = PageConfig.getOption('appNamespace') || 'quantlab';
    var devMode = PageConfig.getOption('devMode') || 'false';
    var settingsDir = PageConfig.getOption('settingsDir') || '';
    var assetsDir = PageConfig.getOption('assetsDir') || '';
    var register = [];

    if (version[0] === 'v') {
        version = version.slice(1);
    }

    // Handle the registered mime extensions.
    var mimeExtensions = [];
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/json-extension')) {
            disabled.matches.push('@quantlab/json-extension');
        } else {
            var module = require('@quantlab/json-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    mimeExtensions.push(plugin);
                });
            } else {
                mimeExtensions.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/pdf-extension')) {
            disabled.matches.push('@quantlab/pdf-extension');
        } else {
            var module = require('@quantlab/pdf-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    mimeExtensions.push(plugin);
                });
            } else {
                mimeExtensions.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/vdom-extension')) {
            disabled.matches.push('@quantlab/vdom-extension');
        } else {
            var module = require('@quantlab/vdom-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    mimeExtensions.push(plugin);
                });
            } else {
                mimeExtensions.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }

    // Handled the registered standard extensions.
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/application-extension')) {
            disabled.matches.push('@quantlab/application-extension');
        } else {
            var module = require('@quantlab/application-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/apputils-extension')) {
            disabled.matches.push('@quantlab/apputils-extension');
        } else {
            var module = require('@quantlab/apputils-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/calendar-extension')) {
            disabled.matches.push('@quantlab/calendar-extension');
        } else {
            var module = require('@quantlab/calendar-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/codemirror-extension')) {
            disabled.matches.push('@quantlab/codemirror-extension');
        } else {
            var module = require('@quantlab/codemirror-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/completer-extension')) {
            disabled.matches.push('@quantlab/completer-extension');
        } else {
            var module = require('@quantlab/completer-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/console-extension')) {
            disabled.matches.push('@quantlab/console-extension');
        } else {
            var module = require('@quantlab/console-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/csvviewer-extension')) {
            disabled.matches.push('@quantlab/csvviewer-extension');
        } else {
            var module = require('@quantlab/csvviewer-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/docmanager-extension')) {
            disabled.matches.push('@quantlab/docmanager-extension');
        } else {
            var module = require('@quantlab/docmanager-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/filebrowser-extension')) {
            disabled.matches.push('@quantlab/filebrowser-extension');
        } else {
            var module = require('@quantlab/filebrowser-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/fileeditor-extension')) {
            disabled.matches.push('@quantlab/fileeditor-extension');
        } else {
            var module = require('@quantlab/fileeditor-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/help-extension')) {
            disabled.matches.push('@quantlab/help-extension');
        } else {
            var module = require('@quantlab/help-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/highcharts-extension')) {
            disabled.matches.push('@quantlab/highcharts-extension');
        } else {
            var module = require('@quantlab/highcharts-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/imageviewer-extension')) {
            disabled.matches.push('@quantlab/imageviewer-extension');
        } else {
            var module = require('@quantlab/imageviewer-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/inspector-extension')) {
            disabled.matches.push('@quantlab/inspector-extension');
        } else {
            var module = require('@quantlab/inspector-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/launcher-extension')) {
            disabled.matches.push('@quantlab/launcher-extension');
        } else {
            var module = require('@quantlab/launcher-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/mainmenu-extension')) {
            disabled.matches.push('@quantlab/mainmenu-extension');
        } else {
            var module = require('@quantlab/mainmenu-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/markdownviewer-extension')) {
            disabled.matches.push('@quantlab/markdownviewer-extension');
        } else {
            var module = require('@quantlab/markdownviewer-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/notebook-extension')) {
            disabled.matches.push('@quantlab/notebook-extension');
        } else {
            var module = require('@quantlab/notebook-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/running-extension')) {
            disabled.matches.push('@quantlab/running-extension');
        } else {
            var module = require('@quantlab/running-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/settingeditor-extension')) {
            disabled.matches.push('@quantlab/settingeditor-extension');
        } else {
            var module = require('@quantlab/settingeditor-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/shortcuts-extension')) {
            disabled.matches.push('@quantlab/shortcuts-extension');
        } else {
            var module = require('@quantlab/shortcuts-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/spreadsheet-extension')) {
            disabled.matches.push('@quantlab/spreadsheet-extension');
        } else {
            var module = require('@quantlab/spreadsheet-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/tabmanager-extension')) {
            disabled.matches.push('@quantlab/tabmanager-extension');
        } else {
            var module = require('@quantlab/tabmanager-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/terminal-extension')) {
            disabled.matches.push('@quantlab/terminal-extension');
        } else {
            var module = require('@quantlab/terminal-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/theme-dark-extension')) {
            disabled.matches.push('@quantlab/theme-dark-extension');
        } else {
            var module = require('@quantlab/theme-dark-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/theme-light-extension')) {
            disabled.matches.push('@quantlab/theme-light-extension');
        } else {
            var module = require('@quantlab/theme-light-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }
    try {
        if (isDeferred('')) {
            deferred.matches.push('');
            ignorePlugins.push('');
        }
        if (isDisabled('@quantlab/tooltip-extension')) {
            disabled.matches.push('@quantlab/tooltip-extension');
        } else {
            var module = require('@quantlab/tooltip-extension/');
            var extension = module.default;

            // Handle CommonJS exports.
            if (!module.hasOwnProperty('__esModule')) {
              extension = module;
            }

            if (Array.isArray(extension)) {
                extension.forEach(function(plugin) {
                    if (isDeferred(plugin.id)) {
                        deferred.matches.push(plugin.id);
                        ignorePlugins.push(plugin.id);
                    }
                    if (isDisabled(plugin.id)) {
                        disabled.matches.push(plugin.id);
                        return;
                    }
                    register.push(plugin);
                });
            } else {
                register.push(extension);
            }
        }
    } catch (e) {
        console.error(e);
    }

    quantlab = new app({
        namespace: namespace,
        name: name,
        version: version,
        devMode: devMode.toLowerCase() === 'true',
        settingsDir: settingsDir,
        assetsDir: assetsDir,
        mimeExtensions: mimeExtensions,
        disabled: disabled,
        deferred: deferred
    });
    register.forEach(function(item) { quantlab.registerPluginModule(item); });
    quantlab.start({ ignorePlugins: ignorePlugins });

    // Handle a selenium test.
    var seleniumTest = PageConfig.getOption('seleniumTest');
    if (seleniumTest.toLowerCase() === 'true') {
        var caught_errors = []
        window.onerror = function(msg, url, line, col, error) {
           caught_errors.push(String(error));
        };
        console.error = function(message) {
            caught_errors.push(String(message));
        }
        quantlab.restored.then(function() {
            var el = document.createElement('div');
            el.id = 'seleniumResult';
            el.textContent = JSON.stringify(caught_errors);
            document.body.appendChild(el);
        });
    }

}

window.addEventListener('load', main);
