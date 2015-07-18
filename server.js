var sys = require("sys");

var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var ss = require('socket.io-stream');
var fs = require('fs');
var exec = require('child_process').exec;

var request = require('request');
var net = require('net');
var util = require('./util');

var portrange = 45032;

function getPort (cb) {
	var port = portrange;
	portrange += 1;

	var server = net.createServer();
	server.listen(port, function (err) {
		server.once('close', function () {
				cb(port);
			});
			server.close();
		});
		server.on('error', function (err) {
		getPort(cb);
	});
}
function checkPort (port, cb) {
	var server = net.createServer();
	server.listen(port, function (err) {
		server.once('close', function () {
				cb(false);
			});
			server.close();
		});
		server.on('error', function (err) {
			cb(true);
	});
}

var pyport = undefined;
getPort(function(port) {
	pyport = port;
	exec('python luciddream.py ' + port.toString() + ' >> luciddream.log',
	function (err, stdout, stderr) {
		console.log('lightdreamer died');
		console.log(err);
		console.log('stdout:', stdout);
		console.log('stderr', stderr);
	});
});
io.on('connection', function(socket) {
	console.log(socket.conn.remoteAddress, 'connected');
  socket.on('image', function(stream) {
		// console.log(stream.buffer);
		// var buffer = 'buffer/'+Date.now()+'.jpg';
		if (pyport != undefined && ready) {
			checkPort(pyport, function(available) {
				if (available) {
					console.log('requesting dream');
					console.log('http://127.0.0.1:'+pyport);
					request.post('http://127.0.0.1:'+pyport+'/deepdream',
					{
						form : {
							image : stream.image,
							buffer : stream.buffer,
							guid: stream.guid
						}
					}, function(err, response, body) {
						if (!err) {
							console.log('emitting back');
							// console.log(body);
							socket.emit('image', {image: true, buffer : body, guid : stream.guid});
							util.ensureExists('memory', function() {
								util.ensureExists('memory/'+new Date().toJSON().slice(0,10), function(){
									util.base64_decode(body, 'memory/'+new Date().toJSON().slice(0,10)+'/'+util.timestamp()+'.jpeg');
								});
							});
						} else {
							console.log(err);
							console.log('emitting back');
							// socket.emit('image', stream);
						}
					});
				} else {
					console.log('pyport not bound');
					// setTimeout(function() {
						// console.log('emitting back');
						// socket.emit('image', stream);
					// });
				}
			});
		} else {
			console.log('pyport undefined');
			// setTimeout(function() {
			// 	console.log('emitting back');
			// 	socket.emit('image', stream);
			// });
		}
	});
	// make sure to clean up after disconnects
	socket.on('disconnect', function(){
		console.log(socket.conn.remoteAddress + ' disconnected');
	});
});


// app.use(express.static('images'));
// app.use(express.static('fonts'));
// app.use(express.static('icon'));
app.use(express.static('js'));
// app.use(express.static('styles'));
app.set('view engine', 'ejs');

var ready = false;
app.get("/",function(req,res){
	if (ready) {
		res.render('preview.ejs', {});
	} else {
		res.send("sorry, still starting up");
	}
});
app.post("/deepdream", function(req, res) {
	ready = true;
	console.log('accepting requests now');
	res.send('200');
})

http.listen(8080, function(){
	console.log('listening on *:8080');
});
sys.puts("Server Running on 8080");
