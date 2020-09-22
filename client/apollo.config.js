const path = require('path')

// Load .env files
// const env = require('../asc-secret.json')

module.exports = {
  client: {
    service: {
      localSchemaFile: path.resolve(__dirname, '../schema.graphql'),
    },
    includes: ['src/**/*.{js,vue,gql}'],
  },
}
