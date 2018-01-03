/* 注意：webpack配置文件只能使用 Common JS 语法 */

const webpackConfig = {
    entry: require('./webpack-config/entry.config'),

    output: require('./webpack-config/output.config'),

    module: require('./webpack-config/module.product.config'),

    resolve: require('./webpack-config/resolve.config'),

    plugins: require('./webpack-config/plugins.product.config'),
};

exports = module.exports = webpackConfig;
