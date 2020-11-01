// From https://dev.to/aisone/getting-vite-vue-3-and-apollo-client-3-running-51bp
import { ApolloClient, HttpLink, split } from '@apollo/client/core'
import { InMemoryCache } from '@apollo/client/cache'
import { setContext } from '@apollo/client/link/context'
import { getMainDefinition } from '@apollo/client/utilities'

const API_BASE =
  process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000'

// Create the apollo client
export const apolloClient = new ApolloClient({
  link: new HttpLink({
    // You should use an absolute URL here
    uri: API_BASE + '/graphql/',
  }),
  cache: new InMemoryCache(),
  connectToDevTools: true,
  onError: ({ graphQLErrors, networkError }) => {
    if (networkError) console.log('networkError', networkError)
    if (graphQLErrors) {
      for (let err of graphQLErrors) {
        if (err.name === 'AuthenticationError') {
        }
        console.dir('graphQLErrors', err)
      }
    }
  },
})
