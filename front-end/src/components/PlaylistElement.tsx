import * as React from 'react';
import styles from './css/PlaylistElement.module.css';

function PlaylistElement  (props: any)  {

    return (
        <div className={styles.PlaylistElementFrame}>
      {/* Left side with one row */}
            <div className={styles.PlaylistElementLeft}>
                <img className={styles.PlaylistElementImage} src="https://images.unsplash.com/photo-1575936123452-b67c3203c357?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aW1hZ2V8ZW58MHx8MHx8fDA%3D"
               />
            </div>

      {/* Right side with two rows */}
            <div className={styles.PlaylistElementRight}>
                <div className={styles.PlaylistElementText} style={{fontSize: '20px', fontWeight: 'bold'}}>
                    {props.song.title}
                </div>
                <div className={styles.PlaylistElementText} style={{fontSize: '15px'}}>
                    {props.song.artist}
                </div>
            </div>
            
            </div>
    )
  };
  
  export default PlaylistElement;