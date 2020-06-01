const webpack = require('webpack')

var git = require('git-rev-sync')

const getGitHash = () => {
  try {
    return git.short()
  } catch {
    // As a fallback for docker builds, try env var
    return process.env.SOURCE_COMMIT.slice(0, 7)
  }
}

module.exports = {
  lintOnSave: process.env.NODE_ENV !== 'production',
  configureWebpack: {
    optimization: {
      splitChunks: {
        minSize: 30000,
        maxSize: 250000,
      },
    },
  },
  chainWebpack: config => {
    config.plugin('define').tap(definitions => {
      const pkgVersion = JSON.stringify(require('./package.json').version)
      const hash = getGitHash()
      definitions[0]['process.env']['VERSION'] = pkgVersion
      definitions[0]['process.env']['COMMIT_HASH'] = `"${hash}"` // prettier-ignore
      return definitions
    })
  },
}
