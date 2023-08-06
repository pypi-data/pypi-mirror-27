//
// This file auto-generated with generate-wrappers.js
// Date: Fri Dec 15 2017 14:52:39 GMT+0100 (W. Europe Standard Time)
//

// Export widget models and views, and the npm package version number.
module.exports['version'] = require('../package.json').version;

// Load all three.js python wrappers
var loadedModules = [
    require('./_base'),
    require('./animation'),
    require('./audio'),
    require('./cameras'),
    require('./controls'),
    require('./core'),
    require('./examples'),
    require('./extras'),
    require('./geometries'),
    require('./helpers'),
    require('./jupyterlab-plugin.js'),
    require('./lights'),
    require('./loaders'),
    require('./materials'),
    require('./math'),
    require('./objects'),
    require('./renderers'),
    require('./scenes'),
    require('./textures'),
];

for (var i in loadedModules) {
    if (loadedModules.hasOwnProperty(i)) {
        var loadedModule = loadedModules[i];
        for (var target_name in loadedModule) {
            if (loadedModule.hasOwnProperty(target_name)) {
                module.exports[target_name] = loadedModule[target_name];
            }
        }
    }
}

