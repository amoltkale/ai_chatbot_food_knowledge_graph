import { classes } from "../util"
import styles from "./SignUp.module.css"
export default function TextInput({ label, data, onChange, name, errors, type = "text", icon, ...props }) {

    return <label className={classes(styles["input-group"], styles["required"],type==="textarea"&& styles["column"])}>
        <span className={styles["input-label"]}>{label}</span>
        <div className={styles["input-wrapper"]}>
            <i className={classes(icon, styles["input-icon"])}></i>
            {type === "textarea" ? <textarea value={data[name]} name={name} onChange={onChange} className={styles["input"]} /> : <input value={data[name]} name={name} onChange={onChange} type={type} className={styles["input"]} />}
        </div>
    </label>
}