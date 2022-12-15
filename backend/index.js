"use strict";
exports.__esModule = true;
var express_1 = require("express");
var dotenv = require("dotenv");
dotenv.config();
var app = (0, express_1["default"])();
var port = process.env.PORT;
app.get("/", function (req, res) {
    res.send("My Coffee Roaster Monitor");
});
app.get("/ambient/:ambientTemp/probe/:probeTemp", function (req, res) {
    var ambient = req.params.ambientTemp;
    var probe = req.params.probeTemp;
    res.json(ambient + probe);
});
app.listen(port, function () {
    console.log("[SERVER]: Listening on port ".concat(port));
});
