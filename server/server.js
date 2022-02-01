import { app } from './app.js'

function run() {
    const port = process.env.SERVER_PORT;
    app.listen(port, function () {
        console.log(`http://127.0.0.1:${port} app listening on port ${port}!`);
    });
}

run();