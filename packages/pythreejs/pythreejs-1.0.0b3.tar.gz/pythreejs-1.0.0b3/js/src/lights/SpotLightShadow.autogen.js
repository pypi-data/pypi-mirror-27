//
// This file auto-generated with generate-wrappers.js
// Date: Tue Dec 19 2017 10:52:06 GMT+0100 (W. Europe Standard Time)
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');

var LightShadowModel = require('./LightShadow.js').LightShadowModel;


var SpotLightShadowModel = LightShadowModel.extend({

    defaults: function() {
        return _.extend(LightShadowModel.prototype.defaults.call(this), {


        });
    },

    constructThreeObject: function() {

        var result = new THREE.SpotLightShadow();
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        LightShadowModel.prototype.createPropertiesArrays.call(this);




    },

}, {

    model_name: 'SpotLightShadowModel',

    serializers: _.extend({
    },  LightShadowModel.serializers),
});

module.exports = {
    SpotLightShadowModel: SpotLightShadowModel,
};
