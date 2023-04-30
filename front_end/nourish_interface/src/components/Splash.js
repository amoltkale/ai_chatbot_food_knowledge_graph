/* Respoinsible for welcoming user to the site and directing them to the onboarding process (sign-up) */

import { Link } from "react-router-dom"
// import { classes } from "../util"
// import styles from "./Splash.module.css"

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
    return <div className="container">
        <div className="column main-section left-section">
            <div className="big-blurb">Welcome to the Nourish Project</div>
            <div>We gather information from various sources to provide an innovative information source for entrepreneurs, organizations, businesses, and anyone interested in learning the business of healthy food.</div>
            <div>
                <Link to="/signup" className="btn">Sign Up</Link>
            </div>
            <div>
                <div>Already a member?</div>
                <Link to="/signup" className="btn">Sign In</Link>
            </div>
        </div>
        <div className="column main-section right-section"></div>
    </div>
}