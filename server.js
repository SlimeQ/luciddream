var sys = require("sys");

var express = require('express');
var app = express();
var http = require('http').Server(app);
var fs = require('fs');
var exec = require('child_process').exec;

var request = require('request');
var net = require('net');
var util = require('./util');

var conf = require('./conf');

var zerorpc = require("zerorpc");

// var client = new zerorpc.Client();
// client.connect("tcp://"+conf.slaves[0].url+":"+conf.slaves[0].port);
// conf.slaves.map(function(x) {
// 	var client = new zerorpc.Client();
// 	client.connect("tcp://"+x.url+":"+x.port);
// 	return {
// 		url   : x.url,
// 		port  : x.port,
// 		client : client,
// 		users : 0
// 	};
// });

var publicIO = require('socket.io')(http);
var client = new zerorpc.Client();
client.connect("tcp://"+conf.slaves[0].url+":"+conf.slaves[0].port);
console.log('created slave client');

publicIO.on('connection', function(socket) {
	console.log(socket.conn.remoteAddress, 'connected');

	// cuda --> client stuff
	// var computeIO = require('socket.io-client')('http://localhost:8080');
	// computeIO.on('connect', function(){
	// 	console.log('connected to localhost:8080');
	// });
	// computeIO.on('image', function(info){
	// 	console.log('emitting to client');
	// 	socket.emit('image', info);
	// 	util.saveToMemory(info);
	// });
	// computeIO.on('disconnect', function(){
	// 	console.log('localhost:8080 disconnected');
	// });

	// client --> cuda stuff
	var sentlast = 0;
	socket.on('image', function(info) {
		if (sentlast != 0) {
			console.log(util.timestamp() - sentlast);
		}
		info.recieved = util.timestamp();
		console.log('recieved image from '+socket.conn.remoteAddress+' at '+info.recieved);
		client.invoke("dream", info.buffer, util.timestamp(), function(err, res, more) {
			info.buffer = res;
			info.returned = util.timestamp();
			sentlast = info.returned;
			socket.emit('image', info);
			console.log('frame processed in ' + (info.returned - info.recieved) + 's');
		});
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
	// if (ready) {
		res.render('preview.ejs', {});
	// } else {
		// res.send("sorry, still starting up");
	// }
});
// app.post("/deepdream", function(req, res) {
// 	ready = true;
// 	console.log('accepting requests now');
// 	res.send('200');
// })

var listenon = process.argv[2];
http.listen(listenon, function(){
	console.log('listening on *:'+listenon);
});
sys.puts("Server Running on "+listenon);
