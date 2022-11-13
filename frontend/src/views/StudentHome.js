import Header from '../components/Header'
import { useEffect, useState } from 'react'
import { Container, Accordion } from 'react-bootstrap'


export default function StudentHome() {

    const currentUser = localStorage.getItem('current_userid')
    console.log(currentUser)

    const [classes, setClasses] = useState([])

    useEffect(() => { //TODO flask fetch
        
        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        };

        let response = -1
        fetch('/api/get-classes?userid=' + currentUser, requestOptions).then(
            response => response.json() 
        ).then(
            data => setClasses(data)
        );

        console.log('fetching classes')
        console.log(classes)
    }, [currentUser]);

    // const sampleClasses = [
    //     {
    //         name: 'c1',
    //         joincode: 'aj09iu231je',
    //         attend: true
    //     },
    //     {
    //         name: 'c2',
    //         joincode: 'jeoij2e19je',
    //         attend: false
    //     },
    //     {
    //         name: 'c3',
    //         joincode: 'cxmzf98201',
    //         attend: true
    //     }
    // ];

	return (
		<div>
            <Header page='student_home'/>
            <Container className='p-4'>
                {currentUser != null ? (
                    <Accordion alwaysOpen>
                        {classes.map((c) => (
                            <Accordion.Item eventKey={c.code} key={c.code}>
                                <Accordion.Header className='bg-red'>{c.name}</Accordion.Header>
                                <Accordion.Body>
                                    <Container className='d-flex justify-content-around'>
                                        <p className='m-3'>Join Code: {c.code}</p>
                                        <p className='m-3'> Today's Attendance: {c.present ? 'Present' : 'Absent'}</p>
                                    </Container>
                                </Accordion.Body>
                            </Accordion.Item>
                        ))}
                    </Accordion>
                ) : (
                    <Container className='d-flex p-5 align-items-center justify-content-center' style={{marginTop: '10rem'}}>
                        <p className='fs-4 mt-4'>You must be logged in to access this page</p>
                    </Container>
                )}
            </Container>
		</div>
	);
}
