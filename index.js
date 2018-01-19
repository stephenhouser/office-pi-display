#!/usr/bin/env node
'use strict';
var fs = require("fs"),
	path = require("path"),
	date = require("datejs"),
	os = require('os'),
	owfs = require('owfs').Client;

var primary_ip = null;
// https://stackoverflow.com/questions/3653065/get-local-ip-address-in-node-js
var ifaces = os.networkInterfaces();
Object.keys(ifaces).forEach(function (ifname) {
	var alias = 0;

	ifaces[ifname].forEach(function (iface) {
		if ('IPv4' !== iface.family || iface.internal !== false) {
			// skip over internal (i.e. 127.0.0.1) and non-ipv4 addresses
			return;
		}

		if (primary_ip === null) {
			primary_ip = iface.address;
		}

		// if (alias >= 1) {
		// 	// this single interface has multiple ipv4 addresses
		// 	console.log(ifname + ':' + alias, iface.address);
		// } else {
		// 	// this interface has only one ipv4 adress
		// 	console.log(ifname, iface.address);
		// }
		++alias;
	});
});

var ow_temp = null;
var ow_humid = null;

var owcon = new Client('localhost');
owcon.read("/26.103D15000000/temperature", function(err, result) {
	ow_temp = result * 1.8 + 32;
}

owcon.read("/26.103D15000000/humidity", function(err, result) {
	ow_humid = result;
}

// Draw the screen...
const width = 320,
	  height = 480;
	  
// ctx.fillStyle = "black";
// ctx.fillRect(0, 0, canvas.width, canvas.height);

var Canvas = require('canvas'),
	Image = Canvas.Image,
	canvas = new Canvas(width, height),
	ctx = canvas.getContext('2d');

// https://github.com/Automattic/node-canvas/tree/v1.x
fs.readFile(__dirname + '/background.png', function(err, background) {
	if (err) throw err;

	var img = new Image;
	img.src = background;	
	ctx.drawImage(img, 0, 0, img.width, img.height);
	
	var now = new Date();

	// https://code.google.com/archive/p/datejs/wikis/FormatSpecifiers.wiki
	var day_s = now.toString('ddd, MMM d');
	ctx.fillStyle = "yellow";
	ctx.font = "bold 36px Roboto";
	ctx.textAlign = "center";
	ctx.fillText(day_s, width/2, 36); //℉

	// https://code.google.com/archive/p/datejs/wikis/FormatSpecifiers.wiki
	var time_s = now.toString('h:mm:ss tt');
	ctx.fillStyle = "yellow";
	ctx.font = "bold 36px Roboto";
	ctx.textAlign = "center";
	ctx.fillText(time_s, width/2, 72); //℉

	ctx.fillStyle = "white";
	ctx.font = "bold 120px Roboto";
	ctx.textAlign = "center";
	ctx.fillText("72.5", width/2, height*0.80); //℉

	ctx.fillStyle = "white";
	ctx.font = "bold 18px Roboto";
	ctx.textAlign = "center";
	ctx.fillText("°F", width*0.90, height*0.80); //℉

	ctx.fillStyle = "skyblue";
	ctx.font = "bold 18px Roboto";
	ctx.textAlign = "center";
	ctx.fillText(primary_ip, width/2, height-12); //℉

	// https://bl.ocks.org/shancarter/f877b05acb3bafb9d5844f2342344385
	canvas.createPNGStream().pipe(fs.createWriteStream(path.join(__dirname, "display.png")));
});
