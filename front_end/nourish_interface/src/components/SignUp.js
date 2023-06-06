/* Collecting information 
from the user for the onboarding process */
import { useCallback, useState } from "react"
import { useNavigate, Link} from "react-router-dom"
import { classes } from "../util"
import EmailInput from "./EmailInput"
import CheckListInput from "./CheckListInput"
import PhoneInput from "./PhoneInput"
import styles from "./SignUp.module.css"
import TextInput from "./TextInput"
import ListInput from "./ListInput"
import SelectInput from "./SelectInput"
import NumberInput from "./NumberInput"
import BooleanInput from "./BooleanInput"
import logo from "../images/Logo_black.PNG"

/* Default function - Takes us to each sub-page for the sign up process */
export default function SignUp() {
    const [aboutMeData, setAboutMeData] = useState(null)
    //const [projectData, setProjectData] = useState(null)
    async function addFinalData(data) {

        const response = await fetch('/api/user/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ...data,
                ...aboutMeData

            })
        })
    }
    function pageContent() {
        if (aboutMeData === null) {
            return <AboutMe onSubmit={setAboutMeData} />
        }
        return <AboutMyProject onSubmit={addFinalData} />
    }
    return <>
    <nav className="main-nav">
        <Link to="/">HOME</Link>
       
    </nav> 
        <div>
          <img className="img-logo" src={logo}/>

          </div>
        {pageContent()}
    </>
}
/* 2nd form page */
function AboutMyProject({ onSubmit }) {
    const [data, setData] = useState({
        current_business_description: "",
        prospective_business_description: "",
        extending_existing_business: "",
        biz_street_address: "",
        biz_city: "",
        biz_state: "",
        biz_zip: "",
        how_many_years_in_current_business: "0",
        nominal_current_revenue: "0",
        desired_funding: "0",
        business_role: "",
        additional_comments: ""
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

    /* function responsible for updating the value for a single value input*/
    const updateData = useCallback((event) => {
        const key = event.target.name
        const value = event.target.value

        updateDataDirect(key, value)
    }, [updateDataDirect])
    function handleSubmit(event) {
        event.preventDefault()
        onSubmit(data)

    }

    return <form onSubmit={handleSubmit}>
        {/* <div style={{ display: "flex", flexDirection: "column" }}> */}
        <div className="form-container flex-column">
            <BooleanInput label="Is this an existing business?" name="extending_existing_business" onChange={updateData} data={data} />

            {/* Existing Business */}
            {data.extending_existing_business === "true" && <>
               
                    <TextInput icon="bi-building" className={styles.grow} type="textarea" autofocus data={data} errors={errors} label="Business Name" onChange={updateData} />

                
                    <TextInput icon="bi-map" data={data} errors={errors} name="biz_street_address" label="Street Address" onChange={updateData} />
                
                    <TextInput icon="bi-map" data={data} errors={errors} name="biz_city" label="City" onChange={updateData} />
                
                    <TextInput icon="bi-map" data={data} errors={errors} name="biz_state" label="State" onChange={updateData} />
                
                    <TextInput icon="bi-map" data={data} errors={errors} name="biz_zip" label="Zip Code" onChange={updateData} />
                

                {/* Existing Business */}
                
                    <NumberInput icon="bi-currency-dollar" data={data} errors={errors} name="current_revenue" label="Current Revenue" onChange={updateData} />
                
                    <NumberInput icon="bi-clock-history"data={data} errors={errors} name="how_many_years_in_current_business" label="How many years in current business?" onChange={updateData} />
               
                {/* Chat section */}
                
                
                    <TextInput icon="bi-chat-left-text" className={styles.grow} type="textarea" autofocus data={data} errors={errors} name="current_business_description" label="Briefly tell us what you are looking for" onChange={updateData} />
    
                    <TextInput icon="bi-chat-left-text" className={styles.grow} type="textarea" autofocus data={data} errors={errors} onChange={updateData}  label="Based on what you are looking for, can you tell us more about the financial assitance you mentioned?"/>
               
                    <NumberInput icon="bi-currency-dollar" data={data} errors={errors} name="desired_funding" label="Desired Funding" onChange={updateData} />
                
                
                    <TextInput icon="bi-person-badge" data={data} errors={errors} name="business_role" label="Business Role" onChange={updateData} />
                
                <button className="btn">Submit</button>
                

            </>}
            {/* New Business */}
            {data.extending_existing_business === "false" && 
                <TextInput data={data} errors={errors} name="prospective_business_description" label="Prospective Business Description" onChange={updateData} />
            
            }


            {/* New and Existing Business
            {data.extending_existing_business && <><div className={styles.row}>
                <NumberInput data={data} errors={errors} name="desired_funding" label="Desired Funding" onChange={updateData} />
            </div>
                <div></div>
                <div className={styles.row}>
                    <TextInput data={data} errors={errors} name="business_role" label="Business Role" onChange={updateData} />
                </div>
                <div><button className="btn">Submit</button>
                </div>
            </>} */}
        </div>
    </form>
}
/* Ethnicities available list*/
const ethnicities = [
    "Hispanic",
    "White alone, non-Hispanic",
    "Black or African American alone, non-Hispanic",
    "American Indian and Alaska Native alone, non-Hispanic",
    "Asian alone, non-Hispanic",
    "Native Hawaiian and Other Pacific Islander alone, non-Hispanic",
    "Multiracial, non-Hispanic",
    "Other"
]
/*Languages Spoken available list  */
const languages = [
    "Arabic",
    "Bengali",
    "Chinese",
    "English",
    "French",
    "Hindi",
    "Korean",
    "Mandarin Chinese",
    "Spanish",
    "Vietnamese",
    "Other"
]
/* Gender - available list for drop down input */
const genders = [
    "Agender",
    "Cisgender",
    "Non-binary",
    "Man",
    "Transgender",
    "Woman",
    "Prefer Not to Answer",
    "Other"
]
/* first form */
function AboutMe({ onSubmit }) {
    const navigate = useNavigate()
    /* state variables responsible for holding on to all of the single value input*/
    const [data, setData] = useState({
        first_name: "",
        middle_name: "",
        last_name: "",
        home_street_address: "",
        email: [""],
        phone: [""],
        gender: "",
        is_veteran: "false",
        // otherEthnicity: "",
        // otherGender: "",
        // otherLanguage: ""
    })
    /* state variables responsible for storing the values of the list inputs*/
    // const [selectedEthnicities, setSelectedEthnicities] = useState([])
    // const [selectedLanguagesWritten, setSelectedLanguagesWritten] = useState([])
    // const [selectedLanguagesSpoken, setSelectedLanguagesSpoken] = useState([])
    const [errors, setErrors] = useState({})

    const updateDataDirect = useCallback((key, value) => {
        setData((prevData) => {
            return {
                ...prevData,
                [key]: value
            }
        })

    }, [])

    /* function responsible for updating the value for a single value input*/
    const updateData = useCallback((event) => {
        const key = event.target.name
        const value = event.target.value

        updateDataDirect(key, value)
    }, [updateDataDirect])



    /* */
    async function handleSubmit(event) {
        event.preventDefault()
        onSubmit(data)
        return
        /* Error handling  */
        const newErrors = {}
        let errored = false
        /*looks each field inside of the single value input data*/
        for (const key in data) {
            if (key.startsWith("other")) {
                continue
            }
            const value = data[key]
            if (value === '') {
                errored = true
                newErrors[key] = 'This field is required.'
            }
        }


        setErrors(newErrors)
        /*if there are errors we do not submit the form and 
        render the errors on the page */
        if (errored) {
            return
        }

        onSubmit({
            ...data,

        })
    }

    return <form onSubmit={handleSubmit}>

        <div className="form-container flex-column">
            {/* <div>*indicates required field</div> */}
            <TextInput autoFocus icon="bi-person" data={data} errors={errors} name="first_name" label="First Name" onChange={updateData} className={classes(styles.grow, styles.row)} />
            <TextInput icon="bi-person" data={data} errors={errors} name="middle_name" label="Middle Name" onChange={updateData} className={classes(styles.grow, styles.row)} />
            <TextInput icon="bi-person" data={data} errors={errors} name="last_name" label="Last Name" onChange={updateData} className={classes(styles.grow, styles.row)} />
            <TextInput icon="bi-map" label="Home Address" data={data} errors={errors} name="home_street_address" onChange={updateData} />
            <ListInput icon="bi-envelope" type="email" name="email" label="Email" onChange={updateDataDirect} />
            <ListInput icon="bi-phone" type="tel" name="phone" label="Phone" onChange={updateDataDirect} />
            <CheckListInput styles="input-list-wrapper" name="ethnicity" label="Ethnicity" options={ethnicities} onChange={updateDataDirect} />
            <CheckListInput name="languages_spoken" label="Languages you speak" options={languages} onChange={updateDataDirect} />
            <CheckListInput name="languages_written" label="Languages you write in" options={languages} onChange={updateDataDirect} />
            <BooleanInput label="Are You a Veteran?" name="is_veteran" onChange={updateData} data={data} />
            <div>
                <button className="btn" type="button" onClick={() => navigate("/")}>Cancel</button>
                <button className="btn" >Next</button>
            </div>
        </div>

    </form>

    
}