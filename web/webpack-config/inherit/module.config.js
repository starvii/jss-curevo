const debug = process.env.NODE_ENV !== 'production';
const dirVars = require('../base/dir-vars.config');

exports = module.exports = {
    rules: [
        {
            test: /\.vue$/,
            use: [{
                loader: 'vue-loader',
                options: {
                    loaders: {
                        // js: 'babel-loader?{"presets":["es2015", "stage-3"],"plugins": ["transform-runtime", "transform-object-rest-spread"]}',
                        js: 'babel-loader?{"presets":["env"],"plugins": ["transform-runtime", "transform-object-rest-spread"]}',
                        css: 'vue-style-loader!css-loader'
                    }
                }
            }],
            include: dirVars.srcRootDir,
            exclude: /node_modules/
        },
        {
            test: /\.js$/,
            use: [
                {
                    loader: 'babel-loader',
                    options: {
                        // presets: ['es2015', 'stage-3'],
                        presets: ['env'],
                        plugins: ["transform-runtime", 'transform-object-rest-spread'],
                        comments: debug,
                    }
                }
            ],
            exclude: /node_modules/
        },
        {
            test: /\.css$/,
            use: [{
                loader: 'style-loader',
            }, {
                loader: 'css-loader',
            }, /*{
                loader: 'postcss-loader',
            }*/],
            exclude: [
                dirVars.srcRootDir
            ],
        },
        {
            test: /\.(png|gif|jpg)$/,
            use: ['file-loader']
        },
        {
            test: /\.less$/,
            use: [{
                loader: "style-loader" // creates style nodes from JS strings
            }, {
                loader: "css-loader" // translates CSS into CommonJS
            }, {
                loader: "less-loader" // compiles Less to CSS
            }]
        },
        {test: /\.woff(\?v=\d+\.\d+\.\d+)?$/, loader: "url-loader?limit=10240&mimetype=application/font-woff"},
        {test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/, loader: "url-loader?limit=10240&mimetype=application/font-woff"},
        {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: "url-loader?limit=10240&mimetype=application/octet-stream"},
        {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: "file-loader"},
        {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: "url-loader?limit=10240&mimetype=image/svg+xml"},
        // {test: require.resolve('jquery'), loader: 'expose-loader?jQuery'},
    ],
};