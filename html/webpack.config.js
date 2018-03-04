const CopyWebpackPlugin = require('copy-webpack-plugin')
const path = require('path')

module.exports = {
  context: path.join(__dirname, 'source'),
  entry: {
    'index': './index.js',
  },
  output: {
    path: path.join(__dirname, 'build'),
    filename: '[name].js',
  },
  module: {
    rules: [{
      exclude: /node_modules/,
      test: /\.js$/,
      use: [{
        loader: 'babel-loader',
        options: {
          presets: ['env'],
        },
      }],
    }],
  },
  plugins: [
    new CopyWebpackPlugin([{
      from: '**/*',
      ignore: ['*.js'],
    }]),
  ],
}