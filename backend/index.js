const express = require("express");
const dotenv = require("dotenv");
dotenv.config();


const app = express()
const port = process.env.PORT

let ambient
let probe

app.get("/", (req, res)=>{
    res.send(`My Coffee Roaster Monitor ambient : ${ambient} probe : ${probe}`)
})
app.get("/ambient/:ambientTemp/probe/:probeTemp", (req, res)=>{
    ambient = req.params.ambientTemp
    probe = req.params.probeTemp
    res.json({"ambient temperaature":ambient, "probe temperature":probe})
    res.status(200)
    console.log(`ambient : ${ambient}   probe : ${probe} `)
})

app.listen(port, ()=>{
    console.log(`[SERVER]: Listening on port ${port}`)
})