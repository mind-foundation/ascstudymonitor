# Foxglove

> Service for providing generating publication thumbnails

Requests document metadata from local network to render title on static background image.
The viewport of the rendered document is governed by the css in the head of the template’s.

#### Installation and development

- `yarn install`
- `yarn run dev`

### Run in production

- `yarn install`
- `yarn start`

### API

> Get thumbnail of publication with id `publicationId` (primary endpoint)

- `/thumbnail/:publicationId`

> Serve intermediary page for publication (for debugging / development)

- `/canvas/:publicationId`
