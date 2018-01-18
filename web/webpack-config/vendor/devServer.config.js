const dirVars = require('../base/dir-vars.config');

exports = module.exports = {
    host: '127.0.0.1',
    port: 8080, // 默认8080
    contentBase: dirVars.buildDir,
    hot: true,
    inline: true,
    compress: true,
    quiet: false,
    noInfo: false,
    lazy: false,
    // 将 api 服务器 代理至本地
    proxy: {
        '/api': {
            target: 'http://10.0.0.3:9001',
            secure: false,
        },
    },
};