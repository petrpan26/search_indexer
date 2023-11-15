/** @type {import('next').NextConfig} */
var webpack = require('webpack');

const nextConfig = {
    output: 'export',
    webpack: (config) => {
        config.experiments = {
            ...config.experiments,
            topLevelAwait: true,
        }
        config.resolve.fallback = {
            process: require.resolve('process/browser'),
            zlib: require.resolve('browserify-zlib'),
            stream: require.resolve('stream-browserify'),
            util: require.resolve('util'),
            buffer: require.resolve('buffer'),
            asset: require.resolve('assert'),
        }
        config.externals.push({ sharp: 'commonjs sharp', canvas: 'commonjs canvas' })
        config.plugins.push(
            new webpack.ProvidePlugin({
              Buffer: ['buffer', 'Buffer'],
              process: 'process/browser',
            })
        )
        return config
    }
}

module.exports = nextConfig
