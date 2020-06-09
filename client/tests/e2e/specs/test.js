// https://docs.cypress.io/api/introduction/api.html

describe('Loads Page', () => {
  it('Visits the app root url', () => {
    cy.visit('/')
    cy.contains('span', 'Study Monitor')
  })
})
