const CACHE_NAME = "placement-v1";

const urlsToCache = [

"/",

"/dashboard",

"/leaderboard",

"/activity-history",

"/static/icon.png",

"/static/manifest.json"

];

self.addEventListener(

"install",

event => {

event.waitUntil(

caches.open(
CACHE_NAME
)

.then(cache => {

return cache.addAll(
urlsToCache
);

})

);

}

);

self.addEventListener(

"fetch",

event => {

event.respondWith(

caches.match(
event.request
)

.then(response => {

return response ||
fetch(
event.request
);

})

);

}

);