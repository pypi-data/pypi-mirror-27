//
// This file auto-generated with generate-wrappers.js
// Date: Fri Dec 15 2017 14:52:38 GMT+0100 (W. Europe Standard Time)
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');

var PerspectiveCameraModel = require('./PerspectiveCamera.js').PerspectiveCameraModel;


var ArrayCameraModel = PerspectiveCameraModel.extend({

    defaults: function() {
        return _.extend(PerspectiveCameraModel.prototype.defaults.call(this), {


        });
    },

    constructThreeObject: function() {

        var result = new THREE.ArrayCamera(
            this.convertFloatModelToThree(this.get('fov'), 'fov'),
            this.convertFloatModelToThree(this.get('aspect'), 'aspect'),
            this.convertFloatModelToThree(this.get('near'), 'near'),
            this.convertFloatModelToThree(this.get('far'), 'far')
        );
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        PerspectiveCameraModel.prototype.createPropertiesArrays.call(this);

        this.props_created_by_three['matrixWorldInverse'] = true;
        this.props_created_by_three['projectionMatrix'] = true;
        this.props_created_by_three['type'] = true;
        this.props_created_by_three['rotation'] = true;
        this.props_created_by_three['quaternion'] = true;
        this.props_created_by_three['matrixWorldNeedsUpdate'] = true;



    },

}, {

    model_name: 'ArrayCameraModel',

    serializers: _.extend({
    },  PerspectiveCameraModel.serializers),
});

module.exports = {
    ArrayCameraModel: ArrayCameraModel,
};
