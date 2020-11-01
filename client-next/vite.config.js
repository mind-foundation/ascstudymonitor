const path = require('path')
const graphqlPlugin = require('vite-plugin-graphql')

module.exports = {
  alias: {
    '/@/': path.resolve(__dirname, 'src'),
    os: path.resolve(__dirname, 'src/shim'),
  },
  plugins: [graphqlPlugin],
  optimizeDeps: {
    allowNodeBuiltins: ['vite-plugin-graphql'],
  },
}
