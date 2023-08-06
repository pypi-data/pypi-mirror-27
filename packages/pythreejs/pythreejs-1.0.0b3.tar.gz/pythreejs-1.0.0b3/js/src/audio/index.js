//
// This file auto-generated with generate-wrappers.js
// Date: Tue Dec 19 2017 10:52:07 GMT+0100 (W. Europe Standard Time)
//
// Load all three.js python wrappers
var loadedModules = [
    require('./Audio.autogen.js'),
    require('./AudioAnalyser.autogen.js'),
    require('./AudioListener.autogen.js'),
    require('./PositionalAudio.autogen.js'),
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

