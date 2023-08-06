//
// This file auto-generated with generate-wrappers.js
// Date: Fri Dec 15 2017 14:52:39 GMT+0100 (W. Europe Standard Time)
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');

var KeyframeTrackModel = require('../KeyframeTrack.autogen.js').KeyframeTrackModel;


var VectorKeyframeTrackModel = KeyframeTrackModel.extend({

    defaults: function() {
        return _.extend(KeyframeTrackModel.prototype.defaults.call(this), {


        });
    },

    constructThreeObject: function() {

        var result = new THREE.VectorKeyframeTrack(
            this.get('name'),
            this.convertArrayBufferModelToThree(this.get('times'), 'times'),
            this.convertArrayBufferModelToThree(this.get('values'), 'values'),
            this.convertEnumModelToThree(this.get('interpolation'), 'interpolation')
        );
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        KeyframeTrackModel.prototype.createPropertiesArrays.call(this);




    },

}, {

    model_name: 'VectorKeyframeTrackModel',

    serializers: _.extend({
    },  KeyframeTrackModel.serializers),
});

module.exports = {
    VectorKeyframeTrackModel: VectorKeyframeTrackModel,
};
