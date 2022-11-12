import {Link} from 'react-router-dom';
export default function Home() {

    return (
        <div class="center">
            <h1>Welcome to Face Attendance!</h1>
            {/* TODO: FIX URL!!! */}
            <Link to="/AdminHome" className="button button1">Teacher Login</Link>
            <Link to="/StudentUpload" className="button button2">Student Login</Link>
        </div>
    )
}