import {Link} from 'react-router-dom';

async function sendMessage() {
    // const classCode = inputRef.current.value
    //console.log('inside sendImage function: ' + JSON.stringify(img))
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // body: JSON.stringify({image: img})
    }
    // if (classCode) { // Truthy check, see if classCode is not empty string
    //     console.log("sending image: . . . ")
    //     console.log(img)
    //     const rawRes = await fetch('/api/email_check/' + classCode, requestOptions)
    //     const jsonRes = await rawRes.json()
    //     console.log(`json response: ${jsonRes.foundUser}`)
    // }

    const rawRes = await fetch('/api/email_check/', requestOptions)
    const jsonRes = await rawRes.json()
    alert(`json response: ${jsonRes.message}`)
}

export default function Home() {
    return (
        <div class="center">
            <h1>Welcome to Face Attendance!</h1>
            
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