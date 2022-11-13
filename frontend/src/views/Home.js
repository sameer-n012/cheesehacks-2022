import {Link} from 'react-router-dom';
export default function Home() {

    return (
        <div class="center">
            <h1>Welcome to Face Attendance!</h1>
            
            {/* Form Padding */}
            <form action="/api/email_check" method="POST">
                <label for="email">Email:</label>
                <input type="text" id="email" name="email"></input>
                <br></br>
                <input type="submit" value="Login" className='button submit'></input>
            </form>

            {/* Sign Up Buttons */}
            <Link to="/AdminHome" className="button button1">Teacher Sign Up</Link>
            <Link to="/Student" className="button button2">Student Sign Up</Link>
        </div>
    )
}