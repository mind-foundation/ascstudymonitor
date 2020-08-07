const git = require('git-rev-sync')

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
  lintOnSave: false, //process.env.NODE_ENV !== 'production',
  configureWebpack: {
    optimization: {
      splitChunks: {
        minSize: 30000,
        maxSize: 250000,
      },
    },
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
      // const BundleAnalyzerPlugin = require('webpack-bundle-analyzer')
      //   .BundleAnalyzerPlugin
      // config
      //   .plugin('webpack-bundle-analyzer')
      //   .use(BundleAnalyzerPlugin)
      //   .init(Plugin => new Plugin({}))
    }

    config.plugin('define').tap(definitions => {
      const pkgVersion = JSON.stringify(require('./package.json').version)
      const hash = getGitHash()
      definitions[0]['process.env']['VERSION'] = pkgVersion
      definitions[0]['process.env']['COMMIT_HASH'] = `"${hash}"` // prettier-ignore
      return definitions
    })
  },
}
