//
// This file auto-generated with generate-wrappers.js
// Date: Fri Dec 15 2017 14:09:57 GMT+0100 (W. Europe Standard Time)
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');

var InterleavedBufferModel = require('./InterleavedBuffer.autogen.js').InterleavedBufferModel;


var InstancedInterleavedBufferModel = InterleavedBufferModel.extend({

    defaults: function() {
        return _.extend(InterleavedBufferModel.prototype.defaults.call(this), {

            meshPerAttribute: 1,

        });
    },

    constructThreeObject: function() {

        var result = new THREE.InstancedInterleavedBuffer(
            this.convertArrayBufferModelToThree(this.get('array'), 'array'),
            this.get('meshPerAttribute')
        );
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        InterleavedBufferModel.prototype.createPropertiesArrays.call(this);

        this.props_created_by_three['version'] = true;
        this.props_created_by_three['needsUpdate'] = true;

        this.property_converters['meshPerAttribute'] = null;


    },

}, {

    model_name: 'InstancedInterleavedBufferModel',

    serializers: _.extend({
    },  InterleavedBufferModel.serializers),
});

module.exports = {
    InstancedInterleavedBufferModel: InstancedInterleavedBufferModel,
};
