import {Link} from 'react-router-dom';
import { Container, Accordion, Form} from 'react-bootstrap'

export default function Home() {

    return (
        <div class="center">
            <h1>Welcome to Face Attendance!</h1>

           
            <Link to="/AdminHome" className="button button1">Teacher Login</Link>
            <Link to="/Student" className="button button2">Student Login</Link>
        </div>
    )
}