//
// This file auto-generated with generate-wrappers.js
// Date: Tue Dec 19 2017 10:52:06 GMT+0100 (W. Europe Standard Time)
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');

var ShaderMaterialModel = require('./ShaderMaterial.autogen.js').ShaderMaterialModel;


var RawShaderMaterialModel = ShaderMaterialModel.extend({

    defaults: function() {
        return _.extend(ShaderMaterialModel.prototype.defaults.call(this), {


        });
    },

    constructThreeObject: function() {

        var result = new THREE.RawShaderMaterial(
            {
            }
        );
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        ShaderMaterialModel.prototype.createPropertiesArrays.call(this);

        this.props_created_by_three['extensions'] = true;
        this.props_created_by_three['type'] = true;



    },

}, {

    model_name: 'RawShaderMaterialModel',

    serializers: _.extend({
    },  ShaderMaterialModel.serializers),
});

module.exports = {
    RawShaderMaterialModel: RawShaderMaterialModel,
};
