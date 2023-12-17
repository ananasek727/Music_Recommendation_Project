import * as React from 'react';
import SongInterface from '../interface/SongInterface';
import CurrentlyPlayingSongInterface from '../interface/CurrentlyPlayingSongInterface';
import PlaylistInterface from '../interface/PlaylistInterface';
import CurrentlyPlayingSong from './CurrentlyPlayingSong';
import styles from './css/MusicControlPanel.module.css';

function MusicControlPanel  (props: any)  {
    const [player, setPlayer] = React.useState<Spotify.Player>();
    const [deviceID, setDeviceID] = React.useState('');
    const [isPlaybackTransferred, setIsPlaybackTransferred] = React.useState(false);
    const [currentSong, setCurrentSong] = React.useState<CurrentlyPlayingSongInterface>();
    const [isSongPlayed, setIsSongPlayed] = React.useState(false);

    // token handling
    const [token, setToken] = React.useState('');
    const [nonEmptyToken, setNonEmptyToken] = React.useState(false);

    React.useEffect(()=>{
      handleTokenRequest();
    },[]);

    const handleTokenRequest = async () => {
      await fetch(`http://127.0.0.1:8000/access-token`, {
            method: "GET"
            })
            .then((response) => {
              if (response.ok) return response.json();
              else {
                throw new Error("ERROR " + response.status);
              }
            })
            .then((data) => {
                setToken(data.access_token);
                console.log(data);
                setNonEmptyToken(true);
                props.setIsLoggedInSpotify(true);
            })
            .catch((e) => {
              console.log("Error when trying to log in: " + e);
            });   
    }

    const handleTokenRefresh = async () => {
      await fetch(`http://127.0.0.1:8000/token-refresh`, {
            method: "GET"
            })
            .then((response) => {
              if (response.ok) return response.json();
              else {
                throw new Error("ERROR " + response.status);
              }
            })
            .then(() => {
               handleTokenRequest();
            })
            .catch((e) => {
              console.log("Error when trying to refresh token: " + e);
            });   
    }

    // refresh token every 55 minutes
    React.useEffect(()=> {
      const interval = setInterval(() => {
        handleTokenRefresh();
      }, 55 * 60 * 1000); // 55 minutes in milliseconds
  
      return () => clearInterval(interval);
    },[])

    React.useEffect(()=>{
    if (window.Spotify !== null && nonEmptyToken) {
        const player = new window.Spotify.Player({
            name: 'Mus4You',
            getOAuthToken: cb => { cb(token); },
            volume: 0.5
        });

        setPlayer(player);

        player.addListener('ready', ({ device_id }) => {
            console.log('Ready with Device ID', device_id);
            setDeviceID(device_id);
        });

        player.addListener('not_ready', ({ device_id }) => {
            console.log('Device ID has gone offline', device_id);
        });

        player.connect();
        }
      
    },[token]);

    // handle adding songs to queue when new playlist is recoommended
    React.useEffect(()=>{
      if(isPlaybackTransferred) {
        addPlaylistToQueue();
      }
    },[props.playlistChangeGuard]);

    // handle adding recommended playlist to queue
    const addPlaylistToQueue = async () => {
        await fetch(`http://127.0.0.1:8000/player/queue`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              "device_id": `${deviceID}`,
              "song_uris": props.playlistSongsURI
            })
            })
            .then((response) => {
                if (response.ok) return response.json();
                else {
                  throw new Error("ERROR " + response.status);
                }
            })
            .catch((e) => {
            console.log("Error when trying to add songs to queue: " + e);
            });
    }

    // play next track
    const nextTrack = async () => {
      await fetch(`http://127.0.0.1:8000/player/next`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              "device_id": `${deviceID}`
            })
          })
          .then((response) => {
            if (response.ok) return response.json();
            else {
              throw new Error("ERROR " + response.status);
            }
          })
          .then(()=>{
            setIsSongPlayed(true);
          })
          .catch((e) => {
          console.log("Error when trying to play next song: " + e);
          });
          
  }
    // pause current track
    const pauseTrack = async () => {
      await fetch(`http://127.0.0.1:8000/player/pause`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              "device_id": `${deviceID}`
            })
          })
          .then((response) => {
            if (response.ok) return response.json();
            else {
              throw new Error("ERROR " + response.status);
            }
          })
          .then(()=>{
            setIsSongPlayed(false);
          })
          .catch((e) => {
            console.log("Error when trying to pause song: " + e);
          });
    }

    // play current track
    const playTrack = async () => {
      // if played for the first time in the app, playback is transfered to this app and recommended songs are added to queue, as playTrack button is disabled when playlist is not recommneded yet
        if(!isPlaybackTransferred){
            await fetch(`http://127.0.0.1:8000/player/tranfer-playback`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json", },
                body: JSON.stringify({
                  device_id:  `${deviceID}`
                    })
            })
            .then((response) => {
              if (response.ok) return response.json();
              else {
                throw new Error("ERROR " + response.status);
              }
            })
            .then(()=>{
              setIsPlaybackTransferred(true);
              addPlaylistToQueue();
            })
            .catch((e) => {
              console.log("Error when trying to transfer playback: " + e);
            });
            
        }

        await fetch(`http://127.0.0.1:8000/player/play`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json", },
            body: JSON.stringify({
              device_id:  `${deviceID}`
                })
        })
        .then((response) => {
          if (response.ok) return response.json();
          else {
            throw new Error("ERROR play" + response.status);
          }
        })
       .then(()=>{
          setIsSongPlayed(true);
        })
        .catch((e) => {
          console.log("Error when trying to play song: " + e);
        });
        
    }
   
    // get data about currently played song, used to display info for a user
    const getCurrentSong = async () => {
            await fetch(`http://127.0.0.1:8000/currently-playing-song`, {
                method: "GET",
                })
                .then((response) => {
                  if (response.ok) return response.json();
                  else {
                    throw new Error("ERROR " + response.status);
                  }
                })
                .then((data) => {
                  setCurrentSong(data);
                  console.log(data);
                })
                .catch((e) => {
                  console.log("Error when trying to fetch current song: " + e);
                });
    }

    // change volume
    const changeVolume = async (volume: number) => {
      await fetch(`http://127.0.0.1:8000/player/set-volume`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              "volume_percent": volume
            })
          })
          .then((response) => {
            if (response.ok) return response.json();
            else {
              throw new Error("ERROR " + response.status);
            }
          })
          .catch((e) => {
            console.log("Error when trying to change volume: " + e);
          });
    }
    const [volume, setVolume] = React.useState<number>(50); // Initial value set to 50
    const [tempVolume, setTempVolume] = React.useState<number | null>(null);

    const handleVolumeSliderChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const newValue = parseInt(event.target.value, 10);
      setTempVolume(newValue);
    };

    const handleVolumeSliderRelease = () => {
      if (tempVolume !== null) {
        setVolume(tempVolume);
        setTempVolume(null);
        changeVolume(tempVolume);
      }
    };

    // refresh current song data displayed to user, active only when song is played
    React.useEffect(()=>{
        const intervalId = setInterval(() => {
           // get current song when track is played
            if(isSongPlayed === true){
                getCurrentSong();
              }
            else {
              clearInterval(intervalId);
            }
          }, 1000); // Runs every second
      
          // Clear the interval when the component unmounts or when dependencies change
          return () => clearInterval(intervalId);
    },[isSongPlayed]);

    

      return (
        <div className={styles.MusicControlPanelFrame}>
          <div className={styles.MusicControlPanelFrameInner}>
            {/* <div className={styles.MusicControlPanelText}>
              Current song
            </div> */}
            <div className={styles.MusicControlPanelSpaceHolder}>

            </div>
            {isSongPlayed 
            ? 
            <button  className={styles.MusicControlPanelButton} onClick={pauseTrack} disabled={props.isPlaylistEmpty}>Pause track</button>
            : 
            <button className={styles.MusicControlPanelButton} onClick={playTrack} disabled={props.isPlaylistEmpty}>Play track</button>}
            
            <button className={styles.MusicControlPanelButton} onClick={nextTrack} disabled={props.isPlaylistEmpty}>Next track</button>

            <input
              data-testid="volume-slider"
              className={styles.MusicControlPanelSlider}
              disabled={props.isPlaylistEmpty}
              type="range"
              min={0}
              max={100}
              value={tempVolume !== null ? tempVolume : volume}
              onChange={handleVolumeSliderChange}
              onMouseUp={handleVolumeSliderRelease}
              step={1}
            />

            </div>
            {currentSong &&
              <CurrentlyPlayingSong data-testid="currently-playing-song" song={currentSong}/>
            }
          
        </div>
      );
  };
  
  export default MusicControlPanel;