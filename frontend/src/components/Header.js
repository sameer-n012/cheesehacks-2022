import { Container, Button, Modal, Form } from 'react-bootstrap'
import { useNavigate } from 'react-router';
import { useState } from 'react'
import { Link } from 'react-router-dom'

export default function Header({page}) {

    const currentUser = localStorage.getItem('current_userid');

    const [className, setClassName] = useState('')

    const handleFormChange = (e) => {
        setClassName(e.target.value);
    }

    const [modalShows, setModalShows] = useState({
        create: false,
        add: false
    })

    const handleClose = () => setModalShows({
        create: false,
        add: false
    });
    const handleAddShow = () => setModalShows({
        create: false,
        add: true
    });
    const handleCreateShow = () => setModalShows({
        add: false,
        create: true
    })

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

    const addClassSubmit = () => {
        // TODO make fetch request here
        if(!className) {
            return;
        }

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: className
        };

        fetch('/api/join-class?userid=' + currentUser, requestOptions).then(
            response => response.status 
        ).then(
            status => { console.log(status) }
        );
        console.log('joining class ' + className);
        handleClose();
        window.location.replace(window.location.href);
    }

    const createClassSubmit = () => {
        if(!className) {
            return;
        }

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: className
        };

        fetch('/api/create-class2?userid=' + currentUser, requestOptions).then(
            response => response.status 
        ).then(
            status => { console.log(status); }
        );
        console.log('creating class ' + className);
        handleClose();
        window.location.replace(window.location.href);
        
    }

    // TODO insert application name
	return (
		<Container fluid className='header w-100 p-3 d-flex  align-items-center uw-red-bg'>
			<Link to='/' style={{width:'inherit'}}><h2 className='header-title text-white text-decoration-none'>Face First</h2></Link>
            <Container className='d-flex align-items-center justify-content-end'>
                {page == 'student_home' && currentUser ? (
                    <div>
                        <Button variant='outline-light' className='header-button m-2' onClick={() => {handleAddShow()}}>Join Class</Button>
                        <Button variant='outline-light' className='header-button m-2' onClick={() => {uploadImage()}}>Upload Image</Button>
                    </div>
                ) : page == 'teacher_home' && currentUser ? (
                    <div>
                        <Button variant='outline-light' className='header-button m-2' onClick={() => {handleCreateShow()}}>Create Class</Button>
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

            <Modal show={modalShows.create} onHide={() => {handleClose()}}>
                <Modal.Header closeButton>
                    <Modal.Title>Create New Class</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={e => { e.preventDefault(); }}>
                        <Form.Group className="">
                            <Form.Label>Class Name</Form.Label>
                            <Form.Control
                                type='text'
                                name='classname'
                                required
                                onChange={(e)=>handleFormChange(e)}
                            />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="outline-dark" onClick={(e) => createClassSubmit(e)}>
                        Add Class
                    </Button>
                </Modal.Footer>
            </Modal>

            <Modal show={modalShows.add} onHide={() => {handleClose()}}>
                <Modal.Header closeButton>
                    <Modal.Title>Join a Class</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={e => { e.preventDefault(); }}>
                        <Form.Group className="">
                            <Form.Label>Class Code</Form.Label>
                            <Form.Control
                                type='text'
                                name='classname'
                                required
                                onChange={(e)=>handleFormChange(e)}
                            />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="outline-dark" onClick={(e) => addClassSubmit(e)}>
                        Join
                    </Button>
                </Modal.Footer>
            </Modal>


		</Container>
	);
}
