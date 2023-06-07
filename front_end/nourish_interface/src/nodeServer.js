// Node.js server code using Express

const express = require('express');
const app = express();
const port = 3001;

const pgp = require('pg-promise')();
const db = pgp('postgres://rhenry:6rufbM90Dt@awesome-hw.sdsc.edu:5432/nourish');

app.get('/users', async (req, res) => {
  const users = await db.any('SELECT * FROM registrants');
  res.json(users);
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});





