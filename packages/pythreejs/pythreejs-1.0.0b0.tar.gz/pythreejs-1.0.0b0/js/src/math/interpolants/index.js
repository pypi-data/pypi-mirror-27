//
// This file auto-generated with generate-wrappers.js
// Date: Fri Dec 15 2017 14:09:58 GMT+0100 (W. Europe Standard Time)
//
// Load all three.js python wrappers
var loadedModules = [
    require('./CubicInterpolant.autogen.js'),
    require('./DiscreteInterpolant.autogen.js'),
    require('./LinearInterpolant.autogen.js'),
    require('./QuaternionLinearInterpolant.autogen.js'),
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

