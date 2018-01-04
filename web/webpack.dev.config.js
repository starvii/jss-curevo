/* 注意：webpack配置文件只能使用 Common JS 语法 */

const webpackConfig = {
    devServer: require('./webpack-config/vendor/devServer.config'),

    entry: require('./webpack-config/entry.config'),

    output: require('./webpack-config/output.config'),

    module: require('./webpack-config/module.dev.config'),

    resolve: require('./webpack-config/resolve.config'),

    plugins: require('./webpack-config/plugins.dev.config'),

    externals: require('./webpack-config/externals.config'),
};

exports = module.exports = webpackConfig;
