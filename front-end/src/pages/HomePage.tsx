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
              window.location.href = data.url;
            })
            .catch((e) => {
              console.log("Error when trying to log in: " + e);
            });    
    }
    
    
    React.useEffect(()=>{
      handleTokenRequest();
    },[]);

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
                setToken(data.access_token);
                console.log(data);
            })
            .catch((e) => {
              console.log("Error when trying to log in: " + e);
            });   
    }
    return (
      <div className={styles.homePageFrame}>
          <div className={styles.homePageBox}>
            <div className={styles.homePageDescription}>
                Description
            </div>
            {token === null ? 
              <button onClick={handleSpotifyLogin} className={styles.homePageButton}>Log in</button>
            :
              <>
              <Link to="/music">
                  <button className={styles.homePageButton}>
                      Music recommendation
                  </button>
              </Link>  
              </>
            }
          </div>
      </div>
    )
  };
  
  export default HomePage;