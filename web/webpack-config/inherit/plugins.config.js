const dirVars = require('../base/dir-vars.config');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

exports = module.exports = [
    new HtmlWebpackPlugin({
        filename: 'index.html',
        inject: 'body',
        template: dirVars.srcRootDir + '/index.template.html',
        favicon: dirVars.srcRootDir + '/img/favicon.ico',
        hash: false
    }),
    new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery',
        jquery: 'jquery',
        'window.jQuery': 'jquery',
        'window.$': 'jquery',
    }),
];