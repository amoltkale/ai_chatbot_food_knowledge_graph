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
    return <label className={"input-group"}>
      <span className={"input-label"}>{label}</span>
      <div
        className="flex-column flex-grow"
      >
         {options.map((option) => {
            return <label key={option}>
                <input className="input" type="checkbox" onClick={toggleOption} checked={selectedOptions.includes(option)} name={option} />
                <span>{option}</span>
            </label>
        })}
        
        
        {selectedOptions.includes("Other") && <div className="input-wrapper">
          <i className={classes("bi-three-dots", "input-icon")}></i>
          <input className={"input"}  />
        </div>}
      </div>
    </label>
    // <label class="input-group">
    //   <span class="input-label">{label}</span>
    //   <div class="flex-column flex-grow">
    //     {vals.map((e) => (
    //       <div>
    //         <input class="input" type="checkbox" />
    //         {e}
    //       </div>
    //     ))}
    //   </div>
    // </label>
}