import * as React from 'react';
import Webcam from "react-webcam";
import styles from './css/WebCamFrame.module.css';

function WebCamFrame  (props: any)  {
      const webcamRef = React.useRef(null); // create a webcam reference
      
      const retake = () => {
        props.setImgSrc(null);
      };

      const capture = React.useCallback(() => {
        if(webcamRef.current != null){
        const imageSrc = (webcamRef.current as any).getScreenshot();
        props.setImgSrc(imageSrc);
        }
      }, [webcamRef]);

    return (
        <>
            <div className={styles.WebCamFrameBox}>
                {props.imgSrc ? (
                    <img className={styles.WebCamFrameImg} src={props.imgSrc} style={{maxWidth: props.width, maxHeight: props.height}}/> 
                ) : (
                    <Webcam height={props.height} width={props.width} ref={webcamRef} mirrored={true}/>
                )}
            </div>
            <div className="btn-container">
            {props.imgSrc ? (
                <button className={styles.webCamFrameButton} onClick={retake}>Retake photo</button>
            ) : (
                <button className={styles.webCamFrameButton} onClick={capture}>Take photo</button>
            )}
            </div>
        </>
    )
  };
  
  export default WebCamFrame;