import { Link, useLocation } from 'react-router-dom';
import styles from './css/NavBarPage.module.css'

function NavBarPage  (props: any)  {
  const location = useLocation();
  const isMusicRoute = location.pathname === '/music';

  const handleLogOut = async () => {
    await fetch(`http://127.0.0.1:8000/logout`, {
          method: "DELETE"
          })
          .then((response) => {
            if (response.ok) return response.json();
            else {
              throw new Error("ERROR " + response.status);
            }
          })
          .then((data) => {
            window.open(data.url, '_blank');
            window.location.reload();
          })
          .catch((e) => {
            console.log("Error when trying to log in: " + e);
          });   
  }

    return (
      <div className={styles.navBarFrame}>
          <div className={styles.navBarTitle}>
            Mus4You
          </div>
          {props.isLoggedInSpotify &&
            <button className={styles.navBarButton} onClick={handleLogOut}>
              Logout
            </button>
          }
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