import { useEffect, useState } from "react";
import { classes } from "../util"
import styles from "./SignUp.module.css"

export default function ListInput({ label, onChange, name, type , icon, required}) {
    const [list, setList] = useState([""])
    useEffect(() => {
        onChange(name, list)
    }, [list, onChange, name])

    function addListItem() {
        setList((previous) => {
            return [...previous, ""]
        })
    }

    function removeListItem(i) {
        setList((previous) => {
            return previous.filter((_item, index) => {
                return index != i
            })
        })
    }

    function updateListItem(i, newItem) {
        setList((previous) => {
            return previous.map((item, index) => {
                return index != i ? item : newItem
            })
        })
    }

    return <label className={classes("input-group", styles["required"])}>
        <span className={"input-label"}>{label}</span>
        <div className="flex-column flex-grow">
        {list.map((item, index)=><div className={"input-wrapper"}>
            <i className={classes(icon, "input-icon")}></i>

        <input value={item} name={name} onChange={(event) => { updateListItem(index, event.target.value) }} type={type} className={"input"}/>
        {/* <input value={item} name={name} onChange={(event) => { updateListItem(index, event.target.value) }} type={type} className={styles["input"]} /> */}

        {list.length > 1 && <button onClick={() => removeListItem(index)}>-</button>}
        </div>)}
        <button type="button" onClick={addListItem}>+</button>
        </div>
    </label>
  
}