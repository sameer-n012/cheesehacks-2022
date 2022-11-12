import Header from '../components/Header'
import { Container, Accordion } from 'react-bootstrap'

export default function StudentHome() {

    const classes = [
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
    ]

	return (
		<div>
            <Header page='student_home'/>
			<Container className='p-4'>
                <Accordion alwaysOpen>
                    {classes.map((c) => (
                        <Accordion.Item eventKey={c.joincode}>
                            <Accordion.Header className='bg-red'>{c.name}</Accordion.Header>
                            <Accordion.Body>
                                <p>Join Code: {c.joincode}</p>
                                <p> Today's Attendance: {c.attend ? 'Yes' : 'No'}</p>
                            </Accordion.Body>
                        </Accordion.Item>
                    ))}
                </Accordion>
            </Container>
		</div>
	);
}
