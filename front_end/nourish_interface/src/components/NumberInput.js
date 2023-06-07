import { useState } from "react";
import TextInput from "./TextInput";

export default function NumberInput (props){
    // const [innerValue, setInnerValue]=useState("")

    return <TextInput {...props}  type="number"/>
}