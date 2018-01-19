#!/usr/bin/env node
'use strict';
var path = require("path");
const { spawn } = require('child_process');

var readDataTimeout = 60000; // one minute
var screenWidth = 320;
var screenHeight = 480;
var owfsDevice = "26.103D15000000";
var currentTemperature = null;
var currentHumidity = null;
var currentIPAddress = null;
var backgroundImageFileName = path.join(__dirname, "background.png");
var outputImageFileName = path.join(__dirname, "display.png");

// OneWire Temperature and Humidity Reading
var owfsClient = require('owfs').Client;
function updateSensors() {
	var owfsConnection = new owfsClient('localhost');
	owfsConnection.read("/" + owfsDevice + "/temperature", function(err, result) {
		if (err) { console.log(err); }
		currentTemperature = Number(result) * 1.8 + 32;
		//console.log("Temperature = (" + result + ") " + currentTemperature);
	});
	
	owfsConnection.read("/" + owfsDevice + "/humidity", function(err, result) {
		if (err) { console.log(err); }
		currentHumidity = Number(result);
		//console.log("Humidity = (" + result + ") " + currentHumidity);
	});
}

// Get IP address from OS
var os = require('os');
function updateIPAddress() {
	// https://stackoverflow.com/questions/3653065/get-local-ip-address-in-node-js
	currentIPAddress = null; // reset each time we look.
	var ifaces = os.networkInterfaces();
	Object.keys(ifaces).forEach(function (ifname) {
		ifaces[ifname].forEach(function (iface) {
			if ('IPv4' !== iface.family || iface.internal !== false) {
				// skip over internal (i.e. 127.0.0.1) and non-ipv4 addresses
				return;
			}
	
			if (currentIPAddress === null) {
				currentIPAddress = iface.address;
			}
		});
	});
}

// Draw the screen...
var fs = require("fs"),
	date = require("datejs");

var Canvas = require('canvas'),
	Image = Canvas.Image;

function createDisplayImage(width, height, imageFileName, imageCreatedCallback) {
	var canvas = new Canvas(width, height),
	ctx = canvas.getContext('2d');

	// https://github.com/Automattic/node-canvas/tree/v1.x
	fs.readFile(backgroundImageFileName, function(err, background) {
		if (err) {
			throw err;
		}

		var backgroundImage = new Image;
		backgroundImage.src = background;	
		ctx.drawImage(backgroundImage, 0, 0, backgroundImage.width, backgroundImage.height);
		
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

		if (currentTemperature !== null) {
			ctx.fillStyle = "white";
			ctx.font = "bold 120px Roboto";
			ctx.textAlign = "center";
			ctx.fillText(currentTemperature.toFixed(1), width/2, height*0.80); //℉

			ctx.fillStyle = "white";
			ctx.font = "bold 18px Roboto";
			ctx.textAlign = "center";
			ctx.fillText("°F", width*0.90, height*0.80); //℉
		}

		if (currentIPAddress !== null) {
			ctx.fillStyle = "skyblue";
			ctx.font = "bold 18px Roboto";
			ctx.textAlign = "center";
			ctx.fillText(currentIPAddress, width/2, height-12);
		}

		// https://bl.ocks.org/shancarter/f877b05acb3bafb9d5844f2342344385
		var pngFile = fs.createWriteStream(imageFileName);
		canvas.createPNGStream().pipe(pngFile);

		pngFile.on('finish', function() {
			if (imageCreatedCallback !== null) {
				imageCreatedCallback(imageFileName);
			}
	  });
	});
}

var fbiProc = null;
function writeFramebuffer(imageFileName) {
	// if (fbiProc !== null) {
	// 	fbiProc.kill();
	// }

	//console.log("fbi -T 2 -d /dev/fb1 -noverbose -a "+ imageFileName);
	fbiProc = spawn('fbi',  ["-T", "2", "-d", "/dev/fb1", "-noverbose", "-a", imageFileName]);
	setTimeout(function() {
		fbiProc.kill();
	}, 500)
	
	fbiProc.on('exit', function (code, signal) {
		console.log(`child process exited with code ${code} and signal ${signal}`);
	});
}

function updateDisplay() {
	createDisplayImage(screenWidth, screenHeight, outputImageFileName, function(imageName) {
		//console.log("ip=" + currentIPAddress);
		//console.log("temp=" + currentTemperature);
		//console.log("humidity=" + currentHumidity);
		writeFramebuffer(imageName)
	});
}

// schedule to read every readDataTimeout
updateSensors();
setInterval(updateSensors, readDataTimeout);

updateIPAddress();
setInterval(updateIPAddress, readDataTimeout);

// update display every second
updateDisplay();
setInterval(updateDisplay, 1000);
