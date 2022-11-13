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
            
            {/* Form Padding 
            <form action="/api/email_check" method="POST">
                <label for="email">Email:</label>
                <input type="text" id="email" name="email"></input>
                <br></br>
                <input type="submit" value="Login" className='button submit' onClick={sendMessage}></input>
            </form>
            */}


            {/* Sign Up Buttons */}
            <Link to="/admin" className="button button1">Teacher Sign Up</Link>
            <Link to="/student" className="button button2">Student Sign Up</Link>
        </div>
    )
}