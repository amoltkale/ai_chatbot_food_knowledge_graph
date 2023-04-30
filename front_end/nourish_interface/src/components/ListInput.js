import { useEffect, useState } from "react";
import { classes } from "../util"
import styles from "./SignUp.module.css"

export default function ListInput({ label, onChange, name, type , icon}) {
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

    return <label className={classes(styles["input-group"], styles["required"])}>
        <span className={styles["input-label"]}>{label}</span>
        <div className={classes(styles["column"],styles["gap-s"])}>
        {list.map((item, index)=><div className={styles["input-wrapper"]}>
            <i className={classes(icon, styles["input-icon"])}></i>

        <input value={item} name={name} onChange={(event) => { updateListItem(index, event.target.value) }} type={type} className={styles["input"]} />
        {list.length > 1 && <button onClick={() => removeListItem(index)}>-</button>}
        </div>)}
        <button type="button" onClick={addListItem}>+</button>
        </div>
    </label>
    return <div>
        <label>{label}</label>
        {list.map((item, index) => {
            return <>
                <input type={type} value={item} onChange={(event) => { updateListItem(index, event.target.value) }} />
                {list.length > 1 && <button onClick={() => removeListItem(index)}>-</button>}
            </>
        })}
        <button onClick={addListItem}>+</button>
    </div>
}