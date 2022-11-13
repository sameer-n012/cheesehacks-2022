import {Link} from 'react-router-dom';

export default function Home() {
    return (
        <div class="center">
            <h1>Welcome to Face Attendance!</h1>
            <br></br>
            
            {/* Form Padding  */}
            <form action="/api/email_check" method="POST">
                <label for="email">Email:</label>
                <input type="text" id="email" name="email"></input>
                <input type="submit" value="Login" className='button submit m-3'></input>
            </form>

            {/* Sign Up Buttons */}
            <Link to="/admin" className="button button1 m-2">Teacher Sign Up</Link>
            <Link to="/student" className="button button2 m-2">Student Sign Up</Link>
        </div>
    )
}