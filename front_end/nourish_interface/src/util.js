export function classes(...classNames){
    return classNames.filter(e=>e).join(" ")
}