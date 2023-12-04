import * as React from 'react';
import styles from './css/MusicControlPanel.module.css';
import { WebPlaybackSDK } from "react-spotify-web-playback-sdk";

function MusicControlPanel  (props: any)  {
    const [token, setToken] = React.useState('BQDEkobq7nTvwWb2p4RqXy9_KaszyVnWckSrz3yz3Zti-eVHmhohxhU5av0AXHeNVkh92jnzTHQpUaDsGdnJgF_stFYdGPhpb6zwdIv1TEj5xmsJ-HNnglZmTK_33EI1_G10ay_WOSVv581rzqBlKcWyEOF7MpxHVcDYiX7WTyj-1tmWqbVYvG8y5i10lrzPebCnMada');
    //const [token, setToken] = React.useState('');
    const [player, setPlayer] = React.useState<Spotify.Player>();
    const [deviceID, setDeviceID] = React.useState('');
    const [isPlaybackTransferred, setIsPlaybackTransferred] = React.useState(false);
    const [currentSong, setCurrentSong] = React.useState();

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
        if(isPlaybackTransferred){
            await fetch(`https://api.spotify.com/v1/me/player/play?device_id=${deviceID}`, {
                method: "PUT",
                headers: {
                    Authorization: `Bearer ${token}`},
            })
            .then(()=>{
                getCurrentSong();
            });
            console.log("playback transferred")
        }
        else {
            await fetch(`https://api.spotify.com/v1/me/player?device_id=${deviceID}`, {
                method: "PUT",
                headers: {
                    Authorization: `Bearer ${token}`},
                body: JSON.stringify({"device_ids": [
                    `${deviceID}`
                    ],
                    "play": true})
            })
            .then(()=>{
                getCurrentSong();
            });
            console.log("playback not transferred")
            setIsPlaybackTransferred(true);
        };
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
              setCurrentSong(data);
              console.log(currentSong);
            })
            .catch((e) => {
              console.log("Error when trying to fetch current song: " + e);
            });
    }

      return (
        <div>
            <button onClick={prevTrack}>Previous track</button>
            <button onClick={pauseTrack}>Pause track</button>
            <button onClick={playTrack}>Play track</button>
            <button onClick={nextTrack}>Next track</button>
        </div>
      );
  };
  
  export default MusicControlPanel;