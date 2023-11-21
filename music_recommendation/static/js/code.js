var spotifyAuthenticated = false
var song = {}

function authenticateSpotify()
{
    fetch("/spotify/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        spotifyAuthenticated = data.status
        if (!data.status) {
          fetch("/spotify/get-auth-url")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            });

        } else {
            location.href='/parameters/camera'
        }
      });
}
function goToCameraPage()
{
    // location.href='/parameters/camera'
    console.log("Dziala");
    authenticateSpotify();
}
function getCurrentSong() {
    fetch("http://127.0.0.1:8000/spotify/current-song")
      .then((response) => {
        if (!response.ok) {
          return {};
        } else {
          return response.json();
        }
      })
      .then((data) => {
          document.getElementById("title").innerText = data.title;
          document.getElementById("artist").innerText = data.artist;
          document.getElementById("albumPhoto").src = data.image_url;
      });
  }
