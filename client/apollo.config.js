const path = require('path')

// Load .env files
const env = require('../asc-secret.json')

module.exports = {
  client: {
    service: 'ascstudymontior',
    includes: ['src/**/*.{js,vue,gql}'],
  },
  service: {
    name: 'ascstudymontior',
    localSchemaFile: path.resolve(__dirname, '../backend/schema.graphql'),
  },
  engine: {
    endpoint: 'http://localhost:5000/graphql',
    apiKey: env.VUE_APP_APOLLO_ENGINE_KEY,
  },
}
