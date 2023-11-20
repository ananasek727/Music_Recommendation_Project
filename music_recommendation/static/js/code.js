var spotifyAuthenticated = false


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
    authenticateSpotify();
}
