// app.js
document.addEventListener("DOMContentLoaded", function() {
    const socket = io.connect({ autoConnect: false });

    const is_translator = document.getElementsByTagName("video")[0].id;

    if (is_translator == 1) {
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((stream) => {
    //                const video = document.querySelector("#videoElement");
                    const video = document.getElementsByTagName("video")[0];
//                    console.log(video)
                    video.srcObject = stream;
                    video.play();
                })
                .catch((error) => {
                    console.error("Error accessing camera:", error);
                });
        }
    }

    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");
//    const room = document.title

    socket.on("connect", function(value){
//        console.log("Connected")
//        console.log(value)
        socket.emit("joined", {room: document.title, is_translator: is_translator})
    });

    socket.on("join", function(value) {
//        console.log("joined")
//        console.log(value)
    });

    socket.on("leave", function(value) {
//        console.log("leaved")
//        console.log(value)
    });

    if (is_translator == 1) {
        const FPS = 30;
        setInterval(() => {
            const video = document.getElementsByTagName("video")[0];
            const width = canvas.width;
            const height = canvas.height;
            context.drawImage(video, 0, 0, width, height);
            const data = canvas.toDataURL("image/jpeg", 0.5);
            context.clearRect(0, 0, width, height);
            socket.emit("image", data);
            }


        , 1000 / FPS);
    }
    console.log(is_translator)

    if (is_translator == 0) {
    socket.on("processed_image", (image) => {
//        if (is_translator == 0) {
//            console.log("processed_image");
//            console.log(image);
            const photo = document.getElementById("photo");
//            console.log("processed_image2");
//            console.log(image);
            photo.setAttribute("src", image);

        });
    }

    socket.on('status', function(data) {
        console.log(data);
    });

    socket.connect();
});
