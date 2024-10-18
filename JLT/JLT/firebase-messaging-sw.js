// firebase-messaging-sw.js
importScripts('https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/9.6.1/firebase-messaging.js');

const firebaseConfig = {
    apiKey: "EiPoPeHG58jzvXYcwxSlpIHarMto68hdQGBhGQeNv4s",
    authDomain: "julienleblanc-2fc4b.firebaseapp.com",
    projectId: "julienleblanc-2fc4b",
    storageBucket: "julienleblanc-2fc4b.appspot.com",
    messagingSenderId: "111852233971",
    appId: "julienleblanc-2fc4b"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: 'path/to/your/icon.png',
        sound: 'path/to/your/sound.mp3', // Path to sound file
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});
