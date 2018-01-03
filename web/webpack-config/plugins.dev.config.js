const webpack = require('webpack');
const pluginsConfig = require('./inherit/plugins.config');

pluginsConfig.push(new webpack.DefinePlugin({
    IS_PRODUCTION: false,
}));

exports = module.exports = pluginsConfig;