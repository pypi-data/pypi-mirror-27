//
// This file auto-generated with generate-wrappers.js
// Date: Fri Dec 15 2017 14:52:39 GMT+0100 (W. Europe Standard Time)
//
// Load all three.js python wrappers
var loadedModules = [
    require('./Controls.autogen.js'),
    require('./FlyControls.js'),
    require('./OrbitControls.js'),
    require('./Picker.js'),
    require('./TrackballControls.js'),
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

