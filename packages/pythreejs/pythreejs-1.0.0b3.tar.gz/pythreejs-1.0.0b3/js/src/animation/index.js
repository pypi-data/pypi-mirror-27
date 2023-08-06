//
// This file auto-generated with generate-wrappers.js
// Date: Tue Dec 19 2017 10:52:07 GMT+0100 (W. Europe Standard Time)
//
// Load all three.js python wrappers
var loadedModules = [
    require('./AnimationAction.js'),
    require('./AnimationClip.autogen.js'),
    require('./AnimationMixer.autogen.js'),
    require('./AnimationObjectGroup.autogen.js'),
    require('./AnimationUtils.autogen.js'),
    require('./KeyframeTrack.autogen.js'),
    require('./PropertyBinding.autogen.js'),
    require('./PropertyMixer.autogen.js'),
    require('./tracks'),
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

