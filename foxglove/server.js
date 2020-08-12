const puppeteer = require('puppeteer')
const assert = require('assert')
const fs = require('fs')
const path = require('path')
const axios = require('axios')
const os = require('os')

const fastify = require('fastify')({
  logger: process.env.NODE_ENV !== 'production',
})

let browser

fastify.register(require('point-of-view'), {
  engine: {
    ejs: require('ejs'),
  },
})

fastify.get('/canvas/:id', async (req, reply) => {
  const id = req.params.id
  const publication = await axios
    .get(`http://localhost:5000/documents/${id}`)
    .then(doc => doc.data)
  if (!publication)
    return reply.code(404).type('text/html').send(`Publication ${id} not found`)

  return reply.view('/thumbnail.ejs', { publication })
})

fastify.get('/thumbnail/:id', async (req, reply) => {
  const id = req.params.id

  const page = await browser.newPage()
  const response = await page.goto('http://localhost:7000/canvas/' + id)

  assert.equal(response.status(), 200, 'Service did not provide thumbnail')

  const screen = await page.screenshot()

  reply.header('Content-Type', 'image/png').send(screen)
})

fastify.get('/background.png', async (req, reply) => {
  reply.send(fs.createReadStream(path.join(__dirname, 'background.png')))
})

fastify.listen(7000, async function (err, address) {
  browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    defaultViewport: {
      width: 1200,
      height: 628,
      isLandscape: true,
    },
  })

  if (err) {
    await browser.close()
    fastify.log.error(err)
    process.exit(1)
  }
  fastify.log.info(`server listening on ${address}`)
})
