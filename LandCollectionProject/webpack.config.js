const path = require('path');
const webpack = require('webpack');


module.exports = {
    module: {
        rules:[
            { test: /\.css$/, use: [ 'style-loader', 'css-loader' ] }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        })
    ],


    entry: {
        card: './assets/JS/singleItem.js',
        page: './assets/JS/multiItem.js',
        default:'./assets/JS/base.js',

      },
      output: {
        filename: '[name].js',
        path: path.resolve(__dirname, '','static')
    },
    optimization: {
        minimize: true,
      }

}