import * as React from 'react';
import styles from './css/MusicParameters.module.css';

function MusicParameters  (props: any)  {

    // get recommended playlist
    const handlePlaylistRecommendation = async () => {
        await fetch(`http://127.0.0.1:8000/create-playlist-based-on-parameters`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                "emotion": props.detectedEmotion,
                "personalization": props.musicParameter2,
                "popularity": props.musicParameter1,
                "genres": props.musicParameter3
              })
              })
              .then((response) => {
                if (response.ok) return response.json();
                else {
                  throw new Error("ERROR " + response.status);
                }
              })
              .then((data) => {
                props.setRecommendedPlaylist(data);
                console.log(data);
              })
              .catch((e) => {
                console.log("Error when trying to get recommended playlist: " + e);
              });       
      }
    
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
                <option value="mainstream">Mainstream</option>
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
            {/* Genres */}
            <button onClick={handlePlaylistRecommendation}>Recommend music</button>
        </div>
    )
  };
  
  export default MusicParameters;