const webpack_resolve = {
    extensions: [
        '.js',
        '.css',
        '.vue',
    ],
    alias: {
        'jquery': 'jquery/dist/jquery.js',
        'semantic-css': 'semantic-ui/src/semantic.less',
        'semantic-js': 'semantic-ui/dist/semantic.js',
    },
};

exports = module.exports = webpack_resolve;