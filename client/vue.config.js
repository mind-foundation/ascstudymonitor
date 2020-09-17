const git = require('git-rev-sync')
const path = require('path')

const getGitHash = () => {
  let hash = ''
  try {
    hash = git.short()
  } catch {
    // As a fallback for docker builds, try env var
    if (process.env['SOURCE_COMMIT']) {
      hash = process.env['SOURCE_COMMIT'].slice(0, 7)
    }
  }

  if (!hash) {
    throw Error('No commit hash found')
  }

  return hash
}

const analyzeBundle = false

module.exports = {
  lintOnSave: true, //process.env.NODE_ENV !== 'production',
  configureWebpack: {
    devtool: 'source-map',
    optimization: {
      splitChunks: {
        minSize: 100000,
        maxSize: 300000,
      },
    },
  },
  devServer: {
    // enables debugging on remote iPad :)
    disableHostCheck: true,
  },
  ...(analyzeBundle && {
    pluginOptions: {
      webpackBundleAnalyzer: {
        openAnalyzer: false,
      },
    },
  }),
  chainWebpack: config => {
    if (analyzeBundle) {
      const BundleAnalyzerPlugin = require('webpack-bundle-analyzer')
        .BundleAnalyzerPlugin
      config
        .plugin('webpack-bundle-analyzer')
        .use(BundleAnalyzerPlugin)
        .init(Plugin => new Plugin({}))
    }

    config.resolve.alias.set('assets', path.resolve(__dirname, 'assets'))

    config.plugin('define').tap(definitions => {
      const pkgVersion = JSON.stringify(require('./package.json').version)
      const hash = getGitHash()
      definitions[0]['process.env']['VERSION'] = pkgVersion
      definitions[0]['process.env']['COMMIT_HASH'] = `"${hash}"` // prettier-ignore
      return definitions
    })
  },
}
