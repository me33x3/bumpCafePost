import { app } from './app.js'

function startServer() {
    app.listen(3000, function () {
        console.log('http://127.0.0.1:3000/login app listening on port 3000!');
    });
}

startServer();