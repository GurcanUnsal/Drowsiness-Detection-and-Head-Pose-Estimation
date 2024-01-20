let startButton = document.getElementById("start-btn");
let stopButton = document.getElementById("stop-btn");
let centeredDiv = document.getElementsByClassName("centered");

const startWebcam = () => {
  let videoPlayer = document.createElement("img");

  videoPlayer.id = "videoPlayer";
  videoPlayer.src = baseVideoUrl;
  videoPlayer.classList.add("rounded");
  videoPlayer.classList.add("d-block");

  document.body.appendChild(videoPlayer);

  startButton.disabled = true;
  stopButton.disabled = false;
};

const stopWebcam = () => {
  let videoPlayer = document.getElementById("videoPlayer");
  videoPlayer.remove();
  window.location.reload()

  startButton.disabled = false;
  stopButton.disabled = true;
};
