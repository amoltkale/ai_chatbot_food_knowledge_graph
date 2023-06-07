import { useCallback, useState } from "react"
import { useNavigate } from "react-router-dom"
import EmailInput from "./EmailInput"
import styles from "./SignUp.module.css"
import TextInput from "./TextInput"



export default function SignIn() {
    const navigate = useNavigate()
    /* state variables responsible for holding the login information*/
    const [data, setData] = useState({  
        email: "",
        password: ""
    })

    const [errors, setErrors] = useState({})

    const updateDataDirect = useCallback((key, value) => {
        setData((prevData) => {
            return {
                ...prevData,
                [key]: value
            }
        })

    }, [])

    const updateData = useCallback((event) => {
        const key = event.target.name
        const value = event.target.value

        updateDataDirect(key, value)
    }, [updateDataDirect])

    async function handleSubmit(e){
        e.preventDefault()
        const response=await fetch("/api/user/login",{
            method:"POST",
            body:JSON.stringify(data),
            headers:{
                "Content-Type":"application/json"
            }
        })
        if(response.ok){
            navigate("/account")
        } else{
            alert("invalid account information")
        }
    }

// Registered User - Sign in Form
return <form onSubmit={handleSubmit}>

    <div className={styles["form-container"]}>
        {/* <div>*indicates required field</div> */}
        <EmailInput icon="bi-envelope" label="Primary Email" data={data} errors={errors} name="email" onChange={updateData} />
        <TextInput type="password" icon="bi-lock-fill" label="Password" data={data} errors={errors} name="password" onChange={updateData} />
        <div>
            <div>
                <button className="btn">Sign In</button>
            </div>
            {/* <div>Forgot Password? Click here to reset.</div>
            <Link to="/signup" className="btn">Reset password</Link> */}
        </div>
    </div>
</form>

}