// Node.js server code using Express
require("dotenv").config()
const express = require('express');
const pgp = require('pg-promise')();
const { v4: uuid } = require('uuid')

const app = express();
const port = process.env.PORT || 3001;

const db = pgp(process.env.DB_URI);
app.use(express.json())
app.get('/users', async (req, res) => {
  const users = await db.any('SELECT * FROM registrants');
  res.json(users);
});

app.post('/test', async (req, res) => {
  const columns = ["first_name", "last_name", "middle_name", "gender", "home_street_address", "primary_email","email", "phone", "ethnicity", "languages_spoken", "languages_written", "is_veteran", "current_business_description",
  "prospective_business_description", "extending_existing_business", "nominal_current_revenue", "desired_funding", "business_role", "how_many_years_in_current_business", "additional_comments", "biz_street_address", "biz_city", "biz_state", "biz_zip"]
  const userUUID = uuid().replaceAll("-", "")
  await db.any(`insert into registrants(uuid, password, ${columns.join(", ")}) values($1,crypt($2, gen_salt('bf')), ${columns.map((column, i) => { return `$${i + 3}` }).join(', ')})`, [userUUID, req.body.password,...columns.map((column) => { return req.body[column] })]);
  res.json({
    uuid: userUUID
  });

})

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});