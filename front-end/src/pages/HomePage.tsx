import * as React from 'react';
import { Link } from 'react-router-dom';
import styles from './css/HomePage.module.css'

function HomePage  ()  {
    const [token, setToken] = React.useState(null);
    const [isLoggedInToSpotify, setIsLoggedInToSpotify] = React.useState(false);
    const [urlSpotifyLog, setUrlSpotifyLog] = React.useState('');
    // TODO: in description add handling spotify log in and on that basis enable/unable music recommendation button
    const handleSpotifyLogin = async () => {
      await fetch(`http://127.0.0.1:8000/get-auth-url`, {
            method: "GET"
            })
            .then((response) => {
              if (response.ok) return response.json();
              else {
                throw new Error("ERROR " + response.status);
              }
            })
            .then((data) => {
              setUrlSpotifyLog(data.url);
              console.log(data);
              //window.open(data.url, "_blank");
              //console.log("guess who is back");
            })
            .catch((e) => {
              console.log("Error when trying to log in: " + e);
            });    
    }

    // handle getting token 
    

    React.useEffect(()=>{
      const handleTokenRequest = async () => {
        await fetch(`http://127.0.0.1:8000/is-authenticated`, {
              method: "GET"
              })
              .then((response) => {
                if (response.ok) return response.json();
                else {
                  throw new Error("ERROR " + response.status);
                }
              })
              .then((data) => {
                if(data.status == true){
                  setToken(data.access_token);
                  console.log(data);
                }
                console.log(data);
                console.log("s");
              })
              .catch((e) => {
                console.log("Error when trying to log in: " + e);
              });   
            if(token != '') return;
           //  setTimeout(handleTokenRequest, 1000);    
      }
      
          if(token === '') {
           // handleTokenRequest();
          }
    },[urlSpotifyLog]);

    const handleTokenRequest = async () => {
      await fetch(`http://127.0.0.1:8000/is-authenticated`, {
            method: "GET"
            })
            .then((response) => {
              if (response.ok) return response.json();
              else {
                throw new Error("ERROR " + response.status);
              }
            })
            .then((data) => {
              if(data.status == true){
                setToken(data.access_token);
                console.log(data);
              }
              console.log(data);
              console.log("s");
            })
            .catch((e) => {
              console.log("Error when trying to log in: " + e);
            });   
          if(token != '') return;
         //  setTimeout(handleTokenRequest, 1000);    
    }
    return (
      <div className={styles.homePageFrame}>
          <div className={styles.homePageBox}>
            <div className={styles.homePageDescription}>
                Description
            </div>
            <button onClick={handleSpotifyLogin}>Log in</button>
            <button onClick={handleTokenRequest}>token</button>
            <Link to="/music">
                <button className={styles.homePageButton}>
                    Music recommendation
                </button>
            </Link>  
          </div>
      </div>
    )
  };
  
  export default HomePage;