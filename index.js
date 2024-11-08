const express = require('express');
require('dotenv').config();


const PORT = 3000;

const app = require('./app')

console.log('App is starting...');

app.use(express.json());  


app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
