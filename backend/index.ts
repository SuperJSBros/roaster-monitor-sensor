import express, { Express, Request, Response } from "express"
import * as dotenv from "dotenv"
dotenv.config()

const app: Express = express()
const port = process.env.PORT


app.get("/", (req:Request, res: Response)=>{
    res.send("My Coffee Roaster Monitor")
})
app.get("/ambient/:ambientTemp/probe/:probeTemp", (req, res)=>{
    let ambient = req.params.ambientTemp
    let probe = req.params.probeTemp
    res.json(ambient+probe)
})

app.listen(port, ()=>{
    console.log(`[SERVER]: Listening on port ${port}`)
})