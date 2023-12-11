import * as React from 'react';
import styles from './css/PlaylistElement.module.css';

function PlaylistElement  (props: any)  {

    return (
        <div data-testid="playlist-element" className={styles.PlaylistElementFrame}>
      {/* Left side with one row */}
            <div className={styles.PlaylistElementLeft}>
                <img className={styles.PlaylistElementImage} src={props.song.image_url}
               />
            </div>

      {/* Right side with two rows */}
            <div className={styles.PlaylistElementRight}>
                <div className={styles.PlaylistElementText} style={{fontSize: '20px', fontWeight: 'bold'}}>
                    {props.song.title}
                </div>
                <div className={styles.PlaylistElementText} style={{fontSize: '15px'}}>
                    {props.song.artist_str}
                </div>
            </div>
            
        </div>
    )
  };
  
  export default PlaylistElement;