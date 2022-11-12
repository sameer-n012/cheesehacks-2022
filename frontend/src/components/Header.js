import { Container, Button } from 'react-bootstrap'

export default function Header({page}) {

    // TODO insert application name
	return (
		<Container fluid className='header w-100 p-3 d-flex  align-items-center uw-red-bg'>
			<h2 className='header-title text-white w-50'>Face Attendance</h2>
            {page == 'student_home' ? (
                <Container className='w-50 d-flex align-items-center justify-content-end'>
                    <Button variant='outline-light' className='header-button m-2'>Join Class</Button>
                    <Button variant='outline-light' className='header-button m-2'>Upload Image</Button>
                    <Button variant='outline-light' className='header-button m-2'>Log Out</Button>
                </Container>
            ) : page == 'teacher_home' ? (
                <Container className='w-50 d-flex align-items-center justify-content-end'>
                    <Button variant='outline-light' className='header-button m-2'>Create Class</Button>
                    <Button variant='outline-light' className='header-button m-2'>Log Out</Button>
                </Container>
            ) : (
                <Container>
                    <Button variant='outline-light' className='header-button m-2'>Log Out</Button>
                </Container>
            )}
		</Container>
	);
}
