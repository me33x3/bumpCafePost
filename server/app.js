import express from 'express';
import dotenv from 'dotenv';
import request from 'request';
import fs from 'fs';

export const app = express();
app.use(express.json());

dotenv.config();

app.get('/home', function(req, res) {
    fs.readFile('index.html', function(error, data) {
        res.writeHead(200, {'Content-Type': 'text/html;charset=utf-8'});
        res.end(data)
    });
});

var client_id = process.env.NAVER_CLIENT_ID;
var client_secret = process.env.NAVER_CLIENT_SECRET;
var state = "RAMDOM_STATE";
var redirectURI = encodeURI(process.env.NAVER_REDIRECT);

var api_url = "";
app.get('/login', function(req, res) {
    api_url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=' + client_id + '&redirect_uri=' + redirectURI + '&state=' + state;
    res.writeHead(200, {'Content-Type': 'text/html;charset=utf-8'});
    res.end("<a href='"+ api_url + "'><img height='50' src='http://static.nid.naver.com/oauth/small_g_in.PNG'/></a>");
});

var token = "";
app.get('/callback', function(req, res) {
   var code = req.query.code;
    var state = req.query.state;

    api_url = 'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id='
    + client_id + '&client_secret=' + client_secret + '&redirect_uri=' + redirectURI + '&code=' + code + '&state=' + state;

    var options = {
        url: api_url,
        headers: {'X-Naver-Client-Id':client_id, 'X-Naver-Client-Secret': client_secret}
    };

    request.get(options, function(error, response, body) {
        if (!error && response.statusCode == 200) {
            token = JSON.parse(body).access_token;
            res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8'});
            res.end(body);
        } else {
            res.status(response.statusCode).end();
            console.log('error = ' + response.statusCode);
        }
    });
});

app.get('/cafe/post', function(req, res) {
    console.log(token);
    res.writeHead(200, {'Content-Type': 'text/html;charset=utf-8'});
    res.end('<h1>글쓰기</h1>')
});