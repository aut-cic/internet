const CatBox = require('catbox');
const CatboxMem = require('catbox-memory');

let ready = false;
const client = new CatBox.Client(CatboxMem);
client.start(() => {
    ready = true;
});

function get(key) {
    if (!ready) return;

    return new Promise((resolve, reject) => {
        client.get(key, (err, cached) => {
            if (err) return reject(err);
            resolve(cached && cached.item);
        });
    });
}

function set(key, value, seconds) {
    if (!ready) return;

    return new Promise((resolve, reject) => {
        client.set(key, value, seconds * 1000, (err) => {
            if (err) return reject(err);
            resolve();
        });
    });
}

function drop(key) {
    if (!ready) return;

    return new Promise((resolve, reject) => {
        client.drop(key, (err) => {
            if (err) return reject(err);
            resolve();
        });
    });
}

module.exports = {
    cache: client,
    get,
    set,
    drop,
    stats: client.stats
};