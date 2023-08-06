//
// This file auto-generated with generate-wrappers.js
// Date: Tue Dec 19 2017 10:52:06 GMT+0100 (W. Europe Standard Time)
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');

var BaseGeometryModel = require('../core/BaseGeometry.autogen.js').BaseGeometryModel;


var EdgesGeometryModel = BaseGeometryModel.extend({

    defaults: function() {
        return _.extend(BaseGeometryModel.prototype.defaults.call(this), {


        });
    },

    constructThreeObject: function() {

        var result = new THREE.EdgesGeometry();
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        BaseGeometryModel.prototype.createPropertiesArrays.call(this);

        this.props_created_by_three['type'] = true;



    },

}, {

    model_name: 'EdgesGeometryModel',

    serializers: _.extend({
    },  BaseGeometryModel.serializers),
});

module.exports = {
    EdgesGeometryModel: EdgesGeometryModel,
};
