import { useEffect, useState } from "react"
import { classes } from "../util"
import styles from "./SignUp.module.css"


export default function CheckListInput({label, options, onChange, name}) {
    const[selectedOptions, setSelectedOptions]=useState([])
    const[otherOption, setOtherOption]=useState("")

    useEffect(()=>{
        onChange(name, selectedOptions.includes("Other") ? [...selectedOptions, otherOption] : selectedOptions)
    },[selectedOptions, otherOption, onChange, name])
    function toggleOption(event) {
        const option = event.target.name
        const enabled = event.target.checked

        if (enabled) {
            setSelectedOptions((prev) => {
                return [
                    ...prev,
                    option
                ]
            })
        } else {
            setSelectedOptions((prev) => {
                return prev.filter((prevOption) => {
                    return prevOption !== option
                })
            })
        }
    }
    return <label className={styles["input-group"]}>
      <span className={styles["input-label"]}>{label}</span>
      <div
        className={classes(
          styles["input-wrapper"],
          styles["column"],
          styles["gap-s"]
        )}
      >
         {options.map((option) => {
            return <label key={option}>
                <input type="checkbox" onClick={toggleOption} checked={selectedOptions.includes(option)} name={option} />
                <span>{option}</span>
            </label>
        })}
        
        
        {selectedOptions.includes("Other") && <div className={styles["input-wrapper"]}>
          <i className={classes("bi-three-dots", styles["input-icon"])}></i>
          <input className={styles["input"]}  />
        </div>}
      </div>
    </label>
    return <div className={styles.column}>
        <label >{label}</label>
        {options.map((option) => {
            return <label key={option}>
                <input type="checkbox" onClick={toggleOption} checked={selectedOptions.includes(option)} name={option} />
                {option}
            </label>
        })}
        {selectedOptions.includes("Other") && <input value={otherOption}  onChange={(e)=>{setOtherOption(e.target.value)}} />}
        {/* <span>{errors.selectedEthnicities}</span> */}
    </div>
}