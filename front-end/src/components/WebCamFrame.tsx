import * as React from 'react';
import Webcam from "react-webcam";
import styles from './css/WebCamFrame.module.css';

function WebCamFrame  (props: any)  {
      const webcamRef = React.useRef(null); // create a webcam reference
      
      const handleEmotionPrediction = async () => {
        await fetch(`http://127.0.0.1:8000/get-emotion-from-photo`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                "base64_photo": props.imgSrc
              })
              })
              .then((response) => {
                if (response.ok) return response.json();
                else {
                  throw new Error("ERROR " + response.status);
                }
              })
              .then((data) => {
                props.setDetectedEmotion(data.emotion);
                console.log(data);
              })
              .catch((e) => {
                console.log("Error when trying to get users emotion: " + e);
              });
              
      }

      const retake = () => {
        props.setImgSrc(null);
      };

      const capture = React.useCallback(() => {
        if(webcamRef.current != null){
        const imageSrc = (webcamRef.current as any).getScreenshot();
        props.setImgSrc(imageSrc);
        }
      }, [webcamRef]);

      React.useEffect(()=>{
        if(props.imgSrc)
          handleEmotionPrediction();
      },[props.imgSrc])

    return (
        <>
            <div className={styles.WebCamFrameBox}>
                {props.imgSrc ? (
                    <img className={styles.WebCamFrameImg} src={props.imgSrc} style={{maxWidth: props.width, maxHeight: props.height}}/> 
                ) : (
                    <Webcam data-testid="webcam-component" height={props.height} width={props.width} ref={webcamRef} mirrored={true}/>
                )}
            </div>
            <button className={styles.webCamFrameButton} onClick={()=>{props.setImgDecision(0);}}>Back</button>
            {props.imgSrc ? (
                <button className={styles.webCamFrameButton} onClick={retake}>Retake photo</button>
            ) : (
                <button className={styles.webCamFrameButton} onClick={capture}>Take photo</button>
            )}
            
            <div className="btn-container">
            
            </div>
            {props.detectedEmotion &&
            <div>
                Emotion: {props.detectedEmotion}
            </div>
            }
        </>
    )
  };
  
  export default WebCamFrame;