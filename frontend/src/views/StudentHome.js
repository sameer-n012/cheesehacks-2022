import Header from '../components/Header'
import { useEffect, useState } from 'react'
import { Container, Accordion } from 'react-bootstrap'


export default function StudentHome() {

    const currentUser = localStorage.getItem('current_userid')
    console.log(currentUser)

    const [classes, setClasses] = useState([{}])

    useEffect(() => { //TODO flask fetch
        fetch('/getclasses/').then(
            response => response.json()
        ).then(
            data => setClasses(data.myData)
        )
    }, []);

    const sampleClasses = [
        {
            name: 'c1',
            joincode: 'aj09iu231je',
            attend: true
        },
        {
            name: 'c2',
            joincode: 'jeoij2e19je',
            attend: false
        },
        {
            name: 'c3',
            joincode: 'cxmzf98201',
            attend: true
        }
    ];

	return (
		<div>
            <Header page='student_home'/>
            <Container className='p-4'>
                {currentUser != null ? (
                    <Accordion alwaysOpen>
                        {sampleClasses.map((c) => (
                            <Accordion.Item eventKey={c.joincode}>
                                <Accordion.Header className='bg-red'>{c.name}</Accordion.Header>
                                <Accordion.Body>
                                    <p>Join Code: {c.joincode}</p>
                                    <p> Today's Attendance: {c.attend ? 'Yes' : 'No'}</p>
                                </Accordion.Body>
                            </Accordion.Item>
                        ))}
                    </Accordion>
                ) : (
                    <Container className='d-flex p-5 align-items-center justify-content-center'>
                        <p className='fs-4'>You must be logged in to access this page</p>
                    </Container>
                )}
            </Container>
		</div>
	);
}
