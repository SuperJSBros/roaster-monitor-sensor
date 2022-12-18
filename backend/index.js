const express = require("express");
const dotenv = require("dotenv");
dotenv.config();


const app = express()
const port = process.env.PORT

app.get("/", (req, res)=>{
    res.send("My Coffee Roaster Monitor")
})
app.get("/ambient/:ambientTemp/probe/:probeTemp", (req, res)=>{
    let ambient = req.params.ambientTemp
    let probe = req.params.probeTemp
    res.json({"ambient temperaature":ambient, "probe temperature":probe})
})

app.listen(port, ()=>{
    console.log(`[SERVER]: Listening on port ${port}`)
})