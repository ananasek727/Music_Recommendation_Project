import * as React from 'react';
import styles from './css/MusicControlPanel.module.css';
import SongInterface from '../interface/SongInterface';
//import { WebPlaybackSDK } from "react-spotify-web-playback-sdk";

function MusicControlPanel  (props: any)  {
    const [token, setToken] = React.useState('BQB7sqzz_-xmLmW-UP4Nm4lQ3oA_niJ9KqAk2QzST9MfueQn42S0m1-qB4qonFLG6Ak8svF6xnsSfaxtUPly2z-fVRzQxXU5QPhcRpXhsFdpcjlT0XuZXPr8r9nM6WEtP0ejTyQ8BsqpYB1Ot3vvlvdicty4sDbdiBghL1JK7pCa0mmRN4kHTNLDDT-7NkxwvskEAsX911U');
    //const [token, setToken] = React.useState('');
    const [player, setPlayer] = React.useState<Spotify.Player>();
    const [deviceID, setDeviceID] = React.useState('');
    const [isPlaybackTransferred, setIsPlaybackTransferred] = React.useState(false);
    const [currentSong, setCurrentSong] = React.useState(null);

    React.useEffect(()=>{
    if (window.Spotify !== null) {
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
      
    },[]);

    const addToQueue = async (songToPlay: string) => {
        // ?uri=${songToPlay}&device_id=${deviceID}
        await fetch(`https://api.spotify.com/v1/me/player/queue?uri=${songToPlay}&device_id=${deviceID}`, {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`
            }
            })
            .then((response) => {
                if (response.ok) return response.json();
                else {
                  throw new Error("ERROR " + response.status);
                }
            })
            .catch((e) => {
            console.log("Error when trying to add song to a queue: " + e);
            });;
    }

    const nextTrack = async () => {
        await fetch(`https://api.spotify.com/v1/me/player/next?device_id=${deviceID}`, {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`},
            });
    }

    const prevTrack = async () => {
        await fetch(`https://api.spotify.com/v1/me/player/previous?device_id=${deviceID}`, {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`},
            });
    }

    const pauseTrack = async () => {
    await fetch(`https://api.spotify.com/v1/me/player/pause?device_id=${deviceID}`, {
        method: "PUT",
        headers: {
            Authorization: `Bearer ${token}`},
        });
    }

    const playTrack = async () => {
        if(!isPlaybackTransferred){
            await fetch(`https://api.spotify.com/v1/me/player?device_id=${deviceID}`, {
                method: "PUT",
                headers: {
                    Authorization: `Bearer ${token}`},
                body: JSON.stringify({"device_ids": [
                    `${deviceID}`
                    ],
                    "play": false})
            })
            setIsPlaybackTransferred(true);

        }
        
        await fetch(`https://api.spotify.com/v1/me/player/play?device_id=${deviceID}`, {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${token}`},
        })
        .then(()=>{
            getCurrentSong();
        });
        
    }

    const getCurrentSong = async () => {
        await fetch(`https://api.spotify.com/v1/me/player/currently-playing`, {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`},
            })
            .then((response) => {
              if (response.ok) return response.json();
              else {
                throw new Error("ERROR " + response.status);
              }
            })
            .then((data) => {
              setCurrentSong(data.item.name);
              console.log(currentSong);
            })
            .catch((e) => {
              console.log("Error when trying to fetch current song: " + e);
            });
    }

    React.useEffect(()=>{
        const intervalId = setInterval(() => {
            // Update the counter every second
            getCurrentSong();
          }, 1000); // Runs every second (1000ms)
      
          // Clear the interval when the component unmounts or when dependencies change
          return () => clearInterval(intervalId);
    },[]);

      return (
        <div>
            <button onClick={prevTrack}>Previous track</button>
            <button onClick={pauseTrack}>Pause track</button>
            <button onClick={playTrack}>Play track</button>
            <button onClick={nextTrack}>Next track</button>
            <button onClick={()=>{addToQueue('spotify%3Atrack%3A11dFghVXANMlKmJXsNCbNl')}}>Add to queue</button>
            {currentSong &&
            <div>
                {currentSong}
            </div>
            }
        </div>
      );
  };
  
  export default MusicControlPanel;