import * as React from 'react';
import SongInterface from '../interface/SongInterface';
import CurrentlyPlayingSongInterface from '../interface/CurrentlyPlayingSongInterface';
import PlaylistInterface from '../interface/PlaylistInterface';
import CurrentlyPlayingSong from './CurrentlyPlayingSong';
//import { WebPlaybackSDK } from "react-spotify-web-playback-sdk";
import styles from './css/MusicControlPanel.module.css';

function MusicControlPanel  (props: any)  {
    const [token, setToken] = React.useState('BQCH6eOUB4lDZ-X9OH0giwImRDV_3ZSb5rpNfXj0EbpOCrGcuH0lgSesXmiyQJi8ZF_fca8SWzmpu5eMQFTDY02GVtSXL5NYwukaRpuUaAqPhmY8B9h3IEjuLJwYZQj7UII10ZxXEbnnkjVWT-F_16gkX43WXdoFBA_eZL7I3utBZwbu0RDuAAUs6X8Phc1VUEFuFlsTxz9FJtOQsPG2zn9Wr_HGur7QSFtAELbLXE5jBT1hPSz0ChbgvVpDuA2Po4-TwwwkW6g');
    //const [token, setToken] = React.useState('');
    const [player, setPlayer] = React.useState<Spotify.Player>();
    const [deviceID, setDeviceID] = React.useState('');
    const [isPlaybackTransferred, setIsPlaybackTransferred] = React.useState(false);
    const [currentSong, setCurrentSong] = React.useState<CurrentlyPlayingSongInterface>();
    const [isSongPlayed, setIsSongPlayed] = React.useState(false);

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

    // handle adding songs to queue when new playlist is recoommended
    React.useEffect(()=>{
      if(isPlaybackTransferred) {
        addPlaylistToQueue();
      }
    },[props.playlistChangeGuard]);

    // handle adding recommended playlist to queue
    const addPlaylistToQueue = async () => {
        await fetch(`http://127.0.0.1:8000/player-queue`, {
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
        await fetch(`https://api.spotify.com/v1/me/player/next?device_id=${deviceID}`, {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`},
            });
            setIsSongPlayed(true);
    }

    // pause current track
    const pauseTrack = async () => {
    await fetch(`https://api.spotify.com/v1/me/player/pause?device_id=${deviceID}`, {
        method: "PUT",
        headers: {
            Authorization: `Bearer ${token}`},
        })
        // .then((response) => {
        //   if (response.ok) return response.json();
        //   else {
        //     throw new Error("ERROR " + response.status);
        //   }
        // })
        //.then(()=>{
          setIsSongPlayed(false);
        //});
        
    }

    // play current track
    const playTrack = async () => {
      // if played for the first time in the app, playback is transfered to this app and recommended songs are added to queue, as playTrack button is disabled when playlist is not recommneded yet
        if(!isPlaybackTransferred){
            await fetch(`https://api.spotify.com/v1/me/player`, {//?device_id=${deviceID}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`},
                body: JSON.stringify({
                  device_ids: [ `${deviceID}`
                    ],
                  play: false })
            })
            // .then((response) => {
            //   if (response.ok) return response.json();
            //   else {
            //     throw new Error("ERROR " + response.status);
            //   }
            // })
            //.then(()=>{
              setIsPlaybackTransferred(true);
            //});
            addPlaylistToQueue();
        }
       

        await fetch(`https://api.spotify.com/v1/me/player/play?device_id=${deviceID}`, {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${token}`},
        })
        // .then((response) => {
        //   if (response.ok) return response.json();
        //   else {
        //     throw new Error("ERROR play" + response.status);
        //   }
        // })
       // .then(()=>{
          setIsSongPlayed(true);
        //});
        
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
            <div className={styles.MusicControlPanelText}>
              Current song
            </div>
            {isSongPlayed 
            ? 
            <button className={styles.MusicControlPanelButton} onClick={pauseTrack} disabled={props.isPlaylistEmpty}>Pause track</button> 
            : 
            <button className={styles.MusicControlPanelButton} onClick={playTrack} disabled={props.isPlaylistEmpty}>Play track</button>}
            
            <button className={styles.MusicControlPanelButton} onClick={nextTrack} disabled={props.isPlaylistEmpty}>Next track</button>
            </div>
            {currentSong &&
              <CurrentlyPlayingSong song={currentSong}/>
            }
          
        </div>
      );
  };
  
  export default MusicControlPanel;