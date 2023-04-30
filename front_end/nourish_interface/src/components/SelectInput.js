import { useEffect, useState } from "react"

export default function SelectInput({label, name, options, onChange}){
    const[value, setValue]=useState("")
    const[other, setOther]=useState("")
    useEffect(()=>{
        if (value==="Other"){
            onChange(name, other)
            return
        }
        onChange(name, value)
    },[value,other,onChange])
return <div>
<label>{label}</label>
<select value={value} name={name} onChange={(e)=>setValue(e.target.value)}>
    <option></option>
    {options.map((entry) => {
        return <option>{entry}</option>
    })}
</select>
{value === "Other" && <input value={other}  onChange={(e)=>setOther(e.target.value)} />}
</div>

}