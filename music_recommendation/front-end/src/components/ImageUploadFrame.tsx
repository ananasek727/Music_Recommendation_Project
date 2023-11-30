import * as React from 'react';
import styles from './css/ImageUploadFrame.module.css';

function ImageUploadFrame  (props: any)  {

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
        <div >
           {props.imgSrc === null ? (
            <input className={styles.imageUploadFrameBox}
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                />
           ) : (
            <div className={styles.imageUploadFramePreview}>
                <img src={props.imgSrc} style={{maxWidth: props.width, maxHeight: props.height}}/>
                <button className={styles.imageUploadFrameBox} onClick={()=>{props.setImgSrc(null)}}>Reupload image</button>
            </div>
           )}
         </div>
    )
  };
  
  export default ImageUploadFrame;