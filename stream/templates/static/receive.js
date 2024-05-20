var socket = io.connect(
   {autoConnect: false}
);

socket.on("connect", function() {
   console.log("Connected...!", socket.connected);
});

socket.on("processed_image", function(image) {
    console.log("processed_image");
    console.log(image);
    photo.setAttribute("src", image);
});

socket.on("disconnect", function() {
   console.log("Disconnected...!", socket.connected);
});