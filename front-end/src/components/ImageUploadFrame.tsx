import * as React from 'react';
import styles from './css/ImageUploadFrame.module.css';

function ImageUploadFrame  (props: any)  {

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
            })
            .catch((e) => {
              console.log("Error when trying to get users emotion: " + e);
            });
            
    }
    
    const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const fileList = event.target.files;
        if (fileList && fileList[0]) {
          const reader = new FileReader();
          reader.onload = () => {
            if (reader.readyState === 2) {
              const base64 = reader.result as string;
              props.setImgSrc(base64);
            }
          };
          reader.readAsDataURL(fileList[0]);
        }
      };

    return (
        <>
           {props.imgSrc === null ? (
            <div className={styles.imageUploadFrameDiv}>
              <input data-testid="input-file" className={styles.imageUploadFrameBox}
                      type="file"
                      accept="image/*"
                      onChange={handleImageChange}
                  />
              <button className={styles.imageUploadFrameButton} onClick={()=>{props.setImgDecision(0);}}>Back</button>
            </div>
           ) : (
            <div className={styles.imageUploadFramePreview}>
                <img src={props.imgSrc} style={{maxWidth: props.width, maxHeight: props.height}}/>
                <div className={styles.imageUploadFrameDiv}>
                  <button className={styles.imageUploadFrameButton} onClick={()=>{props.setImgSrc(null)}}>Reupload image</button>
                  <button className={styles.imageUploadFrameButton} onClick={()=>{handleEmotionPrediction()}}>Predict emotion</button>
                  <button className={styles.imageUploadFrameButton} onClick={()=>{props.setImgDecision(0);}}>Back</button>
                </div>
            </div>
           )}
           {props.detectedEmotion &&
           <div>
              Emotion: {props.detectedEmotion}
           </div>
           }
         </>
    )
  };
  
  export default ImageUploadFrame;