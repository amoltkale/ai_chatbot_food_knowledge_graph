import { classes } from "../util"
import styles from "./SignUp.module.css"
export default function TextInput({ label, data, onChange, name, errors, type = "text", icon, required, ...props }) {

    return <label className={classes("input-group", required && styles["required"],type==="textarea"&& styles["column"])}>
        <span className={"input-label"}>{label}</span>
        <div className={"input-wrapper"}>
            <i className={classes(icon, "input-icon")}></i>
            {type === "textarea" ? <textarea value={data[name]} name={name} onChange={onChange} className={"input"} /> : <input value={data[name]} name={name} onChange={onChange} type={type} className={"input"} />}
        </div>
    </label>

}
