let startButton = document.getElementById("start-btn");
let stopButton = document.getElementById("stop-btn");

const startWebcam = () => {
  let videoPlayer = document.createElement("img");

  videoPlayer.id = "videoPlayer";
  videoPlayer.src = baseVideoUrl;

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
