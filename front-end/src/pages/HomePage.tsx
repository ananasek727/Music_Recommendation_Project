import * as React from 'react';
import { Link } from 'react-router-dom';
import styles from './css/HomePage.module.css'

function HomePage  (props: any)  {
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
      await fetch(`http://127.0.0.1:8000/access-token`, {
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
                props.setIsLoggedInSpotify(true);
            })
            .catch((e) => {
              console.log("Error when trying to log in: " + e);
            });   
    }
    return (
      <div className={styles.homePageFrame}>
          <div className={styles.homePageBox}>
            <div className={styles.homePageDescription}>
            Project of a music recommending application based on emotion recognition
            <br/><br/>
            Prepared as a part of bachelor's diploma thesis in the field of study Computer Science and Information Systems at the Warsaw University of Technology by Błażej Misiura, Piotr Możeluk and Justyna Pokora, supervisor
            dr hab. inż. Jerzy Balicki, prof. ucz.
            <br/><br/>
            Mus4You is an innovative music recommendation application designed to curate playlists tailored to your emotions, preferred genres, personalization level, and popularity preferences. With an intuitive interface and seamless integration with Spotify, Mus4You aims to elevate your music listening experience by delivering curated playlists that resonate with your mood and taste.
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