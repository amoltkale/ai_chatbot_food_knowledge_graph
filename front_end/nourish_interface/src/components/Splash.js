/* Respoinsible for welcoming user to the site and directing them to the onboarding process (sign-up) */

import { Link } from "react-router-dom"
import { classes } from "../util"
import styles from "./Splash.module.css"
import logo from "../images/logo_white.PNG"

// export default function Splash(){
//     const navigate=useNavigate()
//     return <div className={styles.center}>
//         <div className={styles.center}>
//             <h1>Nourish</h1>
//             <p>We nourish businesses in fresh food</p>
//         </div>
//         <div className={classes(styles.center, styles.callout)} onClick={()=>{navigate("/signup")}}>
//             <p>Are you an entrepreneur looking to help?</p>
//             <p>Sign Up</p>
//         </div>
//     </div>
// }
export default function Splash() {
    return <div className={classes("container",styles.bg_home)}>
        <div className="main-section left-section">
            
                <img  src={logo}/>
           
            
        </div>
        <div className="main-section right-section">
       
                <Link to="/signup" className="btn">Sign Up</Link>
                
                <Link to="/signin" className="btn">Sign In</Link>
            
        </div>
    </div>
}