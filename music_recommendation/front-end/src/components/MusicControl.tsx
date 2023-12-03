import * as React from 'react';
import styles from './css/MusicControl.module.css';
import SongInterface from '../interface/SongInterface';
import PlaylistElement from './PlaylistElement';
import MusicControlPanel from './MusicControlPanel';

function MusicControl  (props: any)  {
    const [currentSong, setCurrentSong] = React.useState<SongInterface>();

    React.useEffect(()=>{
        if(props.playlist.songs.length > 0){
           setCurrentSong(props.playlist.songs[0]);
        }
    },[props.playlist]);

    return (
        <div className={styles.MusicControlFrame}>
            <div className={styles.MusicControlPlaylistHolder}>
                {props.playlist.songs.map((song: SongInterface) => (
                    <PlaylistElement song={song}/>
                ))}
            </div>
            <div className={styles.MusicControlPlaybackHolder}>
                    <MusicControlPanel />
            </div>
        </div>
    )
  };
  
  export default MusicControl;