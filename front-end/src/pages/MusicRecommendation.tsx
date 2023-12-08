import * as React from 'react';
import Webcam from 'react-webcam';
import WebCamFrame from '../components/WebCamFrame';
import styles from './css/MusicRecommendationPage.module.css'
import ImageUploadFrame from '../components/ImageUploadFrame';
import MusicParameters from '../components/MusicParameters';
import PlaylistInterface from '../interface/PlaylistInterface';
import MusicControl from '../components/MusicControl';

function MusicRecommendationPage  (props: any)  {
    
  // get current height and width of the window to adjust size of WebCamFrame
  const [windowWidth, setWindowWidth] = React.useState(window.innerWidth*0.3);
  const [windowHeight, setWindowHeight] = React.useState(window.innerHeight*0.3);

  const handleResize = () => {
    setWindowWidth(window.innerWidth*0.3);
    setWindowHeight(window.innerHeight*0.3);
  };

  React.useEffect(() => {
    // Add event listener to update windowWidth/windowHeight state when the window is resized
    window.addEventListener('resize', handleResize);

    // Clean up the event listener on component unmount
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // set variable for storing image
  const [imgSrc, setImgSrc] = React.useState(null); // initialize it

  // set variable for storing users decision whether wants to  take photo based on webcam or upload an image 0-none 1-webcam 2-upload
  const [imgDecision, setImgDecision] = React.useState(0); // initialize it

  // set variable for storing music recommendation parameters
  const [musicParameter1, setMusicParameter1] = React.useState(''); // initialize it
  const [musicParameter2, setMusicParameter2] = React.useState(''); // initialize it
  const [musicParameter3, setMusicParameter3] = React.useState<string[]>([]); // initialize it

  // set variable for detected emotion of a user 
  const [detectedEmotion, setDetectedEmotion] = React.useState('');
  const [recommendedPlaylist, setRecommendedPlaylist] = React.useState<PlaylistInterface[]>([]);
  const [playlistSongsURI, setPlaylistSongURI] = React.useState<string[]>([]);
  const [isPlaylistEmpty, setIsPlaylistEmpty] = React.useState(true);
  const [playlistChangeGuard, setPlaylistChangeGuard] = React.useState(false);

  // const getRecommendedPlaylist = async () => {
  //   await fetch(`http://127.0.0.1:8000/create-playlist-based-on-parameters`, {
  //       method: "POST",
  //       headers: { "Content-Type": "application/json" },
  //       body: JSON.stringify({
  //         "emotion": "sad",
  //         "personalization": "high",
  //         "popularity": "mainstream",
  //         "genres": []
  //       })
  //       })
  //       .then((response) => {
  //           if (response.ok) return response.json();
  //           else {
  //             throw new Error("ERROR " + response.status);
  //           }
  //       })
  //       .then((data)=>{
  //         setRecommendedPlaylist(data);
  //         console.log(data);
  //         const allURI: string[] = data.data.map((item: { uri: any; }) => item.uri);
  //         setPlaylistSongURI(allURI);
  //         console.log(allURI);
  //         setIsPlaylistEmpty(false);
  //         setPlaylistChangeGuard(!playlistChangeGuard);
  //       })
  //       .catch((e) => {
  //       console.log("Error when trying to get playlist with recommended playlist: " + e);
  //       });
  //   }

    return (
      <div className={styles.mRPageFrame}>
          <div className={styles.mRPageBoxLeft}>

            {/* Emotion recognition part */}
            <div className={styles.mRPageBoxLeftText}>
              Emotion recognition
            </div>

            {/* User can decide whether wants to  take photo based on webcam or upload an image*/}
            {imgDecision === 0 && (
              <div className={styles.mRPageBoxLeftDecisionButtonFrame}>
                <button className={styles.mRPageBoxLeftDecisionButton} onClick={()=>setImgDecision(1)}>Web cam</button>
                <button className={styles.mRPageBoxLeftDecisionButton} onClick={()=>setImgDecision(2)}>Upload image</button>
              </div>
            )}
            {imgDecision === 1 && (
              <div className={styles.mRPageBoxLeftWebCamFrame}>
                <WebCamFrame width={windowWidth} height={windowHeight} setImgDecision={setImgDecision} setImgSrc={setImgSrc} imgSrc={imgSrc} setDetectedEmotion={setDetectedEmotion} detectedEmotion={detectedEmotion} />
              </div>
            )}
            {imgDecision === 2 && (
              <div className={styles.mRPageBoxLeftUploadFrame}>
                <ImageUploadFrame width={windowWidth} height={windowHeight} setImgDecision={setImgDecision} setImgSrc={setImgSrc} imgSrc={imgSrc} setDetectedEmotion={setDetectedEmotion} detectedEmotion={detectedEmotion} />
              </div>
            )}

            {/*  Display music parameters choice */}
            <div className={styles.MRPageBoxLeftParametersFrame}>
              <div className={styles.mRPageBoxLeftText}>
                Music recommendation parameters
              </div>
              <MusicParameters musicParameter1={musicParameter1} musicParameter2={musicParameter2} musicParameter3={musicParameter3} setMusicParameter1={setMusicParameter1} setMusicParameter2={setMusicParameter2} setMusicParameter3={setMusicParameter3} detectedEmotion={detectedEmotion} setRecommendedPlaylist={setRecommendedPlaylist} setPlaylistSongURI={setPlaylistSongURI} setIsPlaylistEmpty={setIsPlaylistEmpty} setPlaylistChangeGuard={setPlaylistChangeGuard} playlistChangeGuard={playlistChangeGuard} />
            </div>
          </div>
          {/* Music control section, right frame */}
          <div className={styles.mRPageBoxRight}>
              <MusicControl playlist={recommendedPlaylist} playlistSongsURI={playlistSongsURI} isPlaylistEmpty={isPlaylistEmpty} playlistChangeGuard={playlistChangeGuard} setIsLoggedInSpotify={props.setIsLoggedInSpotify}/>
          </div>
      </div>
    )
  };
  
  export default MusicRecommendationPage;