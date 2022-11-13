import {Link} from 'react-router-dom';

export default function Home() {

    const handleEmailChange = (e) => {
        localStorage.setItem('current_userid', e.target.value);
    }

    return (
        <div class="center">
            <h1>Welcome to Face First!</h1>
            <br></br>
            
            {/* Form Padding  */}
            <form className='form' action="/api/email_check" method="POST">
                <label for="email">Email:</label>
                <input type="text" id="email" name="email" onChange={(e) => {handleEmailChange(e)}}></input>
                <input type="submit" value="Login" className='button submit m-3'></input>
                <br></br>
                <button className='button button1 m-2' formAction='/api/teacher_sign_up'> Teacher Sign Up </button>
                <button className='button button2 m-2' formAction='/api/student_sign_up'> Student Sign Up </button>
            </form>

            {/* Sign Up Buttons
            <Link to="/admin" className="button button1 m-2">Teacher Sign Up</Link>
            <Link to="/student" className="button button2 m-2">Student Sign Up</Link> */}
        </div>
    )
}