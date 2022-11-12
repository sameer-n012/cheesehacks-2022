import Header from '../components/Header'
import { useEffect, useState } from 'react'
import { Container, Accordion } from 'react-bootstrap'

export default function AdminHome() {

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

		
		<div className='teacherhome'>
            <Header  page='teacher_home'/>

		
			<ul>

			<Container className=''>
                <Accordion alwaysOpen>
                    {sampleClasses.map((c) => (
                        <Accordion.Item eventKey={c.joincode}>
                            <Accordion.Header className=''>{c.name}</Accordion.Header>
                            <Accordion.Body>
                                <p>Join Code: {c.joincode}</p>
                                <p> Today's Attendance: {c.attend ? 'Yes' : 'No'}</p>
                            </Accordion.Body>
                        </Accordion.Item>
                    ))}
                </Accordion>
			</Container>
				
			</ul>
		</div>
	);
}
