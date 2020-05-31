const webpack = require('webpack')

var git = require('git-rev-sync')

module.exports = {
  lintOnSave: process.env.NODE_ENV !== 'production',
  chainWebpack: config => {
    config.plugin('define').tap(definitions => {
      const pkgVersion = JSON.stringify(require('../package.json').version)
      const hash = git.short()
      definitions[0]['process.env']['VERSION'] = pkgVersion
      definitions[0]['process.env']['COMMIT_HASH'] = `"${hash}"` // prettier-ignore

      console.info('💫 ', pkgVersion, ' - ', hash)
      return definitions
    })
  },
}
