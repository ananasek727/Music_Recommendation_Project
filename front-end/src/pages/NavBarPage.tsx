import { Link, useLocation } from 'react-router-dom';
import styles from './css/NavBarPage.module.css'

function NavBarPage  ()  {
  const location = useLocation();
  const isMusicRoute = location.pathname === '/music';

    return (
      <div className={styles.navBarFrame}>
          <div className={styles.navBarTitle}>
            Mus4You
          </div>
          {isMusicRoute && (
            <Link to="/">
              <button className={styles.navBarButton}>
                Home
              </button>
            </Link>
          )}
      </div>
    )
  };
  
  export default NavBarPage;