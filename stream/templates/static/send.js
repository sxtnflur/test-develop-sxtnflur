document.addEventListener("DOMContentLoaded", function() {
    const socket = io.connect({ autoConnect: false });

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                const video = document.querySelector("#videoElement");
                video.srcObject = stream;
                video.play();
            })
            .catch((error) => {
                console.error("Error accessing camera:", error);
            });
    }

    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");

    const FPS = 10;
    setInterval(() => {
        const video = document.querySelector("#videoElement");
        const width = canvas.width;
        const height = canvas.height;
        context.drawImage(video, 0, 0, width, height);
        const data = canvas.toDataURL("image/jpeg", 0.5);
        context.clearRect(0, 0, width, height);
        socket.emit("image", data);
    }, 1000 / FPS);

//    socket.on("processed_image", (image) => {
//        console.log("processed_image");
//        console.log(image);
//        const photo = document.getElementById("photo");
//        photo.setAttribute("src", image);
//    });

    socket.connect();
});
