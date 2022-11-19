const nostrnode = "nostrnode"

const assets = []

self.addEventListener("install", installEvent => {
    installEvent.waitUntil(
        caches.open(nostrnode).then(cache => {
            cache.addAll(assets).then(r => {
                console.log("Cache assets downloaded");
            }).catch(err => console.log("Error caching item", err))
            console.log(`Cache ${nostrnode} opened.`);
        }).catch(err => console.log("Error opening cache", err))
    )
})