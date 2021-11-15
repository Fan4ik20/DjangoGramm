const path = require("path");
const webpack = require("webpack");

module.exports = {
    entry: '../django_gramm/static/django_gramm/js/src/main.js',
    output: {
        path: path.resolve(__dirname,
            '../django_gramm/static/django_gramm/js/dist/'),
        filename: 'bundle.js'
    },
    mode: "development",
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery'
    }),
    ],
    resolve: {
        modules: [path.resolve(__dirname, 'node_modules')]
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ]
      }
};