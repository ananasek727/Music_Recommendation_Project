import * as React from 'react';
import { Link } from 'react-router-dom';
import styles from './css/HomePage.module.css'

function HomePage  ()  {
    const [isLoggedInToSpotify, setIsLoggedInToSpotify] = React.useState(false);

    // TODO: in description add handling spotify log in and on that basis enable/unable music recommendation button
    
    return (
      <div className={styles.homePageFrame}>
          <div className={styles.homePageBox}>
            <div className={styles.homePageDescription}>
                Description
            </div>
            
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