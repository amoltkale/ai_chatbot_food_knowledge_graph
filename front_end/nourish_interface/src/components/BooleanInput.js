export default function BooleanInput({label, name, data, onChange, errors}){

    return <div>
    <label>{label}</label>
    <div>
        <label><input type="radio" name={name} checked={data[name] === "true"} onChange={onChange} value={true} /> Yes</label>
        <label><input type="radio" name={name} checked={data[name] === "false"} onChange={onChange} value={false} /> No</label>
    </div>
    {/* <span>{errors[name]}</span> */}
</div>
}