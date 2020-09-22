## Server Routing

| Route                 | Destination                          |
| --------------------- | ------------------------------------ |
| `/` <br/>             | Backend template <br/>               |
| `/index.html`         | `./client/dist/index.html`           |
| `/js/*` <br/>         | Static Files <br/>                   |
| `/css/*` <br/>        | from `./client/dist`                 |
| `/img/*`              |                                      |
| `/robots.txt`         | Static File from `./backend/sitemap` |
| `/sitemap.xml`        | Backend                              |
| `/p/<slug>`           | Backend template <br/>               |
|                       | from `./client/dist/index.html`      |
| `/p/<slug>/download`  | Backend                              |
| `/graphql`            | Redirect to `/graphql/`              |
| `/graphql/`           | Backend                              |
| `/*`                  | Backend at `index.html`              |
| --------------------- | ------------------------------------ |
