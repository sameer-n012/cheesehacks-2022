import {Link} from 'react-router-dom';

export default function Home() {

    async function sendMessage() {
        
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({email: document.getElementById('email').value})
        }
    
        const rawRes = await fetch('/api/email-check/', requestOptions)
        const jsonRes = await rawRes.text()
        alert(`json response: ${jsonRes}`)
    }

    return (
        <div class="center">
            <h1>Welcome to Face Attendance!</h1>
            <br></br>
            
            {/* Form Padding */}
            {/* <div class="form">
                <label for="email">Email:</label>
                <input type="text" id="email" name="email"></input>
                <br></br>
                <input value="Login" className='button submit' onClick={sendMessage}></input>
            </div> */}
            
            {/* Sign Up Buttons */}
            <Link to="/AdminHome" className="button button1 me-2">Teacher Sign Up</Link>
            <Link to="/Student" className="button button2 ms-1">Student Sign Up</Link>
        </div>
    )
}