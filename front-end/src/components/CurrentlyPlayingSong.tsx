import * as React from 'react';
import styles from './css/CurrentlyPlayingSong.module.css';

function CurrentlyPlayingSong  (props: any)  {

    return (
        <div className={styles.CurrentlyPlayingSongFrame}>
      {/* Left side with one row */}
            <div className={styles.CurrentlyPlayingSongLeft}>
                <img className={styles.CurrentlyPlayingSongImage} src={props.song.image_url}
               />
            </div>

      {/* Right side with two rows */}
            <div className={styles.CurrentlyPlayingSongRight}>
                <div className={styles.CurrentlyPlayingSongText} style={{fontSize: '20px', fontWeight: 'bold'}}>
                    {props.song.title}
                </div>
                <div className={styles.CurrentlyPlayingSongText} style={{fontSize: '15px'}}>
                    {props.song.artist}
                </div>
                <div className={styles.CurrentlyPlayingSongText} style={{fontSize: '15px'}}>
                    {props.song.time_stamp}/{props.song.duration}
                </div>
            </div>
            
        </div>
    )
  };
  
  export default CurrentlyPlayingSong;