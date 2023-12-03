import * as React from 'react';
import styles from './css/MusicParameters.module.css';

function MusicParameters  (props: any)  {

    const handleChangePopularity = (event: React.ChangeEvent<HTMLSelectElement>) => {
        props.setMusicParameter1(event.target.value);
    };

    const handleChangePersonalization = (event: React.ChangeEvent<HTMLSelectElement>) => {
        props.setMusicParameter2(event.target.value);
    };
    return (
        <div className={styles.MusicParametersBox}>
            {/* Popularity */}
            <select className={styles.MusicParametersSelect} value={props.musicParameter1} onChange={handleChangePopularity}>
                <option value="">Popularity</option>
                <option value="high">Mainstream</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
            </select>
            {/* Personalization level */}
            <select className={styles.MusicParametersSelect} value={props.musicParameter2} onChange={handleChangePersonalization}>
                <option value="">Personalization</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
            </select>
        </div>
    )
  };
  
  export default MusicParameters;