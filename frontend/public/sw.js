// KILL SWITCH SERVICE WORKER
// This service worker instantly unregisters itself and deletes all caches to escape the Vite death loop.

self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => caches.delete(key)));
    }).then(() => {
      self.registration.unregister();
    }).then(() => {
      self.clients.matchAll().then((clients) => {
        clients.forEach((client) => client.navigate(client.url));
      });
    })
  );
});

// Pass everything to the network just in case it takes a second to unregister
self.addEventListener('fetch', (e) => {
  e.respondWith(fetch(e.request));
});
