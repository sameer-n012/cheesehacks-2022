import { Container, Button } from 'react-bootstrap'
import { useNavigate } from 'react-router';


export default function Header({page}) {

    const currentUser = localStorage.getItem('current_userid');

    let navigate = useNavigate();

    const logout = () => {
        localStorage.setItem('current_userid', null);
        navigate('/');
    }

    const login = () => {
        navigate('/')
    }

    const uploadImage = () => {
        navigate('/upload')
    }

    // TODO insert application name
	return (
		<Container fluid className='header w-100 p-3 d-flex  align-items-center uw-red-bg'>
			<h2 className='header-title text-white w-50'>Face Attendance</h2>
            <Container className='w-50 d-flex align-items-center justify-content-end'>
                {page == 'student_home' ? (
                    <div>
                        <Button variant='outline-light' className='header-button m-2' onClick={() => {alert('incomplete')}}>Join Class</Button>
                        <Button variant='outline-light' className='header-button m-2' onClick={() => {uploadImage()}}>Upload Image</Button>
                    </div>
                ) : page == 'teacher_home' ? (
                    <div>
                        <Button variant='outline-light' className='header-button m-2' onClick={() => {alert('incomplete')}}>Create Class</Button>
                    </div>
                ) : (
                    <div>
                    </div>
                )}

                {currentUser != null ? (
                    <Button variant='outline-light' className='header-button m-2' onClick={() => {logout()}}>Log Out</Button>
                ) : (
                    <Button variant='outline-light' className='header-button m-2' onClick={() => {login()}}>Sign In</Button>
                )}
            </Container>
		</Container>
	);
}
