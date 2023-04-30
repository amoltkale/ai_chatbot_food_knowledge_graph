import { useState } from "react"

export default function ChatBox() {
	const [chat, setChat] = useState([])
	function handle_submit(e){
		e?.preventDefault()
		handle_new_message(e.target.message.value)
	}
	async function handle_new_message(new_message) {
		

		const userMessage = { message: new_message, sender: "user" }
		setChat((prev) => {
			return [...prev, userMessage]
		})

		const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(userMessage)
		})
		const data = await response.json()
		console.log(data)
		const botMessage = {
			sender: "bot",
			message: data[0].text
		}
		setChat((prev) => {
			return [...prev, botMessage]
		})
	}
	return <div className="chatbox-container"> 

		<div className="chatbox-title">What stage is your business at? </div>
		<div className="chatbox-input-container">
			<div className="chatbox-buttons-container">
				<button onClick={()=>{handle_new_message("New Business")}}>Getting ready to start</button>
				<button onClick={()=>{handle_new_message("Operational less than two years")}}>Operational less than 2 years</button>
				<button onClick={()=>{handle_new_message("Established Business")}}>Established Business</button>
			</div>
			<form onSubmit={handle_submit}>
				<input name="message" type="text" />
				<button>send</button>
			</form>
			
		</div>
		<div className="chatbox-messages-container">
		{chat.map((message)=>{
			return <div>{message.message} - {message.sender}</div>
		})}
		</div>
		
	</div>


}