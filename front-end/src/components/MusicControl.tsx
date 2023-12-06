import * as React from 'react';
import styles from './css/MusicControl.module.css';
import SongInterface from '../interface/SongInterface';
import PlaylistElement from './PlaylistElement';
import MusicControlPanel from './MusicControlPanel';
import PlaylistInterface from '../interface/PlaylistInterface';

function MusicControl  (props: any)  {
    const [currentSong, setCurrentSong] = React.useState<SongInterface>();
    

    return (
        <div className={styles.MusicControlFrame}>
            <div className={styles.MusicControlPlaylistHolder}>
                {props.playlist.data &&
                    props.playlist.data.map((song: SongInterface) => (
                        <PlaylistElement key={song.id} song={song}/>
                    ))
                }
            </div>
            <div className={styles.MusicControlPlaybackHolder}>
                    <MusicControlPanel playlist={props.recommendedPlaylist} playlistSongsURI={props.playlistSongsURI} isPlaylistEmpty={props.isPlaylistEmpty} playlistChangeGuard={props.playlistChangeGuard}/>
            </div>
        </div>
    )
  };
  
  export default MusicControl;