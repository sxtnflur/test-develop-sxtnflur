document.addEventListener("DOMContentLoaded", function() {
    const socket = io.connect({ autoConnect: false });

    socket.on("processed_image", (image) => {
        const photo = document.getElementById("photo");
        photo.setAttribute("src", image);
    });

    socket.connect();
});
